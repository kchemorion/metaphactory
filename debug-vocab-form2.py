#!/usr/bin/env python3
"""Debug vocabulary creation - focus on what enables the Create button."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
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
    time.sleep(3)

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title using fill() and dispatch input event
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.click()
    title_input.fill("Vegetables for Recipes")
    # Dispatch input and change events to trigger React state updates
    title_input.dispatch_event("input")
    title_input.dispatch_event("change")
    time.sleep(2)

    # Check all field values
    print("=== AFTER FILL + DISPATCH ===")
    location = page.locator('input[data-testid="asset-location-input"]').first
    print(f"Location value: {location.get_attribute('value')}")

    iri_input = page.locator('input[data-testid="suggest-iri-vocabulary-input"]')
    if iri_input.count() > 0 and iri_input.first.is_visible():
        print(f"IRI value: {iri_input.first.get_attribute('value')}")

    create_dialog_btn = page.locator('.modal button:has-text("Create")').first
    print(f"Create disabled: {create_dialog_btn.get_attribute('disabled')}")

    # Try pressing Tab to leave the field
    title_input.press("Tab")
    time.sleep(2)
    print(f"\nAfter Tab:")
    print(f"Location value: {location.get_attribute('value')}")
    print(f"Create disabled: {create_dialog_btn.get_attribute('disabled')}")

    # Try clicking the title input and pressing Enter
    title_input.click()
    title_input.press("Enter")
    time.sleep(2)
    print(f"\nAfter Enter:")
    print(f"Location value: {location.get_attribute('value')}")
    print(f"Create disabled: {create_dialog_btn.get_attribute('disabled')}")

    page.screenshot(path="cert-screenshots/debug2-after-enter.png")

    # Try clearing and re-typing character by character
    title_input.click()
    title_input.fill("")
    time.sleep(0.5)
    for char in "Vegetables":
        title_input.press(char)
        time.sleep(0.05)
    time.sleep(2)

    print(f"\nAfter character-by-character typing 'Vegetables':")
    print(f"Location value: {location.get_attribute('value')}")
    print(f"Create disabled: {create_dialog_btn.get_attribute('disabled')}")

    # Check if there are validation messages
    errors = page.locator('.invalid-feedback, .error, .text-danger, [class*="error"], [class*="invalid"]')
    print(f"\nError messages: {errors.count()}")
    for i in range(errors.count()):
        err = errors.nth(i)
        if err.is_visible():
            print(f"  Error: {err.inner_text().strip()}")

    # Try looking at the complete form state via JS
    form_state = page.evaluate("""() => {
        const modal = document.querySelector('.modal.show');
        if (!modal) return 'no modal';
        const inputs = modal.querySelectorAll('input, select, textarea');
        const state = [];
        inputs.forEach(inp => {
            state.push({
                tag: inp.tagName,
                type: inp.type,
                name: inp.name,
                id: inp.id,
                value: inp.value,
                placeholder: inp.placeholder,
                disabled: inp.disabled,
                checked: inp.checked,
                testid: inp.getAttribute('data-testid')
            });
        });
        return state;
    }""")
    print(f"\n=== COMPLETE FORM STATE ===")
    for s in form_state:
        if s.get('value') or s.get('checked'):
            print(f"  {s}")

    page.screenshot(path="cert-screenshots/debug2-final.png")

    time.sleep(3)
    browser.close()
