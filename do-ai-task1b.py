#!/usr/bin/env python3
"""AI Task 1: Navigate to AI Services and explore the creation UI."""
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

    # Go to Service Settings
    page.goto(f"{BASE_URL}/resource/Admin:ServiceSettings")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    # Click "All Services" tab (as per task description)
    all_tab = page.locator('a:has-text("All Services"), button:has-text("All Services")').first
    if all_tab.is_visible(timeout=2000):
        all_tab.click()
        time.sleep(3)
    page.screenshot(path="cert-screenshots/ai1-all-services-tab.png", full_page=True)
    print(f"URL after clicking All Services: {page.url}")

    body = page.locator('body').inner_text()
    print(f"\nPage content:\n{body[:3000]}")

    # Look for Create button or service list
    print("\n=== BUTTONS ===")
    btns = page.locator('button, a.btn')
    for i in range(btns.count()):
        btn = btns.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            if text and len(text) > 1:
                print(f"  '{text}'")

    # Also check AI Services tab
    print("\n=== CHECKING AI SERVICES TAB ===")
    ai_tab = page.locator('a:has-text("AI Services"), button:has-text("AI Services")').first
    if ai_tab.is_visible(timeout=2000):
        ai_tab.click()
        time.sleep(3)
        page.screenshot(path="cert-screenshots/ai1-ai-services-tab.png", full_page=True)
        body2 = page.locator('body').inner_text()
        print(f"\nAI Services tab content:\n{body2[:3000]}")

        btns2 = page.locator('button, a.btn')
        for i in range(btns2.count()):
            btn = btns2.nth(i)
            if btn.is_visible():
                text = btn.inner_text().strip()[:50]
                if text and len(text) > 1:
                    print(f"  Button: '{text}'")

    time.sleep(3)
    browser.close()
