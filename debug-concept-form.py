#!/usr/bin/env python3
"""Debug: what does the concept creation form look like and what enables Save?"""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)
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

    # Go to existing Vegetables vocabulary
    page.goto(f"{BASE_URL}/resource/Assets:Vocabularies")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    vocab_link = page.locator('a:has-text("Vegetables")').first
    if vocab_link.is_visible(timeout=3000):
        vocab_link.click()
        time.sleep(3)
        # Dismiss walkthrough
        try:
            page.keyboard.press('Escape')
            time.sleep(0.5)
        except:
            pass
    else:
        print("No Vegetables vocabulary found!")
        browser.close()
        exit()

    print(f"URL: {page.url}")
    page.screenshot(path="cert-screenshots/debug3-vocab-page.png")

    # Click "Create top-level term"
    create_term = page.locator('button:has-text("Create top-level term")').first
    create_term.click()
    time.sleep(2)

    page.screenshot(path="cert-screenshots/debug3-after-click-create.png", full_page=True)

    # What's visible now?
    print("\n=== AFTER CLICKING 'Create top-level term' ===")

    # Check for overlay/modal
    overlays = page.locator('.overlay-modal, .modal, [role="dialog"], .panel, .sidebar, .form-panel')
    print(f"Overlay/modal elements: {overlays.count()}")
    for i in range(overlays.count()):
        ov = overlays.nth(i)
        if ov.is_visible():
            cls = ov.get_attribute('class')
            role = ov.get_attribute('role')
            print(f"  VISIBLE overlay: class={cls} role={role}")

    # All visible inputs
    print("\n=== ALL VISIBLE INPUTS ===")
    inputs = page.locator('input, textarea, select')
    for i in range(inputs.count()):
        inp = inputs.nth(i)
        if inp.is_visible():
            attrs = {}
            for attr in ['type', 'placeholder', 'name', 'data-testid', 'value', 'class', 'id', 'aria-label']:
                val = inp.get_attribute(attr)
                if val is not None:
                    attrs[attr] = val[:100]
            tag = inp.evaluate("el => el.tagName")
            print(f"  {tag}: {attrs}")

    # All visible buttons
    print("\n=== ALL VISIBLE BUTTONS ===")
    buttons = page.locator('button')
    for i in range(buttons.count()):
        btn = buttons.nth(i)
        if btn.is_visible():
            text = btn.inner_text().strip()[:50]
            disabled = btn.get_attribute('disabled')
            name = btn.get_attribute('name')
            cls = (btn.get_attribute('class') or '')[:60]
            if text:
                print(f"  '{text}' disabled={disabled} name={name} class={cls}")

    # Check the right side panel - in vocab editor, the form appears in the right panel
    print("\n=== RIGHT PANEL CONTENT ===")
    right_panel = page.evaluate("""() => {
        // Look for form elements in various containers
        const forms = document.querySelectorAll('form, .form-group, .concept-form, .term-form');
        const result = [];
        forms.forEach(f => {
            if (f.offsetParent !== null) { // visible
                const inputs = f.querySelectorAll('input, textarea, select, button');
                inputs.forEach(inp => {
                    result.push({
                        tag: inp.tagName,
                        type: inp.type,
                        placeholder: inp.placeholder,
                        name: inp.name,
                        value: inp.value?.substring(0, 50),
                        disabled: inp.disabled,
                        visible: inp.offsetParent !== null,
                        class: inp.className?.substring(0, 80)
                    });
                });
            }
        });
        return result;
    }""")
    for item in right_panel:
        if item.get('visible'):
            print(f"  {item}")

    # Try to find where the preferred label input is
    pref_selectors = [
        'input[placeholder="Enter preferred label here..."]',
        'input[placeholder*="preferred" i]',
        'input[placeholder*="label" i]',
        'input[placeholder*="Enter" i]',
        'input[placeholder*="name" i]',
        'input[aria-label*="label" i]',
        'input[data-testid*="label" i]',
    ]
    for sel in pref_selectors:
        matches = page.locator(sel)
        count = matches.count()
        visible = sum(1 for i in range(count) if matches.nth(i).is_visible())
        if count > 0:
            print(f"\n  Selector '{sel}': {count} total, {visible} visible")
            for i in range(count):
                m = matches.nth(i)
                print(f"    [{i}] visible={m.is_visible()} placeholder={m.get_attribute('placeholder')} value={m.get_attribute('value')}")

    # Try a broader approach - dump the page structure around the main content
    print("\n=== PAGE STRUCTURE (simplified) ===")
    structure = page.evaluate("""() => {
        function walk(el, depth) {
            if (depth > 5 || !el || !el.tagName) return '';
            const tag = el.tagName.toLowerCase();
            if (['script', 'style', 'svg', 'path'].includes(tag)) return '';
            const visible = el.offsetParent !== null || el.style.display !== 'none';
            if (!visible && depth > 2) return '';
            const cls = el.className && typeof el.className === 'string' ? '.' + el.className.split(' ').filter(c => c).slice(0, 3).join('.') : '';
            const text = el.childNodes.length === 1 && el.childNodes[0].nodeType === 3 ? ' "' + el.textContent.trim().substring(0, 40) + '"' : '';
            const indent = '  '.repeat(depth);
            let result = indent + '<' + tag + cls + '>' + text + '\\n';
            for (const child of el.children) {
                result += walk(child, depth + 1);
            }
            return result;
        }
        const main = document.querySelector('.page-content-wrapper') || document.querySelector('main') || document.body;
        return walk(main, 0);
    }""")
    # Print first 5000 chars
    print(structure[:5000])

    time.sleep(5)
    browser.close()
