"""
metaphactory Playwright Automation Helpers

A battle-tested library for driving the metaphactory UI via Playwright.
Every pattern here was learned from real failures against live metaphactory
instances (cloud training + local Docker 5.10.0) and re-verified against the
running platform.

THE CARDINAL RULES (read reference.md for the full list):
  1. React forms ignore fill() — type char-by-char with react_type().
  2. Each tree concept has its OWN more_vert button — never use .first globally.
  3. SPARQL editor = CodeMirror (JS .setValue works). Page templates = Monaco
     (no window.monaco; keyboard.type only).
  4. Call dismiss_modals() between every multi-step action.
  5. networkidle times out constantly — wrap and continue.
  6. The Git versioning dialog stays open after Save — close it explicitly.

Usage:
    from mf_helpers import *
    login(page, "http://localhost:10214", "admin", "admin")
"""

import os
import time
from datetime import datetime
from pathlib import Path

SCREENSHOT_DIR = "screenshots"
SLOW = 0.3  # seconds between UI actions


# ---------------------------------------------------------------------------
# Login & Navigation
# ---------------------------------------------------------------------------

def login(page, base_url, username, password):
    """Log in. The login form uses plain HTML inputs, so fill() is fine HERE
    (React-form quirks only apply inside the ontology/vocabulary editors)."""
    page.goto(f"{base_url}/login", wait_until="domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('input[type="submit"]')
    page.wait_for_timeout(3000)
    return "/login" not in page.url


def navigate(page, url, username="admin", password="admin", retries=2):
    """Navigate with retry + automatic re-login on session expiry.
    networkidle frequently times out — that is normal and the page is usable."""
    for attempt in range(retries + 1):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            if "/login" in page.url:
                page.fill('input[name="username"]', username)
                page.fill('input[name="password"]', password)
                page.click('input[type="submit"]')
                page.wait_for_timeout(2500)
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(SLOW)
            return
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            if "/login" in page.url:
                raise e
            return  # timeout but page usable


def safe_navigate(page, url):
    """Navigate, never raise."""
    try:
        navigate(page, url)
    except Exception as e:
        print(f"[safe_navigate] {url}: {e}")
    time.sleep(SLOW)


def screenshot(page, name):
    """Full-page screenshot into SCREENSHOT_DIR (auto-created)."""
    Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    print(f"[screenshot] {path}")
    return path


# ---------------------------------------------------------------------------
# Modal / Dropdown Cleanup  — call between EVERY multi-step action
# ---------------------------------------------------------------------------

def dismiss_modals(page):
    """Force-close stuck modals, dialogs, and dropdowns. The #1 fix for flaky
    failures: leftover overlays silently block the next click."""
    try:
        page.evaluate(
            "document.querySelectorAll('.dropdown-menu.show')"
            ".forEach(m => m.classList.remove('show'));"
        )
    except Exception:
        pass
    for _ in range(3):
        try:
            modal = page.locator('.modal.show, .overlay-modal.show, .create-term-dialog.show')
            if modal.is_visible(timeout=300):
                close = modal.locator(
                    '.btn-close, button:has-text("Close"), button:has-text("Cancel")'
                ).first
                if close.is_visible(timeout=300):
                    close.click(force=True)
                else:
                    page.keyboard.press('Escape')
                time.sleep(SLOW)
            else:
                break
        except Exception:
            page.keyboard.press('Escape')
            time.sleep(SLOW)
    try:
        page.evaluate(
            "document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());"
            "document.body.classList.remove('modal-open');"
        )
    except Exception:
        pass


def dismiss_walkthrough(page):
    """Close the Welcome / walkthrough carousel shown on first visits."""
    for _ in range(3):
        try:
            modal = page.locator('.walkthroughCarousel.show, .modal.show')
            if modal.is_visible(timeout=1000):
                close = page.locator('.modal.show .btn-close')
                if close.count() > 0 and close.first.is_visible(timeout=500):
                    close.first.click(force=True)
                else:
                    page.keyboard.press('Escape')
            else:
                break
        except Exception:
            page.keyboard.press('Escape')
    time.sleep(SLOW)


# ---------------------------------------------------------------------------
# React Form Helpers
# ---------------------------------------------------------------------------

def react_type(locator, text, delay=30):
    """Type char-by-char so React's synthetic onChange fires. fill() does NOT
    update React state — the form stays 'empty' and buttons stay disabled.
    30ms is the sweet spot; faster drops events. NEVER fill('') a React input
    first — it corrupts the controlled state."""
    locator.click()
    time.sleep(0.1)
    locator.type(text, delay=delay)
    time.sleep(0.5)


def react_select_pick(page, option_text, container=None):
    """Pick from a react-select dropdown. The .Select__input-container div
    intercepts clicks on the real <input>, so force-click it, wait for the
    menu, then click the [role=option]."""
    scope = container if container else page
    page.mouse.click(10, 10)  # dismiss any hovering tooltip/popover
    time.sleep(SLOW)
    for sel in ('.Select__input-container', '[class*="Select__input-container"]',
                '.css-1hwfws3', '[class*="indicatorContainer"]'):
        el = scope.locator(sel).first
        if el.count() > 0:
            el.click(force=True)
            break
    time.sleep(1)
    option = page.locator(f'[role="option"]:has-text("{option_text}")').first
    if option.is_visible(timeout=3000):
        option.click()
        time.sleep(SLOW)
        return True
    return False


def unique_iri(base):
    """Timestamped IRI to dodge 'already exists' conflicts from ghost data left
    by previously deleted assets (DROP GRAPH does not clear git-backed storage)."""
    return f"{base.rstrip('/#')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def create_asset_dialog(page, title, asset_type="vocabulary"):
    """Fill the Create Vocabulary/Ontology dialog and click Create.
    asset_type: 'vocabulary' or 'ontology'. Detects IRI conflict (Create button
    stays disabled) and falls back to a unique IRI.

    Open the dialog first via the catalog's 'Create' button. Verified testids
    (5.10.0): asset-title-input, suggest-iri-{type}, suggest-iri-{type}-input
    (the -input only appears AFTER you uncheck the suggest checkbox)."""
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=5000)
    react_type(title_input, title)
    time.sleep(1)

    create_btn = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    time.sleep(1)
    if create_btn.get_attribute("disabled") is not None:
        print("[create_asset_dialog] IRI conflict -> unique IRI")
        suggest_cb = page.locator(f'input[data-testid="suggest-iri-{asset_type}"]').first
        if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
            suggest_cb.click()
            time.sleep(0.5)
        iri_input = page.locator(f'input[data-testid="suggest-iri-{asset_type}-input"]').first
        if iri_input.is_visible(timeout=2000):
            host = "ontologies" if asset_type == "ontology" else "vocabularies"
            base = f"https://{host}.metaphacts.com/{title.lower().replace(' ', '-')}"
            react_type(iri_input, unique_iri(base) + "/0.1")
            time.sleep(0.5)

    for _ in range(30):
        if create_btn.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    create_btn.click()
    time.sleep(3)
    dismiss_walkthrough(page)


