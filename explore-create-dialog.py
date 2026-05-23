#!/usr/bin/env python3
"""Explore the Create Ontology dialog to understand why button stays disabled."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:10214"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(15000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Go to Ontologies
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(3)

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Capture the dialog state before typing
    print("=== DIALOG STATE BEFORE TYPING ===")
    dialog = page.locator('.modal.show, [role="dialog"].show').first
    if dialog.is_visible():
        print(f"Dialog visible: true")
        inner = dialog.inner_html()
        # Look for inputs
        inputs = dialog.locator('input')
        count = inputs.count()
        print(f"Input count: {count}")
        for i in range(count):
            inp = inputs.nth(i)
            attrs = {}
            for attr in ['type', 'data-testid', 'placeholder', 'name', 'value', 'disabled', 'checked']:
                val = inp.get_attribute(attr)
                if val is not None:
                    attrs[attr] = val
            print(f"  Input {i}: {attrs}")

        # Look for buttons
        buttons = dialog.locator('button')
        bcount = buttons.count()
        print(f"Button count: {bcount}")
        for i in range(bcount):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            disabled = btn.get_attribute("disabled")
            print(f"  Button {i}: '{text}' disabled={disabled}")

    # Type the title
    print("\n=== TYPING TITLE ===")
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.click()
    title_input.type("MIGx Enterprise Ontology")
    time.sleep(1)

    # Check state after typing
    print("\n=== DIALOG STATE AFTER TYPING (Suggest IRI checked) ===")
    inputs = dialog.locator('input')
    count = inputs.count()
    for i in range(count):
        inp = inputs.nth(i)
        attrs = {}
        for attr in ['type', 'data-testid', 'placeholder', 'name', 'value', 'disabled', 'checked']:
            val = inp.get_attribute(attr)
            if val is not None:
                attrs[attr] = val
        print(f"  Input {i}: {attrs}")

    buttons = dialog.locator('button')
    bcount = buttons.count()
    for i in range(bcount):
        btn = buttons.nth(i)
        text = btn.inner_text().strip()
        disabled = btn.get_attribute("disabled")
        print(f"  Button {i}: '{text}' disabled={disabled}")

    # Try pressing Tab to trigger blur
    print("\n=== AFTER TAB (trigger blur) ===")
    page.keyboard.press("Tab")
    time.sleep(2)

    buttons = dialog.locator('button')
    bcount = buttons.count()
    for i in range(bcount):
        btn = buttons.nth(i)
        text = btn.inner_text().strip()
        disabled = btn.get_attribute("disabled")
        print(f"  Button {i}: '{text}' disabled={disabled}")

    # Check IRI value
    iri_inputs = dialog.locator('input[data-testid*="iri"], input[data-testid*="suggest"]')
    icount = iri_inputs.count()
    print(f"IRI-related inputs: {icount}")
    for i in range(icount):
        inp = iri_inputs.nth(i)
        val = inp.input_value()
        testid = inp.get_attribute("data-testid")
        print(f"  {testid}: '{val}'")

    # Now try unchecking suggest IRI and setting a custom one
    print("\n=== UNCHECK SUGGEST IRI ===")
    suggest_cb = page.locator('input[data-testid="suggest-iri-ontology"]').first
    if suggest_cb.is_visible(timeout=2000):
        checked = suggest_cb.is_checked()
        print(f"  Suggest IRI checked: {checked}")
        if checked:
            suggest_cb.click()
            time.sleep(1)

    # Check for IRI input
    iri_input = page.locator('input[data-testid="suggest-iri-ontology-input"]').first
    if iri_input.is_visible(timeout=2000):
        current = iri_input.input_value()
        print(f"  Current IRI: '{current}'")

        # Set a custom IRI that doesn't conflict
        iri_input.click()
        iri_input.fill("")
        iri_input.type("https://purl.migx.ch/ontology/enterprise/MIGxEnterpriseOntology")
        time.sleep(1)

        new_val = iri_input.input_value()
        print(f"  New IRI: '{new_val}'")

    # Check Create button state
    print("\n=== FINAL BUTTON STATE ===")
    buttons = dialog.locator('button')
    bcount = buttons.count()
    for i in range(bcount):
        btn = buttons.nth(i)
        text = btn.inner_text().strip()
        disabled = btn.get_attribute("disabled")
        print(f"  Button {i}: '{text}' disabled={disabled}")

    time.sleep(5)
    browser.close()
