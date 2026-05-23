#!/usr/bin/env python3
"""Find exactly how CodeMirror is attached in the template editor."""
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

    # Navigate to template editor
    url = (f"{BASE_URL}/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies"
           ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit")
    try:
        page.goto(url)
        page.wait_for_load_state("networkidle")
    except:
        pass
    time.sleep(5)

    # Find CodeMirror
    result = page.evaluate("""() => {
        const info = {};

        // Check for .CodeMirror class
        const cm = document.querySelector('.CodeMirror');
        info.dotCodeMirror = cm ? {
            tag: cm.tagName,
            hasInstance: !!cm.CodeMirror,
            class: cm.className.substring(0, 100)
        } : null;

        // Search ALL elements for CodeMirror property
        const allEls = document.querySelectorAll('*');
        const cmElements = [];
        allEls.forEach(el => {
            if (el.CodeMirror) {
                cmElements.push({
                    tag: el.tagName,
                    class: el.className?.toString().substring(0, 80),
                    id: el.id
                });
            }
        });
        info.elementsWithCodeMirrorProp = cmElements;

        // Check for CodeMirror-related classes
        const cmClasses = document.querySelectorAll('[class*="CodeMirror"], [class*="codemirror"], [class*="cm-"]');
        info.cmClassElements = [];
        cmClasses.forEach(el => {
            if (el.offsetParent !== null) {
                info.cmClassElements.push({
                    tag: el.tagName,
                    class: el.className?.toString().substring(0, 100)
                });
            }
        });

        // Check textareas
        const textareas = document.querySelectorAll('textarea');
        info.textareas = [];
        textareas.forEach(ta => {
            info.textareas.push({
                visible: ta.offsetParent !== null,
                value: ta.value.substring(0, 100),
                class: ta.className.substring(0, 80),
                rows: ta.rows,
                id: ta.id
            });
        });

        // Check for Monaco editor
        const monaco = document.querySelector('.monaco-editor');
        info.hasMonaco = !!monaco;

        // Check for Ace editor
        const ace = document.querySelector('.ace_editor');
        info.hasAce = !!ace;

        return info;
    }""")

    import json
    print(json.dumps(result, indent=2))

    browser.close()
