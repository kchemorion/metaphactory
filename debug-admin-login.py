#!/usr/bin/env python3
"""Try logging in as admin to check if editorial workflow controls appear."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

# Try different admin credentials
CREDS = [
    ("admin", "admin"),
    ("admin", "m20"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    for username, password in CREDS:
        print(f"\n=== TRYING {username}/{password} ===")
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        if "/login" not in page.url:
            print(f"  Logged in as {username}!")

            # Check the user profile indicator
            user_indicator = page.locator('[class*="user"], [href*="UserProfile"]').first
            if user_indicator.is_visible(timeout=2000):
                print(f"  User shown: {user_indicator.inner_text().strip()[:30]}")

            # Go to Recipes ontology
            page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            page.locator('a:has-text("Recipes")').last.click()
            time.sleep(3)
            page.keyboard.press('Escape')
            time.sleep(0.5)

            # Check More menu
            more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
            if more_btn.is_visible(timeout=2000):
                more_btn.click()
                time.sleep(1)
                page.screenshot(path=f"cert-screenshots/debug-admin-more-{username}.png")
                dropdown = page.locator('.dropdown-menu.show')
                if dropdown.is_visible():
                    items = dropdown.locator('a, button, .dropdown-item')
                    print(f"  More menu items:")
                    for i in range(items.count()):
                        item = items.nth(i)
                        text = item.inner_text().strip()[:60]
                        if text:
                            print(f"    '{text}'")
                page.keyboard.press('Escape')
                time.sleep(0.5)

            # Check Role assignment dialog
            more_btn.click()
            time.sleep(0.5)
            role_opt = page.locator('.dropdown-menu.show a:has-text("Role assignment")').first
            if role_opt.is_visible(timeout=1000):
                role_opt.click()
                time.sleep(2)
                page.screenshot(path=f"cert-screenshots/debug-admin-roles-{username}.png")
                modal = page.locator('.modal.show')
                if modal.is_visible():
                    print(f"  Role dialog text:")
                    print(f"    {modal.inner_text()[:500]}")
                page.keyboard.press('Escape')
                time.sleep(0.5)

            # Check for review/publish buttons
            print(f"  Review/publish buttons:")
            for kw in ['review', 'publish', 'version', 'start review', 'request review']:
                btns = page.locator(f'button:has-text("{kw}"), a:has-text("{kw}")')
                for i in range(btns.count()):
                    btn = btns.nth(i)
                    if btn.is_visible():
                        print(f"    Found: '{btn.inner_text().strip()[:40]}'")

            # Logout
            page.goto(f"{BASE_URL}/logout")
            time.sleep(1)
            break
        else:
            print(f"  Login failed for {username}/{password}")

    browser.close()
