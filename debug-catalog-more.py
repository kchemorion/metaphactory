#!/usr/bin/env python3
"""Check the 'More' submenu inside the catalog more_vert dropdown."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click more_vert for Recipes (first one)
    more_btn = page.locator('button:has-text("more_vert")').first
    more_btn.click()
    time.sleep(1)

    # Click the "More" submenu
    more_submenu = page.locator('.dropdown-menu.show a:has-text("More"), .dropdown-menu.show button:has-text("More")').first
    if more_submenu.is_visible(timeout=2000):
        more_submenu.hover()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-catalog-more-submenu.png")

        # Check for submenu that appeared
        all_items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button, .dropdown-item')
        print("=== ALL DROPDOWN ITEMS (after hovering More) ===")
        for i in range(all_items.count()):
            item = all_items.nth(i)
            if item.is_visible():
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  '{text}'")

        # Try clicking More
        more_submenu.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-catalog-more-clicked.png")

        all_items2 = page.locator('.dropdown-menu.show a, .dropdown-menu.show button, .dropdown-item')
        print("\n=== AFTER CLICKING More ===")
        for i in range(all_items2.count()):
            item = all_items2.nth(i)
            if item.is_visible():
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  '{text}'")

    time.sleep(2)
    browser.close()
