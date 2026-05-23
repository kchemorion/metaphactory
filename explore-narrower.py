#!/usr/bin/env python3
"""Explore how to create a narrower concept in the vocabulary editor."""
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

    # Go to Vocabularies page and find the test vocabulary
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(3)

    # Click on the test vocabulary to open it
    vocab_link = page.locator('a:has-text("Test Vocabulary")').first
    if vocab_link.is_visible(timeout=3000):
        vocab_link.click()
        time.sleep(3)
        print("Opened Test Vocabulary")
    else:
        print("Test Vocabulary not found on page")
        # Check what's on the page
        body_text = page.locator('body').inner_text()[:2000]
        print(f"Page text: {body_text}")
        browser.close()
        exit(1)

    # Now we should be in the vocabulary editor with ParentConcept in the tree
    # First, click on ParentConcept in the tree panel
    print("\n=== SELECTING PARENT CONCEPT IN TREE ===")

    # The tree node is in the left panel - find it by the a > span pattern
    tree_link = page.locator('a:has(span:text("ParentConcept"))').first
    if tree_link.is_visible(timeout=3000):
        tree_link.click()
        time.sleep(1)
        print("  Clicked ParentConcept in tree")
    else:
        print("  ParentConcept tree link not found")

    # Now look for the more_vert button
    print("\n=== LOOKING FOR MORE_VERT MENU ===")
    more_btn = page.locator('button:has-text("more_vert")').first
    if more_btn.is_visible(timeout=2000):
        print("  Found more_vert button, clicking...")
        more_btn.click()
        time.sleep(1)

        # Capture the dropdown menu items
        dropdown_items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button, [role="menu"] [role="menuitem"]')
        dcount = dropdown_items.count()
        print(f"  Dropdown items: {dcount}")
        for i in range(dcount):
            item = dropdown_items.nth(i)
            text = item.inner_text().strip()[:80]
            visible = item.is_visible()
            print(f"    {i}: visible={visible} '{text}'")

        # Also look for any visible text containing "narrower"
        narrower = page.locator('text=narrower')
        ncount = narrower.count()
        print(f"  'narrower' text elements: {ncount}")
        for i in range(ncount):
            el = narrower.nth(i)
            visible = el.is_visible()
            tag = el.evaluate("el => el.tagName")
            text = el.inner_text().strip()[:80]
            print(f"    {i}: visible={visible} tag={tag} '{text}'")

        # Also look for any visible dropdown
        dropdowns = page.locator('.dropdown-menu.show')
        ddcount = dropdowns.count()
        print(f"  Visible dropdown menus: {ddcount}")
        for i in range(ddcount):
            dd = dropdowns.nth(i)
            html = dd.inner_html()[:500]
            print(f"    {i}: {html}")

    else:
        print("  more_vert button not visible")
        # Maybe it's under a different selector
        all_btns = page.locator('button')
        bcount = all_btns.count()
        for i in range(bcount):
            btn = all_btns.nth(i)
            try:
                if btn.is_visible(timeout=100):
                    text = btn.inner_text().strip()[:40]
                    if 'more' in text.lower() or 'vert' in text.lower() or '⋮' in text:
                        classes = btn.evaluate("el => el.className")
                        print(f"    Found: '{text}' class='{classes}'")
            except:
                pass

    # Try creating a narrower concept
    print("\n=== ATTEMPTING NARROWER CONCEPT CREATION ===")
    narrower_option = page.locator('text="Create narrower term"').first
    if narrower_option.is_visible(timeout=2000):
        narrower_option.click()
        time.sleep(1)
        print("  Clicked 'Create narrower term'")

        # Check if the form appeared
        pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
        if pref_input.is_visible(timeout=3000):
            print("  Form appeared!")
            pref_input.click()
            pref_input.type("ChildConcept")
            time.sleep(0.5)

            # Save
            save_btn = page.locator('.overlay-modal.show button[name="submit"], [role="dialog"].show button[name="submit"]').first
            for _ in range(10):
                if save_btn.get_attribute("disabled") is None:
                    break
                time.sleep(0.3)
            save_btn.click()
            time.sleep(2)
            print("  Created ChildConcept as narrower!")
        else:
            print("  Form did NOT appear")
    else:
        print("  'Create narrower term' not visible")

        # Check all visible text for 'Create' or 'narrower'
        all_text = page.locator('body').inner_text()
        if 'narrower' in all_text.lower():
            idx = all_text.lower().find('narrower')
            print(f"  'narrower' found in page text: ...{all_text[max(0,idx-50):idx+80]}...")
        else:
            print("  'narrower' not found anywhere in page text")

    time.sleep(5)
    browser.close()
