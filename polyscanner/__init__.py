"""Polymarket Signal Scanner (MVP).

The current focus is a minimal, working, end-to-end wiring test:
- load `bit_domain` from Postgres (Supabase local)
- fetch Polymarket markets
- rank top candidates
- use Gemini to assign a domain per market
- write a markdown report
"""
