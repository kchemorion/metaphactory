#!/usr/bin/env python3
"""Completely remove all vegetable-related vocabulary data from the instance."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

# All named graphs to drop (each vocab has /graph, /graph_Metadata, /graph_Provenance)
GRAPHS_TO_DROP = [
    "https://vocabularies.metaphacts.com/vegetables/0.1/graph",
    "https://vocabularies.metaphacts.com/vegetables/0.1/graph_Metadata",
    "https://vocabularies.metaphacts.com/vegetables/0.1/graph_Provenance",
    "https://vocabularies.metaphacts.com/vegetables-for-recipes/0.1/graph",
    "https://vocabularies.metaphacts.com/vegetables-for-recipes/0.1/graph_Metadata",
    "https://vocabularies.metaphacts.com/vegetables-for-recipes/0.1/graph_Provenance",
    "https://m20.academy.metaphacts.cloud/vocabulary/Vegetables/graph",
    "https://m20.academy.metaphacts.cloud/vocabulary/Vegetables/graph_Metadata",
    "https://m20.academy.metaphacts.cloud/vocabulary/Vegetables/graph_Provenance",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    def run_update(query, label):
        page.goto(f"{BASE_URL}/sparql")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{ cm.CodeMirror.setValue({repr(query)}); }}
        }}""")
        time.sleep(0.3)
        page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
        time.sleep(2)
        print(f"  {label}")

    # Step 1: Drop all named graphs
    print("=== DROPPING NAMED GRAPHS ===")
    for g in GRAPHS_TO_DROP:
        run_update(f"DROP SILENT GRAPH <{g}>", f"DROP {g.split('/')[-2]}/{g.split('/')[-1]}")

    # Step 2: Clean up default graph - delete all triples about vegetable-related subjects
    print("\n=== CLEANING DEFAULT GRAPH ===")
    run_update("""
DELETE WHERE {
    ?s ?p ?o .
    FILTER(
        CONTAINS(LCASE(STR(?s)), "vegetables") &&
        (CONTAINS(STR(?s), "vocabularies.metaphacts.com") || CONTAINS(STR(?s), "academy.metaphacts.cloud"))
    )
}""", "Deleted default graph triples about vegetable subjects")

    # Step 3: Also delete any triples where vegetables appear as objects
    run_update("""
DELETE WHERE {
    ?s ?p ?o .
    FILTER(
        CONTAINS(LCASE(STR(?o)), "vegetables") &&
        (CONTAINS(STR(?o), "vocabularies.metaphacts.com") || CONTAINS(STR(?o), "academy.metaphacts.cloud"))
    )
}""", "Deleted default graph triples referencing vegetables as objects")

    # Verify
    print("\n=== VERIFICATION ===")
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    check_query = """SELECT DISTINCT ?g WHERE {
    GRAPH ?g { ?s ?p ?o }
    FILTER(CONTAINS(LCASE(STR(?g)), "vegetable"))
}"""
    page.evaluate(f"""() => {{
        const cm = document.querySelector('.CodeMirror');
        if (cm && cm.CodeMirror) {{ cm.CodeMirror.setValue({repr(check_query)}); }}
    }}""")
    time.sleep(0.3)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    results = page.evaluate("""() => {
        const cells = document.querySelectorAll('table td');
        return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 5);
    }""")
    if results:
        print(f"  WARNING: Still have vegetable graphs: {results}")
    else:
        print("  All vegetable graphs removed!")

    # Check vocabularies page
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    links = page.locator('a')
    found = []
    for i in range(links.count()):
        link = links.nth(i)
        if link.is_visible():
            text = link.inner_text().strip()
            if 'vegetable' in text.lower():
                found.append(text)
    if found:
        print(f"  WARNING: Vocabularies still listed: {found}")
    else:
        print("  Vocabularies page clean!")

    page.screenshot(path="cert-screenshots/nuke-result.png")
    time.sleep(2)
    browser.close()
