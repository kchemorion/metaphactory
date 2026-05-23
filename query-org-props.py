#!/usr/bin/env python3
"""Get the actual properties of metaphacts org instance as text."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
IRI = "https://ontologies.metaphacts.com/organization-ontology/Organization/instances/d6e6251a-ce86-4e94-9c10-6bade6713932"

def run_query(page, query):
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(1)
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query)}); }}
    }}""")
    time.sleep(0.3)
    page.locator('button:has-text("Execute")').first.click()
    time.sleep(3)
    # Get results as text from the page
    result_text = page.evaluate("""() => {
        const rows = document.querySelectorAll('.sparql-query-result tr, .result-table tr, table.table tr');
        return Array.from(rows).slice(0, 30).map(r => {
            const cells = r.querySelectorAll('td, th');
            return Array.from(cells).map(c => c.textContent.replace('content_copy', '').trim()).join(' | ');
        }).filter(r => r.length > 5);
    }""")
    return result_text

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Query 1: All outgoing properties
    print("=== OUTGOING PROPERTIES ===")
    results = run_query(page, f"SELECT ?p ?o WHERE {{ <{IRI}> ?p ?o }}")
    for r in results:
        print(f"  {r}")

    # Query 2: All incoming properties (what points TO metaphacts)
    print("\n=== INCOMING PROPERTIES ===")
    results = run_query(page, f"SELECT ?s ?p WHERE {{ ?s ?p <{IRI}> }} LIMIT 20")
    for r in results:
        print(f"  {r}")

    # Query 3: Members with labels
    print("\n=== MEMBERS (various predicates) ===")
    results = run_query(page, f"""
PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?member ?label ?via WHERE {{
    {{ ?member org:memberOf <{IRI}> . BIND("memberOf" AS ?via) }}
    UNION
    {{ <{IRI}> org:hasMember ?member . BIND("hasMember" AS ?via) }}
    UNION
    {{ ?member <http://www.w3.org/ns/org#memberOf> <{IRI}> . BIND("w3-memberOf" AS ?via) }}
    OPTIONAL {{ ?member rdfs:label ?label }}
}}""")
    for r in results:
        print(f"  {r}")

    # Query 4: Projects
    print("\n=== PROJECTS ===")
    results = run_query(page, f"""
PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?project ?name ?via WHERE {{
    {{ ?project org:hasClient <{IRI}> . BIND("hasClient" AS ?via) }}
    UNION
    {{ <{IRI}> org:hasProject ?project . BIND("hasProject" AS ?via) }}
    OPTIONAL {{ ?project rdfs:label ?name }}
}}""")
    for r in results:
        print(f"  {r}")

    browser.close()
