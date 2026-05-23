#!/usr/bin/env python3
"""Explore the Instance Data Manager page to understand how to create instances."""
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

    # Go to Instance Data Manager
    page.goto(f"{BASE_URL}/resource/Admin:InstanceDataManager")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.screenshot(path="cert-screenshots/debug-idm-page.png", full_page=True)
    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")

    # Get page text
    body = page.locator('body').inner_text()
    print(f"\n=== PAGE TEXT ===")
    print(body[:3000])

    # Get all visible inputs, selects, buttons
    print(f"\n=== VISIBLE CONTROLS ===")
    controls = page.locator('input, select, button, a.btn')
    for i in range(controls.count()):
        c = controls.nth(i)
        if c.is_visible():
            tag = c.evaluate("el => el.tagName")
            text = c.inner_text().strip()[:40]
            placeholder = c.get_attribute('placeholder') or ''
            cls = (c.get_attribute('class') or '')[:60]
            if text or placeholder:
                print(f"  {tag}: '{text}' placeholder='{placeholder}' class={cls}")

    # Look for class/type selector to pick Recipe
    print(f"\n=== LOOKING FOR TYPE SELECTOR ===")
    selects = page.locator('select, .Select, [class*="select" i]')
    for i in range(selects.count()):
        s = selects.nth(i)
        if s.is_visible():
            cls = (s.get_attribute('class') or '')[:60]
            text = s.inner_text().strip()[:60]
            print(f"  Select: class={cls} text='{text}'")

    page.screenshot(path="cert-screenshots/debug-idm-controls.png")
    time.sleep(3)
    browser.close()
