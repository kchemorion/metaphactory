#!/usr/bin/env python3
"""Explore the Import ontology modal in the Ontology Editor."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:10214"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()

    # Login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    print("Logged in\n")

    # Navigate to Ontologies
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Check if any ontologies already exist
    existing = page.locator('table tbody tr, .asset-list-item, [class*="asset"]').all()
    print(f"Existing ontologies on page: {len(existing)}")

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title using data-testid
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.click()
    title_input.type("Test Ontology")
    time.sleep(0.5)

    # Uncheck Suggest IRI
    suggest_cb = page.locator('input[data-testid="suggest-iri-ontology"]').first
    if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
        suggest_cb.click()
        time.sleep(0.5)

    # Fill IRI
    iri_input = page.locator('input[data-testid="asset-iri-input"], input[placeholder*="IRI"]').first
    if iri_input.is_visible(timeout=1500):
        iri_input.click()
        iri_input.fill("")
        iri_input.type("https://example.org/test-ontology/")
        time.sleep(0.3)

    page.screenshot(path="/Users/kiptengwer/Documents/metaphactory-tutorial/screenshots/explore-iri-unchecked.png")

    # Click Create in dialog
    dialog_create = page.locator('.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")').first
    for _ in range(10):
        if dialog_create.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    dialog_create.click()
    time.sleep(3)

    # Dismiss walkthrough
    for _ in range(5):
        try:
            wt = page.locator('.walkthroughCarousel.show, .modal.show')
            if wt.is_visible(timeout=1000):
                close_btn = page.locator('.modal.show .btn-close, .modal.show [class*="close"]')
                if close_btn.count() > 0 and close_btn.first.is_visible(timeout=500):
                    close_btn.first.click(force=True)
                else:
                    page.keyboard.press('Escape')
            else:
                break
        except:
            page.keyboard.press('Escape')
    time.sleep(0.5)

    page.screenshot(path="/Users/kiptengwer/Documents/metaphactory-tutorial/screenshots/test-create-result.png")
    print("Ontology editor opened\n")

    # Now explore Info & Metadata tab
    info_tab = page.locator('button:has-text("Info & Metadata"), button:has-text("Info")').first
    if info_tab.is_visible(timeout=2000):
        info_tab.click()
        time.sleep(1)
        print("Info & Metadata tab clicked\n")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)

        # Look for Import ontology button
        import_btn = page.locator('button:has-text("Import ontology")').first
        if import_btn.is_visible(timeout=2000):
            print("Found 'Import ontology' button")
            import_btn.click()
            time.sleep(2)

            # Capture the modal
            modal = page.locator('.import-ontology-modal.show, [aria-label="Import ontology"]').first
            if modal.is_visible(timeout=2000):
                inner = modal.inner_html()
                print(f"\nImport modal HTML (first 3000 chars):\n{inner[:3000]}\n")

                # Find all inputs
                inputs = modal.locator('input, textarea, select').all()
                for i, inp in enumerate(inputs):
                    tag = inp.evaluate("el => el.tagName")
                    name = inp.get_attribute("name") or ""
                    ph = inp.get_attribute("placeholder") or ""
                    typ = inp.get_attribute("type") or ""
                    vis = inp.is_visible()
                    print(f"  Input [{i}]: tag={tag} name='{name}' placeholder='{ph}' type='{typ}' visible={vis}")

                # Find all buttons
                btns = modal.locator('button').all()
                for b in btns:
                    text = b.text_content().strip()
                    disabled = b.get_attribute("disabled")
                    cls = b.get_attribute("class") or ""
                    print(f"  Button: text='{text}' disabled={disabled} class='{cls}'")

                page.screenshot(path="/Users/kiptengwer/Documents/metaphactory-tutorial/screenshots/explore-import-modal.png")

                # Try filling and importing
                modal_input = modal.locator('input[type="text"], input').first
                if modal_input.is_visible(timeout=1000):
                    modal_input.fill("http://www.w3.org/2004/02/skos/core")
                    time.sleep(1)
                    print("\nFilled IRI, re-checking buttons:")
                    btns = modal.locator('button').all()
                    for b in btns:
                        text = b.text_content().strip()
                        disabled = b.get_attribute("disabled")
                        print(f"  Button: text='{text}' disabled={disabled}")

                    # Click the import/confirm button
                    confirm_btn = modal.locator('button.btn-primary, button:has-text("Import")').first
                    if confirm_btn.is_visible(timeout=500):
                        print(f"\nClicking confirm button: '{confirm_btn.text_content().strip()}'")
                        confirm_btn.click()
                        time.sleep(2)

                        # Check if modal closed
                        still_visible = page.locator('.import-ontology-modal.show').is_visible(timeout=1000)
                        print(f"Modal still visible after import: {still_visible}")
                        if still_visible:
                            # Check for error messages
                            errors = page.locator('.import-ontology-modal.show .alert, .import-ontology-modal.show .error, .import-ontology-modal.show [class*="error"]').all()
                            for e in errors:
                                print(f"  Error: {e.text_content().strip()[:200]}")
                            page.screenshot(path="/Users/kiptengwer/Documents/metaphactory-tutorial/screenshots/explore-import-after-click.png")
            else:
                print("Import modal did NOT appear")
        else:
            print("'Import ontology' button not found")
    else:
        print("Info & Metadata tab not found")

    browser.close()
    print("\nDone.")
