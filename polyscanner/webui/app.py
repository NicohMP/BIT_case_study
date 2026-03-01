from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi import Form
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from polyscanner.db.pg import connect
from polyscanner.db.security_signal_report import upsert_pm_security_signal_report
from polyscanner.env import get_env, load_env
from polyscanner.llm.client import get_backend, get_model
from polyscanner.llm.gemini import GeminiError
from polyscanner.llm.ollama import OllamaError
from polyscanner.llm.security_signal_report_v1 import PROMPT_VERSION, generate_security_signal_report_v1
from polyscanner.reporting.security_report_pack import build_security_context_pack
from polyscanner.reporting.security_report_validation import validate_security_report_json
from polyscanner.reporting.security_signal_report_audit import audit_security_signal_report
from polyscanner.reporting.security_signal_report_markdown import render_security_signal_report_markdown
from polyscanner.webui import db
from polyscanner.webui.markdown_render import render_markdown

log = logging.getLogger(__name__)


def _load_db_url() -> str:
    load_env()
    db_url = (get_env("DATABASE_URL") or "").strip()
    if not db_url:
        raise RuntimeError("Missing DATABASE_URL in environment/.env")
    return db_url


APP_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def _fmt_prob(p: Any) -> str:
    try:
        v = float(p)
    except Exception:
        return "—"
    pct = v * 100.0
    if pct < 1.0:
        return f"{pct:.2f}%"
    if pct < 10.0:
        return f"{pct:.1f}%"
    return f"{pct:.0f}%"


def _fmt_usd(x: Any) -> str:
    try:
        v = float(x)
    except Exception:
        return "—"
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1_000_000_000:
        return f"{sign}${v/1_000_000_000:.2f}B"
    if v >= 1_000_000:
        return f"{sign}${v/1_000_000:.2f}M"
    if v >= 10_000:
        return f"{sign}${v/1_000:.1f}k"
    if v >= 1_000:
        return f"{sign}${v/1_000:.2f}k"
    return f"{sign}${v:,.0f}"


def _fmt_date(x: Any) -> str:
    if x is None:
        return "—"
    if isinstance(x, datetime):
        dt = x
    else:
        # Best-effort parse for string-ish timestamps.
        try:
            dt = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
        except Exception:
            return str(x)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%b %d, %Y")


def _fmt_ends_in(x: Any) -> str:
    if x is None:
        return "—"
    if isinstance(x, datetime):
        dt = x
    else:
        try:
            dt = datetime.fromisoformat(str(x).replace("Z", "+00:00"))
        except Exception:
            return "—"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta_s = (dt.astimezone(timezone.utc) - now).total_seconds()
    if delta_s <= 0:
        return "ended"
    days = max(0.0, delta_s / 86400.0)
    if days < 1.0:
        return "today"
    if days < 14.0:
        return f"{math.ceil(days):.0f}d"
    if days < 60.0:
        return f"{math.ceil(days/7.0):.0f}w"
    if days < 365.0:
        return f"{math.ceil(days/30.0):.0f}mo"
    return f"{math.ceil(days/365.0):.0f}y"


templates.env.filters["fmt_prob"] = _fmt_prob
templates.env.filters["fmt_usd"] = _fmt_usd
templates.env.filters["fmt_date"] = _fmt_date
templates.env.filters["fmt_ends_in"] = _fmt_ends_in

app = FastAPI(title="Polymarket Signal Scanner", version="0.1")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _build_report_id(*, security_id: int, pack_hash: str, prompt_version: str, model: str) -> str:
    return _sha256(f"{security_id}:{pack_hash}:{prompt_version}:{model}")[:32]


