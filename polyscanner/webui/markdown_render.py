from __future__ import annotations

from markdown_it import MarkdownIt


def render_markdown(md_text: str) -> str:
    """Render markdown to safe HTML for the Web UI.

    Security:
    - Disables raw HTML in markdown (`html=False`) so LLM output can't inject scripts.
    """
    md = MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": True})

    # Optional rules (if available in the installed markdown-it build).
    for rule in ("table", "strikethrough"):
        try:
            md.enable(rule)
        except Exception:
            pass

    return md.render(md_text or "")

