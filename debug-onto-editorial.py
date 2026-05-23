#!/usr/bin/env python3
"""Explore the ontology editorial workflow UI to understand the review/publish flow."""
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

    # Go to Ontologies listing
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-onto-list.png", full_page=True)

    # Find the Recipes ontology row and check for editorial workflow controls
    print("=== ONTOLOGIES LIST ===")
    body = page.locator('body').inner_text()
    for line in body.split('\n'):
        if 'recipe' in line.lower():
            print(f"  {line.strip()[:100]}")

    # Look for status indicators and workflow buttons on the Recipes row
    print("\n=== LOOKING FOR WORKFLOW CONTROLS ON RECIPES ROW ===")
    # Find the Recipes entry and check nearby elements
    recipes_entries = page.locator('a:has-text("Recipes")')
    print(f"Recipes links: {recipes_entries.count()}")
    for i in range(recipes_entries.count()):
        entry = recipes_entries.nth(i)
        if entry.is_visible():
            href = entry.get_attribute('href') or ''
            text = entry.inner_text().strip()[:40]
            print(f"  [{i}] '{text}' -> {href[:80]}")
            # Check parent row for buttons
            parent = entry.locator('xpath=ancestor::tr | xpath=ancestor::div[contains(@class,"row")]').first
            if parent.is_visible(timeout=500):
                btns = parent.locator('button, a.btn')
                for j in range(btns.count()):
                    btn = btns.nth(j)
                    if btn.is_visible():
                        print(f"    Button: '{btn.inner_text().strip()[:30]}'")

    # Now open the Recipes ontology
    print("\n=== OPENING RECIPES ONTOLOGY ===")
    recipes_link = page.locator('a:has-text("Recipes")').last
    recipes_link.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)
    page.screenshot(path="cert-screenshots/debug-onto-opened.png")

    # Check the "More" dropdown for editorial workflow options
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=2000):
        more_btn.click()
        time.sleep(1)
        page.screenshot(path="cert-screenshots/debug-onto-more-menu.png")
        dropdown = page.locator('.dropdown-menu.show')
        if dropdown.is_visible():
            items = dropdown.locator('a, button, .dropdown-item')
            print(f"\nMore menu items:")
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  '{text}'")
        page.keyboard.press('Escape')
        time.sleep(0.5)

    # Check the status bar / header area for workflow status
    print("\n=== STATUS/WORKFLOW INDICATORS ===")
    status_els = page.locator('[class*="status"], [class*="workflow"], [class*="editorial"], [class*="badge"]')
    for i in range(status_els.count()):
        el = status_els.nth(i)
        if el.is_visible():
            text = el.inner_text().strip()[:60]
            cls = (el.get_attribute('class') or '')[:60]
            print(f"  '{text}' class={cls}")

    # Check for "Start review", "Publish", "New version" buttons
    print("\n=== REVIEW/PUBLISH BUTTONS ===")
    for keyword in ['review', 'publish', 'version', 'accept', 'approve', 'reject']:
        btns = page.locator(f'button:has-text("{keyword}"), a:has-text("{keyword}")')
        for i in range(btns.count()):
            btn = btns.nth(i)
            if btn.is_visible():
                print(f"  Found: '{btn.inner_text().strip()[:40]}'")

    # Go back to listing and check for "Role assignment" which is where you add reviewers
    print("\n=== CHECKING ROLE ASSIGNMENT ===")
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=2000):
        more_btn.click()
        time.sleep(0.5)
        role_opt = page.locator('.dropdown-menu.show a:has-text("Role assignment")').first
        if role_opt.is_visible(timeout=1000):
            print("  Found 'Role assignment' in More menu - clicking")
            role_opt.click()
            time.sleep(2)
            page.screenshot(path="cert-screenshots/debug-role-assignment.png")

            # Explore the role assignment dialog
            modal = page.locator('.modal.show')
            if modal.is_visible(timeout=2000):
                modal_text = modal.inner_text()[:500]
                print(f"  Role dialog: {modal_text}")

                # Look for inputs to add reviewer
                inputs = modal.locator('input, select')
                for i in range(inputs.count()):
                    inp = inputs.nth(i)
                    if inp.is_visible():
                        placeholder = inp.get_attribute('placeholder') or ''
                        cls = (inp.get_attribute('class') or '')[:60]
                        print(f"    Input: placeholder='{placeholder}' class={cls}")

            page.keyboard.press('Escape')
            time.sleep(0.5)

    # Check the "Info & Metadata" tab
    print("\n=== INFO & METADATA TAB ===")
    info_tab = page.locator('button:has-text("Info & Metadata")').first
    if info_tab.is_visible(timeout=2000):
        info_tab.click()
        time.sleep(2)
        page.screenshot(path="cert-screenshots/debug-onto-info.png")

        # Look for editorial workflow section
        body = page.locator('body').inner_text()
        for line in body.split('\n'):
            if any(kw in line.lower() for kw in ['review', 'publish', 'version', 'status', 'workflow', 'editorial']):
                print(f"  '{line.strip()[:80]}'")

    time.sleep(2)
    browser.close()
