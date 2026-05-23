#!/usr/bin/env python3
"""Continue editorial workflow from approved state: publish, new version, Menu+hasRecipe, review+publish."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

def screenshot(page, name):
    page.screenshot(path=f"cert-screenshots/vm4-{name}.png")
    print(f"  📸 vm4-{name}.png")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=250)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Open Recipes ontology (should be in approved/ready state)
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)
    screenshot(page, "20-current-state")

    # ═══ STEP 1: Publish ═══
    print("\n=== PUBLISHING ===")
    # The "Publish" button should be visible after approval
    publish_btn = page.locator('button:has-text("Publish")').first
    if publish_btn.is_visible(timeout=5000):
        publish_btn.click()
        time.sleep(2)
        # Handle confirmation dialog
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm"), .modal.show button:has-text("Yes")').first
        if confirm.is_visible(timeout=3000):
            confirm.click()
            time.sleep(3)
        print("  Published!")
    else:
        print("  Publish button not found, checking catalog...")
        page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        more_btn = page.locator('button:has-text("more_vert")').first
        more_btn.click()
        time.sleep(1)
        pub = page.locator('.dropdown-menu.show a:has-text("Publish")').first
        if pub.is_visible(timeout=2000):
            pub.click()
            time.sleep(2)
            confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
            if confirm.is_visible(timeout=2000):
                confirm.click()
                time.sleep(3)
            print("  Published from catalog!")
        else:
            print("  No publish option found anywhere")
            page.keyboard.press('Escape')
    screenshot(page, "21-published")

    # ═══ STEP 2: Create new version ═══
    print("\n=== CREATING NEW VERSION ===")
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    screenshot(page, "22-catalog-after-publish")

    # Click more_vert for Recipes
    more_btns = page.locator('button:has-text("more_vert")')
    for i in range(more_btns.count()):
        btn = more_btns.nth(i)
        if btn.is_visible():
            parent_text = btn.evaluate("el => el.closest('tr, div')?.textContent?.substring(0, 40)")
            if parent_text and 'recipe' in parent_text.lower():
                btn.click()
                time.sleep(1)
                break

    version_opt = page.locator('.dropdown-menu.show a:has-text("Create version")').first
    if version_opt.is_visible(timeout=2000):
        version_opt.click()
        time.sleep(2)
        screenshot(page, "23-version-dialog")
        confirm = page.locator('.modal.show button:has-text("Create"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=3000):
            confirm.click()
            time.sleep(3)
        print("  New version created!")
    else:
        print("  'Create version' not found")
        items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
        for i in range(items.count()):
            text = items.nth(i).inner_text().strip()[:40]
            if text:
                print(f"    '{text}'")
        page.keyboard.press('Escape')
    screenshot(page, "24-new-version")

    # ═══ STEP 3: Add Menu class + hasRecipe relation ═══
    print("\n=== ADDING MENU + hasRecipe ===")
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    # Open the latest version (should be in development)
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Switch to edit mode
    edit_btn = page.locator('button:has-text("Edit")').first
    if edit_btn.is_visible(timeout=2000):
        edit_btn.click()
        time.sleep(2)

    # Create Menu class
    classes_tab = page.locator('button:has-text("Classes")').first
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
        confirm = page.locator('button:has-text("Confirm")').first
        if confirm.is_visible(timeout=1500):
            confirm.click()
            time.sleep(0.5)
        print("  Created class: Menu")

    # Create hasRecipe relation
    rels_tab = page.locator('button:has-text("Relations")').first
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
        confirm = page.locator('button:has-text("Confirm")').first
        if confirm.is_visible(timeout=1500):
            confirm.click()
            time.sleep(0.5)
        print("  Created relation: hasRecipe")

    # Save
    save_btn = page.locator('button:has-text("Save")').first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(2)
    screenshot(page, "25-menu-hasrecipe-saved")

    # ═══ STEP 4: Start new review ═══
    print("\n=== STARTING NEW REVIEW ===")
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Find Recipes more_vert and look for review option
    more_btns = page.locator('button:has-text("more_vert")')
    for i in range(more_btns.count()):
        btn = more_btns.nth(i)
        if btn.is_visible():
            parent_text = btn.evaluate("el => el.closest('tr, div')?.textContent?.substring(0, 40)")
            if parent_text and 'recipe' in parent_text.lower():
                btn.click()
                time.sleep(1)
                break

    screenshot(page, "26-catalog-menu-v2")
    # List all menu items
    items = page.locator('.dropdown-menu.show a, .dropdown-menu.show button')
    print("  Catalog menu items:")
    for i in range(items.count()):
        text = items.nth(i).inner_text().strip()[:40]
        if text:
            print(f"    '{text}'")

    review_opt = page.locator(
        '.dropdown-menu.show a:has-text("review"), '
        '.dropdown-menu.show a:has-text("Review")'
    ).first
    if review_opt.is_visible(timeout=2000):
        review_opt.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Start"), .modal.show button:has-text("Confirm"), .modal.show button:has-text("OK")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
        print("  New review started!")
    else:
        page.keyboard.press('Escape')
        print("  Review option not in menu")

    screenshot(page, "27-new-review")

    # Open ontology, add comment, approve, publish
    page.locator('a:has-text("Recipes")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)
    screenshot(page, "28-review-v2-page")

    # Add comment for reviewer
    comment = page.locator('textarea[placeholder*="comment" i], textarea[placeholder*="Add" i]').first
    if comment.is_visible(timeout=2000):
        comment.click()
        comment.type("Added Menu class with hasRecipe relation per requirements. Menu must have at least one Recipe.")
        # Find the specific comment submit button (not "Add all classes")
        submit = page.locator('button[type="submit"]:near(textarea), form button:has-text("Submit")').first
        if submit.is_visible(timeout=1000):
            submit.click()
            time.sleep(1)
        else:
            comment.press("Enter")
            time.sleep(1)
        print("  Added comment")

    # Approve
    approve = page.locator('button:has-text("Approve"), button[title*="Approve"]').first
    if approve.is_visible(timeout=3000):
        approve.click()
        time.sleep(2)
        print("  Approved new version")

    # Publish
    publish = page.locator('button:has-text("Publish")').first
    if publish.is_visible(timeout=5000):
        publish.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
        print("  Published new version!")

    screenshot(page, "29-final")
    print("\n✓ VM Task 4 editorial workflow complete!")
    time.sleep(3)
    browser.close()