def _ensure_meta_fields(*, report: dict[str, Any], pack: dict[str, Any], model: str, backend: str | None = None) -> None:
    report.setdefault("as_of_utc", (pack.get("report_meta") or {}).get("as_of_utc"))
    report.setdefault("security", pack.get("security") or {})
    versions = report.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    pack_versions = (pack.get("report_meta") or {}).get("versions") or {}
    versions["run_id"] = (pack.get("report_meta") or {}).get("run_id")
    for k in ("filter_version", "matcher_version", "scoring_version", "selection_version"):
        if k in pack_versions and pack_versions.get(k) is not None:
            versions[k] = pack_versions.get(k)
    versions["prompt_version"] = PROMPT_VERSION
    if backend:
        versions["backend"] = str(backend)
    versions["model"] = model
    report["versions"] = versions


def _render_error_page(
    *,
    request: Request,
    title: str,
    message: str,
    detail: str | None = None,
    status_code: int = 500,
) -> HTMLResponse:
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "title": title, "message": message, "detail": detail or "", "status_code": int(status_code)},
        status_code=int(status_code),
    )


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request) -> Any:
    db_url = _load_db_url()
    run = db.latest_pipeline_run(db_url=db_url)
    counts = db.pipeline_counts(db_url=db_url)

    wl = db.watchlist_securities(db_url=db_url)
    security_ids = [int(x["security_id"]) for x in wl]
    latest_reports = db.latest_reports_for_security_ids(db_url=db_url, security_ids=security_ids)

    previews: dict[int, list[dict[str, Any]]] = {}
    for s in wl:
        sid = int(s.get("security_id") or 0)
        if not sid:
            continue
        # Show a diversified preview: prefer non-rate-like markets, then fill remaining slots.
        rows = db.selected_markets_for_security_id(db_url=db_url, security_id=sid, limit=20)
        non_rate = [r for r in rows if not bool(r.get("is_rate_like"))]
        rate = [r for r in rows if bool(r.get("is_rate_like"))]
        preview = (non_rate + rate)[:5]
        previews[sid] = preview

    backend = get_backend()
    model = get_model(backend=backend)
    llm = {"backend": backend, "model": model, "prompt_version": PROMPT_VERSION}

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "run": run,
            "counts": counts,
            "watchlist": wl,
            "latest_reports": latest_reports,
            "previews": previews,
            "llm": llm,
        },
    )


@app.get("/watchlist", response_class=HTMLResponse)
def watchlist_page(request: Request) -> Any:
    db_url = _load_db_url()
    secs = db.list_securities(db_url=db_url)
    wl = {int(x["security_id"]) for x in db.watchlist_securities(db_url=db_url)}
    run = db.latest_pipeline_run(db_url=db_url)
    counts = db.pipeline_counts(db_url=db_url)
    return templates.TemplateResponse(
        "watchlist.html",
        {"request": request, "securities": secs, "watchlist": wl, "run": run, "counts": counts},
    )


@app.get("/pipeline", response_class=HTMLResponse)
def pipeline(request: Request) -> Any:
    db_url = _load_db_url()
    run = db.latest_pipeline_run(db_url=db_url)
    counts = db.pipeline_counts(db_url=db_url)
    return templates.TemplateResponse("pipeline.html", {"request": request, "run": run, "counts": counts})


@app.get("/securities", response_class=HTMLResponse)
def securities(request: Request) -> Any:
    db_url = _load_db_url()
    secs = db.list_securities(db_url=db_url)
    return templates.TemplateResponse("securities.html", {"request": request, "securities": secs})


@app.get("/securities/{security_id}", response_class=HTMLResponse)
def security_detail(request: Request, security_id: int) -> Any:
    db_url = _load_db_url()
    secs = {int(s["security_id"]): s for s in db.list_securities(db_url=db_url)}
    sec = secs.get(int(security_id))
    if not sec:
        raise HTTPException(status_code=404, detail="Unknown security_id")
    exposures = db.security_exposures(db_url=db_url, security_id=int(security_id))
    return templates.TemplateResponse("security_detail.html", {"request": request, "sec": sec, "exposures": exposures})


