#!/usr/bin/env python3
"""AI Task 1: Create a Search & Discovery Agent service."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

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

    # Navigate to Admin > Service Settings > All Services
    print("=== NAVIGATING TO ALL SERVICES ===")
    # Try the settings/admin area
    page.goto(f"{BASE_URL}/resource/?uri=http%3A%2F%2Fwww.metaphacts.com%2Fresource%2Fadmin%2F")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/ai1-admin-page.png")

    # Look for Service Settings link
    service_link = page.locator('a:has-text("Service Settings"), a:has-text("All Services")').first
    if service_link.is_visible(timeout=3000):
        service_link.click()
        time.sleep(3)
    else:
        # Try direct URL
        page.goto(f"{BASE_URL}/resource/Admin:AllServices")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        if "empty" in page.locator('body').inner_text().lower():
            page.goto(f"{BASE_URL}/resource/Admin:ServiceSettings")
            page.wait_for_load_state("networkidle")
            time.sleep(3)

    page.screenshot(path="cert-screenshots/ai1-services-page.png")
    print(f"URL: {page.url}")

    # Look for "All Services" tab or link
    all_services = page.locator('a:has-text("All Services"), button:has-text("All Services")').first
    if all_services.is_visible(timeout=2000):
        all_services.click()
        time.sleep(2)

    page.screenshot(path="cert-screenshots/ai1-all-services.png")

    # Get page text to understand the layout
    body_text = page.locator('body').inner_text()
    print(f"\nPage text (first 2000 chars):\n{body_text[:2000]}")

    # Look for "Create" or template selection buttons
    print("\n=== LOOKING FOR CREATE/TEMPLATE OPTIONS ===")
    buttons = page.locator('button, a.btn')
    for i in range(buttons.count()):
        btn = buttons.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            if text and len(text) > 1:
                print(f"  Button: '{text}'")

    # Look for existing services and "Create" button
    create_btn = page.locator(
        'button:has-text("Create"), '
        'button:has-text("Add"), '
        'button:has-text("New"), '
        'a:has-text("Create")'
    ).first
    if create_btn.is_visible(timeout=2000):
        print(f"\nFound create button: '{create_btn.inner_text().strip()[:30]}'")
        create_btn.click()
        time.sleep(2)
        page.screenshot(path="cert-screenshots/ai1-create-dialog.png")

        # Check for template selection
        modal = page.locator('.modal.show')
        if modal.is_visible(timeout=2000):
            print(f"Modal text:\n{modal.inner_text()[:500]}")

    # Also check for existing AI service templates on the page
    print("\n=== AI SERVICE TEMPLATES ===")
    templates = page.locator('[class*="template"], [class*="card"], tr')
    for i in range(min(templates.count(), 20)):
        t = templates.nth(i)
        if t.is_visible():
            text = t.inner_text().strip()[:100]
            if any(kw in text.lower() for kw in ['agent', 'search', 'discovery', 'conversational', 'llm']):
                print(f"  '{text}'")

    time.sleep(3)
    browser.close()
