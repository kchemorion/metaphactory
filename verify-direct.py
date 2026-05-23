#!/usr/bin/env python3
"""Check if INSERT actually persisted by querying specific instance."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=100)
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

    # Direct check for PastaPrimavera
    query = """SELECT * WHERE {
    <http://ontologies.metaphacts.com/recipes/PastaPrimavera> ?p ?o
} LIMIT 10"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    results = page.evaluate("""() => {
        const cells = document.querySelectorAll('table td');
        return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 3);
    }""")
    print(f"PastaPrimavera triples: {len(results)}")
    for r in results[:20]:
        print(f"  {r}")

    if not results:
        print("\nINSERT didn't persist! Trying to find WHY...")
        # Check if we can do a simple INSERT test
        test_query = """INSERT DATA {
    <http://test.example.com/test1> <http://www.w3.org/2000/01/rdf-schema#label> "test" .
}"""
        page.evaluate(f"""() => {{
            const editors = window.monaco?.editor?.getEditors?.();
            if (editors && editors.length > 0) {{ editors[0].setValue({repr(test_query)}); }}
        }}""")
        time.sleep(0.5)
        page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
        time.sleep(3)

        # Check the result message
        body = page.locator('body').inner_text()
        for line in body.split('\n'):
            if 'error' in line.lower() or 'update' in line.lower() or 'executed' in line.lower():
                print(f"  {line.strip()[:100]}")

        # Now verify
        verify = """SELECT * WHERE {
    <http://test.example.com/test1> ?p ?o
}"""
        page.evaluate(f"""() => {{
            const editors = window.monaco?.editor?.getEditors?.();
            if (editors && editors.length > 0) {{ editors[0].setValue({repr(verify)}); }}
        }}""")
        time.sleep(0.5)
        page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
        time.sleep(3)

        results2 = page.evaluate("""() => {
            const cells = document.querySelectorAll('table td');
            return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 3);
        }""")
        print(f"\nTest insert results: {len(results2)}")
        for r in results2[:10]:
            print(f"  {r}")

    browser.close()
