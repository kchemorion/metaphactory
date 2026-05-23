"""
metaphactory Playwright Automation Helpers (v2)

A battle-tested library for automating metaphactory UI tasks via Playwright.
Every pattern here was learned from round 1 failures against a live training instance.

Key lessons encoded:
- React forms need char-by-char typing (fill() skips React state updates)
- React Select dropdowns need force-click on the input container
- Vocabulary tree more_vert buttons are per-concept, never use .first globally
- Monaco editor (page templates) needs keyboard.type, not fill/insert
- CodeMirror (service configs) works via JS .setValue()
- networkidle timeouts are normal; wrap in try/except
"""

import os
import time
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCREENSHOT_DIR = "v2/screenshots"
SLOW = 0.3  # seconds between UI actions


# ---------------------------------------------------------------------------
# Login & Navigation
# ---------------------------------------------------------------------------

def login(page, base_url: str, username: str, password: str):
    """
    Log in to metaphactory.

    The login form uses standard HTML inputs — fill() works fine here.
    React form issues only apply to the ontology/vocabulary editors.
    """
    page.goto(f"{base_url}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(1)


def navigate(page, url: str, retries: int = 2):
    """
    Navigate to a URL with retry and session recovery.

    networkidle often times out on metaphactory — this is normal and the
    page is usually usable. We catch the timeout and continue.
    If the page redirects to login, we raise so the caller can re-login.
    """
    for attempt in range(retries + 1):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            # Try networkidle but don't fail if it times out
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass  # Page is usually usable even without networkidle
            time.sleep(SLOW)
            return
        except Exception as e:
            if attempt < retries:
                time.sleep(2)
                continue
            raise e


def safe_navigate(page, url: str):
    """Navigate without raising — logs errors but never throws."""
    try:
        navigate(page, url)
    except Exception as e:
        print(f"[safe_navigate] Failed to navigate to {url}: {e}")


def screenshot(page, name: str):
    """
    Take a screenshot with auto-created directory.

    Saves to SCREENSHOT_DIR/{name}.png. Creates the directory if missing.
    """
    Path(SCREENSHOT_DIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    page.screenshot(path=path, full_page=True)
    print(f"[screenshot] Saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Modal / Dropdown Cleanup
# ---------------------------------------------------------------------------

def dismiss_modals(page):
    """
    Aggressively close any open modals, dropdowns, or overlays.

    CRITICAL: Call this between multi-step UI actions. Leftover modals and
    dropdowns block subsequent clicks. This was the #1 source of flaky
    failures in round 1.
    """
    # Press Escape to close any focused modal/dropdown
    try:
        page.keyboard.press("Escape")
        time.sleep(0.2)
    except Exception:
        pass

    # Close modal backdrops via JS click
    try:
        page.evaluate("""
            document.querySelectorAll('.modal-backdrop, .modal.show .btn-close, .modal.show [data-dismiss="modal"]')
                .forEach(el => el.click());
        """)
    except Exception:
        pass

    # Close any React Select menus
    try:
        page.evaluate("""
            document.querySelectorAll('.Select__menu, [class*="menu-list"]')
                .forEach(el => el.remove());
        """)
    except Exception:
        pass

    # Close Bootstrap dropdowns
    try:
        page.evaluate("""
            document.querySelectorAll('.dropdown-menu.show')
                .forEach(el => el.classList.remove('show'));
        """)
    except Exception:
        pass

    time.sleep(0.2)


def dismiss_walkthrough(page):
    """
    Dismiss the Welcome carousel / walkthrough dialog.

    metaphactory shows a multi-step welcome overlay on first visit.
    We look for 'Skip' or close buttons to get past it.
    """
    try:
        skip = page.locator('button:has-text("Skip"), button:has-text("Got it"), button:has-text("Close")')
        if skip.count() > 0:
            skip.first.click()
            time.sleep(0.3)
    except Exception:
        pass

    # Also try the X button on walkthrough modals
    try:
        close_btn = page.locator('.walkthrough-close, .introjs-skipbutton, .modal-header .close, .btn-close')
        if close_btn.count() > 0:
            close_btn.first.click()
            time.sleep(0.3)
    except Exception:
        pass

    dismiss_modals(page)


# ---------------------------------------------------------------------------
# React Form Helpers
# ---------------------------------------------------------------------------

def react_type(locator, text: str, delay: int = 30):
    """
    Type text character-by-character into a React input.

    CRITICAL: Playwright's fill() does NOT trigger React's synthetic
    onChange events. The form state stays empty and buttons remain disabled.
    type() with a delay fires keydown/keypress/keyup per character, which
    React picks up correctly. 30ms delay is the sweet spot — faster can
    miss events, slower wastes time.
    """
    locator.type(text, delay=delay)


def react_select_pick(page, option_text: str, container=None):
    """
    Pick an option from a React Select dropdown.

    React Select renders a div that intercepts clicks on the actual <input>.
    We must force-click the .Select__input-container (or similar), wait
    for the menu to appear, then click the matching option.

    Args:
        page: Playwright page
        option_text: Exact text of the option to select
        container: Optional parent locator to scope the Select within
    """
    scope = container if container else page

    # Try multiple React Select container selectors
    select_selectors = [
        '.Select__input-container',
        '[class*="Select__input-container"]',
        '.css-1hwfws3',  # Common React Select class
        '[class*="indicatorContainer"]',
    ]

    clicked = False
    for sel in select_selectors:
        try:
            el = scope.locator(sel).first
            if el.count() > 0:
                el.click(force=True)
                clicked = True
                break
        except Exception:
            continue

    if not clicked:
        # Fallback: try clicking any select-like container
        try:
            scope.locator('[class*="Select"]').first.click(force=True)
        except Exception:
            raise RuntimeError("Could not find React Select container")

    time.sleep(0.5)

    # Click the option
    option = page.locator(f'[role="option"]:has-text("{option_text}")').first
    option.wait_for(timeout=5000)
    option.click()
    time.sleep(SLOW)


def unique_iri(base: str) -> str:
    """
    Generate a timestamp-based unique IRI to avoid conflicts.

    metaphactory disables the Create button when an IRI already exists.
    Appending a timestamp guarantees uniqueness across runs.
    """
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    # Strip trailing slash/hash, append timestamp
    base = base.rstrip("/#")
    return f"{base}_{ts}"


def create_asset_dialog(page, title: str, asset_type: str = None, description: str = None):
    """
    Fill the Create Asset dialog (used for ontologies, vocabularies, etc.).

    Handles IRI conflict detection: if the Create button is disabled with
    title 'already exists', the IRI is taken and we need to modify it.

    Args:
        page: Playwright page
        title: Asset title
        asset_type: Optional type to select from dropdown
        description: Optional description
    """
    time.sleep(SLOW)

    # Fill title — use react_type (char-by-char) to trigger React state updates.
    # NEVER call fill("") first — it breaks React form state and disables buttons.
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=5000)
    react_type(title_input, title)
    time.sleep(1)

    # Check if Create button is enabled (IRI conflict check)
    create_btn = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    time.sleep(1)

    if create_btn.get_attribute("disabled") is not None:
        # IRI conflict — uncheck Suggest IRI and use a unique one
        print(f"[create_asset_dialog] IRI conflict, generating unique IRI")
        suggest_testid = f"suggest-iri-{asset_type}" if asset_type else "suggest-iri-vocabulary"
        suggest_cb = page.locator(f'input[data-testid="{suggest_testid}"]').first
        if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
            suggest_cb.click()
            time.sleep(0.5)
        iri_input = page.locator(f'input[data-testid="{suggest_testid}-input"]').first
        if iri_input.is_visible(timeout=2000):
            base = f"https://vocabularies.metaphacts.com/{title.lower().replace(' ', '-')}"
            if asset_type == "ontology":
                base = f"https://ontologies.metaphacts.com/{title.lower().replace(' ', '-')}"
            react_type(iri_input, unique_iri(base) + "/0.1")
            time.sleep(0.5)

    # Wait for Create to become enabled and click
    for _ in range(30):
        if create_btn.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    create_btn.click()
    time.sleep(3)
    dismiss_walkthrough(page)
    return True


# ---------------------------------------------------------------------------
# Vocabulary Tree Helpers
# ---------------------------------------------------------------------------

def tree_click_concept(page, label: str):
    """
    Click a concept in the vocabulary tree, expanding parents if collapsed.

    Waits for the tree to render, finds the concept link, and clicks it.
    If the concept is inside a collapsed subtree, expands parent nodes first.
    """
    time.sleep(SLOW)

    # Wait for tree to be present
    page.wait_for_selector('.termTree, [class*="termTree"]', timeout=10000)

    # Find the concept link
    link = page.locator(f'.termTree a:has-text("{label}"), [class*="termTree"] a:has-text("{label}")').first
    link.wait_for(timeout=5000)

    # Check if visible; if not, try expanding parent nodes
    if not link.is_visible():
        # Try clicking expand toggles
        expanders = page.locator('.termTree .caret, .termTree [class*="expand"], .termTree .tree-toggle')
        count = expanders.count()
        for i in range(count):
            try:
                expanders.nth(i).click()
                time.sleep(0.3)
                if link.is_visible():
                    break
            except Exception:
                continue

    link.click()
    time.sleep(SLOW)


def tree_concept_menu(page, label: str):
    """
    Open the more_vert (three-dot) menu for a SPECIFIC concept in the tree.

    CRITICAL: Each concept has its OWN more_vert button inside its
    span.termTree__node. NEVER use page.locator('button:has-text("more_vert")').first
    — that grabs the first one on the page, which is often the WRONG concept.

    Instead, we find the concept's <a> link, navigate up to its containing
    span.termTree__node, then find the more_vert button within that scope.
    """
    time.sleep(SLOW)

    # Find the concept link in the tree
    link = page.locator(f'.termTree a:has-text("{label}"), [class*="termTree"] a:has-text("{label}")').first
    link.wait_for(timeout=5000)

    # Hover to reveal the more_vert button (some UIs show it on hover)
    link.hover()
    time.sleep(0.3)

    # Navigate to the parent termTree__node span, then find its more_vert button
    more_vert = link.locator(
        'xpath=ancestor::span[contains(@class,"termTree__node")]'
    ).locator('button:has-text("more_vert")')

    more_vert.wait_for(timeout=5000)
    more_vert.click()
    time.sleep(SLOW)


def create_top_concept(page, label: str, definition: str = ""):
    """
    Create a top-level concept in the current vocabulary.

    Uses the vocabulary-level 'Add top concept' button/menu, then fills
    the concept form with label and optional definition.
    """
    time.sleep(SLOW)

    # Look for "Add top concept" or similar button
    add_btn = page.locator(
        'button:has-text("Add top concept"), '
        'a:has-text("Add top concept"), '
        'button:has-text("Add Top Concept"), '
        '[data-testid="add-top-concept"]'
    ).first

    if add_btn.count() > 0:
        add_btn.click()
    else:
        # Try via the vocabulary-level more_vert menu
        vocab_menu = page.locator('.termTree button:has-text("more_vert"), button:has-text("add")').first
        if vocab_menu.count() > 0:
            vocab_menu.click()
            time.sleep(0.3)
            page.locator('[role="menuitem"]:has-text("Add top concept")').first.click()

    time.sleep(0.5)

    # Fill label — React form
    label_input = page.locator(
        'input[placeholder*="label"], input[placeholder*="Label"], '
        'input[name="label"], input[data-field="label"]'
    ).first
    label_input.wait_for(timeout=5000)
    label_input.click()
    label_input.fill("")
    react_type(label_input, label)

    # Fill definition if provided
    if definition:
        def_input = page.locator(
            'textarea[placeholder*="definition"], textarea[placeholder*="Definition"], '
            'textarea[name="definition"], input[placeholder*="definition"]'
        ).first
        if def_input.count() > 0:
            def_input.click()
            def_input.fill("")
            react_type(def_input, definition, delay=15)

    time.sleep(0.3)

    # Submit
    submit = page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first
    if submit.is_enabled():
        submit.click()
        time.sleep(1)

    dismiss_modals(page)


def create_narrower_concept(page, parent: str, child: str, definition: str = ""):
    """
    Create a narrower (child) concept under a parent concept.

    Opens the parent concept's more_vert menu, selects 'Add narrower concept',
    then fills the form.
    """
    # Open parent's context menu
    tree_concept_menu(page, parent)

    # Click 'Add narrower concept'
    page.locator(
        '[role="menuitem"]:has-text("Add narrower"), '
        'a:has-text("Add narrower"), '
        'button:has-text("Add narrower")'
    ).first.click()
    time.sleep(0.5)

    # Fill label
    label_input = page.locator(
        'input[placeholder*="label"], input[placeholder*="Label"], '
        'input[name="label"], input[data-field="label"]'
    ).first
    label_input.wait_for(timeout=5000)
    label_input.click()
    label_input.fill("")
    react_type(label_input, child)

    # Fill definition if provided
    if definition:
        def_input = page.locator(
            'textarea[placeholder*="definition"], textarea[placeholder*="Definition"], '
            'textarea[name="definition"], input[placeholder*="definition"]'
        ).first
        if def_input.count() > 0:
            def_input.click()
            def_input.fill("")
            react_type(def_input, definition, delay=15)

    time.sleep(0.3)

    # Submit
    submit = page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first
    if submit.is_enabled():
        submit.click()
        time.sleep(1)

    dismiss_modals(page)


def set_concept_status(page, label: str, status: str):
    """
    Set a concept's editorial status.

    CRITICAL: Status buttons are <button class="termSetStatusButton">,
    NOT <a> tags. Available statuses:
    - "In review"
    - "Ready for review"
    - "Accepted for publication"
    - "Request changes"

    First click the concept in the tree, then find and click the
    matching status button.
    """
    # Click the concept to select it
    tree_click_concept(page, label)
    time.sleep(0.5)

    # Find the status button matching the target status
    status_btn = page.locator(f'button.termSetStatusButton:has-text("{status}")').first
    status_btn.wait_for(timeout=5000)
    status_btn.click()
    time.sleep(1)

    # Confirm if a confirmation dialog appears
    confirm = page.locator('button:has-text("Confirm"), button:has-text("Yes"), button:has-text("OK")')
    if confirm.count() > 0:
        confirm.first.click()
        time.sleep(0.5)

    dismiss_modals(page)


# ---------------------------------------------------------------------------
# Ontology Editor Helpers
# ---------------------------------------------------------------------------

def switch_ontology_tab(page, tab: str):
    """
    Switch to a tab in the ontology editor (Classes, Attributes, Relations).

    Args:
        tab: One of 'Classes', 'Attributes', 'Relations', 'Graph'
    """
    tab_el = page.locator(f'.nav-tabs a:has-text("{tab}"), .nav-link:has-text("{tab}"), [role="tab"]:has-text("{tab}")').first
    tab_el.click()
    time.sleep(SLOW)


def create_ontology_class(page, name: str):
    """
    Create a new class in the ontology editor.

    Switches to the Classes tab, clicks Add, and fills the name.
    """
    switch_ontology_tab(page, "Classes")
    time.sleep(SLOW)

    # Click Add/Create button
    add_btn = page.locator(
        'button:has-text("Add class"), button:has-text("Create class"), '
        'button:has-text("Add"), [data-testid="add-class"]'
    ).first
    add_btn.click()
    time.sleep(0.5)

    # Fill name
    name_input = page.locator(
        'input[placeholder*="name"], input[placeholder*="Name"], '
        'input[placeholder*="label"], input[name="name"]'
    ).first
    name_input.wait_for(timeout=5000)
    name_input.click()
    name_input.fill("")
    react_type(name_input, name)

    # Submit
    submit = page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first
    time.sleep(0.3)
    if submit.is_enabled():
        submit.click()
        time.sleep(1)

    dismiss_modals(page)


def create_ontology_attribute(page, name: str):
    """
    Create a new attribute (datatype property) in the ontology editor.

    Switches to the Attributes tab, clicks Add, and fills the name.
    """
    switch_ontology_tab(page, "Attributes")
    time.sleep(SLOW)

    add_btn = page.locator(
        'button:has-text("Add attribute"), button:has-text("Create attribute"), '
        'button:has-text("Add"), [data-testid="add-attribute"]'
    ).first
    add_btn.click()
    time.sleep(0.5)

    name_input = page.locator(
        'input[placeholder*="name"], input[placeholder*="Name"], '
        'input[placeholder*="label"], input[name="name"]'
    ).first
    name_input.wait_for(timeout=5000)
    name_input.click()
    name_input.fill("")
    react_type(name_input, name)

    submit = page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first
    time.sleep(0.3)
    if submit.is_enabled():
        submit.click()
        time.sleep(1)

    dismiss_modals(page)


def create_ontology_relation(page, name: str):
    """
    Create a new relation (object property) in the ontology editor.

    Switches to the Relations tab, clicks Add, and fills the name.
    """
    switch_ontology_tab(page, "Relations")
    time.sleep(SLOW)

    add_btn = page.locator(
        'button:has-text("Add relation"), button:has-text("Create relation"), '
        'button:has-text("Add"), [data-testid="add-relation"]'
    ).first
    add_btn.click()
    time.sleep(0.5)

    name_input = page.locator(
        'input[placeholder*="name"], input[placeholder*="Name"], '
        'input[placeholder*="label"], input[name="name"]'
    ).first
    name_input.wait_for(timeout=5000)
    name_input.click()
    name_input.fill("")
    react_type(name_input, name)

    submit = page.locator('button:has-text("Create"), button:has-text("Save"), button[type="submit"]').first
    time.sleep(0.3)
    if submit.is_enabled():
        submit.click()
        time.sleep(1)

    dismiss_modals(page)


# ---------------------------------------------------------------------------
# Editor Helpers — CodeMirror & Monaco
# ---------------------------------------------------------------------------

def codemirror_set(page, content: str):
    """
    Set content in a CodeMirror editor via JavaScript.

    This works perfectly — CodeMirror exposes its instance on the DOM element.
    Used for: AI Services config dialogs, SPARQL editor, Turtle editor.
    """
    # Escape content for JS string
    escaped = content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
    page.evaluate(f"""
        const cm = document.querySelector('.CodeMirror');
        if (cm && cm.CodeMirror) {{
            cm.CodeMirror.setValue(`{escaped}`);
        }} else {{
            throw new Error('CodeMirror instance not found');
        }}
    """)
    time.sleep(SLOW)


def codemirror_get(page) -> str:
    """Get the current content from a CodeMirror editor."""
    return page.evaluate("""
        const cm = document.querySelector('.CodeMirror');
        if (cm && cm.CodeMirror) {
            return cm.CodeMirror.getValue();
        }
        throw new Error('CodeMirror instance not found');
    """)


def codemirror_replace(page, find: str, replace: str):
    """
    Find and replace text in a CodeMirror editor.

    Gets current content, does string replacement, sets it back.
    Useful for modifying existing configs without rewriting everything.
    """
    current = codemirror_get(page)
    updated = current.replace(find, replace)
    codemirror_set(page, updated)


def monaco_set_via_keyboard(page, content: str):
    """
    Set Monaco editor content via keyboard typing.

    CRITICAL: window.monaco is undefined in metaphactory's build. The usual
    monaco.editor.getModels() approach does NOT work. insert_text() and
    Playwright type() corrupt special characters like <, >, {, }.

    The only reliable method:
    1. Click the editor to focus it
    2. Select all existing content (Ctrl+A)
    3. Delete it
    4. Type new content via page.keyboard.type() with a small delay

    This works for short-to-medium content. For very long content (>5KB),
    consider breaking into chunks or using clipboard paste.
    """
    # Click the Monaco editor to focus it
    editor = page.locator('.monaco-editor .view-lines, .monaco-editor textarea').first
    editor.click()
    time.sleep(0.3)

    # Select all and delete
    mod_key = "Meta" if os.uname().sysname == "Darwin" else "Control"
    page.keyboard.press(f"{mod_key}+a")
    time.sleep(0.2)
    page.keyboard.press("Delete")
    time.sleep(0.2)

    # Type content character by character
    page.keyboard.type(content, delay=3)
    time.sleep(SLOW)


def sparql_update(page, base_url: str, query: str):
    """
    Run a SPARQL UPDATE query via the SPARQL editor page.

    Navigates to the SPARQL editor, sets the query in CodeMirror,
    and executes it.
    """
    navigate(page, f"{base_url}/sparql")
    time.sleep(1)
    dismiss_modals(page)

    # Set query in CodeMirror
    codemirror_set(page, query)
    time.sleep(0.5)

    # Click Execute / Run
    run_btn = page.locator(
        'button:has-text("Execute"), button:has-text("Run"), '
        'button[title="Execute"], button[title="Run query"]'
    ).first
    run_btn.click()
    time.sleep(2)


# ---------------------------------------------------------------------------
# Editorial Workflow Helpers
# ---------------------------------------------------------------------------

def git_save(page):
    """
    Save via Git versioning: More menu > Git versioning > Save, then close.

    CRITICAL: The Git versioning dialog stays open after save — you MUST
    explicitly close it or subsequent interactions will fail.
    """
    # Click the More menu button
    more_btn = page.locator(
        'button:has-text("More"), '
        '[data-testid="more-menu"], '
        'button:has-text("more_horiz")'
    ).first
    more_btn.click()
    time.sleep(0.5)

    # Click Git versioning
    git_item = page.locator(
        '[role="menuitem"]:has-text("Git versioning"), '
        'a:has-text("Git versioning"), '
        'button:has-text("Git versioning")'
    ).first
    git_item.click()
    time.sleep(1)

    # Click Save in the Git dialog
    save_btn = page.locator(
        '.modal button:has-text("Save"), '
        '[role="dialog"] button:has-text("Save"), '
        'button:has-text("Save to Git")'
    ).first
    save_btn.click()
    time.sleep(2)

    # CRITICAL: Close the Git dialog — it stays open after save
    close_btn = page.locator(
        '.modal button:has-text("Close"), '
        '[role="dialog"] button:has-text("Close"), '
        '.modal .btn-close, '
        '.modal button[aria-label="Close"]'
    ).first
    try:
        close_btn.click(timeout=3000)
    except Exception:
        # Try Escape as fallback
        page.keyboard.press("Escape")

    time.sleep(SLOW)
    dismiss_modals(page)


def catalog_more_vert(page, asset_name: str):
    """
    Click the more_vert (three-dot) menu for an asset on the catalog page.

    Editorial workflow controls (publish, approve, etc.) are on the
    Ontologies/Vocabularies CATALOG page — NOT inside the editor.
    Each row has its own more_vert button.
    """
    time.sleep(SLOW)

    # Find the row/card containing the asset name
    row = page.locator(f'tr:has-text("{asset_name}"), [class*="card"]:has-text("{asset_name}"), [class*="row"]:has-text("{asset_name}")').first
    row.wait_for(timeout=5000)

    # Click the more_vert button within that row
    menu_btn = row.locator('button:has-text("more_vert"), [aria-label="more"], button[class*="menu"]').first
    menu_btn.click()
    time.sleep(SLOW)


def catalog_action(page, asset_name: str, action: str):
    """
    Execute an action from the catalog page's more_vert menu.

    Handles both top-level menu items and items nested under a 'More' submenu.
    Common actions: 'Publish', 'Approve', 'Reject', 'Delete', 'Edit',
    'Request publication', 'More'.

    Args:
        page: Playwright page
        asset_name: Name of the asset in the catalog
        action: Action text to click (e.g. 'Publish', 'Approve')
    """
    # Open the asset's context menu
    catalog_more_vert(page, asset_name)

    # Try to click the action directly
    action_item = page.locator(
        f'[role="menuitem"]:has-text("{action}"), '
        f'.dropdown-item:has-text("{action}"), '
        f'a:has-text("{action}")'
    ).first

    if action_item.count() > 0 and action_item.is_visible():
        action_item.click()
        time.sleep(1)
    else:
        # Action might be under "More" submenu
        more_item = page.locator(
            '[role="menuitem"]:has-text("More"), '
            '.dropdown-item:has-text("More")'
        ).first

        if more_item.count() > 0:
            more_item.hover()
            time.sleep(0.5)

            # Now find the action in the submenu
            sub_action = page.locator(
                f'[role="menuitem"]:has-text("{action}"), '
                f'.dropdown-item:has-text("{action}")'
            ).first
            sub_action.click()
            time.sleep(1)
        else:
            raise RuntimeError(
                f"Action '{action}' not found in menu for '{asset_name}'"
            )

    # Handle confirmation dialogs
    confirm = page.locator(
        'button:has-text("Confirm"), button:has-text("Yes"), '
        'button:has-text("OK"), button:has-text("Proceed")'
    )
    if confirm.count() > 0:
        confirm.first.click()
        time.sleep(1)

    dismiss_modals(page)
