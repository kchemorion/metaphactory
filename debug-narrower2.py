#!/usr/bin/env python3
"""Debug: find the Create narrower term mechanism in the correct vocabulary."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Go to Vocabularies and find the latest one
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click the LAST "Vegetables for Recipes" (most recent)
    links = page.locator('a:has-text("Vegetables for Recipes")')
    print(f"Found {links.count()} 'Vegetables for Recipes' links")
    if links.count() > 0:
        links.last.click()
    else:
        page.locator('a:has-text("Vegetables")').last.click()
    time.sleep(3)
    try:
        page.keyboard.press('Escape')
        time.sleep(0.5)
    except:
        pass

    print(f"URL: {page.url}")

    # List all tree nodes
    print("\n=== TREE NODES ===")
    # Try different selectors for tree
    for sel in ['[class*="tree"] a', '.vocabulary-tree a', 'nav a', '.terms-panel a']:
        nodes = page.locator(sel)
        if nodes.count() > 2:
            print(f"  Selector '{sel}' found {nodes.count()} nodes")

    # Get all visible links in the left panel
    left_panel = page.locator('.ontodia-accordion, [class*="sidebar"], [class*="panel"]:first-child')
    if left_panel.count() > 0:
        all_links = left_panel.first.locator('a')
        print(f"\nLeft panel links: {all_links.count()}")
        for i in range(all_links.count()):
            link = all_links.nth(i)
            if link.is_visible():
                text = link.inner_text().strip()[:40]
                if text and text not in ['Terms', 'Collections', 'Elements', 'Info & Metadata']:
                    print(f"  '{text}'")

    # Click "Bean" to select it
    print("\n=== SELECTING BEAN ===")
    bean = page.locator('a:has-text("Bean")').first
    if bean.is_visible(timeout=2000):
        bean.click()
        time.sleep(1.5)
        print("Bean selected")

        # Check what the detail panel shows
        hierarchy_text = page.evaluate("""() => {
            const h = document.querySelector('[class*="hierarchy"], [class*="Hierarchy"]');
            return h ? h.textContent.trim().substring(0, 200) : 'not found';
        }""")
        print(f"Hierarchy: {hierarchy_text}")
    else:
        print("Bean not found in tree!")

    # Now explore the bottom-left Create area
    print("\n=== BOTTOM CREATE AREA ===")
    # Find the small dropdown button next to "Create top-level term"
    # It's likely a split button or a separate small dropdown toggle
    all_bottom_btns = page.locator('button')
    for i in range(all_bottom_btns.count()):
        btn = all_bottom_btns.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            cls = (btn.get_attribute('class') or '')[:80]
            aria = btn.get_attribute('aria-label') or ''
            if 'create' in text.lower() or 'create' in cls.lower() or 'narrower' in text.lower() or 'dropdown' in cls.lower() or 'split' in cls.lower() or 'arrow' in text.lower():
                print(f"  Button: '{text}' class={cls} aria='{aria}'")

    # Find dropdown toggles (the small arrow next to a button)
    toggles = page.locator('.dropdown-toggle, [data-bs-toggle="dropdown"], button[aria-expanded]')
    print(f"\nDropdown toggles: {toggles.count()}")
    for i in range(toggles.count()):
        t = toggles.nth(i)
        if t.is_visible():
            text = t.inner_text().strip()[:30]
            cls = (t.get_attribute('class') or '')[:60]
            print(f"  Toggle: '{text}' class={cls}")

    # Look for split button group near "Create top-level term"
    btn_groups = page.locator('.btn-group, [class*="btn-group"]')
    print(f"\nButton groups: {btn_groups.count()}")
    for i in range(btn_groups.count()):
        bg = btn_groups.nth(i)
        if bg.is_visible():
            text = bg.inner_text().strip()[:60]
            btns = bg.locator('button')
            print(f"  Group: '{text}' with {btns.count()} buttons")
            for j in range(btns.count()):
                b = btns.nth(j)
                btext = b.inner_text().strip()[:30]
                bcls = (b.get_attribute('class') or '')[:60]
                print(f"    [{j}] '{btext}' class={bcls}")

    # Try clicking the dropdown toggle near "Create top-level term"
    print("\n=== CLICKING SPLIT DROPDOWN ===")
    # The + dropdown is likely the button right after "Create top-level term"
    split_toggle = page.locator('button.dropdown-toggle:near(:text("Create top-level term"))').first
    if not split_toggle.is_visible(timeout=1000):
        # Try other selectors
        split_toggle = page.locator('button:has-text("+"):near(:text("Create"))').first
    if not split_toggle.is_visible(timeout=1000):
        # Get all buttons in the same parent as "Create top-level term"
        create_btn = page.locator('button:has-text("Create top-level term")').first
        if create_btn.is_visible():
            parent = create_btn.locator('..')  # parent element
            sibling_btns = parent.locator('button')
            print(f"Sibling buttons to Create: {sibling_btns.count()}")
            for i in range(sibling_btns.count()):
                sb = sibling_btns.nth(i)
                text = sb.inner_text().strip()[:30]
                print(f"  [{i}] '{text}'")
                if i > 0:  # skip the "Create top-level term" button itself
                    split_toggle = sb
                    break

    if split_toggle.is_visible(timeout=1000):
        print(f"Found split toggle, clicking...")
        split_toggle.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-narrow-split-menu.png")

        # Check dropdown
        dropdown = page.locator('.dropdown-menu.show')
        if dropdown.is_visible(timeout=1000):
            items = dropdown.locator('a, button, li')
            print(f"Dropdown items:")
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()
                if text:
                    print(f"  '{text}'")

    page.screenshot(path="cert-screenshots/debug-narrow-final.png")
    time.sleep(3)
    browser.close()
