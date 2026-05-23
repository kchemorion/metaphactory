#!/usr/bin/env python3
"""Dump the exact DOM structure of the vocabulary tree to find more_vert buttons."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=100)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Open the vocabulary
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(3)
    page.locator('a:has-text("Vegetables")').last.click()
    time.sleep(3)
    page.keyboard.press('Escape')
    time.sleep(0.5)

    # Dump the tree HTML
    print("=== TREE HTML STRUCTURE ===")
    tree_html = page.evaluate("""() => {
        // Find the tree container
        const accordion = document.querySelector('.ontodia-accordion');
        if (!accordion) return 'No .ontodia-accordion found';

        // Get a cleaner view - just the first panel's tree
        const panels = accordion.querySelectorAll('.ontodia-accordion-item');
        let html = '';
        panels.forEach((panel, idx) => {
            if (idx === 0) {  // First panel (Terms)
                html = panel.innerHTML;
            }
        });

        // If no panels, try the whole accordion
        if (!html) html = accordion.innerHTML;
        return html.substring(0, 8000);
    }""")
    print(tree_html[:5000])

    # Also find ALL more_vert buttons and their parent chain
    print("\n\n=== ALL MORE_VERT BUTTONS WITH ANCESTRY ===")
    ancestry = page.evaluate("""() => {
        const btns = document.querySelectorAll('button');
        const results = [];
        btns.forEach(btn => {
            if (btn.textContent.trim() === 'more_vert' && btn.offsetParent !== null) {
                let chain = [];
                let el = btn;
                for (let i = 0; i < 6; i++) {
                    const tag = el.tagName.toLowerCase();
                    const cls = el.className ? '.' + el.className.toString().split(' ').filter(c=>c).slice(0,3).join('.') : '';
                    const text = el.childNodes.length === 1 && el.childNodes[0].nodeType === 3
                                 ? '"' + el.textContent.trim().substring(0, 20) + '"' : '';
                    chain.push(tag + cls + text);
                    el = el.parentElement;
                    if (!el) break;
                }
                results.push(chain);
            }
        });
        return results;
    }""")
    for i, chain in enumerate(ancestry):
        print(f"\nmore_vert button #{i}:")
        for j, el in enumerate(chain):
            print(f"  {'  ' * j}{el}")

    # Specifically look at what's near tree concept nodes
    print("\n\n=== CONCEPT NODE STRUCTURE ===")
    concept_html = page.evaluate("""() => {
        // Find links that look like concept nodes (containing concept labels)
        const links = document.querySelectorAll('a');
        for (const link of links) {
            const text = link.textContent.trim();
            if (text === 'Vegetables' && link.offsetParent !== null) {
                // Go up a few levels to get the full tree node structure
                let parent = link.parentElement;
                for (let i = 0; i < 4; i++) {
                    if (parent && parent.parentElement) parent = parent.parentElement;
                }
                if (parent) return parent.outerHTML.substring(0, 4000);
            }
        }
        return 'not found';
    }""")
    print(concept_html[:3000])

    browser.close()
