#!/usr/bin/env python3
"""Debug: what options are in the concept's more_vert dropdown?"""
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

    # Open vocabulary
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.locator('a:has-text("Vegetables for Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Expand tree by clicking the expand toggle on Vegetables
    expand = page.locator('[data-testid*="expand-toggle"]').first
    if expand.is_visible(timeout=2000):
        expand.click()
        time.sleep(1)

    # Click "Vegetables" first to expand it
    veg = page.locator('.ontodia-accordion a:has-text("Vegetables")').first
    if veg.is_visible(timeout=2000):
        veg.click()
        time.sleep(1)
        # Expand by clicking the arrow/toggle
        veg_node = veg.locator('xpath=ancestor::div[contains(@class,"LazyTreeSelector--item")]').first
        toggle = veg_node.locator('.LazyTreeSelector--expandToggle').first
        if toggle.is_visible(timeout=1000):
            toggle.click()
            time.sleep(1)

    # Click on "Bean"
    bean = page.locator('.ontodia-accordion a:has-text("Bean")').first
    if not bean.is_visible(timeout=3000):
        # Try expanding via clicking the text
        print("Bean not visible, trying to expand tree...")
        page.locator('a:has-text("Vegetables")').first.dblclick()
        time.sleep(1)
    bean = page.locator('a:has-text("Bean")').first
    bean.click()
    time.sleep(1)

    # Click Bean's more_vert
    tree_node = bean.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
    menu_btn = tree_node.locator('button:has-text("more_vert")').first
    menu_btn.click()
    time.sleep(1)

    # List ALL dropdown items
    page.screenshot(path="cert-screenshots/debug-concept-menu.png")
    dropdown = page.locator('.dropdown-menu.show')
    if dropdown.is_visible(timeout=2000):
        items = dropdown.locator('a, button, li, .dropdown-item')
        print(f"Dropdown items: {items.count()}")
        for i in range(items.count()):
            item = items.nth(i)
            text = item.inner_text().strip()[:60]
            cls = (item.get_attribute('class') or '')[:60]
            tag = item.evaluate("el => el.tagName")
            if text:
                print(f"  [{i}] {tag} '{text}' class={cls}")

        # Also dump raw HTML
        print(f"\nDropdown HTML:")
        html = dropdown.inner_html()
        print(html[:3000])
    else:
        print("No dropdown visible!")

    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Also check the page-level "More" button in the toolbar
    print("\n=== PAGE-LEVEL 'More' BUTTON ===")
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=2000):
        more_btn.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-page-more-menu.png")
        dropdown = page.locator('.dropdown-menu.show')
        if dropdown.is_visible():
            items = dropdown.locator('a, button, .dropdown-item')
            print(f"Page More items: {items.count()}")
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  '{text}'")

    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Check the status dot area - maybe clicking the status dot changes status
    print("\n=== STATUS DOTS ===")
    dots = page.locator('.assetStatus, [class*="Status"]')
    print(f"Status elements: {dots.count()}")
    for i in range(dots.count()):
        dot = dots.nth(i)
        if dot.is_visible():
            cls = dot.get_attribute('class') or ''
            text = dot.inner_text().strip()[:30]
            print(f"  [{i}] class={cls} text='{text}'")

    # Check the detail panel for any status controls
    print("\n=== DETAIL PANEL STATUS CONTROLS ===")
    detail_btns = page.locator('button, select, [role="button"]')
    for i in range(detail_btns.count()):
        btn = detail_btns.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:40]
            cls = (btn.get_attribute('class') or '')[:60]
            if any(kw in text.lower() for kw in ['review', 'status', 'publish', 'accept', 'request', 'approve', 'draft', 'development']):
                print(f"  Button: '{text}' class={cls}")
            if any(kw in cls.lower() for kw in ['status', 'review', 'workflow']):
                print(f"  Button: '{text}' class={cls}")

    time.sleep(3)
    browser.close()
