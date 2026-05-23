#!/usr/bin/env python3
"""Create recipe instances via SPARQL INSERT and the Visual Instance Authoring form."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # First find the Recipes ontology IRI
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Get the Recipes ontology IRI from the link
    recipes_link = page.locator('a:has-text("Recipes")').last
    recipes_href = recipes_link.get_attribute('href') or ''
    print(f"Recipes link href: {recipes_href}")

    # Navigate to the ontology to find class IRIs
    recipes_link.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    onto_url = page.url
    print(f"Ontology URL: {onto_url}")

    # Extract the ontology base IRI from the URL
    # It should be something like https://ontologies.metaphacts.com/recipes/0.1
    # The classes would be under this namespace
    page.screenshot(path="cert-screenshots/debug-onto-for-instances.png")

    # Try to find class IRIs by looking at the ontology editor's class list
    print("\n=== FINDING CLASS IRIS ===")
    class_iris = page.evaluate("""() => {
        // Look for class elements in the ontology canvas or list
        const elements = document.querySelectorAll('[data-testid*="class"], [class*="class-node"], a[href*="ontology"]');
        const iris = [];
        elements.forEach(el => {
            const href = el.getAttribute('href') || '';
            const text = el.textContent.trim();
            if (text && href) iris.push({text: text.substring(0, 40), href: href.substring(0, 100)});
        });
        return iris;
    }""")
    for cls in class_iris[:10]:
        print(f"  {cls}")

    # Use SPARQL to find the Recipe class IRI
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    find_classes_query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?label WHERE {
    ?class a owl:Class .
    OPTIONAL { ?class rdfs:label ?label }
    FILTER(CONTAINS(LCASE(STR(?class)), "recipe") || CONTAINS(LCASE(STR(?label)), "recipe"))
} LIMIT 20"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(find_classes_query)}); }}
        else {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{ cm.CodeMirror.setValue({repr(find_classes_query)}); }}
        }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    results = page.evaluate("""() => {
        const cells = document.querySelectorAll('table td');
        return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 5);
    }""")
    print(f"\n=== RECIPE CLASSES ===")
    for r in results[:20]:
        print(f"  {r}")

    page.screenshot(path="cert-screenshots/debug-recipe-classes.png")

    # Also find ALL classes in the ontology
    find_all_query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class ?label WHERE {
    ?class a owl:Class .
    OPTIONAL { ?class rdfs:label ?label }
    FILTER(CONTAINS(STR(?class), "recipes") || CONTAINS(STR(?class), "Recipes"))
} LIMIT 30"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(find_all_query)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    results2 = page.evaluate("""() => {
        const cells = document.querySelectorAll('table td');
        return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 5);
    }""")
    print(f"\n=== ALL ONTOLOGY CLASSES ===")
    for r in results2[:30]:
        print(f"  {r}")

    page.screenshot(path="cert-screenshots/debug-all-classes.png")
    time.sleep(2)
    browser.close()
