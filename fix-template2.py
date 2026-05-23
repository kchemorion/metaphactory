#!/usr/bin/env python3
"""Write the correct template with actual property names from the data."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

TEMPLATE = """<div class="page">
  <h1><mp-label iri='[[this]]'></mp-label></h1>
  <p>IRI: [[this]]</p>
  <p>Type: <semantic-link iri="https://ontologies.metaphacts.com/organization-ontology/Organization">Organization</semantic-link></p>

  <semantic-query
    query="SELECT ?label WHERE { ?? rdfs:label ?label }"
    template="<p><b>Label:</b> {{label.value}}</p>">
  </semantic-query>

  <semantic-query
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?member ?memberLabel WHERE { ?? org:hasMember ?member . ?member rdfs:label ?memberLabel }"
    template="<p><b>Members:</b> {{#each bindings}}<semantic-link iri='{{member.value}}'>{{memberLabel.value}}</semantic-link>{{#unless @last}}, {{/unless}}{{/each}}</p>">
  </semantic-query>

  <h3>Project Portfolio</h3>
  <semantic-table
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?name WHERE { ?? org:isInvolvedIn ?project . ?project rdfs:label ?name }"
    column-configuration='[{"variableName": "name", "displayName": "name"}]'>
  </semantic-table>
</div>"""

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

    # Navigate to template editor
    url = (f"{BASE_URL}/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies"
           ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit")
    try:
        page.goto(url)
        page.wait_for_load_state("networkidle")
    except:
        pass
    time.sleep(5)

    # Click in Monaco editor and replace content
    editor = page.locator('.monaco-editor .view-lines').first
    if editor.is_visible(timeout=5000):
        editor.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        page.keyboard.insert_text(TEMPLATE)
        time.sleep(1)
        print("Template content inserted")

    # Click Save
    save_btn = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(3)
        print("Saved!")

    page.screenshot(path="cert-screenshots/fix2-saved.png")

    # Verify by visiting metaphacts instance
    page.goto(f"{BASE_URL}/resource/?uri=https%3A%2F%2Fontologies.metaphacts.com%2Forganization-ontology%2FOrganization%2Finstances%2Fd6e6251a-ce86-4e94-9c10-6bade6713932")
    time.sleep(5)
    page.screenshot(path="cert-screenshots/fix2-rendered.png")
    print("Rendered!")

    time.sleep(3)
    browser.close()