@app.get("/signals", response_class=HTMLResponse)
def signals(request: Request, security_id: int | None = None, ticker: str | None = None, limit: int = 20) -> Any:
    db_url = _load_db_url()
    secs = db.list_securities(db_url=db_url)
    sec = None
    if security_id is not None:
        for s in secs:
            if int(s.get("security_id") or 0) == int(security_id):
                sec = s
                break
    elif ticker:
        matches = [s for s in secs if str(s.get("ticker") or "").upper() == str(ticker).upper()]
        if len(matches) == 1:
            sec = matches[0]
        elif matches:
            # Best-effort: pick the first and let the user refine via the dropdown.
            sec = matches[0]
    if sec is None and secs:
        sec = secs[0]
    if sec is None:
        raise HTTPException(status_code=404, detail="No securities found in DB.")

    sid = int(sec.get("security_id"))
    rows = db.selected_markets_for_security_id(db_url=db_url, security_id=sid, limit=int(limit))
    macro_domains = db.list_macro_domains(db_url=db_url)

    # Default UX: hide rate-like markets unless explicitly included.
    # The form submits hide_rate_like=0 when unchecked, hide_rate_like=1 when checked.
    # When arriving via a link (no param), default to hiding them.
    hide_rate_like_param = (request.query_params.get("hide_rate_like") or "1").strip().lower()
    hide_rate_like = hide_rate_like_param in {"1", "true", "t", "yes", "y", "on"}

    # Optional domain filter (read-only "configuration" for reviewers).
    domain_id = request.query_params.get("domain_id")
    if domain_id:
        try:
            did = int(domain_id)
        except Exception:
            did = None
        if did:
            filtered: list[dict[str, Any]] = []
            for r in rows:
                sb = r.get("score_breakdown") or {}
                top = (sb.get("top_domains") or []) if isinstance(sb, dict) else []
                if any(int(d.get("macro_domain_id") or 0) == did for d in top if isinstance(d, dict)):
                    filtered.append(r)
            rows = filtered

    if hide_rate_like:
        rows = [r for r in rows if not bool(r.get("is_rate_like"))]

    context = f"{sec.get('ticker')}@{sec.get('exchange_mic')}" if sec.get("exchange_mic") else str(sec.get("ticker") or "")
    return templates.TemplateResponse(
        "signals.html",
        {
            "request": request,
            "securities": secs,
            "security_id": sid,
            "ticker": str(sec.get("ticker") or "").upper(),
            "context": context,
            "rows": rows,
            "limit": int(limit),
            "macro_domains": macro_domains,
            "hide_rate_like": hide_rate_like,
        },
    )


@app.get("/markets", response_class=HTMLResponse)
def markets(request: Request, q: str | None = None, limit: int = 200, offset: int = 0) -> Any:
    db_url = _load_db_url()
    rows = db.kept_markets(db_url=db_url, q=q, limit=int(limit), offset=int(offset))
    return templates.TemplateResponse(
        "markets.html",
        {"request": request, "rows": rows, "q": q or "", "limit": int(limit), "offset": int(offset)},
    )


@app.get("/markets/{market_id}", response_class=HTMLResponse)
def market_detail(request: Request, market_id: int, security_id: int | None = None, ticker: str | None = None) -> Any:
    db_url = _load_db_url()
    m = db.market_detail(db_url=db_url, market_id=int(market_id))
    if not m:
        raise HTTPException(status_code=404, detail="Unknown market_id")

    decision = db.market_filter_decision_latest(db_url=db_url, market_id=int(market_id))
    matches = db.market_family_matches_latest(db_url=db_url, market_id=int(market_id), limit=20)

    sel = None
    context = ""
    if security_id is not None:
        sel = db.selected_market_for_security_id_and_market_id(db_url=db_url, security_id=int(security_id), market_id=int(market_id))
        if sel:
            context = f"{sel.get('ticker')}@{sel.get('exchange_mic')}" if sel.get("exchange_mic") else str(sel.get("ticker") or "")
    elif ticker:
        sel = db.selected_market_for_ticker_and_market_id(db_url=db_url, ticker=str(ticker).upper(), market_id=int(market_id))
        context = str(ticker).upper()

    return templates.TemplateResponse(
        "market_detail.html",
        {"request": request, "market": m, "decision": decision, "matches": matches, "selected": sel, "context": context},
    )


