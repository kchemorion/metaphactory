#!/usr/bin/env python3
"""Debug the vocabulary concept creation form to understand what enables Save."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Navigate to Vocabularies
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Screenshot the create dialog
    page.screenshot(path="cert-screenshots/debug-create-dialog.png")

    # Explore the dialog structure
    print("=== CREATE VOCABULARY DIALOG ===")
    dialog = page.locator('.modal.show, [role="dialog"]').first
    if dialog.is_visible():
        # Get all inputs
        inputs = dialog.locator('input, textarea, select')
        print(f"Inputs found: {inputs.count()}")
        for i in range(inputs.count()):
            inp = inputs.nth(i)
            attrs = {}
            for attr in ['type', 'data-testid', 'placeholder', 'name', 'value', 'disabled', 'checked', 'class', 'id']:
                val = inp.get_attribute(attr)
                if val is not None:
                    attrs[attr] = val[:80]
            tag = inp.evaluate("el => el.tagName")
            print(f"  {tag} {i}: {attrs}")

        # Get all buttons
        buttons = dialog.locator('button')
        print(f"\nButtons found: {buttons.count()}")
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            text = btn.inner_text().strip()
            disabled = btn.get_attribute('disabled')
            cls = btn.get_attribute('class') or ''
            print(f"  Button {i}: '{text}' disabled={disabled} class={cls[:60]}")

    # Fill title
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.click()
    title_input.type("Vegetables for Recipes")
    time.sleep(1)

    page.screenshot(path="cert-screenshots/debug-after-title.png")

    # Check the IRI field state
    print("\n=== AFTER TITLE ===")
    iri_input = page.locator('input[data-testid="suggest-iri-vocabulary-input"]')
    if iri_input.count() > 0:
        print(f"IRI input visible: {iri_input.first.is_visible()}")
        print(f"IRI value: {iri_input.first.get_attribute('value')}")

    suggest_cb = page.locator('input[data-testid="suggest-iri-vocabulary"]')
    if suggest_cb.count() > 0:
        print(f"Suggest IRI checkbox checked: {suggest_cb.first.is_checked()}")

    # Check Create button state
    create_btns = page.locator('.modal button:has-text("Create")')
    for i in range(create_btns.count()):
        btn = create_btns.nth(i)
        print(f"Create button {i}: disabled={btn.get_attribute('disabled')} text='{btn.inner_text().strip()}'")

    # Wait and check again
    time.sleep(2)
    for i in range(create_btns.count()):
        btn = create_btns.nth(i)
        print(f"Create button {i} (after wait): disabled={btn.get_attribute('disabled')}")

    # Click Create (if enabled)
    dialog_create = page.locator('.modal button:has-text("Create")').first
    for _ in range(20):
        if dialog_create.get_attribute("disabled") is None:
            break
        time.sleep(0.5)

    if dialog_create.get_attribute("disabled") is None:
        print("\nCreate button ENABLED - clicking")
        dialog_create.click()
        time.sleep(5)

        # Dismiss walkthrough
        try:
            page.keyboard.press('Escape')
            time.sleep(1)
        except:
            pass

        page.screenshot(path="cert-screenshots/debug-vocab-editor.png")
        print(f"\nURL after create: {page.url}")

        # Now explore the concept creation form
        print("\n=== CONCEPT CREATION ===")
        create_term = page.locator('button:has-text("Create top-level term")')
        print(f"Create top-level term visible: {create_term.first.is_visible()}")
        create_term.first.click()
        time.sleep(2)

        page.screenshot(path="cert-screenshots/debug-concept-form.png")

        # Explore the concept form
        print("\n=== CONCEPT FORM ===")
        # Look for the form/modal
        modals = page.locator('.overlay-modal.show, .modal.show, [role="dialog"].show')
        print(f"Modals visible: {modals.count()}")

        # Get ALL inputs on the page (not just in modal)
        all_inputs = page.locator('input, textarea')
        print(f"\nAll inputs on page: {all_inputs.count()}")
        for i in range(all_inputs.count()):
            inp = all_inputs.nth(i)
            if inp.is_visible():
                attrs = {}
                for attr in ['type', 'placeholder', 'name', 'data-testid', 'value', 'class']:
                    val = inp.get_attribute(attr)
                    if val is not None:
                        attrs[attr] = val[:80]
                tag = inp.evaluate("el => el.tagName")
                print(f"  VISIBLE {tag}: {attrs}")

        # Find all buttons currently visible
        all_btns = page.locator('button')
        print(f"\nAll visible buttons:")
        for i in range(all_btns.count()):
            btn = all_btns.nth(i)
            if btn.is_visible():
                text = btn.inner_text().strip()[:50]
                disabled = btn.get_attribute('disabled')
                name = btn.get_attribute('name')
                if text:
                    print(f"  Button: '{text}' disabled={disabled} name={name}")

        # Try filling the preferred label
        pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
        if pref_input.is_visible():
            print(f"\nPreferred label input found, filling...")
            pref_input.click()
            pref_input.fill("")
            pref_input.type("Vegetables")
            time.sleep(1)

            page.screenshot(path="cert-screenshots/debug-concept-filled.png")

            # Check Save button state now
            save_btns = page.locator('button[name="submit"]')
            for i in range(save_btns.count()):
                btn = save_btns.nth(i)
                if btn.is_visible():
                    print(f"  Save button: disabled={btn.get_attribute('disabled')} text='{btn.inner_text().strip()}'")

            # Also check if there's a confirm/add button
            action_btns = page.locator('button:has-text("Save"), button:has-text("Add"), button:has-text("Create"), button:has-text("Confirm")')
            for i in range(action_btns.count()):
                btn = action_btns.nth(i)
                if btn.is_visible():
                    print(f"  Action button: '{btn.inner_text().strip()}' disabled={btn.get_attribute('disabled')} name={btn.get_attribute('name')}")

            # Try pressing Enter or Tab to trigger validation
            pref_input.press("Tab")
            time.sleep(1)

            save_btns = page.locator('button[name="submit"]')
            for i in range(save_btns.count()):
                btn = save_btns.nth(i)
                if btn.is_visible():
                    print(f"  Save button after Tab: disabled={btn.get_attribute('disabled')}")

            # Also try clicking outside the input
            page.locator('body').click(position={"x": 10, "y": 10}, force=True)
            time.sleep(1)
            for i in range(save_btns.count()):
                btn = save_btns.nth(i)
                if btn.is_visible():
                    print(f"  Save button after blur: disabled={btn.get_attribute('disabled')}")

        else:
            print("Preferred label input NOT found")
            # Try other selectors
            for sel in ['input[placeholder*="label" i]', 'input[placeholder*="Enter" i]', 'input[type="text"]']:
                matches = page.locator(sel)
                for i in range(matches.count()):
                    m = matches.nth(i)
                    if m.is_visible():
                        print(f"  Found via '{sel}': placeholder={m.get_attribute('placeholder')} value={m.get_attribute('value')}")

    else:
        print("\nCreate button still DISABLED!")
        page.screenshot(path="cert-screenshots/debug-create-disabled.png")

    # Wait for user to observe
    time.sleep(5)
    browser.close()
