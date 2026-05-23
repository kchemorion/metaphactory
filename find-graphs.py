#!/usr/bin/env python3
"""Find all named graphs and vocabulary-related data to figure out deletion."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

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

    # Query 1: Find all named graphs
    def run_query(query, label):
        page.goto(f"{BASE_URL}/sparql")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{ cm.CodeMirror.setValue({repr(query)}); }}
        }}""")
        time.sleep(0.5)
        page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
        time.sleep(3)

        # Try to read the results table
        results = page.evaluate("""() => {
            const cells = document.querySelectorAll('.sparql-query-result td, .result-table td, table td');
            return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 0);
        }""")
        print(f"\n=== {label} ===")
        for r in results[:50]:
            print(f"  {r[:120]}")
        return results

    # Find all graphs with 'vegetable' or 'Vegetables' in any triple
    run_query("""
SELECT DISTINCT ?g WHERE {
    GRAPH ?g { ?s ?p ?o }
    FILTER(
        CONTAINS(LCASE(STR(?g)), "vegetable") ||
        CONTAINS(LCASE(STR(?s)), "vegetable") ||
        CONTAINS(LCASE(STR(?o)), "vegetable")
    )
}""", "Graphs containing 'vegetable' data")

    # Find vocabulary metadata - where are vocabularies registered?
    run_query("""
SELECT DISTINCT ?g ?s ?type WHERE {
    GRAPH ?g {
        ?s a ?type .
        FILTER(CONTAINS(LCASE(STR(?s)), "vegetable"))
    }
} LIMIT 30""", "Graphs with vegetable entities")

    # Check the asset metadata graph
    run_query("""
SELECT ?s ?p ?o WHERE {
    ?s ?p ?o .
    FILTER(CONTAINS(LCASE(STR(?s)), "vegetable"))
} LIMIT 30""", "Default graph vegetable triples")

    # Check all concept scheme entries
    run_query("""
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT ?g ?cs ?label WHERE {
    GRAPH ?g {
        ?cs a skos:ConceptScheme .
        OPTIONAL { ?cs skos:prefLabel ?label }
    }
    FILTER(CONTAINS(LCASE(STR(?cs)), "vegetable") || CONTAINS(LCASE(STR(?label)), "vegetable"))
} LIMIT 20""", "Concept schemes with 'vegetable'")

    time.sleep(2)
    browser.close()
