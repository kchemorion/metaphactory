#!/usr/bin/env python3
"""Delete vocabulary named graphs via the Named Graphs UI delete buttons."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
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

    # Go to Named Graphs
    page.goto(f"{BASE_URL}/resource/Assets:NamedGraphs")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.screenshot(path="cert-screenshots/cleanup-ng-page.png", full_page=True)

    # Find rows containing 'vegetable' or 'Vegetables'
    # The page shows a table with graph IRIs and delete buttons
    print("=== LOOKING FOR VEGETABLE GRAPHS ===")

    # Find all table rows or list items that contain vegetable-related text
    rows = page.locator('tr, [class*="row"]')
    deleted_count = 0

    for attempt in range(5):  # Multiple passes since deleting shifts rows
        found_this_pass = False
        rows = page.locator('tr')
        for i in range(rows.count()):
            row = rows.nth(i)
            try:
                text = row.inner_text().strip()
                if 'vegetable' in text.lower():
                    print(f"\n  Found row: {text[:100]}")
                    # Click the delete button in this row
                    del_btn = row.locator('button:has-text("delete"), button[title*="Delete"], a:has-text("delete")')
                    if del_btn.count() > 0:
                        del_btn.first.click()
                        time.sleep(1)

                        # Handle confirmation dialog
                        confirm = page.locator(
                            '.modal.show button:has-text("Yes"), '
                            '.modal.show button:has-text("Delete"), '
                            '.modal.show button:has-text("Confirm"), '
                            '.modal.show button:has-text("OK"), '
                            '[data-testid="confirmation-dialog-button-confirm"]'
                        ).first
                        if confirm.is_visible(timeout=3000):
                            confirm.click()
                            time.sleep(2)
                            print(f"  Deleted!")
                            deleted_count += 1
                            found_this_pass = True
                            break  # Restart row scan after deletion
                        else:
                            print(f"  No confirm dialog")
                            page.keyboard.press('Escape')
                            time.sleep(0.5)
            except:
                continue

        if not found_this_pass:
            break
        # Reload page for next pass
        page.reload()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

    print(f"\n  Total deleted: {deleted_count}")

    # Verify
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    print("\n=== VOCABULARIES AFTER CLEANUP ===")
    body = page.locator('body').inner_text()
    if 'vegetable' in body.lower():
        print("  WARNING: Vegetable vocabularies still present!")
        # Find remaining
        links = page.locator('a')
        for i in range(links.count()):
            link = links.nth(i)
            if link.is_visible():
                text = link.inner_text().strip()
                if 'vegetable' in text.lower():
                    print(f"    '{text}'")
    else:
        print("  All vegetable vocabularies removed!")

    page.screenshot(path="cert-screenshots/cleanup-done.png", full_page=True)
    time.sleep(2)
    browser.close()