@app.get("/reports", response_class=HTMLResponse)
def reports(request: Request) -> Any:
    db_url = _load_db_url()
    rows = db.list_reports(db_url=db_url)
    return templates.TemplateResponse("reports.html", {"request": request, "rows": rows})


@app.get("/reports/{report_id}", response_class=HTMLResponse)
def report_detail(request: Request, report_id: str, view: str = "md") -> Any:
    db_url = _load_db_url()
    rep = db.fetch_report(db_url=db_url, report_id=report_id)
    if not rep:
        raise HTTPException(status_code=404, detail="Unknown report_id")
    report_json = rep.get("report_json")
    md = rep.get("report_md")
    if not md and isinstance(report_json, dict):
        md = render_security_signal_report_markdown(report=report_json)
    if view == "json":
        pretty = json.dumps(report_json, ensure_ascii=False, indent=2)
        return templates.TemplateResponse("report_json.html", {"request": request, "rep": rep, "pretty": pretty})
    md_text = md or ""
    if view == "raw":
        return templates.TemplateResponse("report_md.html", {"request": request, "rep": rep, "md": md_text, "md_html": ""})
    md_html = render_markdown(md_text)
    return templates.TemplateResponse("report_md.html", {"request": request, "rep": rep, "md": md_text, "md_html": md_html})


@app.post("/watchlist", response_class=HTMLResponse)
def update_watchlist(request: Request, security_id: list[int] = Form(default=[])) -> Any:
    db_url = _load_db_url()
    out = db.set_watchlist(db_url=db_url, security_ids=[int(x) for x in (security_id or [])])
    secs = db.list_securities(db_url=db_url)
    wl = {int(x["security_id"]) for x in db.watchlist_securities(db_url=db_url)}
    run = db.latest_pipeline_run(db_url=db_url)
    counts = db.pipeline_counts(db_url=db_url)
    msg = f"Saved watchlist: {out['selected']} stocks."
    return templates.TemplateResponse(
        "watchlist.html",
        {"request": request, "securities": secs, "watchlist": wl, "run": run, "counts": counts, "toast": msg},
    )


