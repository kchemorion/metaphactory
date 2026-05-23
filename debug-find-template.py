#!/usr/bin/env python3
"""Find the correct template URL by following the UI flow."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Go to search and find metaphacts organization
    page.goto(f"{BASE_URL}/resource/:SimpleSearch")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    search = page.locator('input[placeholder*="Search" i]').first
    if search.is_visible(timeout=3000):
        search.click()
        search.type("metaphacts")
        time.sleep(2)
        # Press Enter or click search
        search.press("Enter")
        time.sleep(3)

    page.screenshot(path="cert-screenshots/debug-search-metaphacts.png")
    print(f"Search URL: {page.url}")

    # Find and click metaphacts result
    result = page.locator('a:has-text("metaphacts")').first
    if result.is_visible(timeout=3000):
        href = result.get_attribute('href')
        print(f"metaphacts link: {href}")
        result.click()
        time.sleep(3)
        print(f"Instance URL: {page.url}")
        page.screenshot(path="cert-screenshots/debug-metaphacts-instance.png")

        # Click Edit Page
        edit = page.locator('a:has-text("Edit Page")').first
        if edit.is_visible(timeout=3000):
            edit.click()
            time.sleep(3)
            print(f"Edit URL: {page.url}")
            page.screenshot(path="cert-screenshots/debug-edit-page.png", full_page=True)

            # Find ALL template-related links
            print("\n=== TEMPLATE LINKS ===")
            links = page.locator('a')
            for i in range(links.count()):
                link = links.nth(i)
                if link.is_visible():
                    text = link.inner_text().strip()[:80]
                    href = link.get_attribute('href') or ''
                    if 'template' in text.lower() or 'Template' in href or 'PanelTemplate' in href:
                        print(f"  '{text}' -> {href}")

    time.sleep(3)
    browser.close()
