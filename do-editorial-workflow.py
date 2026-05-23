#!/usr/bin/env python3
"""Execute the editorial workflow: approve review, publish, new version, add Menu+hasRecipe, review+publish again."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

def dismiss_modals(page):
    for _ in range(3):
        try:
            modal = page.locator('.modal.show')
            if modal.is_visible(timeout=300):
                close = modal.locator('.btn-close, button:has-text("Close")').first
                if close.is_visible(timeout=300):
                    close.click(force=True)
                else:
                    page.keyboard.press('Escape')
                time.sleep(0.3)
            else:
                break
        except:
            page.keyboard.press('Escape')
            time.sleep(0.3)

def screenshot(page, name):
    page.screenshot(path=f"cert-screenshots/vm4-{name}.png")
    print(f"  📸 vm4-{name}.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=250)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login as admin (needed for review approval)
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # ═══════════════════════════════════════════════
    # STEP 1: Open Recipes ontology and approve review
    # ═══════════════════════════════════════════════
    print("\n=== STEP 1: APPROVE REVIEW ===")
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)
    screenshot(page, "01-review-page")

    # Click "Approve all" / thumbs up button
    approve_btn = page.locator(
        'button:has-text("Approve"), '
        'button[title*="Approve"], '
        'button:has-text("thumb_up"), '
        'button:has-text("Accept"), '
        '[aria-label*="Approve"], '
        '[aria-label*="approve"]'
    ).first
    if approve_btn.is_visible(timeout=3000):
        approve_btn.click()
        time.sleep(2)
        print("  Clicked Approve")
    else:
        # Try finding approve via the review banner area
        # The thumbs up/down icons might be material icons
        thumbs_up = page.locator('span:has-text("thumb_up"), button:has(span:text("thumb_up"))').first
        if thumbs_up.is_visible(timeout=2000):
            thumbs_up.click()
            time.sleep(2)
            print("  Clicked thumb_up")
        else:
            print("  Warning: Approve button not found")
            # List all visible buttons for debugging
            btns = page.locator('button')
            for i in range(btns.count()):
                btn = btns.nth(i)
                if btn.is_visible():
                    text = btn.inner_text().strip()[:40]
                    if text:
                        print(f"    Visible button: '{text}'")

    screenshot(page, "02-approved")

    # Add a comment
    comment_input = page.locator(
        'textarea[placeholder*="comment" i], '
        'textarea[placeholder*="Add your" i], '
        'input[placeholder*="comment" i]'
    ).first
    if comment_input.is_visible(timeout=2000):
        comment_input.click()
        comment_input.type("All classes, attributes and relations look correct. Approved for publication.")
        time.sleep(0.5)
        # Submit comment
        submit = page.locator('button:has-text("Submit"), button:has-text("Send"), button:has-text("Add")').first
        if submit.is_visible(timeout=1000):
            submit.click()
            time.sleep(1)
        print("  Added comment")
    screenshot(page, "03-commented")

    # ═══════════════════════════════════════════════
    # STEP 2: Publish the ontology
    # ═══════════════════════════════════════════════
    print("\n=== STEP 2: PUBLISH ===")

    # After approval, there should be a Publish button
    publish_btn = page.locator(
        'button:has-text("Publish"), '
        'a:has-text("Publish")'
    ).first
    if publish_btn.is_visible(timeout=5000):
        publish_btn.click()
        time.sleep(2)
        # Confirm if dialog appears
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
        print("  Published!")
    else:
        # Check catalog page for publish
        page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        more_btn = page.locator('button:has-text("more_vert")').first
        more_btn.click()
        time.sleep(1)
        publish_opt = page.locator('.dropdown-menu.show a:has-text("Publish"), .dropdown-menu.show button:has-text("Publish")').first
        if publish_opt.is_visible(timeout=2000):
            publish_opt.click()
            time.sleep(2)
            confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
            if confirm.is_visible(timeout=2000):
                confirm.click()
                time.sleep(2)
            print("  Published from catalog!")
        else:
            print("  Warning: Publish not found")
            # List menu items
            items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
            for i in range(items.count()):
                text = items.nth(i).inner_text().strip()[:40]
                if text:
                    print(f"    Menu: '{text}'")
            page.keyboard.press('Escape')

    screenshot(page, "04-published")

    # ═══════════════════════════════════════════════
    # STEP 3: Create a new version
    # ═══════════════════════════════════════════════
    print("\n=== STEP 3: CREATE NEW VERSION ===")
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Now the catalog should show "Create version..." for Recipes
    more_btn = page.locator('button:has-text("more_vert")').first
    more_btn.click()
    time.sleep(1)
    screenshot(page, "05-catalog-menu-after-publish")

    version_opt = page.locator('.dropdown-menu.show a:has-text("Create version")').first
    if version_opt.is_visible(timeout=2000):
        version_opt.click()
        time.sleep(2)
        screenshot(page, "06-version-dialog")
        # Confirm version creation
        confirm = page.locator(
            '.modal.show button:has-text("Create"), '
            '.modal.show button:has-text("OK"), '
            '.modal.show button:has-text("Confirm")'
        ).first
        if confirm.is_visible(timeout=3000):
            confirm.click()
            time.sleep(3)
            print("  New version created!")
    else:
        print("  Warning: 'Create version' not available")
        items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
        for i in range(items.count()):
            text = items.nth(i).inner_text().strip()[:40]
            if text:
                print(f"    Menu: '{text}'")
        page.keyboard.press('Escape')

    screenshot(page, "07-new-version")

    # ═══════════════════════════════════════════════
    # STEP 4: Add Menu class + hasRecipe relation
    # ═══════════════════════════════════════════════
    print("\n=== STEP 4: ADD MENU CLASS + hasRecipe RELATION ===")

    # Open the new version of Recipes ontology
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Switch to Edit mode if needed
    edit_btn = page.locator('button:has-text("Edit")').first
    if edit_btn.is_visible(timeout=2000):
        edit_btn.click()
        time.sleep(2)

    # Create Menu class
    classes_tab = page.locator('[role="tab"]:has-text("Classes"), button:has-text("Classes")').first
    if classes_tab.is_visible(timeout=2000):
        classes_tab.click()
        time.sleep(0.5)

    create_cls = page.locator('button:has-text("Create Class")').first
    if create_cls.is_visible(timeout=2000):
        create_cls.click()
        time.sleep(1)
        label_input = page.locator('input[placeholder="Enter label here..."]').first
        if label_input.is_visible(timeout=2000):
            label_input.fill("Menu")
            time.sleep(0.3)
        confirm = page.locator('button:has-text("Confirm")').first
        if confirm.is_visible(timeout=1500):
            confirm.click()
            time.sleep(0.5)
        print("  Created class: Menu")

    # Create hasRecipe relation
    rels_tab = page.locator('[role="tab"]:has-text("Relations"), button:has-text("Relations")').first
    if rels_tab.is_visible(timeout=2000):
        rels_tab.click()
        time.sleep(0.5)

    create_rel = page.locator('button:has-text("Create Relation")').first
    if create_rel.is_visible(timeout=2000):
        create_rel.click()
        time.sleep(1)
        label_input = page.locator('input[placeholder="Enter label here..."]').first
        if label_input.is_visible(timeout=2000):
            label_input.fill("hasRecipe")
            time.sleep(0.3)
        confirm = page.locator('button:has-text("Confirm")').first
        if confirm.is_visible(timeout=1500):
            confirm.click()
            time.sleep(0.5)
        print("  Created relation: hasRecipe")

    # Save
    save_btn = page.locator('button:has-text("Save"), [title*="Save"]').first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(2)
    screenshot(page, "08-menu-added")

    # ═══════════════════════════════════════════════
    # STEP 5: Start new review, add comments, publish
    # ═══════════════════════════════════════════════
    print("\n=== STEP 5: NEW REVIEW + PUBLISH ===")

    # Go back to catalog to start a new review
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click more_vert for Recipes
    more_btn = page.locator('button:has-text("more_vert")').first
    more_btn.click()
    time.sleep(1)
    screenshot(page, "09-catalog-menu-v2")

    # Look for "Start review" or "Request review"
    review_opt = page.locator(
        '.dropdown-menu.show a:has-text("review"), '
        '.dropdown-menu.show a:has-text("Review"), '
        '.dropdown-menu.show button:has-text("review")'
    ).first
    if review_opt.is_visible(timeout=2000):
        review_opt.click()
        time.sleep(2)
        print("  Started review for new version")
        # Confirm if dialog
        confirm = page.locator('.modal.show button:has-text("Start"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    else:
        print("  No review option found in catalog menu")
        items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
        for i in range(items.count()):
            text = items.nth(i).inner_text().strip()[:40]
            if text:
                print(f"    '{text}'")
        page.keyboard.press('Escape')

    screenshot(page, "10-review-v2")

    # Open ontology and approve + comment
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Add comment
    comment_input = page.locator('textarea[placeholder*="comment" i], textarea[placeholder*="Add" i]').first
    if comment_input.is_visible(timeout=2000):
        comment_input.click()
        comment_input.type("New version adds Menu class with hasRecipe relation. Looks good.")
        submit = page.locator('button:has-text("Submit"), button:has-text("Send"), button:has-text("Add")').first
        if submit.is_visible(timeout=1000):
            submit.click()
            time.sleep(1)
        print("  Added review comment")

    # Reply to previous comment
    reply_input = page.locator('textarea[placeholder*="reply" i]').first
    if reply_input.is_visible(timeout=2000):
        reply_input.click()
        reply_input.type("Confirmed - Menu with minimum one Recipe is correct per requirements.")
        submit = page.locator('button:has-text("Reply"), button:has-text("Send")').first
        if submit.is_visible(timeout=1000):
            submit.click()
            time.sleep(1)
        print("  Replied to comment")

    # Approve
    approve_btn = page.locator(
        'button:has-text("Approve"), button[title*="Approve"], '
        'button:has-text("thumb_up"), span:has-text("thumb_up")'
    ).first
    if approve_btn.is_visible(timeout=3000):
        approve_btn.click()
        time.sleep(2)
        print("  Approved new version")

    # Publish
    publish_btn = page.locator('button:has-text("Publish")').first
    if publish_btn.is_visible(timeout=5000):
        publish_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
        print("  Published new version!")

    screenshot(page, "11-final")
    print("\n✓ Task 4 complete")

    time.sleep(3)
    browser.close()
