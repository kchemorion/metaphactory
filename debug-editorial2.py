#!/usr/bin/env python3
"""Focused exploration of ontology editorial workflow."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Open Recipes ontology
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Step 1: Role assignment - add self as reviewer
    print("=== STEP 1: ROLE ASSIGNMENT ===")
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    more_btn.click()
    time.sleep(1)

    role_opt = page.locator('.dropdown-menu.show a:has-text("Role assignment")').first
    if role_opt.is_visible(timeout=2000):
        role_opt.click()
        time.sleep(2)
        page.screenshot(path="cert-screenshots/debug-role-dialog.png", full_page=True)

        # Dump everything in the modal
        modal = page.locator('.modal.show')
        if modal.is_visible():
            print(f"Modal text:\n{modal.inner_text()[:1000]}")
            print(f"\nModal HTML (controls only):")
            controls = modal.evaluate("""el => {
                const items = [];
                el.querySelectorAll('input, select, button, a, [role="button"]').forEach(c => {
                    if (c.offsetParent !== null) {
                        items.push({
                            tag: c.tagName,
                            type: c.type,
                            placeholder: c.placeholder,
                            text: c.textContent?.trim()?.substring(0, 50),
                            class: c.className?.substring(0, 60),
                            name: c.name,
                            value: c.value?.substring(0, 50)
                        });
                    }
                });
                return items;
            }""")
            for c in controls:
                print(f"  {c}")

        page.keyboard.press('Escape')
        time.sleep(0.5)

    # Step 2: Check Info & Metadata tab for editorial status
    print("\n=== STEP 2: INFO & METADATA ===")
    info_tab = page.locator('button:has-text("Info & Metadata")').first
    if info_tab.is_visible(timeout=2000):
        info_tab.click()
        time.sleep(2)
        page.screenshot(path="cert-screenshots/debug-onto-info-tab.png", full_page=True)

        # Get all text
        content = page.locator('.page-content-wrapper, main').first.inner_text()
        print(content[:2000])

    # Step 3: Check for status/workflow buttons in the header area
    print("\n=== STEP 3: ALL BUTTONS ===")
    buttons = page.locator('button, a.btn')
    for i in range(buttons.count()):
        btn = buttons.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            if text and len(text) > 1:
                print(f"  '{text}'")

    time.sleep(2)
    browser.close()