# ---------------------------------------------------------------------------
# Vocabulary Tree Helpers
# ---------------------------------------------------------------------------

def tree_click_concept(page, label):
    """Click a concept in the vocabulary tree, expanding collapsed parents.
    Scoped to the tree panel (.ontodia-accordion) so we don't match the same
    label in the detail panel."""
    tree = page.locator('.ontodia-accordion, .termTree, [class*="termTree"]').first
    node = tree.locator(f'a:has-text("{label}")').first
    if not node.is_visible(timeout=2000):
        toggles = tree.locator('.LazyTreeSelector--expandToggle, .caret, [class*="expand"]')
        for i in range(toggles.count()):
            t = toggles.nth(i)
            if t.is_visible():
                t.click()
                time.sleep(0.3)
                if node.is_visible():
                    break
        node = tree.locator(f'a:has-text("{label}")').first
    node.click(force=True)
    time.sleep(1)
    return node


def tree_concept_menu(page, label):
    """Open the more_vert (three-dot) menu for a SPECIFIC concept.

    CRITICAL: every concept has its OWN more_vert inside its
    span.termTree__node. page.locator('button:has-text("more_vert")').first
    grabs the WRONG concept. Anchor to the concept's <a>, walk up to its node
    container, then find more_vert within that scope."""
    node = tree_click_concept(page, label)
    container = node.locator(
        'xpath=ancestor::span[contains(@class,"termTree__node")]'
    ).first
    menu_btn = container.locator('button:has-text("more_vert")').first
    if not menu_btn.is_visible(timeout=1500):
        container = node.locator(
            'xpath=ancestor::div[contains(@class,"LazyTreeSelector--itemContent")]'
        ).first
        menu_btn = container.locator('button:has-text("more_vert")').first
    menu_btn.wait_for(state="visible", timeout=3000)
    menu_btn.click()
    time.sleep(0.5)


def _fill_concept_form(page, label, definition=""):
    pref = page.locator('input[placeholder="Enter preferred label here..."]').first
    pref.wait_for(state="visible", timeout=5000)
    pref.click()
    pref.type(label, delay=30)
    time.sleep(0.5)
    if definition:
        d = page.locator('textarea[placeholder="Enter definition here..."]').first
        if d.is_visible(timeout=1000):
            d.click()
            d.type(definition, delay=20)
    save = page.locator('.overlay-modal.show button[name="submit"]').first
    save.wait_for(state="visible", timeout=3000)
    time.sleep(0.3)
    save.click()
    time.sleep(1.5)


