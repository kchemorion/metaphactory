#!/usr/bin/env python3
"""Explore each module page to catalog all tasks."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

MODULE_PAGES = [
    ("metaphactory basics", "/resource/training:SampleApp"),
    ("Visual modeling basics", "/resource/:BusinessTraining"),
    ("Visual modeling advanced", "/resource/training:VisualModellingAdv"),
    ("KG Engineer Certification", "/resource/certification:knowledgeGraphEnginner"),
    ("App Building Basics", "/resource/training:AppBuildingBasicsSelfGuided"),
    ("App Building Advanced", "/resource/training:AppBuildingAdvanced"),
    ("KG App Engineer Certification", "/resource/certification:knowledgeGraphAppEngineer"),
    ("metis Basics", "/resource/training:metisBasics"),
    ("AI metis Engineer Certification", "/resource/certification:aiMetisEngineer"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    for module_name, module_path in MODULE_PAGES:
        print(f"\n{'='*80}")
        print(f"MODULE: {module_name}")
        print(f"URL: {BASE_URL}{module_path}")
        print(f"{'='*80}")

        page.goto(f"{BASE_URL}{module_path}")
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        # Screenshot
        safe_name = module_name.replace(" ", "_").replace("/", "_")
        page.screenshot(path=f"cert-screenshots/module-{safe_name}.png", full_page=True)

        # Get full text
        body_text = page.locator('body').inner_text()
        print(f"\n--- PAGE TEXT ---")
        print(body_text[:5000])

        # Get all headings
        print(f"\n--- HEADINGS ---")
        headings = page.locator('h1, h2, h3, h4, h5')
        for i in range(headings.count()):
            h = headings.nth(i)
            try:
                tag = h.evaluate("el => el.tagName")
                text = h.inner_text().strip()
                if text and len(text) < 200:
                    print(f"  {tag}: {text}")
            except:
                pass

        # Get all links
        print(f"\n--- LINKS ---")
        links = page.evaluate("""() => {
            const links = [];
            document.querySelectorAll('a[href]').forEach(a => {
                const text = a.textContent.trim();
                const href = a.getAttribute('href');
                if (text && href && text.length > 2 && text.length < 100) {
                    links.push({text, href});
                }
            });
            return links;
        }""")
        for link in links:
            href = link['href']
            if href.startswith('/') or href.startswith('http'):
                # Skip nav/header links we've already seen
                if any(skip in href for skip in ['/login', '/logout', 'Assets:', 'Admin:', 'SimpleSearch', '/sparql', 'UserProfile']):
                    continue
                print(f"  '{link['text'][:60]}' -> {href[:80]}")

        # Scroll and get more content
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)

        # Check if there are sub-sections or cards with tasks
        cards = page.locator('.card, [class*="task"], [class*="exercise"]')
        if cards.count() > 0:
            print(f"\n--- CARDS/TASKS ({cards.count()}) ---")
            for i in range(min(cards.count(), 20)):
                card = cards.nth(i)
                text = card.inner_text().strip()[:300]
                if text:
                    print(f"  Card {i}: {text[:200]}")

    browser.close()
    print("\n\nDONE - All modules explored")
