#!/usr/bin/env python3
"""Write the Project knowledge panel template with correct properties."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

PANEL_TEMPLATE = """<div class="knowledge-panel">
  <h3><mp-label iri='[[this]]'></mp-label></h3>

  <semantic-query
    query="SELECT ?label WHERE { ?? rdfs:label ?label }"
    template="<p><b>Label:</b> {{label.value}}</p>">
  </semantic-query>

  <semantic-query
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?member ?memberLabel WHERE {
             ?member org:isInvolvedIn ?? .
             ?member a org:Person .
             ?member rdfs:label ?memberLabel
           }"
    template="<p><b>Members:</b> {{#each bindings}}<semantic-link iri='{{member.value}}'>{{memberLabel.value}}</semantic-link>{{#unless @last}}, {{/unless}}{{/each}}</p>">
  </semantic-query>

  <semantic-query
    query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
           SELECT ?org ?orgLabel WHERE {
             ?org org:isInvolvedIn ?? .
             ?org a org:Organization .
             ?org rdfs:label ?orgLabel
           }"
    template="<p><b>Organizations:</b> {{#each bindings}}<semantic-link iri='{{org.value}}'>{{orgLabel.value}}</semantic-link>{{#unless @last}}, {{/unless}}{{/each}}</p>">
  </semantic-query>
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

    # Navigate to PanelTemplate for Project (action=edit)
    url = (f"{BASE_URL}/resource/?uri=PanelTemplate%3Ahttps%3A%2F%2Fontologies"
           ".metaphacts.com%2Forganization-ontology%2FProject&action=edit")
    try:
        page.goto(url)
        page.wait_for_load_state("networkidle")
    except:
        pass
    time.sleep(5)

    # Insert content via keyboard
    editor = page.locator('.monaco-editor .view-lines').first
    if editor.is_visible(timeout=5000):
        editor.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        page.keyboard.insert_text(PANEL_TEMPLATE)
        time.sleep(1)
        print("Panel template content inserted")

    page.screenshot(path="cert-screenshots/panel-project-edited.png")

    # Save
    save_btn = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(3)
        print("Saved!")

    page.screenshot(path="cert-screenshots/panel-project-saved.png")
    time.sleep(2)
    browser.close()