def create_top_concept(page, label, definition=""):
    """Create a top-level concept. Uses the editor's 'Create top-level term'."""
    page.locator('button:has-text("Create top-level term")').first.click()
    time.sleep(1.5)
    _fill_concept_form(page, label, definition)
    print(f"[create_top_concept] {label}")


def create_narrower_concept(page, parent, child, definition=""):
    """Create a narrower (child) concept via parent's more_vert > 'Create
    narrower term'."""
    tree_concept_menu(page, parent)
    narrower = page.locator('.dropdown-menu.show a:has-text("Create narrower term")').first
    if not narrower.is_visible(timeout=2000):
        dismiss_modals(page)
        print(f"[create_narrower_concept] 'Create narrower term' missing for {parent}")
        return
    narrower.click()
    time.sleep(1)
    _fill_concept_form(page, child, definition)
    print(f"[create_narrower_concept] {child} under {parent}")


def set_concept_status(page, label, status):
    """Set a concept's editorial status via its more_vert menu.
    Status controls are <button class='termSetStatusButton'>, NOT <a>.
    Values: 'In review', 'Ready for review', 'Accepted for publication',
    'Request changes'."""
    tree_concept_menu(page, label)
    btn = page.locator(
        f'.dropdown-menu.show button.termSetStatusButton:has-text("{status}")'
    ).first
    if btn.is_visible(timeout=2000):
        btn.click()
        time.sleep(1)
        confirm = page.locator('button:has-text("Confirm"), button:has-text("Yes")')
        if confirm.count() > 0 and confirm.first.is_visible(timeout=800):
            confirm.first.click()
            time.sleep(0.5)
        dismiss_modals(page)
        print(f"[set_concept_status] {label} -> {status}")
    else:
        dismiss_modals(page)
        print(f"[set_concept_status] '{status}' unavailable for {label}")


# ---------------------------------------------------------------------------
# Ontology Editor Helpers
# ---------------------------------------------------------------------------

def switch_ontology_tab(page, tab):
    """Switch Classes / Attributes / Relations / Graph tab."""
    page.locator(
        f'button:has-text("{tab}"), .nav-link:has-text("{tab}"), [role="tab"]:has-text("{tab}")'
    ).first.click()
    time.sleep(SLOW)


def _create_ontology_entity(page, button_text, name):
    page.locator(f'button:has-text("{button_text}")').first.click()
    time.sleep(1)
    label = page.locator('input[placeholder="Enter label here..."]').first
    if label.is_visible(timeout=2000):
        label.click()
        react_type(label, name)
    confirm = page.locator(
        'button[data-testid="confirmation-dialog-button-confirm"], button:has-text("Confirm")'
    ).first
    if confirm.is_visible(timeout=1500):
        confirm.click()
        time.sleep(0.5)
    dismiss_modals(page)
    print(f"[ontology] created '{name}' via {button_text}")


def create_ontology_class(page, name):
    _create_ontology_entity(page, "Create Class", name)


def create_ontology_attribute(page, name):
    """Attribute = datatype property."""
    _create_ontology_entity(page, "Create Attribute", name)


def create_ontology_relation(page, name):
    """Relation = object property."""
    _create_ontology_entity(page, "Create Relation", name)


# ---------------------------------------------------------------------------
# Editors — CodeMirror (SPARQL, service config) & Monaco (page templates)
# ---------------------------------------------------------------------------

def codemirror_set(page, content):
    """Set a CodeMirror editor's content via its JS instance. Works perfectly.
    Used by: SPARQL editor, AI service config dialog, Turtle editor."""
    page.evaluate(
        "(content) => {"
        "  const cm = document.querySelector('.CodeMirror');"
        "  if (cm && cm.CodeMirror) cm.CodeMirror.setValue(content);"
        "  else throw new Error('CodeMirror instance not found');"
        "}",
        content,
    )
    time.sleep(SLOW)


def codemirror_get(page):
    return page.evaluate(
        "() => { const cm = document.querySelector('.CodeMirror');"
        " return cm && cm.CodeMirror ? cm.CodeMirror.getValue() : ''; }"
    )


def codemirror_replace(page, find, replace):
    """Find/replace inside a CodeMirror editor (good for tweaking a config
    without rewriting it)."""
    codemirror_set(page, codemirror_get(page).replace(find, replace))


