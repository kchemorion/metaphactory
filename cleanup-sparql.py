#!/usr/bin/env python3
"""Delete leftover vocabulary named graphs via SPARQL UPDATE."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

# Named graphs to drop (from the vocabulary IRIs we found)
GRAPHS_TO_DROP = [
    "https://m20.academy.metaphacts.cloud/vocabulary/Vegetables",
    "https://vocabularies.metaphacts.com/vegetables-for-recipes/0.1",
    "https://vocabularies.metaphacts.com/vegetables/0.1",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Approach 1: Try Named Graphs page to delete
    page.goto(f"{BASE_URL}/resource/Assets:NamedGraphs")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/cleanup-named-graphs.png", full_page=True)

    # List all named graphs with "vegetable" or "Vegetable"
    print("=== NAMED GRAPHS ===")
    body = page.locator('body').inner_text()
    for line in body.split('\n'):
        if 'vegetable' in line.lower() or 'recipes' in line.lower():
            print(f"  {line.strip()[:100]}")

    # Look for delete buttons on the named graphs page
    delete_btns = page.locator('button:has-text("delete"), a:has-text("delete"), button[title*="Delete"], button[title*="delete"]')
    print(f"\nDelete buttons found: {delete_btns.count()}")
    for i in range(min(delete_btns.count(), 5)):
        btn = delete_btns.nth(i)
        if btn.is_visible():
            print(f"  '{btn.inner_text().strip()[:30]}'")

    # Approach 2: Use SPARQL UPDATE to drop the graphs
    print("\n=== SPARQL UPDATE APPROACH ===")
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    for graph_iri in GRAPHS_TO_DROP:
        query = f"DROP GRAPH <{graph_iri}>"
        print(f"\nExecuting: {query}")

        try:
            page.evaluate(f"""() => {{
                const cm = document.querySelector('.CodeMirror');
                if (cm && cm.CodeMirror) {{
                    cm.CodeMirror.setValue({repr(query)});
                }}
            }}""")
            time.sleep(0.5)

            # Click Execute/Run
            execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
            if execute_btn.is_visible(timeout=2000):
                execute_btn.click()
                time.sleep(2)

            # Check for results/errors
            result_text = page.locator('.alert, .query-results, .result-panel, [class*="result"]').first
            if result_text.is_visible(timeout=2000):
                print(f"  Result: {result_text.inner_text().strip()[:200]}")
            else:
                print(f"  Executed (no visible result)")
        except Exception as e:
            print(f"  Error: {e}")

    # Also try to clear any vocabulary metadata
    # Delete triples about these vocabulary IRIs from the default graph
    cleanup_query = """
DELETE WHERE {
  GRAPH ?g {
    ?s ?p ?o .
  }
  FILTER(?g IN (
    <https://m20.academy.metaphacts.cloud/vocabulary/Vegetables>,
    <https://vocabularies.metaphacts.com/vegetables-for-recipes/0.1>,
    <https://vocabularies.metaphacts.com/vegetables/0.1>
  ))
}"""
    print(f"\nExecuting cleanup query...")
    try:
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{
                cm.CodeMirror.setValue({repr(cleanup_query)});
            }}
        }}""")
        time.sleep(0.5)
        execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
        if execute_btn.is_visible(timeout=2000):
            execute_btn.click()
            time.sleep(2)
            print("  Done")
    except Exception as e:
        print(f"  Error: {e}")

    # Verify: check vocabularies page again
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    print("\n=== VOCABULARIES AFTER CLEANUP ===")
    links = page.locator('a')
    for i in range(links.count()):
        link = links.nth(i)
        if link.is_visible():
            text = link.inner_text().strip()
            if 'vegetable' in text.lower():
                print(f"  Still exists: '{text}'")

    page.screenshot(path="cert-screenshots/cleanup-after-sparql.png", full_page=True)
    time.sleep(3)
    browser.close()
