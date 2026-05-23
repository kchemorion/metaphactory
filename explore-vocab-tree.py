#!/usr/bin/env python3
"""Explore the vocabulary editor tree structure to fix narrower concept creation."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:10214"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(15000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Navigate to Vocabularies
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(3)

    # Check if any vocabularies exist
    print("=== EXISTING VOCABULARIES ===")
    vocab_links = page.locator('a[href*="vocabulary"], a[href*="Vocabulary"]')
    count = vocab_links.count()
    print(f"Found {count} vocabulary links")
    for i in range(min(count, 10)):
        link = vocab_links.nth(i)
        text = link.inner_text().strip()
        href = link.get_attribute("href")
        print(f"  {i}: '{text}' -> {href}")

    # Create a test vocabulary
    print("\n=== CREATING TEST VOCABULARY ===")
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.click()
    title_input.type("Test Vocabulary")
    time.sleep(0.5)

    # Uncheck Suggest IRI
    suggest_cb = page.locator('input[data-testid="suggest-iri-vocabulary"]').first
    if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
        suggest_cb.click()
        time.sleep(0.5)

    # Set custom IRI
    iri_input = page.locator('input[data-testid="suggest-iri-vocabulary-input"]').first
    if iri_input.is_visible(timeout=2000):
        iri_input.click()
        iri_input.fill("")
        iri_input.type("https://example.org/test-vocabulary/TestVocabulary")
        time.sleep(0.5)

    # Click Create
    dialog_create = page.locator('.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")').first
    for _ in range(15):
        if dialog_create.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    if dialog_create.get_attribute("disabled") is None:
        dialog_create.click()
        print("  Created vocabulary")
    else:
        print("  Create button stayed disabled")
        browser.close()
        exit(1)

    time.sleep(3)

    # Dismiss walkthrough if present
    try:
        close = page.locator('button:has-text("Close"), button:has-text("Skip"), button:has-text("×")').first
        if close.is_visible(timeout=2000):
            close.click()
            time.sleep(0.5)
    except:
        pass

    # Create a top-level concept
    print("\n=== CREATING TOP-LEVEL CONCEPT ===")
    create_term = page.locator('button:has-text("Create top-level term")').first
    if create_term.is_visible(timeout=3000):
        create_term.click()
        time.sleep(1)

        pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
        pref_input.click()
        pref_input.fill("")
        pref_input.type("ParentConcept")
        time.sleep(0.5)

        # Save
        save_btn = page.locator('.overlay-modal.show button[name="submit"], [role="dialog"].show button[name="submit"]').first
        for _ in range(10):
            if save_btn.get_attribute("disabled") is None:
                break
            time.sleep(0.3)
        save_btn.click()
        time.sleep(2)
        print("  Created ParentConcept")

    # Now explore the tree DOM
    print("\n=== TREE STRUCTURE ===")

    # Look for tree items
    tree_items = page.locator('.SemanticTreeInput--itemHolder, [class*="tree"] [class*="item"], [class*="TreeNode"], [data-testid*="tree"]')
    tcount = tree_items.count()
    print(f"Tree items (various selectors): {tcount}")

    # Look for the concept text in the tree
    parent_text = page.locator('text="ParentConcept"')
    ptcount = parent_text.count()
    print(f"'ParentConcept' text elements: {ptcount}")
    for i in range(ptcount):
        el = parent_text.nth(i)
        tag = el.evaluate("el => el.tagName")
        classes = el.evaluate("el => el.className")
        parent_html = el.evaluate("el => el.parentElement ? el.parentElement.outerHTML.substring(0, 300) : 'no parent'")
        print(f"  {i}: tag={tag} class='{classes}'")
        print(f"     parent: {parent_html}")

    # Try clicking the concept in the tree
    print("\n=== CLICKING PARENT CONCEPT ===")
    try:
        parent_node = page.locator('text="ParentConcept"').first
        parent_node.click(force=True)
        time.sleep(1)

        # Look for context menu, three-dot menu, or right-click options
        print("\n  After click - looking for menus:")

        # Check for any newly visible menus or buttons
        menu_items = page.locator('[class*="more"], [aria-label*="more"], button:has-text("⋮"), [class*="menu"], [class*="dropdown"], [class*="context"]')
        mcount = menu_items.count()
        print(f"  Menu-like elements: {mcount}")
        for i in range(min(mcount, 10)):
            el = menu_items.nth(i)
            visible = el.is_visible()
            tag = el.evaluate("el => el.tagName")
            classes = el.evaluate("el => el.className")
            text = el.inner_text().strip()[:50]
            print(f"    {i}: visible={visible} tag={tag} class='{classes}' text='{text}'")

        # Try right-clicking
        print("\n  After right-click:")
        parent_node.click(button="right", force=True)
        time.sleep(1)

        # Check for context menu
        ctx_items = page.locator('[class*="context-menu"], [class*="dropdown-menu"], [role="menu"], [class*="popover"]')
        ccount = ctx_items.count()
        print(f"  Context menu elements: {ccount}")
        for i in range(min(ccount, 10)):
            el = ctx_items.nth(i)
            visible = el.is_visible()
            html = el.inner_html()[:300]
            print(f"    {i}: visible={visible} html='{html}'")

        # Try hovering
        print("\n  After hover:")
        parent_node.hover(force=True)
        time.sleep(1)

        # Look for action buttons that appeared on hover
        hover_btns = page.locator('[class*="action"], [class*="hover"], button[title*="narrower"], button[title*="create"], [class*="icon-button"]')
        hcount = hover_btns.count()
        print(f"  Hover-triggered elements: {hcount}")
        for i in range(min(hcount, 10)):
            el = hover_btns.nth(i)
            visible = el.is_visible()
            tag = el.evaluate("el => el.tagName")
            title = el.get_attribute("title") or ""
            classes = el.evaluate("el => el.className")
            print(f"    {i}: visible={visible} tag={tag} title='{title}' class='{classes}'")

    except Exception as e:
        print(f"  Error: {e}")

    # Try to find the tree container and dump its HTML
    print("\n=== TREE CONTAINER HTML ===")
    tree_containers = page.locator('[class*="TreeInput"], [class*="tree-panel"], [class*="concept-tree"]')
    tccount = tree_containers.count()
    print(f"Tree containers: {tccount}")
    if tccount > 0:
        html = tree_containers.first.inner_html()[:2000]
        print(html)
    else:
        # Try broader search
        left_panel = page.locator('[class*="panel"], [class*="sidebar"], [class*="left"]')
        lpcount = left_panel.count()
        print(f"Panel elements: {lpcount}")

    # Dump the entire page's interesting buttons
    print("\n=== ALL VISIBLE BUTTONS ===")
    all_btns = page.locator('button')
    bcount = all_btns.count()
    for i in range(min(bcount, 30)):
        btn = all_btns.nth(i)
        try:
            if btn.is_visible(timeout=100):
                text = btn.inner_text().strip()[:60]
                classes = btn.evaluate("el => el.className")
                title = btn.get_attribute("title") or ""
                print(f"  {i}: '{text}' title='{title}' class='{classes}'")
        except:
            pass

    time.sleep(3)
    browser.close()