def monaco_set_via_keyboard(page, content):
    """Set a Monaco editor (page/panel templates) via keyboard typing.

    CRITICAL: window.monaco is undefined in metaphactory's build, so
    monaco.editor.getModels() does NOT work. insert_text() and clipboard paste
    corrupt special chars (< > { }). Click -> select-all -> delete -> type is
    the only reliable path. Slow for large content; for >5KB consider chunking."""
    editor = page.locator('.monaco-editor .view-lines, .monaco-editor textarea').first
    editor.wait_for(state="visible", timeout=5000)
    editor.click()
    time.sleep(0.3)
    mod = "Meta" if os.uname().sysname == "Darwin" else "Control"
    page.keyboard.press(f"{mod}+a")
    time.sleep(0.2)
    page.keyboard.press("Backspace")
    time.sleep(0.3)
    page.keyboard.type(content, delay=3)
    time.sleep(1)
    return True


def sparql_update(page, base_url, query):
    """Run a SPARQL query/update via /sparql. The SPARQL page uses CodeMirror
    (verified 5.10.0), so codemirror_set is the right tool."""
    safe_navigate(page, f"{base_url}/sparql")
    time.sleep(1)
    dismiss_modals(page)
    codemirror_set(page, query)
    time.sleep(0.5)
    page.locator(
        'button:has-text("Execute"), button:has-text("Run"), button[title*="xecute"]'
    ).first.click()
    time.sleep(2)


# ---------------------------------------------------------------------------
# Editorial Workflow Helpers
# ---------------------------------------------------------------------------

def git_save(page):
    """Save vocabulary/ontology via More > Git versioning > Save.
    CRITICAL: the Git dialog stays open after Save — dismiss_modals() closes it,
    otherwise the next interaction is blocked."""
    more = page.locator(
        'button:has-text("More"), [data-testid="more-menu"], button:has-text("more_horiz")'
    ).first
    if not more.is_visible(timeout=3000):
        return
    more.click()
    time.sleep(0.5)
    git = page.locator(
        '.dropdown-menu.show a:has-text("Git versioning"), [role="menuitem"]:has-text("Git versioning")'
    ).first
    if not git.is_visible(timeout=2000):
        dismiss_modals(page)
        return
    git.click()
    time.sleep(2)
    save = page.locator(
        '.modal.show button:has-text("Save"), .modal.show button:has-text("Commit")'
    ).first
    if save.is_visible(timeout=3000):
        save.click()
        time.sleep(2)
    dismiss_modals(page)  # closes the lingering git dialog
    print("[git_save] committed")


def catalog_more_vert(page, asset_name):
    """Open the more_vert menu for a SPECIFIC asset on a catalog page.
    Catalog rows are NOT <tr> — they're divs — so we iterate every visible
    more_vert and match on the nearest container's text. Returns True on open."""
    btns = page.locator('button:has-text("more_vert")')
    for i in range(btns.count()):
        btn = btns.nth(i)
        if not btn.is_visible():
            continue
        text = btn.evaluate("el => el.closest('tr, div, li')?.textContent?.slice(0,80) || ''")
        if asset_name.lower() in (text or "").lower():
            btn.click()
            time.sleep(1)
            return True
    return False


def catalog_action(page, asset_name, action):
    """Run an editorial action from a catalog row's more_vert menu, descending
    into a 'More' submenu if needed. Common actions: 'Create version...',
    'Start review request', 'Request publication', 'Approve', 'Publish',
    'Export', 'Delete'. NOTE: editorial controls live on the CATALOG page, not
    inside the editor."""
    if not catalog_more_vert(page, asset_name):
        print(f"[catalog_action] '{asset_name}' not found")
        return False
    opt = page.locator(
        f'.dropdown-menu.show a:has-text("{action}"), [role="menuitem"]:has-text("{action}")'
    ).first
    if opt.is_visible(timeout=2000):
        opt.click()
        time.sleep(1.5)
    else:
        more_sub = page.locator('.dropdown-menu.show a:has-text("More")').first
        if not more_sub.is_visible(timeout=1000):
            dismiss_modals(page)
            print(f"[catalog_action] '{action}' not found for '{asset_name}'")
            return False
        more_sub.hover()
        time.sleep(1)
        opt = page.locator(f'.dropdown-menu.show a:has-text("{action}")').first
        if not opt.is_visible(timeout=2000):
            dismiss_modals(page)
            return False
        opt.click()
        time.sleep(1.5)
    confirm = page.locator(
        'button:has-text("Confirm"), button:has-text("Yes"), button:has-text("Proceed")'
    )
    if confirm.count() > 0 and confirm.first.is_visible(timeout=800):
        confirm.first.click()
        time.sleep(1)
    dismiss_modals(page)
    return True
