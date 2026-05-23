#!/usr/bin/env python3
"""Explore the metaphactory training instance to catalog all modules and tasks."""
import time
import json
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=100)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    # Login
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    # Take screenshot of login page
    page.screenshot(path="cert-screenshots/explore-login.png")

    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Screenshot after login
    page.screenshot(path="cert-screenshots/explore-after-login.png")
    print(f"Current URL after login: {page.url}")

    # Navigate to Start page
    page.goto(f"{BASE_URL}/resource/Start")
    page.wait_for_load_state("networkidle")
    time.sleep(3)

    page.screenshot(path="cert-screenshots/explore-start-page.png", full_page=True)
    print(f"\n=== START PAGE ===")
    print(f"URL: {page.url}")
    print(f"Title: {page.title()}")

    # Get all text content to understand page structure
    body_text = page.locator('body').inner_text()
    print(f"\n=== PAGE TEXT (first 3000 chars) ===")
    print(body_text[:3000])

    # Find all headings
    print(f"\n=== HEADINGS ===")
    headings = page.locator('h1, h2, h3, h4')
    for i in range(headings.count()):
        h = headings.nth(i)
        tag = h.evaluate("el => el.tagName")
        text = h.inner_text().strip()
        if text:
            print(f"  {tag}: {text}")

    # Find all links on the page
    print(f"\n=== ALL LINKS ===")
    links = page.locator('a[href]')
    link_count = links.count()
    print(f"Total links: {link_count}")

    module_links = []
    for i in range(link_count):
        link = links.nth(i)
        try:
            text = link.inner_text().strip()
            href = link.get_attribute("href")
            if text and href and len(text) > 2 and not text.startswith("http"):
                print(f"  [{i}] '{text}' -> {href}")
                if any(kw in text.lower() for kw in ['module', 'task', 'exercise', 'tutorial', 'building', 'modeling', 'basics', 'visual', 'app', 'ai', 'metis']):
                    module_links.append((text, href))
        except:
            pass

    # Find all buttons
    print(f"\n=== BUTTONS ===")
    buttons = page.locator('button')
    for i in range(min(buttons.count(), 30)):
        btn = buttons.nth(i)
        text = btn.inner_text().strip()
        if text:
            print(f"  Button: '{text}'")

    # Find cards, panels, sections that might contain modules
    print(f"\n=== CARDS/PANELS ===")
    cards = page.locator('.card, .panel, .module, [class*="card"], [class*="module"], [class*="tile"]')
    for i in range(min(cards.count(), 20)):
        card = cards.nth(i)
        text = card.inner_text().strip()[:200]
        cls = card.get_attribute("class")
        if text:
            print(f"  Card [{cls}]: {text}")

    # Scroll down to find more content
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    page.screenshot(path="cert-screenshots/explore-start-scrolled.png", full_page=True)

    # Get the full page HTML structure (key sections only)
    print(f"\n=== MAIN CONTENT STRUCTURE ===")
    main_html = page.evaluate("""() => {
        const main = document.querySelector('main, .main-content, #main, [role="main"], .page-content')
                     || document.querySelector('.container')
                     || document.body;
        // Get a simplified view of the structure
        function simplify(el, depth=0) {
            if (depth > 4) return '';
            let result = '';
            const indent = '  '.repeat(depth);
            const tag = el.tagName.toLowerCase();
            const cls = el.className ? `.${el.className.toString().split(' ').join('.')}` : '';
            const id = el.id ? `#${el.id}` : '';
            const text = el.childNodes.length === 1 && el.childNodes[0].nodeType === 3
                         ? el.textContent.trim().substring(0, 80) : '';

            if (['script', 'style', 'link', 'meta', 'noscript'].includes(tag)) return '';

            result += `${indent}<${tag}${id}${cls}>${text ? ' ' + text : ''}\\n`;
            for (const child of el.children) {
                result += simplify(child, depth + 1);
            }
            return result;
        }
        return simplify(main);
    }""")
    print(main_html[:5000])

    # Now explore each potential module link
    print(f"\n\n{'='*80}")
    print("EXPLORING MODULE LINKS")
    print(f"{'='*80}")

    # Collect all links that might be modules/tasks from the start page
    all_links = page.evaluate("""() => {
        const links = [];
        document.querySelectorAll('a[href]').forEach(a => {
            const text = a.textContent.trim();
            const href = a.getAttribute('href');
            const parent = a.parentElement;
            const parentText = parent ? parent.textContent.trim().substring(0, 100) : '';
            if (text && href && text.length > 2) {
                links.push({text, href, parentText});
            }
        });
        return links;
    }""")

    print(f"\nAll links from Start page ({len(all_links)} total):")
    for link in all_links:
        if link['href'].startswith('/') or link['href'].startswith('http'):
            print(f"  '{link['text'][:60]}' -> {link['href'][:80]}")

    browser.close()
