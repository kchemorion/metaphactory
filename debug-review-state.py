#!/usr/bin/env python3
"""Check the current state of Recipes ontology after user started review."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Go to Ontologies catalog
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-review-catalog.png", full_page=True)

    # Check the more_vert menu for Recipes now
    print("=== RECIPES MORE_VERT MENU (after review started) ===")
    more_btn = page.locator('button:has-text("more_vert")').first
    more_btn.click()
    time.sleep(1)
    page.screenshot(path="cert-screenshots/debug-review-menu.png")

    dropdown = page.locator('.dropdown-menu.show')
    if dropdown.is_visible():
        items = dropdown.locator('a, button, .dropdown-item')
        for i in range(items.count()):
            item = items.nth(i)
            text = item.inner_text().strip()[:60]
            if text:
                print(f"  '{text}'")

        # Check More submenu
        more_sub = dropdown.locator('a:has-text("More"), button:has-text("More")').first
        if more_sub.is_visible():
            more_sub.hover()
            time.sleep(1)
            all_items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button, .dropdown-item')
            print(f"\n  More submenu:")
            for i in range(all_items.count()):
                item = all_items.nth(i)
                if item.is_visible():
                    text = item.inner_text().strip()[:60]
                    if text and text != 'More':
                        print(f"    '{text}'")

    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Open the ontology to check for review controls inside
    print("\n=== OPENING RECIPES ONTOLOGY ===")
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)
    page.screenshot(path="cert-screenshots/debug-review-ontology.png", full_page=True)

    # Check for review/accept/publish buttons
    print("\nAll visible buttons with review/publish/accept keywords:")
    buttons = page.locator('button, a.btn, a')
    for i in range(buttons.count()):
        btn = buttons.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            if any(kw in text.lower() for kw in ['review', 'accept', 'publish', 'approve', 'reject', 'version', 'request']):
                print(f"  '{text}'")

    # Check the More dropdown inside the ontology
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=2000):
        more_btn.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-review-inside-more.png")
        dropdown = page.locator('.dropdown-menu.show')
        if dropdown.is_visible():
            items = dropdown.locator('a, button, .dropdown-item')
            print(f"\nMore menu inside ontology:")
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  '{text}'")
        page.keyboard.press('Escape')

    # Check status indicators
    print("\nStatus indicators:")
    status = page.locator('[class*="status"], [class*="badge"], [class*="workflow"]')
    for i in range(status.count()):
        el = status.nth(i)
        if el.is_visible():
            text = el.inner_text().strip()[:40]
            cls = (el.get_attribute('class') or '')[:60]
            if text:
                print(f"  '{text}' class={cls}")

    time.sleep(2)
    browser.close()
