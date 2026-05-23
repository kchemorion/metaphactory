#!/usr/bin/env python3
"""Verify recipe instances exist."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    query = """PREFIX recipe: <http://ontologies.metaphacts.com/recipes/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?instance ?type ?label WHERE {
    ?instance a ?type .
    ?instance rdfs:label ?label .
    FILTER(STRSTARTS(STR(?instance), "http://ontologies.metaphacts.com/recipes/"))
    FILTER(?type != <http://www.w3.org/2002/07/owl#Class>)
}
ORDER BY ?type ?label"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    page.screenshot(path="cert-screenshots/verify-instances.png")

    results = page.evaluate("""() => {
        const rows = document.querySelectorAll('table tbody tr');
        return Array.from(rows).map(r => {
            const cells = r.querySelectorAll('td');
            return Array.from(cells).map(c => c.textContent.trim()).join(' | ');
        });
    }""")
    print(f"=== INSTANCES ({len(results)} rows) ===")
    for r in results[:30]:
        print(f"  {r}")

    browser.close()
