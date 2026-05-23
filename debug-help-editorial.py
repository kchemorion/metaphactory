#!/usr/bin/env python3
"""Check the help documentation for editorial workflows."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=100)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "admin")
    page.fill('input[name="password"]', "admin")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Check the training page for editorial workflow
    page.goto(f"{BASE_URL}/resource/training:editorialWorkflow")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.screenshot(path="cert-screenshots/debug-editorial-training.png", full_page=True)

    body = page.locator('body').inner_text()
    print("=== EDITORIAL WORKFLOW TRAINING PAGE ===")
    print(body[:4000])

    time.sleep(2)
    browser.close()
