#!/usr/bin/env python3
"""Check the more_vert menu on the ontologies CATALOG page (not inside editor)."""
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

    # Go to Ontologies CATALOG page
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-catalog-page.png", full_page=True)

    # Find the more_vert buttons on the catalog page
    print("=== MORE_VERT BUTTONS ON CATALOG ===")
    more_btns = page.locator('button:has-text("more_vert")')
    print(f"Found {more_btns.count()} more_vert buttons")

    # Click each one and check what's in the dropdown
    for i in range(more_btns.count()):
        btn = more_btns.nth(i)
        if btn.is_visible():
            # Find nearby text to identify which ontology this belongs to
            parent = btn.evaluate("el => el.closest('tr, [class*=row], [class*=card]')?.textContent?.trim()?.substring(0, 60)")
            print(f"\n  Button #{i} near: '{parent}'")
            btn.click()
            time.sleep(1)
            page.screenshot(path=f"cert-screenshots/debug-catalog-menu-{i}.png")

            dropdown = page.locator('.dropdown-menu.show')
            if dropdown.is_visible():
                items = dropdown.locator('a, button, .dropdown-item')
                for j in range(items.count()):
                    item = items.nth(j)
                    text = item.inner_text().strip()[:60]
                    if text:
                        print(f"    '{text}'")
            page.keyboard.press('Escape')
            time.sleep(0.5)

    time.sleep(2)
    browser.close()
