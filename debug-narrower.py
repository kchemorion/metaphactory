#!/usr/bin/env python3
"""Debug: how does the 'Create narrower term' work for a specific parent?"""
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

    # Go to the existing Vegetables for Recipes vocabulary
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click on the latest vocabulary
    vocab_link = page.locator('a:has-text("Vegetables for Recipes")').first
    if not vocab_link.is_visible(timeout=3000):
        vocab_link = page.locator('a:has-text("Vegetables")').first
    vocab_link.click()
    time.sleep(3)
    try:
        page.keyboard.press('Escape')
        time.sleep(0.5)
    except:
        pass

    print(f"URL: {page.url}")
    page.screenshot(path="cert-screenshots/debug-narrow-vocab.png")

    # Explore the tree structure
    print("\n=== TREE STRUCTURE ===")
    tree_nodes = page.locator('.ontodia-accordion a, .tree-node a, [class*="tree"] a')
    print(f"Tree node links: {tree_nodes.count()}")
    for i in range(tree_nodes.count()):
        node = tree_nodes.nth(i)
        if node.is_visible():
            text = node.inner_text().strip()
            href = node.get_attribute('href') or ''
            cls = (node.get_attribute('class') or '')[:60]
            print(f"  [{i}] '{text}' class={cls}")

    # Click on "Bean" specifically
    print("\n=== CLICKING BEAN ===")
    bean_node = page.locator('a:has(span:text-is("Bean"))').first
    if not bean_node.is_visible(timeout=2000):
        bean_node = page.locator('a:has-text("Bean")').first

    if bean_node.is_visible():
        print(f"Bean node found, clicking...")
        bean_node.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-narrow-bean-selected.png")

        # What does the hierarchy panel show now?
        hierarchy = page.locator('text=broader').first
        if hierarchy.is_visible(timeout=2000):
            parent_text = page.locator(':text("broader")').first.evaluate(
                "el => el.closest('div, section, li')?.textContent?.trim()?.substring(0, 200)"
            )
            print(f"  Hierarchy context: {parent_text}")

        # Now look for the more_vert / three-dot button NEAR Bean
        # It might be a button that appears when hovering or selecting a tree node
        print("\n=== LOOKING FOR CONTEXT MENU ON BEAN ===")

        # Check for inline buttons near tree nodes
        # In metaphactory, tree nodes might show action buttons on hover
        bean_parent = bean_node.locator('..').first  # parent element
        nearby_btns = bean_parent.locator('button, [role="button"]')
        print(f"Buttons near Bean node: {nearby_btns.count()}")
        for i in range(nearby_btns.count()):
            btn = nearby_btns.nth(i)
            if btn.is_visible():
                text = btn.inner_text().strip()[:30]
                title = btn.get_attribute('title') or ''
                print(f"  Button near Bean: '{text}' title='{title}'")

        # Try right-clicking Bean to see context menu
        bean_node.click(button="right")
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-narrow-rightclick.png")

        # Check for context menu
        ctx_menu = page.locator('.dropdown-menu.show, [role="menu"], .context-menu')
        if ctx_menu.count() > 0 and ctx_menu.first.is_visible(timeout=1000):
            items = ctx_menu.first.locator('a, button, li')
            print(f"\nContext menu items: {items.count()}")
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()
                if text:
                    print(f"  '{text}'")
        else:
            print("No context menu from right-click")
            page.keyboard.press('Escape')

        # Look for the global more_vert button
        print("\n=== MORE_VERT BUTTON ===")
        more_btns = page.locator('button:has-text("more_vert")')
        print(f"more_vert buttons: {more_btns.count()}")
        for i in range(more_btns.count()):
            btn = more_btns.nth(i)
            if btn.is_visible():
                cls = (btn.get_attribute('class') or '')[:60]
                # Get the parent to understand context
                parent_text = btn.evaluate("el => el.parentElement?.className?.substring(0, 60)")
                print(f"  [{i}] class={cls} parent={parent_text}")

        # Click the first visible more_vert
        more_btn = more_btns.first
        if more_btn.is_visible():
            more_btn.click()
            time.sleep(1)
            page.screenshot(path="cert-screenshots/debug-narrow-more-menu.png")

            # List dropdown items
            dropdown = page.locator('.dropdown-menu.show')
            if dropdown.is_visible(timeout=1000):
                items = dropdown.locator('a, button')
                print(f"\nDropdown items:")
                for i in range(items.count()):
                    item = items.nth(i)
                    text = item.inner_text().strip()
                    if text:
                        print(f"  '{text}'")
            page.keyboard.press('Escape')
            time.sleep(0.5)

        # Try the + button or "Create top-level term" dropdown arrow
        print("\n=== BOTTOM CREATE BUTTONS ===")
        bottom_btns = page.locator('button:near(:text("Create top-level term"))')
        print(f"Buttons near 'Create top-level term': {bottom_btns.count()}")
        for i in range(bottom_btns.count()):
            btn = bottom_btns.nth(i)
            if btn.is_visible():
                text = btn.inner_text().strip()[:40]
                cls = (btn.get_attribute('class') or '')[:60]
                print(f"  '{text}' class={cls}")

        # Check for a dropdown arrow next to "Create top-level term"
        # The screenshot from earlier showed a "+" button with a dropdown arrow
        arrow_btn = page.locator('button:has-text("arrow_drop_down"), [class*="dropdown-toggle"]:near(:text("Create"))').first
        if arrow_btn.is_visible(timeout=1000):
            print("\nFound dropdown arrow near Create - clicking")
            arrow_btn.click()
            time.sleep(1)
            page.screenshot(path="cert-screenshots/debug-narrow-create-dropdown.png")

            dropdown = page.locator('.dropdown-menu.show')
            if dropdown.is_visible(timeout=1000):
                items = dropdown.locator('a, button')
                for i in range(items.count()):
                    item = items.nth(i)
                    text = item.inner_text().strip()
                    if text:
                        print(f"  Dropdown item: '{text}'")

    time.sleep(3)
    browser.close()
