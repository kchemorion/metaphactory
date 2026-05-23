#!/usr/bin/env python3
"""Properly delete existing Vegetables vocabulary and Recipes ontology via the UI."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Navigate to Vocabularies
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # List all visible vocabularies
    print("=== VOCABULARIES LIST ===")
    page.screenshot(path="cert-screenshots/cleanup-vocabs.png", full_page=True)

    # Look for Vegetables in the list
    links = page.locator('a')
    for i in range(links.count()):
        link = links.nth(i)
        if link.is_visible():
            text = link.inner_text().strip()
            if 'vegetable' in text.lower() or 'recipes' in text.lower():
                href = link.get_attribute('href') or ''
                print(f"  Found: '{text}' -> {href}")

    # Try to find delete functionality in the vocabulary list
    # metaphactory typically shows a table/list with actions
    # Look for a "More" or context menu on the Vegetables row
    vocab_row = page.locator('tr:has-text("Vegetables"), li:has-text("Vegetables"), [class*="row"]:has-text("Vegetables")')
    if vocab_row.count() > 0:
        print(f"\nFound vocab row element(s): {vocab_row.count()}")
        row = vocab_row.first
        # Look for delete button in the row
        delete_in_row = row.locator('button:has-text("delete"), a:has-text("delete"), button:has-text("Delete")')
        if delete_in_row.count() > 0:
            print(f"  Delete button in row: {delete_in_row.first.inner_text()}")

    # Navigate to the vocabulary itself
    vocab_link = page.locator('a:has-text("Vegetables")').first
    if vocab_link.is_visible(timeout=3000):
        vocab_link.click()
        time.sleep(3)
        # Dismiss walkthrough
        try:
            page.keyboard.press('Escape')
            time.sleep(0.5)
        except:
            pass

        print(f"\nOn vocabulary page: {page.url}")
        page.screenshot(path="cert-screenshots/cleanup-vocab-page.png")

        # Look for "More" dropdown at the top
        more_btn = page.locator('button:has-text("More"), .moreActions button, [class*="moreActions"] button').first
        if more_btn.is_visible(timeout=2000):
            print("Found 'More' button - clicking")
            more_btn.click()
            time.sleep(1)
            page.screenshot(path="cert-screenshots/cleanup-more-menu.png")

            # List all dropdown items
            dropdown_items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
            print(f"Dropdown items: {dropdown_items.count()}")
            for i in range(dropdown_items.count()):
                item = dropdown_items.nth(i)
                text = item.inner_text().strip()
                print(f"  Item: '{text}'")

            # Try delete
            delete_opt = page.locator('.dropdown-menu.show a:has-text("Delete"), .dropdown-menu.show button:has-text("Delete")').first
            if delete_opt.is_visible(timeout=1000):
                print("\nFound Delete option - clicking")
                delete_opt.click()
                time.sleep(2)
                page.screenshot(path="cert-screenshots/cleanup-delete-confirm.png")

                # Look for confirmation
                confirm = page.locator(
                    '.modal.show button:has-text("Delete"), '
                    '.modal.show button:has-text("Confirm"), '
                    '.modal.show button:has-text("Yes"), '
                    '[data-testid*="confirm"] button'
                )
                print(f"Confirm buttons: {confirm.count()}")
                for i in range(confirm.count()):
                    btn = confirm.nth(i)
                    if btn.is_visible():
                        print(f"  Confirm: '{btn.inner_text().strip()}'")
                        btn.click()
                        time.sleep(3)
                        print("  Clicked confirm!")
                        break
            else:
                print("No Delete option in dropdown")
                page.keyboard.press('Escape')
        else:
            print("No 'More' button found")

            # Try looking for other delete mechanisms
            all_btns = page.locator('button')
            for i in range(all_btns.count()):
                btn = all_btns.nth(i)
                if btn.is_visible():
                    text = btn.inner_text().strip()[:40]
                    if text and ('delete' in text.lower() or 'remove' in text.lower() or 'more' in text.lower()):
                        print(f"  Potential: '{text}'")

    page.screenshot(path="cert-screenshots/cleanup-final.png")
    print(f"\nFinal URL: {page.url}")
    time.sleep(3)
    browser.close()
