#!/usr/bin/env python3
"""
Complete, runnable metaphactory automation example.

Demonstrates the core patterns end-to-end against a live instance:
  - login + resilient navigation
  - create a vocabulary (React create-asset dialog, IRI-conflict safe)
  - build a SKOS concept hierarchy (per-concept tree menus, React forms)
  - set editorial status and commit to git
  - run a SPARQL query through the CodeMirror editor

Run against the local Docker instance:
    python3 example.py --url http://localhost:10214 --user admin --pass admin --headed

This file is the canonical reference for HOW the helpers compose. Copy it as a
starting point and adapt the content; keep the helper calls.
"""

import argparse
import sys
import time

from playwright.sync_api import sync_playwright

# When running from inside the skill dir, mf_helpers is a sibling module.
from mf_helpers import (
    login, navigate, screenshot, dismiss_modals,
    create_asset_dialog, create_top_concept, create_narrower_concept,
    set_concept_status, git_save, sparql_update,
)


def build_vocabulary(page, base_url):
    """Create a small 'Vegetables' vocabulary with a 2-level hierarchy."""
    navigate(page, f"{base_url}/resource/Assets:Vocabularies")
    time.sleep(2)
    dismiss_modals(page)

    # Open the create dialog and fill it (handles IRI conflicts internally).
    page.locator('button:has-text("Create"), a:has-text("Create")').first.click()
    time.sleep(1)
    create_asset_dialog(page, "Vegetables Demo", asset_type="vocabulary")
    dismiss_modals(page)
    screenshot(page, "01_vocab_created")

    # Top concept, then narrower concepts under it.
    create_top_concept(page, "Vegetables", "All vegetables used in recipes")
    git_save(page)  # first commit so the asset exists in git

    for child, definition in [
        ("Carrot", "Root vegetable"),
        ("Onion", "Bulb vegetable"),
        ("Green beans", "Legume"),
    ]:
        create_narrower_concept(page, "Vegetables", child, definition)
    screenshot(page, "02_hierarchy")

    # Move every concept through the editorial states.
    for concept in ["Vegetables", "Carrot", "Onion", "Green beans"]:
        set_concept_status(page, concept, "In review")
    for concept in ["Vegetables", "Carrot", "Onion", "Green beans"]:
        set_concept_status(page, concept, "Accepted for publication")

    git_save(page)  # final commit
    screenshot(page, "03_committed")


def query_data(page, base_url):
    """Run a read query through the SPARQL (CodeMirror) editor."""
    sparql_update(page, base_url, """
        SELECT ?concept ?label WHERE {
          ?concept a <http://www.w3.org/2004/02/skos/core#Concept> ;
                   <http://www.w3.org/2000/01/rdf-schema#label> ?label .
        } LIMIT 25
    """.strip())
    screenshot(page, "04_sparql_results")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:10214")
    ap.add_argument("--user", default="admin")
    ap.add_argument("--pass", dest="password", default="admin")
    ap.add_argument("--headed", action="store_true")
    args = ap.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, slow_mo=150)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="recordings",
        )
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        page.set_default_timeout(15000)

        if not login(page, args.url, args.user, args.password):
            print("Login failed — check URL/credentials", file=sys.stderr)
            sys.exit(1)
        print(f"Logged in to {args.url}")

        try:
            build_vocabulary(page, args.url)
            query_data(page, args.url)
            print("Done. See screenshots/ and recordings/.")
        except Exception as e:
            print(f"FAILED: {e}", file=sys.stderr)
            screenshot(page, "error")
            dismiss_modals(page)
            sys.exit(1)
        finally:
            ctx.close()
            browser.close()


if __name__ == "__main__":
    main()