@app.post("/actions/generate_and_open", response_class=HTMLResponse)
def action_generate_and_open(
    request: Request,
    security_id: int | None = Form(None),
    ticker: str = Form(""),
    temperature: float = Form(0.0),
    max_markets: int = Form(8),
) -> Any:
    """Generate one report, persist it, then redirect to the report viewer."""
    db_url = _load_db_url()
    backend = get_backend()
    model = get_model(backend=backend)
    sid = int(security_id) if security_id is not None else None
    t = str(ticker).upper().strip() or None

    try:
        pack = build_security_context_pack(
            db_url=db_url,
            ticker=t if sid is None else None,
            security_id=sid,
            exchange_mic=None,
            top_k_markets=max(int(max_markets), 10),
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Failed to build context pack (security_id=%s ticker=%s): %s", sid, t, e)
        return _render_error_page(
            request=request,
            title="Context pack build failed",
            message="Could not build the deterministic context pack from the database.",
            detail=str(e),
            status_code=500,
        )

    # If an identical report already exists for this (security, pack_hash, prompt_version, model),
    # just open it (saves time + avoids unnecessary LLM calls during demos).
    try:
        pack_hash = str((pack.get("report_meta") or {}).get("pack_sha256") or "")
        sec = pack.get("security") or {}
        security_id = int(sec.get("security_id"))
        existing_report_id = _build_report_id(security_id=security_id, pack_hash=pack_hash, prompt_version=PROMPT_VERSION, model=model)

        conn = connect(db_url)
        try:
            row = db.fetch_one(conn, "select 1 as ok from pm_security_signal_report where report_id=%s limit 1;", (existing_report_id,))
        finally:
            conn.close()
        if row:
            return RedirectResponse(url=f"/reports/{existing_report_id}", status_code=303)
    except Exception:
        # Best-effort only; proceed to generation.
        pass

    try:
        report = generate_security_signal_report_v1(
            pack=pack,
            backend=backend,
            model=model,
            temperature=float(temperature),
            timeout_s=180,
            max_retries=2,
            retry_base_s=1.0,
            retry_max_s=15.0,
            max_markets=int(max_markets),
        )
    except (GeminiError, OllamaError, TimeoutError) as e:
        log.exception("LLM generation failed (backend=%s model=%s ticker=%s): %s", backend, model, t, e)
        hint = (
            "If Gemini is throttled (HTTP 429), wait a few minutes and retry. "
            "Alternatively, run locally with Ollama by setting `LLM_BACKEND=ollama` and `OLLAMA_MODEL=...` in `.env`."
        )
        return _render_error_page(
            request=request,
            title="LLM report generation failed",
            message=hint,
            detail=f"backend={backend} model={model}\nerror={e}",
            status_code=502,
        )
    except Exception as e:  # noqa: BLE001
        log.exception("Unexpected error during report generation (ticker=%s): %s", t, e)
        return _render_error_page(
            request=request,
            title="Unexpected error",
            message="An unexpected error happened while generating the report.",
            detail=str(e),
            status_code=500,
        )

    if isinstance(report, dict):
        report.pop("_raw", None)
    _ensure_meta_fields(report=report, pack=pack, model=model, backend=backend)

    issues = validate_security_report_json(report, pack=pack)
    errors = [x for x in issues if x.level == "error"]
    if errors:
        detail = "\n".join(
            [f"- {it.message}" + (f" ({it.path})" if it.path else "") for it in errors[:12]]
            + ([f"... ({len(errors) - 12} more)"] if len(errors) > 12 else [])
        )
        return _render_error_page(
            request=request,
            title="Model output failed validation",
            message="The model returned JSON that failed grounding checks against the deterministic context pack.",
            detail=detail,
            status_code=422,
        )

    pack_hash = str((pack.get("report_meta") or {}).get("pack_sha256") or "")
    sec = pack.get("security") or {}
    security_id = int(sec.get("security_id"))
    report_id = _build_report_id(security_id=security_id, pack_hash=pack_hash, prompt_version=PROMPT_VERSION, model=model)
    pv = (pack.get("report_meta") or {}).get("versions") or {}
    md = render_security_signal_report_markdown(report=report)

    try:
        conn = connect(db_url)
        try:
            upsert_pm_security_signal_report(
                conn,
                report_id=str(report_id),
                run_id=(pack.get("report_meta") or {}).get("run_id"),
                security_id=int(security_id),
                filter_version=pv.get("filter_version"),
                matcher_version=pv.get("matcher_version"),
                scoring_version=str(pv.get("scoring_version") or ""),
                selection_version=str(pv.get("selection_version") or ""),
                prompt_version=PROMPT_VERSION,
                model=str(model),
                context_pack_hash=str(pack_hash),
                report_json=report,
                report_md=md,
            )
        finally:
            conn.close()
    except Exception as e:  # noqa: BLE001
        log.exception("Failed to persist report (ticker=%s report_id=%s): %s", t, report_id, e)
        return _render_error_page(
            request=request,
            title="Failed to persist report",
            message="The report was generated but could not be stored in Postgres.",
            detail=str(e),
            status_code=500,
        )

    return RedirectResponse(url=f"/reports/{report_id}", status_code=303)


@app.get("/generate", response_class=HTMLResponse)
def generate_page(request: Request) -> Any:
    db_url = _load_db_url()
    wl = db.watchlist_securities(db_url=db_url)
    backend = get_backend()
    model = get_model(backend=backend)
    return templates.TemplateResponse("generate.html", {"request": request, "watchlist": wl, "backend": backend, "model": model})


@app.post("/generate", response_class=HTMLResponse)
def generate_submit(
    request: Request,
    security_id: list[int] = Form(default=[]),
    ticker: list[str] = Form(default=[]),
    temperature: float = Form(0.0),
    max_markets: int = Form(8),
) -> Any:
    """Generate and persist reports for one or more tickers (on-demand LLM)."""
    db_url = _load_db_url()
    wl = db.watchlist_securities(db_url=db_url)
    wl_by_id = {int(s.get("security_id")): s for s in wl if s.get("security_id") is not None}

    security_ids = [int(x) for x in (security_id or []) if int(x) in wl_by_id]
    if not security_ids and ticker:
        wl_tickers = {str(s.get("ticker") or "").upper() for s in wl}
        tickers = [str(t).upper() for t in (ticker or []) if str(t).upper() in wl_tickers]
        for t in tickers:
            for s in wl:
                if str(s.get("ticker") or "").upper() == t:
                    security_ids.append(int(s.get("security_id")))
    security_ids = sorted({int(x) for x in security_ids})

    backend = get_backend()
    model = get_model(backend=backend)

    results: list[dict[str, Any]] = []
    for sid in security_ids:
        try:
            pack = build_security_context_pack(
                db_url=db_url,
                ticker=None,
                security_id=int(sid),
                exchange_mic=None,
                top_k_markets=max(int(max_markets), 10),
            )
            report = generate_security_signal_report_v1(
                pack=pack,
                backend=backend,
                model=model,
                temperature=float(temperature),
                timeout_s=180,
                max_retries=2,
                retry_base_s=1.0,
                retry_max_s=15.0,
                max_markets=int(max_markets),
            )
            report.pop("_raw", None)
            _ensure_meta_fields(report=report, pack=pack, model=model, backend=backend)

            issues = validate_security_report_json(report, pack=pack)
            errors = [x for x in issues if x.level == "error"]
            if errors:
                sec = pack.get("security") or {}
                results.append(
                    {
                        "security_id": int(sid),
                        "ticker": str(sec.get("ticker") or wl_by_id.get(int(sid), {}).get("ticker") or ""),
                        "ok": False,
                        "error": "Model output failed grounding checks.",
                        "issues": issues,
                    }
                )
                continue

            audit_issues = audit_security_signal_report(report=report, pack=pack, max_markets=int(max_markets), max_rate_like=3)
            n_err = len([x for x in audit_issues if x.level == "error"])
            n_warn = len([x for x in audit_issues if x.level == "warning"])

            pack_hash = str((pack.get("report_meta") or {}).get("pack_sha256") or "")
            sec = pack.get("security") or {}
            security_id = int(sec.get("security_id"))
            report_id = _build_report_id(security_id=security_id, pack_hash=pack_hash, prompt_version=PROMPT_VERSION, model=model)

            pv = (pack.get("report_meta") or {}).get("versions") or {}
            md = render_security_signal_report_markdown(report=report)
            conn = connect(db_url)
            try:
                upsert_pm_security_signal_report(
                    conn,
                    report_id=str(report_id),
                    run_id=(pack.get("report_meta") or {}).get("run_id"),
                    security_id=int(security_id),
                    filter_version=pv.get("filter_version"),
                    matcher_version=pv.get("matcher_version"),
                    scoring_version=str(pv.get("scoring_version") or ""),
                    selection_version=str(pv.get("selection_version") or ""),
                    prompt_version=PROMPT_VERSION,
                    model=str(model),
                    context_pack_hash=str(pack_hash),
                    report_json=report,
                    report_md=md,
                )
            finally:
                conn.close()

            results.append(
                {
                    "security_id": int(security_id),
                    "ticker": str(sec.get("ticker") or ""),
                    "ok": True,
                    "report_id": report_id,
                    "audit_errors": n_err,
                    "audit_warnings": n_warn,
                }
            )
        except (GeminiError, OllamaError, TimeoutError) as e:
            ticker_guess = str(wl_by_id.get(int(sid), {}).get("ticker") or "")
            results.append({"security_id": int(sid), "ticker": ticker_guess, "ok": False, "error": f"LLM error ({backend}/{model}): {e}"})
        except Exception as e:  # noqa: BLE001
            ticker_guess = str(wl_by_id.get(int(sid), {}).get("ticker") or "")
            results.append({"security_id": int(sid), "ticker": ticker_guess, "ok": False, "error": str(e)})

    toast = None
    if security_ids:
        n_ok = len([r for r in results if r.get("ok")])
        toast = f"Generated {n_ok}/{len(security_ids)} reports using {backend}/{model}."
    else:
        toast = "No securities selected (or securities not in watchlist)."

    return templates.TemplateResponse(
        "generate.html",
        {"request": request, "watchlist": wl, "backend": backend, "model": model, "results": results, "toast": toast},
    )


@app.get("/stocks/new", response_class=HTMLResponse)
def new_stock_form(request: Request) -> Any:
    db_url = _load_db_url()
    macro_domains = db.list_macro_domains(db_url=db_url)
    return templates.TemplateResponse("new_stock.html", {"request": request, "macro_domains": macro_domains})


@app.post("/stocks/new", response_class=HTMLResponse)
def create_stock(
    request: Request,
    company_name: str = Form(...),
    ticker: str = Form(...),
    exchange_mic: str = Form("XNAS"),
    primary_macro_domain_id: int = Form(...),
    isin: str = Form(""),
    add_to_watchlist: str | None = Form(None),
) -> Any:
    db_url = _load_db_url()
    macro_domains = db.list_macro_domains(db_url=db_url)
    try:
        out = db.add_security_with_primary_domain(
            db_url=db_url,
            company_name=company_name,
            ticker=ticker,
            exchange_mic=exchange_mic,
            primary_macro_domain_id=int(primary_macro_domain_id),
            isin=(isin.strip() or None),
        )
    except Exception as e:  # noqa: BLE001
        return templates.TemplateResponse(
            "new_stock.html",
            {"request": request, "macro_domains": macro_domains, "error": f"Failed to add stock: {e}"},
        )

    if add_to_watchlist is not None:
        try:
            db.add_to_watchlist(db_url=db_url, security_id=int(out["security_id"]))
        except Exception:
            pass
    return templates.TemplateResponse(
        "new_stock_done.html",
        {"request": request, "security_id": out["security_id"], "ticker": ticker.strip().upper()},
    )


@app.get("/actions/build_pack", response_class=JSONResponse)
def action_build_pack(security_id: int | None = None, ticker: str | None = None) -> Any:
    db_url = _load_db_url()
    if security_id is None and not ticker:
        raise HTTPException(status_code=400, detail="Provide security_id or ticker")
    pack = build_security_context_pack(
        db_url=db_url,
        ticker=str(ticker).upper() if (security_id is None and ticker) else None,
        security_id=int(security_id) if security_id is not None else None,
        exchange_mic=None,
    )
    return pack


@app.get("/actions/generate_report", response_class=JSONResponse)
def action_generate_report(security_id: int | None = None, ticker: str | None = None, temperature: float = 0.0, max_markets: int = 8) -> Any:
    """On-demand report generation (JSON only). Will fail if Gemini is unavailable (429)."""
    db_url = _load_db_url()
    if security_id is None and not ticker:
        raise HTTPException(status_code=400, detail="Provide security_id or ticker")
    pack = build_security_context_pack(
        db_url=db_url,
        ticker=str(ticker).upper() if (security_id is None and ticker) else None,
        security_id=int(security_id) if security_id is not None else None,
        exchange_mic=None,
    )
    backend = get_backend()
    model = get_model(backend=backend)
    report = generate_security_signal_report_v1(
        pack=pack,
        backend=backend,
        model=model,
        temperature=float(temperature),
        timeout_s=180,
        max_markets=int(max_markets),
    )
    report.pop("_raw", None)
    _ensure_meta_fields(report=report, pack=pack, model=model)
    issues = validate_security_report_json(report, pack=pack)
    errors = [x for x in issues if x.level == "error"]
    if errors:
        return JSONResponse(
            status_code=400,
            content={
                "error": "invalid_report",
                "issues": [x.__dict__ for x in issues],
                "hint": "Model output failed grounding checks. Try again or use a different backend/model.",
            },
        )
    return report


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"
