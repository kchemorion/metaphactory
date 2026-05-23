#!/usr/bin/env python3
"""Quick debug: click Vegetables concept's more_vert and dump dropdown contents."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Screenshot the vocabularies page to see three-dot options
    page.screenshot(path="cert-screenshots/debug-vocabs-list.png", full_page=True)

    # Check for three-dot menu on the vocabulary row
    print("=== VOCABULARY LIST ROW BUTTONS ===")
    rows = page.locator('tr, [class*="row"]')
    for i in range(rows.count()):
        row = rows.nth(i)
        text = row.inner_text().strip()[:60]
        if 'vegetable' in text.lower():
            btns = row.locator('button, a')
            print(f"Row '{text}': {btns.count()} buttons")
            for j in range(btns.count()):
                b = btns.nth(j)
                if b.is_visible():
                    print(f"  '{b.inner_text().strip()[:30]}'")

    # Open the vocabulary
    page.locator('a:has-text("Vegetables for Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Click the Vegetables concept's more_vert (should be the only visible one)
    veg_link = page.locator('a:has-text("Vegetables")').first
    if veg_link.is_visible(timeout=3000):
        veg_node = veg_link.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
        menu_btn = veg_node.locator('button:has-text("more_vert")').first
        if menu_btn.is_visible(timeout=2000):
            menu_btn.click()
            time.sleep(1)
            page.screenshot(path="cert-screenshots/debug-veg-menu.png")

            # Dump EVERYTHING in the dropdown
            dropdown = page.locator('.dropdown-menu.show')
            print(f"\n=== VEGETABLES MORE_VERT DROPDOWN ===")
            print(f"HTML:\n{dropdown.inner_html()[:3000]}")

            items = dropdown.locator('*')
            for i in range(items.count()):
                item = items.nth(i)
                if item.is_visible():
                    tag = item.evaluate("el => el.tagName")
                    text = item.inner_text().strip()[:60]
                    cls = (item.get_attribute('class') or '')[:60]
                    if text and tag not in ['SPAN', 'DIV']:
                        print(f"  {tag}.{cls}: '{text}'")
        else:
            print("more_vert not visible for Vegetables")
    else:
        print("Vegetables not found")

    time.sleep(2)
    browser.close()
