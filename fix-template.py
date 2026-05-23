#!/usr/bin/env python3
"""Query the actual properties of the metaphacts organization, then write the correct template."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
METAPHACTS_IRI = "https://ontologies.metaphacts.com/organization-ontology/Organization/instances/d6e6251a-ce86-4e94-9c10-6bade6713932"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=150)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Query all properties of the metaphacts organization
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    query = f"""SELECT ?p ?o WHERE {{
    <{METAPHACTS_IRI}> ?p ?o
}} LIMIT 50"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)

    page.screenshot(path="cert-screenshots/debug-metaphacts-props.png")

    # Also query what links TO metaphacts (members, projects)
    query2 = f"""SELECT ?s ?p WHERE {{
    ?s ?p <{METAPHACTS_IRI}>
}} LIMIT 30"""
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query2)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-metaphacts-incoming.png")

    # Query members specifically
    query3 = f"""PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?member ?memberLabel WHERE {{
    ?member org:memberOf <{METAPHACTS_IRI}> .
    OPTIONAL {{ ?member rdfs:label ?memberLabel }}
}} LIMIT 20"""
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query3)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-members.png")

    # Query projects
    query4 = f"""PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?project ?name WHERE {{
    ?project org:hasClient <{METAPHACTS_IRI}> .
    OPTIONAL {{ ?project rdfs:label ?name }}
}} LIMIT 20"""
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(query4)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-projects.png")

    # Now write and save the template
    print("\n=== WRITING TEMPLATE ===")

    TEMPLATE = """<div class="page">
  <h1>[[this]]</h1>
  <p>IRI: [[this]]</p>
  <p>Type: <semantic-link iri="https://ontologies.metaphacts.com/organization-ontology/Organization">Organization</semantic-link></p>

  <semantic-query
    query="SELECT ?label WHERE { ?? rdfs:label ?label }"
    template="<p><b>Label:</b> {{label.value}}</p>">
  </semantic-query>

  <semantic-query
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?member ?memberLabel WHERE { ?member org:memberOf ?? . ?member rdfs:label ?memberLabel }"
    template="<p><b>Members:</b> {{#each bindings}}<semantic-link iri='{{member.value}}'>{{memberLabel.value}}</semantic-link>{{#unless @last}}, {{/unless}}{{/each}}</p>">
  </semantic-query>

  <h3>Project Portfolio</h3>
  <semantic-table
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?name WHERE { ?project org:hasClient ?? . ?project rdfs:label ?name }"
    column-configuration='[{"variableName": "name", "displayName": "name"}]'>
  </semantic-table>
</div>"""

    # Navigate to template editor
    template_url = (f"{BASE_URL}/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies"
                    ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit")
    try:
        page.goto(template_url)
        page.wait_for_load_state("networkidle")
    except:
        pass
    time.sleep(5)

    # Click in the Monaco editor area and replace content
    editor_area = page.locator('.monaco-editor .view-lines').first
    if editor_area.is_visible(timeout=5000):
        editor_area.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        page.keyboard.insert_text(TEMPLATE)
        time.sleep(1)
        print("  Template content inserted")
    else:
        print("  Editor not found!")

    page.screenshot(path="cert-screenshots/fix-template-edited.png")

    # Click Save (not Save & View)
    save_btn = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(3)
        print("  Saved!")
    page.screenshot(path="cert-screenshots/fix-template-saved.png")

    # Now verify by visiting the metaphacts instance page
    page.goto(f"{BASE_URL}/resource/?uri={METAPHACTS_IRI.replace(':', '%3A').replace('/', '%2F')}")
    time.sleep(5)
    page.screenshot(path="cert-screenshots/fix-template-rendered.png")
    print("  Rendered instance page")

    time.sleep(3)
    browser.close()
