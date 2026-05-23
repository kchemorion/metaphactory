#!/usr/bin/env python3
"""Explore the Instance Data Manager to understand how to create recipe instances."""
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

    # Open the Recipes ontology
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    recipes_link = page.locator('a:has-text("Recipes")').last
    if recipes_link.is_visible(timeout=3000):
        recipes_link.click()
        time.sleep(3)
        try:
            page.keyboard.press('Escape')
            time.sleep(0.5)
        except:
            pass

    print(f"URL: {page.url}")
    page.screenshot(path="cert-screenshots/debug-onto-page.png")

    # Look for Instance Data Manager access
    print("\n=== LOOKING FOR INSTANCE MANAGEMENT ===")

    # Check the "More" dropdown
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=2000):
        more_btn.click()
        time.sleep(1)
        dropdown = page.locator('.dropdown-menu.show')
        if dropdown.is_visible():
            items = dropdown.locator('a, button')
            for i in range(items.count()):
                item = items.nth(i)
                text = item.inner_text().strip()[:60]
                if text:
                    print(f"  More menu: '{text}'")
        page.keyboard.press('Escape')
        time.sleep(0.5)

    # Check all visible buttons/links for instance-related text
    print("\n=== ALL INSTANCE-RELATED ELEMENTS ===")
    all_elements = page.locator('a, button')
    for i in range(all_elements.count()):
        el = all_elements.nth(i)
        if el.is_visible():
            text = el.inner_text().strip()[:60]
            href = el.get_attribute('href') or ''
            if any(kw in text.lower() for kw in ['instance', 'manage', 'data manager', 'create instance', 'authoring']):
                print(f"  '{text}' -> {href[:80]}")

    # Check tabs in the ontology editor
    print("\n=== TABS ===")
    tabs = page.locator('[role="tab"], .nav-link, button.btn-secondary')
    for i in range(tabs.count()):
        tab = tabs.nth(i)
        if tab.is_visible():
            text = tab.inner_text().strip()[:40]
            if text:
                print(f"  Tab: '{text}'")

    # Try navigating to Instance Data Manager directly
    print("\n=== TRYING DIRECT URLS ===")
    for url_suffix in [
        "Admin:InstanceDataManager",
        "resource/Admin:InstanceDataManager",
    ]:
        test_url = f"{BASE_URL}/resource/{url_suffix}" if not url_suffix.startswith("resource") else f"{BASE_URL}/{url_suffix}"
        page.goto(test_url)
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        title = page.title()
        body_start = page.locator('body').inner_text()[:100]
        print(f"  {url_suffix}: title='{title}' body='{body_start}'")

    # Look for "Visual Instance Authoring" or similar
    page.goto(f"{BASE_URL}/resource/Assets:Ontologies")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    recipes_link = page.locator('a:has-text("Recipes")').last
    if recipes_link.is_visible(timeout=3000):
        recipes_link.click()
        time.sleep(3)
        page.keyboard.press('Escape')
        time.sleep(0.5)

    # Try "Info & Metadata" tab which might have instance management
    info_tab = page.locator('button:has-text("Info & Metadata")').first
    if info_tab.is_visible(timeout=2000):
        info_tab.click()
        time.sleep(2)
        page.screenshot(path="cert-screenshots/debug-info-metadata.png")

        # Look for instance-related content
        body = page.locator('body').inner_text()
        for line in body.split('\n'):
            if any(kw in line.lower() for kw in ['instance', 'manage', 'authoring', 'create']):
                print(f"  Info tab: '{line.strip()[:80]}'")

    # Try the ontology editor's class context - right click on Recipe class
    print("\n=== CHECKING ONTOLOGY EDITOR FOR INSTANCE CREATION ===")
    elements_tab = page.locator('button:has-text("Elements")').first
    if elements_tab.is_visible(timeout=2000):
        elements_tab.click()
        time.sleep(1)

    # Click on Recipe class in the canvas or list
    recipe_node = page.locator('text=Recipe').first
    if recipe_node.is_visible(timeout=2000):
        recipe_node.click()
        time.sleep(1)
        # Check right panel for instance creation options
        panel_text = page.evaluate("""() => {
            const panels = document.querySelectorAll('[class*="panel"], [class*="sidebar"], [class*="detail"]');
            let text = '';
            panels.forEach(p => { if (p.offsetParent !== null) text += p.textContent.trim().substring(0, 500) + '\\n'; });
            return text;
        }""")
        for line in panel_text.split('\n'):
            if any(kw in line.lower() for kw in ['instance', 'manage', 'create', 'authoring']):
                print(f"  Panel: '{line.strip()[:100]}'")

    page.screenshot(path="cert-screenshots/debug-instance-final.png")
    time.sleep(2)
    browser.close()
