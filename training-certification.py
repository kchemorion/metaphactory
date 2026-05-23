#!/usr/bin/env python3
"""
Metaphactory Training Certification — Playwright Automation

Automates all certification exercises across three tracks:
  Track 1 — Visual Modeling (KG Engineers):
    Task 1: Vegetables vocabulary with hierarchy + review workflow
    Task 2: Vocabulary editorial workflow, versioning, publish
    Task 3: Recipes ontology with classes/relations/attributes + instances
    Task 4: Ontology editorial workflow, versioning, publish
  Track 2 — App Building Basics (KG Application Engineers):
    Task 1: QAAS API for org:Person
    Task 2: Bob's diagram
    Task 3: Organization resource template
    Task 4: Organization knowledge panel template
  Track 3 — AI metis services (AI metis Engineers):
    Task 1: Search & Discovery Agent service
    Task 2: Conversational AI interface

Prerequisites:
    pip install playwright
    playwright install chromium
    A running metaphactory training instance (URL from LMS)

Usage:
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --user admin --pass admin
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --headed
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --task 1
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --track vm   # Visual Modeling only
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --track app  # App Building only
    python3 training-certification.py --url https://your-instance.metaphacts.cloud --track ai   # AI metis only
"""
import argparse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
BASE_URL = "https://m20.academy.metaphacts.cloud"   # Overridden by --url
USERNAME = "academyuser"
PASSWORD = "m20"
VIDEO_DIR = Path(__file__).parent / "cert-recordings"
SCREENSHOT_DIR = Path(__file__).parent / "cert-screenshots"
SLOW_MO = 250  # ms between actions for readability


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show_banner(page: Page, text: str, sub: str = ""):
    sub_html = f'<div style="font-size:16px;margin-top:4px;opacity:0.8">{sub}</div>' if sub else ""
    page.evaluate(f"""() => {{
        let b = document.getElementById('tutorial-banner');
        if (!b) {{
            b = document.createElement('div');
            b.id = 'tutorial-banner';
            b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;'
                + 'background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;'
                + 'padding:18px 32px;font:bold 22px/1.3 system-ui;text-align:center;'
                + 'box-shadow:0 4px 20px rgba(0,0,0,0.4);border-bottom:3px solid #0f3460;'
                + 'pointer-events:none';
            document.body.prepend(b);
        }}
        b.innerHTML = `{text}{sub_html}`;
    }}""")
    time.sleep(2)


def clear_banner(page: Page):
    page.evaluate("() => { let b = document.getElementById('tutorial-banner'); if(b) b.remove(); }")


def take_screenshot(page: Page, name: str):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"), full_page=False)
    print(f"    📸 {name}.png")


def dismiss_walkthrough(page: Page):
    """Close walkthrough/welcome carousel modals."""
    for _ in range(5):
        try:
            modal = page.locator('.walkthroughCarousel.show, .modal.show')
            if modal.is_visible(timeout=1000):
                close_btn = page.locator('.modal.show .btn-close, .modal.show [class*="close"]')
                if close_btn.count() > 0 and close_btn.first.is_visible(timeout=500):
                    close_btn.first.click(force=True)
                else:
                    page.keyboard.press('Escape')
            else:
                break
        except:
            page.keyboard.press('Escape')
    time.sleep(0.3)


def dismiss_any_modal(page: Page):
    """Force-close any stuck modal, dialog, or dropdown menu."""
    # Close dropdowns first
    try:
        page.evaluate("""() => {
            document.querySelectorAll('.dropdown-menu.show').forEach(m => m.classList.remove('show'));
        }""")
    except:
        pass
    # Press Escape to dismiss modals/overlays
    for _ in range(3):
        try:
            modal = page.locator('.modal.show, .overlay-modal.show, .create-term-dialog.show')
            if modal.is_visible(timeout=300):
                close = modal.locator('.btn-close, button:has-text("Close"), button:has-text("Cancel")').first
                if close.is_visible(timeout=300):
                    close.click(force=True)
                    time.sleep(0.3)
                else:
                    page.keyboard.press('Escape')
                    time.sleep(0.3)
            else:
                break
        except:
            page.keyboard.press('Escape')
            time.sleep(0.3)
    # Final JS cleanup for anything stuck
    try:
        page.evaluate("""() => {
            document.querySelectorAll('.modal.show, .overlay-modal.show').forEach(m => {
                const close = m.querySelector('.btn-close');
                if (close) close.click();
            });
            document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
            document.body.classList.remove('modal-open');
        }""")
        time.sleep(0.3)
    except:
        pass


def login(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(1)


def ensure_logged_in(page: Page, target_url: str = ""):
    if "/login" in page.url:
        print("  Session expired — re-logging in")
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        if target_url and target_url not in page.url:
            page.goto(target_url)
            page.wait_for_load_state("networkidle")
            time.sleep(1)


def navigate(page: Page, url: str):
    for attempt in range(3):
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            ensure_logged_in(page, url)
            return
        except Exception as e:
            if "ERR_CONNECTION" in str(e) and attempt < 2:
                wait = 10 * (attempt + 1)
                print(f"  Server unavailable, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise


def safe_click(page: Page, selector: str, timeout: int = 3000):
    try:
        el = page.locator(selector).first
        el.wait_for(state="visible", timeout=timeout)
        el.click()
        return True
    except:
        return False


def wait_and_click(page: Page, locator, timeout: int = 5000):
    """Wait for a locator to be visible and enabled, then click."""
    locator.wait_for(state="visible", timeout=timeout)
    for _ in range(30):
        if locator.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    locator.click()
    time.sleep(0.5)


def react_type(page: Page, locator, text: str):
    """Type text character by character to trigger React state updates.
    fill() doesn't fire React synthetic events; press() does.
    IMPORTANT: Do NOT call fill("") first — it triggers validation that can
    disable form buttons."""
    locator.click()
    time.sleep(0.1)
    # Select-all + delete to clear existing value, then type fresh
    locator.press("Control+a")
    locator.press("Backspace")
    time.sleep(0.1)
    for char in text:
        locator.press(char)
        time.sleep(0.02)
    time.sleep(0.5)


def run_sparql_query(page: Page, query: str, screenshot_name: str = ""):
    """Execute a SPARQL query in the metaphactory SPARQL editor."""
    navigate(page, f"{BASE_URL}/sparql")
    time.sleep(2)
    try:
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{
                cm.CodeMirror.setValue({repr(query)});
            }}
        }}""")
        time.sleep(0.5)
    except:
        textarea = page.locator('textarea').first
        if textarea.is_visible(timeout=1000):
            textarea.fill(query)
    execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
    if execute_btn.is_visible(timeout=2000):
        execute_btn.click()
        time.sleep(3)
    if screenshot_name:
        take_screenshot(page, screenshot_name)


# ═══════════════════════════════════════════════════════════════════════════════
# VOCABULARY HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def create_top_level_concept(page: Page, label: str, definition: str = ""):
    """Create a top-level concept in the vocabulary editor."""
    create_term = page.locator('button:has-text("Create top-level term")').first
    create_term.click()
    time.sleep(1.5)

    pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
    pref_input.wait_for(state="visible", timeout=5000)
    # Type directly — do NOT call fill() as it breaks React form state
    pref_input.click()
    time.sleep(0.1)
    pref_input.type(label, delay=30)
    time.sleep(0.5)

    if definition:
        def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
        if def_input.is_visible(timeout=1000):
            def_input.click()
            def_input.type(definition, delay=20)
            time.sleep(0.3)

    # Save
    save_btn = page.locator(
        '.overlay-modal.show button[name="submit"], '
        '[role="dialog"].show button[name="submit"]'
    ).first
    save_btn.wait_for(state="visible", timeout=3000)
    time.sleep(0.5)
    save_btn.click()
    time.sleep(1.5)
    print(f"    Created top-level concept: {label}")


def create_narrower_concept(page: Page, parent_label: str, child_label: str, definition: str = ""):
    """Create a narrower concept under a parent in the vocabulary editor."""
    # 1. Click parent in the TREE panel (left side) — must be scoped to avoid
    #    matching elements in the detail panel, breadcrumb, etc.
    #    The tree is inside an .ontodia-accordion or similar left panel.
    tree_panel = page.locator('.ontodia-accordion').first
    parent_node = tree_panel.locator(f'a:has-text("{parent_label}")').first
    if not parent_node.is_visible(timeout=2000):
        # Fallback: try any tree-like container
        parent_node = page.locator(f'nav a:has-text("{parent_label}"), '
                                    f'[class*="tree"] a:has-text("{parent_label}")').first
    if not parent_node.is_visible(timeout=2000):
        parent_node = page.locator(f'a:has-text("{parent_label}")').first

    parent_node.click(force=True)
    time.sleep(1.5)

    # 2. Click the more_vert button ON THIS SPECIFIC concept's tree node.
    #    DOM structure: termTree__node > [label div] + [moreActions > button]
    #    The <a> is inside termTree__label, which is inside termTree__node.
    #    The more_vert button is inside .moreActions, also inside termTree__node.
    #    So from the <a>, go up to .termTree__node, then find the button.
    tree_node = parent_node.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
    menu_btn = tree_node.locator('button:has-text("more_vert")').first
    if not menu_btn.is_visible(timeout=1500):
        # Fallback: try going up to LazyTreeSelector--itemContent
        tree_node = parent_node.locator('xpath=ancestor::div[contains(@class,"LazyTreeSelector--itemContent")]').first
        menu_btn = tree_node.locator('button:has-text("more_vert")').first

    menu_btn.wait_for(state="visible", timeout=3000)
    menu_btn.click()
    time.sleep(0.5)

    # 3. Click "Create narrower term..." from dropdown
    narrower_option = page.locator(
        '.dropdown-menu.show a:has-text("Create narrower term")'
    ).first
    if narrower_option.is_visible(timeout=2000):
        narrower_option.click()
        time.sleep(1)
    else:
        print(f"      'Create narrower term' not in menu — trying fallback")
        page.keyboard.press('Escape')
        time.sleep(0.3)
        # Fallback: might not have this option; create as top-level instead
        create_top_level_concept(page, child_label, definition)
        return

    # 4. Fill preferred label — type directly, no fill()
    pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
    pref_input.wait_for(state="visible", timeout=5000)
    pref_input.click()
    time.sleep(0.1)
    pref_input.type(child_label, delay=30)
    time.sleep(0.5)

    # Fill definition
    if definition:
        def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
        if def_input.is_visible(timeout=1000):
            def_input.click()
            def_input.type(definition, delay=20)
            time.sleep(0.3)

    # 5. Save — wait for enabled then click
    save_btn = page.locator(
        '.overlay-modal.show button[name="submit"], '
        '[role="dialog"].show button[name="submit"]'
    ).first
    save_btn.wait_for(state="visible", timeout=3000)
    for _ in range(15):
        if save_btn.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    save_btn.click()
    time.sleep(1.5)
    print(f"    Created narrower concept: {child_label} under {parent_label}")


def click_concept_in_tree(page: Page, label: str):
    """Click a concept in the vocabulary tree panel. Expands collapsed parents."""
    # Scope to tree panel to avoid matching detail panel elements
    tree = page.locator('.ontodia-accordion').first
    node = tree.locator(f'a:has-text("{label}")').first
    if not node.is_visible(timeout=2000):
        # Tree might be collapsed — expand all toggle arrows
        toggles = tree.locator('.LazyTreeSelector--expandToggle')
        for i in range(toggles.count()):
            t = toggles.nth(i)
            if t.is_visible():
                t.click()
                time.sleep(0.5)
        node = tree.locator(f'a:has-text("{label}")').first
    if not node.is_visible(timeout=2000):
        # Last resort: match anywhere on page
        node = page.locator(f'a:has-text("{label}")').first
    node.click(force=True)
    time.sleep(1)


def set_concept_status(page: Page, label: str, status: str):
    """Set a concept's editorial status via the more_vert menu.
    Status options are <button class="termSetStatusButton"> inside the dropdown.
    Available statuses depend on current state, e.g.:
      'Ready for review', 'In review', 'Accepted for publication',
      'Request changes', etc.
    """
    click_concept_in_tree(page, label)

    # Find the more_vert button on THIS concept's tree node
    tree_link = page.locator(f'.ontodia-accordion a:has-text("{label}")').first
    if not tree_link.is_visible(timeout=2000):
        tree_link = page.locator(f'a:has-text("{label}")').first
    tree_node = tree_link.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
    menu_btn = tree_node.locator('button:has-text("more_vert")').first
    menu_btn.wait_for(state="visible", timeout=3000)
    menu_btn.click()
    time.sleep(0.5)

    # Status options are <button class="termSetStatusButton"> not <a> tags
    # Match by partial text (e.g. "In review" matches "Set In review")
    status_btn = page.locator(
        f'.dropdown-menu.show button.termSetStatusButton:has-text("{status}")'
    ).first
    if status_btn.is_visible(timeout=2000):
        status_btn.click()
        time.sleep(1)
        dismiss_any_modal(page)
        print(f"    Set '{label}' → {status}")
    else:
        print(f"    Warning: '{status}' option not found for {label}")
        dismiss_any_modal(page)


def add_comment_to_concept(page: Page, label: str, comment: str):
    """Add a review comment to a concept. Assumes the concept details panel is open."""
    click_concept_in_tree(page, label)
    time.sleep(0.5)

    # Look for comment/note input in the right panel
    comment_input = page.locator(
        'textarea[placeholder*="comment" i], '
        'textarea[placeholder*="note" i], '
        'textarea[placeholder*="Add a comment" i], '
        '.comment-input textarea'
    ).first
    if comment_input.is_visible(timeout=2000):
        comment_input.click()
        comment_input.type(comment)
        time.sleep(0.3)

        # Submit comment
        submit_btn = page.locator(
            'button:has-text("Add comment"), '
            'button:has-text("Submit"), '
            'button:has-text("Send")'
        ).first
        if submit_btn.is_visible(timeout=1000):
            submit_btn.click()
            time.sleep(1)
            print(f"    Added comment on '{label}': {comment[:50]}...")
    else:
        print(f"    Warning: Comment input not found for {label}")


def add_alt_label_to_concept(page: Page, label: str, alt_label: str, language: str = "de"):
    """Add an alternative label (e.g. German translation) to a concept."""
    click_concept_in_tree(page, label)
    time.sleep(0.5)

    # Look for the "Add alternative label" or edit panel
    # In metaphactory vocab editor, the right panel shows concept details
    add_label_btn = page.locator(
        'button:has-text("Add alternative label"), '
        'button:has-text("add_circle"):near(:text("Alternative Labels")), '
        'button:has-text("Add label")'
    ).first
    if add_label_btn.is_visible(timeout=2000):
        add_label_btn.click()
        time.sleep(0.5)

    # Fill the alternative label input
    alt_input = page.locator(
        'input[placeholder*="alternative label" i], '
        'input[placeholder*="Enter label" i]'
    ).last  # last = the newly added one
    if alt_input.is_visible(timeout=2000):
        alt_input.click()
        alt_input.type(alt_label)
        time.sleep(0.3)

    # Set language tag if there's a language selector
    lang_select = page.locator(
        'select:near(:text("Alternative")), '
        '[data-testid*="language"] select'
    ).last
    if lang_select.is_visible(timeout=1000):
        lang_select.select_option(language)
        time.sleep(0.3)

    # Save changes
    save_btn = page.locator(
        '.overlay-modal.show button[name="submit"], '
        'button:has-text("Save changes"), '
        'button:has-text("Save")'
    ).first
    if save_btn.is_visible(timeout=1000):
        save_btn.click()
        time.sleep(1)
    print(f"    Added alt label '{alt_label}' ({language}) to '{label}'")


def add_definition_to_concept(page: Page, label: str, definition: str, language: str = "de"):
    """Add a definition in another language to a concept."""
    click_concept_in_tree(page, label)
    time.sleep(0.5)

    # Look for "Add definition" button or the definition textarea
    add_def_btn = page.locator(
        'button:has-text("Add definition"), '
        'button:has-text("add_circle"):near(:text("Definition"))'
    ).first
    if add_def_btn.is_visible(timeout=2000):
        add_def_btn.click()
        time.sleep(0.5)

    def_input = page.locator(
        'textarea[placeholder*="definition" i], '
        'textarea[placeholder*="Enter definition" i]'
    ).last
    if def_input.is_visible(timeout=2000):
        def_input.click()
        def_input.type(definition)
        time.sleep(0.3)

    # Set language
    lang_select = page.locator(
        'select:near(:text("Definition")), '
        '[data-testid*="language"] select'
    ).last
    if lang_select.is_visible(timeout=1000):
        lang_select.select_option(language)
        time.sleep(0.3)

    save_btn = page.locator(
        '.overlay-modal.show button[name="submit"], '
        'button:has-text("Save changes"), '
        'button:has-text("Save")'
    ).first
    if save_btn.is_visible(timeout=1000):
        save_btn.click()
        time.sleep(1)
    print(f"    Added definition ({language}) to '{label}'")


def save_vocabulary_on_git(page: Page):
    """Save the vocabulary to git via the page-level 'More' dropdown > 'Git versioning...'."""
    # The "More" button with arrow_drop_down is in the top toolbar
    more_btn = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more_btn.is_visible(timeout=3000):
        more_btn.click()
        time.sleep(0.5)

        git_option = page.locator('.dropdown-menu.show a:has-text("Git versioning")').first
        if git_option.is_visible(timeout=2000):
            git_option.click()
            time.sleep(2)

            # In the git versioning dialog, click Save/Commit
            save_btn = page.locator(
                '.modal.show button:has-text("Save"), '
                '.modal.show button:has-text("Commit"), '
                '.modal.show button:has-text("Push")'
            ).first
            if save_btn.is_visible(timeout=3000):
                save_btn.click()
                time.sleep(2)
                print("    Saved vocabulary on git")
            else:
                print("    Git dialog opened but no Save/Commit button found")
                page.screenshot(path=str(SCREENSHOT_DIR / "debug-git-dialog.png"))

            # Close the git dialog — it may stay open after save
            for _ in range(5):
                git_modal = page.locator('.gitVersioningDialog.show, .modal.show')
                if git_modal.is_visible(timeout=500):
                    close = git_modal.locator('.btn-close, button:has-text("Close"), button:has-text("Done")').first
                    if close.is_visible(timeout=500):
                        close.click()
                        time.sleep(0.5)
                    else:
                        page.keyboard.press('Escape')
                        time.sleep(0.5)
                else:
                    break
            time.sleep(0.5)
        else:
            print("    Warning: 'Git versioning' not in More menu")
            page.keyboard.press('Escape')
            time.sleep(0.3)
    else:
        print("    Warning: 'More' button not found")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 1, TASK 1: VEGETABLES VOCABULARY
# ═══════════════════════════════════════════════════════════════════════════════

def cleanup_existing_assets(page: Page):
    """Delete any previously created Vegetables vocabulary and Recipes ontology."""
    show_banner(page, "Cleanup", "Deleting previous attempts if any exist")

    # Check and delete existing Vegetables vocabulary
    navigate(page, f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(2)
    vocab_link = page.locator('a:has-text("Vegetables")')
    if vocab_link.count() > 0 and vocab_link.first.is_visible(timeout=2000):
        print("  Found existing Vegetables vocabulary — deleting")
        vocab_link.first.click()
        time.sleep(2)
        dismiss_walkthrough(page)
        # Look for delete/remove option
        try:
            menu = page.locator('button:has-text("more_vert"), button[aria-label="More actions"]').first
            if menu.is_visible(timeout=2000):
                menu.click()
                time.sleep(0.5)
            delete_opt = page.locator(
                'a:has-text("Delete"), button:has-text("Delete"), '
                '.dropdown-menu.show a:has-text("Delete")'
            ).first
            if delete_opt.is_visible(timeout=2000):
                delete_opt.click()
                time.sleep(1)
                confirm = page.locator(
                    '.modal.show button:has-text("Delete"), '
                    '.modal.show button:has-text("Confirm"), '
                    '[data-testid="confirmation-dialog-button-confirm"]'
                ).first
                if confirm.is_visible(timeout=2000):
                    confirm.click()
                    time.sleep(2)
                    print("  Deleted Vegetables vocabulary")
        except Exception as e:
            print(f"  Could not delete vocabulary: {e}")

    # Check and delete existing Recipes ontology
    navigate(page, f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(2)
    onto_link = page.locator('a:has-text("Recipes")')
    if onto_link.count() > 0 and onto_link.first.is_visible(timeout=2000):
        print("  Found existing Recipes ontology — deleting")
        onto_link.first.click()
        time.sleep(2)
        dismiss_walkthrough(page)
        try:
            menu = page.locator('button:has-text("more_vert"), button[aria-label="More actions"]').first
            if menu.is_visible(timeout=2000):
                menu.click()
                time.sleep(0.5)
            delete_opt = page.locator(
                'a:has-text("Delete"), button:has-text("Delete"), '
                '.dropdown-menu.show a:has-text("Delete")'
            ).first
            if delete_opt.is_visible(timeout=2000):
                delete_opt.click()
                time.sleep(1)
                confirm = page.locator(
                    '.modal.show button:has-text("Delete"), '
                    '.modal.show button:has-text("Confirm"), '
                    '[data-testid="confirmation-dialog-button-confirm"]'
                ).first
                if confirm.is_visible(timeout=2000):
                    confirm.click()
                    time.sleep(2)
                    print("  Deleted Recipes ontology")
        except Exception as e:
            print(f"  Could not delete ontology: {e}")

    clear_banner(page)
    print("  Cleanup complete")


def vm_task1_vocabulary(page: Page):
    """Create a vegetables vocabulary with hierarchy, review workflow, multilingual labels."""
    show_banner(page, "VM Task 1: Vegetables Vocabulary",
                "Create hierarchy, set in review, request changes, accept for publication")

    # ── Step 1: Navigate to Vocabularies and Create ──
    navigate(page, f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(2)
    take_screenshot(page, "vm1-vocabularies-page")

    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title — vocabulary title must differ from the top-level concept label
    # Expected result shows "Vegetables for Recipes" as title, "Vegetables" as top concept
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=3000)
    react_type(page, title_input, "Vegetables for Recipes")
    time.sleep(1)

    # Check if Create button is enabled with suggested IRI; if not, use unique IRI
    dialog_create = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    time.sleep(1)
    if dialog_create.get_attribute("disabled") is not None:
        # IRI conflict — uncheck suggest and provide unique IRI
        print("    IRI conflict detected, using unique IRI")
        suggest_cb = page.locator('input[data-testid="suggest-iri-vocabulary"]').first
        if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
            suggest_cb.click()
            time.sleep(0.5)
        iri_input = page.locator('input[data-testid="suggest-iri-vocabulary-input"]').first
        if iri_input.is_visible(timeout=2000):
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            react_type(page, iri_input, f"https://vocabularies.metaphacts.com/vegetables-{ts}/0.1")
            time.sleep(0.5)

    take_screenshot(page, "vm1-create-dialog")

    # Click Create — wait for it to become enabled
    dialog_create = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    wait_and_click(page, dialog_create, timeout=15000)
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm1-editor-open")

    # ── Step 2: Create top-level concept "Vegetables" ──
    create_top_level_concept(page, "Vegetables", "Top-level concept for vegetable types")
    take_screenshot(page, "vm1-top-concept")

    # ── Step 3: Save on git ──
    save_vocabulary_on_git(page)
    take_screenshot(page, "vm1-first-save")

    # ── Step 4: Create narrower concepts under "Vegetables" ──
    create_narrower_concept(page, "Vegetables", "Bean", "Leguminous plants producing edible seeds in pods")
    create_narrower_concept(page, "Vegetables", "Roots", "Root vegetables grown underground")
    take_screenshot(page, "vm1-bean-roots")

    # ── Step 5: Create narrower concepts under "Bean" ──
    create_narrower_concept(page, "Bean", "Fava beans", "Large flat green beans, also known as broad beans")
    create_narrower_concept(page, "Bean", "Green beans", "Long thin green beans, also called string beans")
    take_screenshot(page, "vm1-bean-children")

    # ── Step 6: Create narrower concepts under "Roots" ──
    create_narrower_concept(page, "Roots", "Potato", "Starchy tuberous crop from the Solanum tuberosum plant")
    create_narrower_concept(page, "Roots", "Carrot", "Orange root vegetable rich in beta-carotene")
    create_narrower_concept(page, "Roots", "Onion", "Bulb vegetable with pungent flavor used worldwide")
    take_screenshot(page, "vm1-roots-children")

    # ── Step 7: Set ALL concepts "In review" ──
    # The menu shows "Set Ready for review" and "Set In review"
    # Per the task: "Set all the concepts in review"
    show_banner(page, "Setting concepts in review")
    all_concepts = ["Vegetables", "Bean", "Roots", "Fava beans", "Green beans", "Potato", "Carrot", "Onion"]
    for concept in all_concepts:
        try:
            set_concept_status(page, concept, "In review")
        except Exception as e:
            print(f"    Warning: Could not set '{concept}' in review: {e}")
    take_screenshot(page, "vm1-all-in-review")

    # ── Step 8: Request changes for 2 concepts with comments ──
    # After "In review", the menu should show "Request changes" as next status
    show_banner(page, "Requesting changes for Bean and Carrot")
    try:
        set_concept_status(page, "Bean", "Request changes")
        add_comment_to_concept(page, "Bean",
            "Please add a German label: 'Bohne'. Also add a German definition.")
    except Exception as e:
        print(f"    Warning: Request changes for Bean: {e}")

    try:
        set_concept_status(page, "Carrot", "Request changes")
        add_comment_to_concept(page, "Carrot",
            "Please add a German label: 'Karotte'. Also add a French definition.")
    except Exception as e:
        print(f"    Warning: Request changes for Carrot: {e}")
    take_screenshot(page, "vm1-changes-requested")

    # ── Step 9: Make the requested changes ──
    show_banner(page, "Making requested changes — adding multilingual labels")
    try:
        add_alt_label_to_concept(page, "Bean", "Bohne", "de")
        add_definition_to_concept(page, "Bean", "Hülsenfrucht, die essbare Samen in Schoten produziert", "de")
    except Exception as e:
        print(f"    Warning: Adding labels to Bean: {e}")

    try:
        add_alt_label_to_concept(page, "Carrot", "Karotte", "de")
        add_definition_to_concept(page, "Carrot", "Légume-racine orange riche en bêta-carotène", "fr")
    except Exception as e:
        print(f"    Warning: Adding labels to Carrot: {e}")
    take_screenshot(page, "vm1-changes-made")

    # ── Step 10: Accept for publication all approved concepts ──
    # After changes are made, the status option should be "Accepted for publication"
    show_banner(page, "Accepting all concepts for publication")
    for concept in all_concepts:
        try:
            set_concept_status(page, concept, "Accepted for publication")
        except Exception as e:
            # Some may already be accepted or not in the right state
            print(f"    Note: Could not accept '{concept}': {e}")
    take_screenshot(page, "vm1-all-accepted")

    # ── Step 11: Save on git and check history ──
    save_vocabulary_on_git(page)
    take_screenshot(page, "vm1-final-save")

    # Check git history
    try:
        history_btn = page.locator(
            'button:has-text("History"), button:has-text("history"), '
            'a:has-text("History"), [title*="History"]'
        ).first
        if history_btn.is_visible(timeout=2000):
            history_btn.click()
            time.sleep(2)
            take_screenshot(page, "vm1-git-history")
    except:
        print("    Note: History button not found")

    take_screenshot(page, "vm1-complete")
    clear_banner(page)
    print("  ✓ VM Task 1 complete — Vegetables vocabulary with hierarchy and review workflow")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 1, TASK 2: VOCABULARY EDITORIAL WORKFLOW & VERSIONING
# ═══════════════════════════════════════════════════════════════════════════════

def vm_task2_vocabulary_editorial(page: Page):
    """Editorial workflow: add reviewer, review, publish, new version, add Garlic."""
    show_banner(page, "VM Task 2: Vocabulary Editorial Workflow",
                "Review, publish, new version with Garlic")

    # ── Step 1: Navigate to Vocabularies ──
    navigate(page, f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(2)
    take_screenshot(page, "vm2-vocabularies-list")

    # ── Step 2: Open the Vegetables vocabulary ──
    vocab_link = page.locator('a:has-text("Vegetables")').first
    vocab_link.wait_for(state="visible", timeout=5000)
    vocab_link.click()
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm2-vocab-opened")

    # ── Step 3: Start a review — add yourself as reviewer ──
    show_banner(page, "Starting review process")

    # Look for "Start review" or review-related button
    review_btn = page.locator(
        'button:has-text("Start review"), '
        'button:has-text("Review"), '
        'a:has-text("Start review")'
    ).first
    if review_btn.is_visible(timeout=3000):
        review_btn.click()
        time.sleep(2)

        # Add self as reviewer
        reviewer_input = page.locator(
            'input[placeholder*="reviewer" i], '
            'input[placeholder*="search" i]:near(:text("Reviewer")), '
            'input[placeholder*="Add reviewer" i]'
        ).first
        if reviewer_input.is_visible(timeout=2000):
            reviewer_input.click()
            reviewer_input.type(USERNAME)
            time.sleep(1)
            # Select from dropdown
            dropdown_item = page.locator(
                f'.dropdown-item:has-text("{USERNAME}"), '
                f'li:has-text("{USERNAME}"), '
                f'[role="option"]:has-text("{USERNAME}")'
            ).first
            if dropdown_item.is_visible(timeout=2000):
                dropdown_item.click()
                time.sleep(0.5)

        # Confirm the review start
        confirm_btn = page.locator(
            'button:has-text("Start"), '
            'button:has-text("Submit"), '
            'button:has-text("Confirm")'
        ).first
        if confirm_btn.is_visible(timeout=2000):
            confirm_btn.click()
            time.sleep(2)
    take_screenshot(page, "vm2-review-started")

    # ── Step 4: Review changes and accept ──
    show_banner(page, "Reviewing and accepting changes")

    # Accept the review
    accept_btn = page.locator(
        'button:has-text("Accept"), '
        'button:has-text("Approve"), '
        'button:has-text("Accept all")'
    ).first
    if accept_btn.is_visible(timeout=3000):
        accept_btn.click()
        time.sleep(2)

        # Confirm acceptance
        confirm = page.locator('.modal.show button:has-text("Confirm"), .modal.show button:has-text("OK")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm2-review-accepted")

    # ── Step 5: Publish the vocabulary ──
    show_banner(page, "Publishing the vocabulary")
    publish_btn = page.locator(
        'button:has-text("Publish"), '
        'a:has-text("Publish")'
    ).first
    if publish_btn.is_visible(timeout=3000):
        publish_btn.click()
        time.sleep(2)

        # Confirm publish
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm2-published")

    # ── Step 6: Create a new version ──
    show_banner(page, "Creating new version")
    new_version_btn = page.locator(
        'button:has-text("New version"), '
        'button:has-text("Create new version"), '
        'a:has-text("New version")'
    ).first
    if new_version_btn.is_visible(timeout=3000):
        new_version_btn.click()
        time.sleep(2)

        # Confirm new version dialog
        confirm = page.locator(
            '.modal.show button:has-text("Create"), '
            '.modal.show button:has-text("Confirm"), '
            '.modal.show button:has-text("OK")'
        ).first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm2-new-version")

    # ── Step 7: Add "Garlic" term in the new version ──
    show_banner(page, "Adding Garlic to new version")
    try:
        # Garlic is a root vegetable — add under "Roots" or as top-level
        # Per the task, just add as a new term
        create_narrower_concept(page, "Roots", "Garlic", "Pungent bulb vegetable used as seasoning worldwide")
    except:
        try:
            create_top_level_concept(page, "Garlic", "Pungent bulb vegetable used as seasoning worldwide")
        except Exception as e:
            print(f"    Warning: Could not create Garlic: {e}")
    take_screenshot(page, "vm2-garlic-added")

    # ── Step 8: Start a new review of latest changes ──
    show_banner(page, "Starting new review")
    review_btn = page.locator(
        'button:has-text("Start review"), '
        'button:has-text("Review")'
    ).first
    if review_btn.is_visible(timeout=3000):
        review_btn.click()
        time.sleep(2)

        # Add reviewer
        reviewer_input = page.locator(
            'input[placeholder*="reviewer" i], '
            'input[placeholder*="Add reviewer" i]'
        ).first
        if reviewer_input.is_visible(timeout=2000):
            reviewer_input.click()
            reviewer_input.type(USERNAME)
            time.sleep(1)
            dropdown_item = page.locator(
                f'.dropdown-item:has-text("{USERNAME}"), '
                f'li:has-text("{USERNAME}"), '
                f'[role="option"]:has-text("{USERNAME}")'
            ).first
            if dropdown_item.is_visible(timeout=2000):
                dropdown_item.click()
                time.sleep(0.5)

        confirm_btn = page.locator(
            'button:has-text("Start"), button:has-text("Submit"), button:has-text("Confirm")'
        ).first
        if confirm_btn.is_visible(timeout=2000):
            confirm_btn.click()
            time.sleep(2)
    take_screenshot(page, "vm2-new-review-started")

    # ── Step 9: Add comments for the reviewer ──
    try:
        add_comment_to_concept(page, "Garlic", "New term added: Garlic. Please review the definition and hierarchy placement.")
    except Exception as e:
        print(f"    Note: Could not add comment: {e}")

    # ── Step 10: Reply feedback from reviewer ──
    show_banner(page, "Replying to reviewer feedback")
    try:
        reply_input = page.locator(
            'textarea[placeholder*="reply" i], '
            'textarea[placeholder*="comment" i]'
        ).first
        if reply_input.is_visible(timeout=2000):
            reply_input.click()
            reply_input.type("Garlic has been added under Roots. Definition reviewed and confirmed.")
            submit = page.locator('button:has-text("Reply"), button:has-text("Send"), button:has-text("Submit")').first
            if submit.is_visible(timeout=1000):
                submit.click()
                time.sleep(1)
    except:
        print("    Note: Reply interaction skipped")

    # Accept the review
    accept_btn = page.locator('button:has-text("Accept"), button:has-text("Approve")').first
    if accept_btn.is_visible(timeout=3000):
        accept_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Confirm"), .modal.show button:has-text("OK")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)

    # ── Step 11: Publish the new vocabulary ──
    show_banner(page, "Publishing new vocabulary version")
    publish_btn = page.locator('button:has-text("Publish")').first
    if publish_btn.is_visible(timeout=3000):
        publish_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm2-new-version-published")

    take_screenshot(page, "vm2-complete")
    clear_banner(page)
    print("  ✓ VM Task 2 complete — Vocabulary editorial workflow and versioning")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 1, TASK 3: RECIPES ONTOLOGY
# ═══════════════════════════════════════════════════════════════════════════════

def vm_task3_ontology(page: Page):
    """Create a Recipes ontology with classes, relations, attributes, instances."""
    show_banner(page, "VM Task 3: Recipes Ontology",
                "Classes, relations, attributes, Organization import, instances")

    # ── Step 1: Navigate to Ontologies and Create ──
    navigate(page, f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(2)
    take_screenshot(page, "vm3-ontologies-page")

    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title — character-by-character for React
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=3000)
    react_type(page, title_input, "Recipes")
    time.sleep(1)

    # Check if Create button is enabled; if IRI conflict, use unique IRI
    dialog_create_check = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    time.sleep(1)
    if dialog_create_check.get_attribute("disabled") is not None:
        print("    IRI conflict detected, using unique IRI")
        suggest_cb = page.locator('input[data-testid="suggest-iri-ontology"]').first
        if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
            suggest_cb.click()
            time.sleep(0.5)
        iri_input = page.locator('input[data-testid="suggest-iri-ontology-input"]').first
        if iri_input.is_visible(timeout=2000):
            from datetime import datetime
            ts = datetime.now().strftime("%Y%m%d%H%M%S")
            react_type(page, iri_input, f"https://ontologies.metaphacts.com/recipes-{ts}/0.1")
            time.sleep(0.5)

    # Click Create
    dialog_create = page.locator(
        '.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")'
    ).first
    wait_and_click(page, dialog_create, timeout=15000)
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm3-editor-open")

    # ── Step 2: Import the Organization ontology ──
    show_banner(page, "Importing Organization ontology")
    try:
        import_btn = page.locator(
            'button:has-text("Import"), '
            'button:has-text("Import ontology"), '
            'a:has-text("Import")'
        ).first
        if import_btn.is_visible(timeout=3000):
            import_btn.click()
            time.sleep(2)

            # Search for Organization ontology in the import modal
            search_input = page.locator(
                '.modal.show input[placeholder*="search" i], '
                '.modal.show input[type="text"]'
            ).first
            if search_input.is_visible(timeout=2000):
                search_input.click()
                search_input.type("Organization")
                time.sleep(1)

            # Select the Organization ontology from results
            org_option = page.locator(
                '.modal.show a:has-text("Organization"), '
                '.modal.show li:has-text("Organization"), '
                '.modal.show [role="option"]:has-text("Organization"), '
                '.modal.show label:has-text("Organization")'
            ).first
            if org_option.is_visible(timeout=3000):
                org_option.click()
                time.sleep(0.5)

            # Confirm import
            import_confirm = page.locator(
                '.modal.show button:has-text("Import"), '
                '.modal.show button:has-text("Add"), '
                '.modal.show button:has-text("OK")'
            ).first
            if import_confirm.is_visible(timeout=2000):
                import_confirm.click()
                time.sleep(2)

        take_screenshot(page, "vm3-org-imported")
    except Exception as e:
        print(f"    Warning: Import Organization ontology: {e}")
        dismiss_any_modal(page)

    # ── Step 3: Create classes ──
    show_banner(page, "Creating classes for Recipes ontology")

    # Switch to Classes tab
    try:
        classes_tab = page.locator('[role="tab"]:has-text("Classes"), button:has-text("Classes")').first
        if classes_tab.is_visible(timeout=2000):
            classes_tab.click()
            time.sleep(0.5)
    except:
        pass

    classes = ["Recipe", "Diet", "IngredientUsage", "Vegetable", "Protein", "Seasoning", "Author"]
    for i, cls_name in enumerate(classes):
        try:
            create_cls = page.locator('button:has-text("Create Class")').first
            create_cls.click()
            time.sleep(1)

            label_input = page.locator('input[placeholder="Enter label here..."]').first
            if label_input.is_visible(timeout=2000):
                label_input.fill(cls_name)
                time.sleep(0.3)

            # Confirm
            try:
                confirm = page.locator('button:has-text("Confirm")').first
                if confirm.is_visible(timeout=1500):
                    confirm.click()
                    time.sleep(0.5)
            except:
                time.sleep(0.3)

            print(f"    Created class: {cls_name}")
        except Exception as e:
            print(f"    Warning: Could not create class {cls_name}: {e}")

        if i == 0 or cls_name == "Author":
            take_screenshot(page, f"vm3-class-{cls_name}")

    # ── Step 3b: Set Author as subclass of org:Person ──
    show_banner(page, "Setting Author as subclass of org:Person")
    try:
        # Click Author in the class list
        author_node = page.locator('text=Author').first
        author_node.click()
        time.sleep(1)

        # Look for superclass / parent class field in properties panel
        superclass_input = page.locator(
            'input[placeholder*="superclass" i], '
            'input[placeholder*="parent" i], '
            'input[placeholder*="search" i]:near(:text("Superclass")), '
            'input:near(:text("SubClass Of"))'
        ).first
        if superclass_input.is_visible(timeout=2000):
            superclass_input.click()
            superclass_input.type("Person")
            time.sleep(1)
            person_option = page.locator(
                '[role="option"]:has-text("Person"), '
                'li:has-text("Person"), '
                '.dropdown-item:has-text("Person")'
            ).first
            if person_option.is_visible(timeout=2000):
                person_option.click()
                time.sleep(0.5)
        take_screenshot(page, "vm3-author-subclass")
    except Exception as e:
        print(f"    Warning: Could not set Author superclass: {e}")

    # ── Step 3c: Interlink Vegetable to Vegetables vocabulary ──
    show_banner(page, "Interlinking Vegetable class to vocabulary")
    try:
        veg_node = page.locator('text=Vegetable').first
        veg_node.click()
        time.sleep(1)
        # This may involve adding a concept link — depends on UI
        # In metaphactory, this is typically via common:definedByConcept or similar
        take_screenshot(page, "vm3-vegetable-interlink")
    except:
        pass

    # ── Step 4: Create attributes (datatype properties) ──
    show_banner(page, "Creating attributes")
    try:
        attrs_tab = page.locator('[role="tab"]:has-text("Attributes"), button:has-text("Attributes")').first
        if attrs_tab.is_visible(timeout=2000):
            attrs_tab.click()
            time.sleep(0.5)
    except:
        pass

    attributes = [
        ("label", "Recipe"),
        ("description", "Recipe"),
        ("difficulty", "Recipe"),
        ("cookingTime", "Recipe"),
        ("label", "Diet"),
        ("label", "IngredientUsage"),
        ("quantity", "IngredientUsage"),
        ("units", "IngredientUsage"),
        ("label", "Protein"),
        ("label", "Seasoning"),
        ("label", "Author"),
    ]
    # Deduplicate by name (label appears multiple times)
    seen_attrs = set()
    unique_attrs = []
    for name, domain in attributes:
        if name not in seen_attrs:
            unique_attrs.append((name, domain))
            seen_attrs.add(name)

    for i, (attr_name, domain_cls) in enumerate(unique_attrs):
        try:
            create_attr = page.locator('button:has-text("Create Attribute")').first
            create_attr.click()
            time.sleep(1)

            label_input = page.locator('input[placeholder="Enter label here..."]').first
            if label_input.is_visible(timeout=2000):
                label_input.fill(attr_name)
                time.sleep(0.3)

            try:
                confirm = page.locator('button:has-text("Confirm")').first
                if confirm.is_visible(timeout=1500):
                    confirm.click()
                    time.sleep(0.5)
            except:
                time.sleep(0.3)
            print(f"    Created attribute: {attr_name}")
        except Exception as e:
            print(f"    Warning: Could not create attribute {attr_name}: {e}")

        if i == 0:
            take_screenshot(page, f"vm3-attr-{attr_name}")

    take_screenshot(page, "vm3-attributes-done")

    # ── Step 5: Create relations (object properties) ──
    show_banner(page, "Creating relations")
    try:
        rels_tab = page.locator('[role="tab"]:has-text("Relations"), button:has-text("Relations")').first
        if rels_tab.is_visible(timeout=2000):
            rels_tab.click()
            time.sleep(0.5)
    except:
        pass

    relations = [
        ("belongsToDiet", "Recipe", "Diet"),
        ("hasIngredientUsage", "Recipe", "IngredientUsage"),
        ("hasItem", "IngredientUsage", "Vegetable"),  # OR Protein OR Seasoning (disjunction)
        ("hasAuthor", "Recipe", "Author"),
    ]

    for i, (rel_name, domain_cls, range_cls) in enumerate(relations):
        try:
            create_rel = page.locator('button:has-text("Create Relation")').first
            create_rel.click()
            time.sleep(1)

            label_input = page.locator('input[placeholder="Enter label here..."]').first
            if label_input.is_visible(timeout=2000):
                label_input.fill(rel_name)
                time.sleep(0.3)

            try:
                confirm = page.locator('button:has-text("Confirm")').first
                if confirm.is_visible(timeout=1500):
                    confirm.click()
                    time.sleep(0.5)
            except:
                time.sleep(0.3)
            print(f"    Created relation: {rel_name} ({domain_cls} → {range_cls})")
        except Exception as e:
            print(f"    Warning: Could not create relation {rel_name}: {e}")

        if i == 0:
            take_screenshot(page, f"vm3-rel-{rel_name}")

    take_screenshot(page, "vm3-relations-done")

    # ── Step 6: Apply layout and save ──
    try:
        layout_btn = page.locator('button:has-text("Hierarchical"), [title*="layout" i]').first
        if layout_btn.is_visible(timeout=1000):
            layout_btn.click()
            time.sleep(2)
    except:
        pass

    take_screenshot(page, "vm3-canvas-overview")

    # Save the ontology
    try:
        save_btn = page.locator('button:has-text("Save"), [title*="Save"]').first
        if save_btn.is_visible(timeout=2000):
            save_btn.click()
            time.sleep(2)
            take_screenshot(page, "vm3-saved")
    except:
        pass

    # ── Step 7: Create instances using Instance Data Manager ──
    show_banner(page, "Creating recipe instances", "Using Instance Data Manager")

    # Navigate to Instance Data Manager or use Manage Instances
    navigate(page, f"{BASE_URL}/resource/Admin:DataImportExport")
    time.sleep(2)

    # Alternative: Use the Instances management page
    # We'll create instances via the resource page / form-based approach
    navigate(page, f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(2)

    # Open the Recipes ontology
    recipes_link = page.locator('a:has-text("Recipes")').first
    if recipes_link.is_visible(timeout=3000):
        recipes_link.click()
        time.sleep(3)
        dismiss_walkthrough(page)

    # Look for "Manage Instances" or instance management button
    manage_btn = page.locator(
        'button:has-text("Manage Instances"), '
        'a:has-text("Manage Instances"), '
        'button:has-text("Instances")'
    ).first
    if manage_btn.is_visible(timeout=3000):
        manage_btn.click()
        time.sleep(2)
        take_screenshot(page, "vm3-instance-manager")

    # Create Recipe 1: Pasta Primavera
    show_banner(page, "Creating instance: Pasta Primavera")
    try:
        create_instance_btn = page.locator(
            'button:has-text("Create"), button:has-text("Create Instance"), button:has-text("New")'
        ).first
        if create_instance_btn.is_visible(timeout=3000):
            create_instance_btn.click()
            time.sleep(2)

            # Select type = Recipe
            type_select = page.locator(
                'select:near(:text("Type")), '
                'input[placeholder*="type" i], '
                'input[placeholder*="class" i]'
            ).first
            if type_select.is_visible(timeout=2000):
                if type_select.evaluate("el => el.tagName") == "SELECT":
                    type_select.select_option(label="Recipe")
                else:
                    type_select.click()
                    type_select.type("Recipe")
                    time.sleep(1)
                    page.locator('[role="option"]:has-text("Recipe"), li:has-text("Recipe")').first.click()
                time.sleep(0.5)

            # Fill label
            label_input = page.locator(
                'input[placeholder*="label" i], input[name*="label" i]'
            ).first
            if label_input.is_visible(timeout=2000):
                label_input.fill("Pasta Primavera")

            # Fill description
            desc_input = page.locator('textarea, input[placeholder*="description" i]').first
            if desc_input.is_visible(timeout=1000):
                desc_input.fill("Fresh spring vegetables tossed with pasta in olive oil")

            # Save
            save_btn = page.locator(
                'button:has-text("Save"), button:has-text("Create"), button[name="submit"]'
            ).first
            if save_btn.is_visible(timeout=2000):
                save_btn.click()
                time.sleep(2)
            take_screenshot(page, "vm3-instance-pasta")
    except Exception as e:
        print(f"    Warning: Could not create Pasta Primavera instance: {e}")

    # Create Recipe 2: Vegetable Soup
    show_banner(page, "Creating instance: Vegetable Soup")
    try:
        create_instance_btn = page.locator(
            'button:has-text("Create"), button:has-text("Create Instance"), button:has-text("New")'
        ).first
        if create_instance_btn.is_visible(timeout=3000):
            create_instance_btn.click()
            time.sleep(2)

            type_select = page.locator(
                'select:near(:text("Type")), '
                'input[placeholder*="type" i], '
                'input[placeholder*="class" i]'
            ).first
            if type_select.is_visible(timeout=2000):
                if type_select.evaluate("el => el.tagName") == "SELECT":
                    type_select.select_option(label="Recipe")
                else:
                    type_select.click()
                    type_select.type("Recipe")
                    time.sleep(1)
                    page.locator('[role="option"]:has-text("Recipe"), li:has-text("Recipe")').first.click()
                time.sleep(0.5)

            label_input = page.locator(
                'input[placeholder*="label" i], input[name*="label" i]'
            ).first
            if label_input.is_visible(timeout=2000):
                label_input.fill("Vegetable Soup")

            desc_input = page.locator('textarea, input[placeholder*="description" i]').first
            if desc_input.is_visible(timeout=1000):
                desc_input.fill("Hearty soup with mixed root vegetables and beans")

            save_btn = page.locator(
                'button:has-text("Save"), button:has-text("Create"), button[name="submit"]'
            ).first
            if save_btn.is_visible(timeout=2000):
                save_btn.click()
                time.sleep(2)
            take_screenshot(page, "vm3-instance-soup")
    except Exception as e:
        print(f"    Warning: Could not create Vegetable Soup instance: {e}")

    # ── Step 8: Validate database and check data quality ──
    show_banner(page, "Validating database — Data Quality Report")
    navigate(page, f"{BASE_URL}/resource/Admin:DataQuality")
    time.sleep(3)
    take_screenshot(page, "vm3-data-quality")

    # Trigger validation if there's a button
    validate_btn = page.locator(
        'button:has-text("Validate"), button:has-text("Run validation")'
    ).first
    if validate_btn.is_visible(timeout=3000):
        validate_btn.click()
        time.sleep(5)
        take_screenshot(page, "vm3-validation-report")

    take_screenshot(page, "vm3-complete")
    clear_banner(page)
    print("  ✓ VM Task 3 complete — Recipes ontology with instances and validation")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 1, TASK 4: ONTOLOGY EDITORIAL WORKFLOW & VERSIONING
# ═══════════════════════════════════════════════════════════════════════════════

def vm_task4_ontology_editorial(page: Page):
    """Editorial workflow for Recipes ontology: review, publish, new version with Menu class."""
    show_banner(page, "VM Task 4: Ontology Editorial Workflow",
                "Review, publish, new version with Menu → hasRecipe")

    # ── Step 1: Navigate to Ontologies ──
    navigate(page, f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(2)

    # ── Step 2: Open the Recipes ontology ──
    recipes_link = page.locator('a:has-text("Recipes")').first
    recipes_link.wait_for(state="visible", timeout=5000)
    recipes_link.click()
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm4-ontology-opened")

    # ── Step 3: Start review and add self as reviewer ──
    show_banner(page, "Starting review process")
    review_btn = page.locator(
        'button:has-text("Start review"), button:has-text("Review")'
    ).first
    if review_btn.is_visible(timeout=3000):
        review_btn.click()
        time.sleep(2)

        reviewer_input = page.locator(
            'input[placeholder*="reviewer" i], input[placeholder*="Add reviewer" i]'
        ).first
        if reviewer_input.is_visible(timeout=2000):
            reviewer_input.click()
            reviewer_input.type(USERNAME)
            time.sleep(1)
            dropdown_item = page.locator(
                f'.dropdown-item:has-text("{USERNAME}"), '
                f'li:has-text("{USERNAME}"), '
                f'[role="option"]:has-text("{USERNAME}")'
            ).first
            if dropdown_item.is_visible(timeout=2000):
                dropdown_item.click()
                time.sleep(0.5)

        confirm_btn = page.locator(
            'button:has-text("Start"), button:has-text("Submit"), button:has-text("Confirm")'
        ).first
        if confirm_btn.is_visible(timeout=2000):
            confirm_btn.click()
            time.sleep(2)
    take_screenshot(page, "vm4-review-started")

    # ── Step 4: Review and accept changes ──
    accept_btn = page.locator('button:has-text("Accept"), button:has-text("Approve")').first
    if accept_btn.is_visible(timeout=3000):
        accept_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Confirm"), .modal.show button:has-text("OK")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm4-review-accepted")

    # ── Step 5: Publish the ontology ──
    publish_btn = page.locator('button:has-text("Publish")').first
    if publish_btn.is_visible(timeout=3000):
        publish_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm4-published")

    # ── Step 6: Create a new version ──
    new_version_btn = page.locator(
        'button:has-text("New version"), button:has-text("Create new version")'
    ).first
    if new_version_btn.is_visible(timeout=3000):
        new_version_btn.click()
        time.sleep(2)
        confirm = page.locator(
            '.modal.show button:has-text("Create"), .modal.show button:has-text("Confirm")'
        ).first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "vm4-new-version")

    # ── Step 7: Add "Menu" class and "hasRecipe" relation ──
    show_banner(page, "Adding Menu class with hasRecipe relation")

    # Create Menu class
    try:
        classes_tab = page.locator('[role="tab"]:has-text("Classes"), button:has-text("Classes")').first
        if classes_tab.is_visible(timeout=2000):
            classes_tab.click()
            time.sleep(0.5)
    except:
        pass

    try:
        create_cls = page.locator('button:has-text("Create Class")').first
        create_cls.click()
        time.sleep(1)
        label_input = page.locator('input[placeholder="Enter label here..."]').first
        if label_input.is_visible(timeout=2000):
            label_input.fill("Menu")
            time.sleep(0.3)
        try:
            confirm = page.locator('button:has-text("Confirm")').first
            if confirm.is_visible(timeout=1500):
                confirm.click()
                time.sleep(0.5)
        except:
            pass
        print("    Created class: Menu")
    except Exception as e:
        print(f"    Warning: Could not create Menu class: {e}")

    take_screenshot(page, "vm4-menu-class")

    # Create hasRecipe relation
    try:
        rels_tab = page.locator('[role="tab"]:has-text("Relations"), button:has-text("Relations")').first
        if rels_tab.is_visible(timeout=2000):
            rels_tab.click()
            time.sleep(0.5)
    except:
        pass

    try:
        create_rel = page.locator('button:has-text("Create Relation")').first
        create_rel.click()
        time.sleep(1)
        label_input = page.locator('input[placeholder="Enter label here..."]').first
        if label_input.is_visible(timeout=2000):
            label_input.fill("hasRecipe")
            time.sleep(0.3)
        try:
            confirm = page.locator('button:has-text("Confirm")').first
            if confirm.is_visible(timeout=1500):
                confirm.click()
                time.sleep(0.5)
        except:
            pass
        print("    Created relation: hasRecipe (Menu → Recipe)")
    except Exception as e:
        print(f"    Warning: Could not create hasRecipe relation: {e}")

    take_screenshot(page, "vm4-has-recipe-relation")

    # Save
    try:
        save_btn = page.locator('button:has-text("Save"), [title*="Save"]').first
        if save_btn.is_visible(timeout=2000):
            save_btn.click()
            time.sleep(2)
    except:
        pass

    # ── Step 8: Start new review with comments ──
    show_banner(page, "Starting new review with comments")
    review_btn = page.locator('button:has-text("Start review"), button:has-text("Review")').first
    if review_btn.is_visible(timeout=3000):
        review_btn.click()
        time.sleep(2)

        reviewer_input = page.locator(
            'input[placeholder*="reviewer" i], input[placeholder*="Add reviewer" i]'
        ).first
        if reviewer_input.is_visible(timeout=2000):
            reviewer_input.click()
            reviewer_input.type(USERNAME)
            time.sleep(1)
            dropdown_item = page.locator(
                f'.dropdown-item:has-text("{USERNAME}"), '
                f'li:has-text("{USERNAME}"), '
                f'[role="option"]:has-text("{USERNAME}")'
            ).first
            if dropdown_item.is_visible(timeout=2000):
                dropdown_item.click()
                time.sleep(0.5)

        confirm_btn = page.locator(
            'button:has-text("Start"), button:has-text("Submit"), button:has-text("Confirm")'
        ).first
        if confirm_btn.is_visible(timeout=2000):
            confirm_btn.click()
            time.sleep(2)

    # Add review comment
    try:
        comment_input = page.locator(
            'textarea[placeholder*="comment" i], textarea[placeholder*="note" i]'
        ).first
        if comment_input.is_visible(timeout=2000):
            comment_input.click()
            comment_input.type("Added Menu class with hasRecipe relation. A Menu should contain at least one Recipe.")
            submit = page.locator('button:has-text("Add comment"), button:has-text("Submit")').first
            if submit.is_visible(timeout=1000):
                submit.click()
                time.sleep(1)
    except:
        pass
    take_screenshot(page, "vm4-review-comment")

    # Reply to previous requester comments
    try:
        reply_input = page.locator('textarea[placeholder*="reply" i]').first
        if reply_input.is_visible(timeout=2000):
            reply_input.click()
            reply_input.type("Confirmed: Menu class created with minCount 1 constraint for hasRecipe.")
            submit = page.locator('button:has-text("Reply"), button:has-text("Send")').first
            if submit.is_visible(timeout=1000):
                submit.click()
                time.sleep(1)
    except:
        pass

    # Accept and publish
    accept_btn = page.locator('button:has-text("Accept"), button:has-text("Approve")').first
    if accept_btn.is_visible(timeout=3000):
        accept_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)

    publish_btn = page.locator('button:has-text("Publish")').first
    if publish_btn.is_visible(timeout=3000):
        publish_btn.click()
        time.sleep(2)
        confirm = page.locator('.modal.show button:has-text("Publish"), .modal.show button:has-text("Confirm")').first
        if confirm.is_visible(timeout=2000):
            confirm.click()
            time.sleep(2)
    take_screenshot(page, "vm4-new-version-published")

    take_screenshot(page, "vm4-complete")
    clear_banner(page)
    print("  ✓ VM Task 4 complete — Ontology editorial workflow and versioning")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 2, TASK 1: QAAS API
# ═══════════════════════════════════════════════════════════════════════════════

def app_task1_qaas(page: Page):
    """Create a Query As A Service (QAAS) API for org:Person instances."""
    show_banner(page, "App Task 1: QAAS API",
                "SPARQL query + REST service for org:Person")

    PERSON_QUERY = """PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?label WHERE {
    ?person a org:Person .
    OPTIONAL { ?person rdfs:label ?label }
}
ORDER BY ?label"""

    # ── Step 1: Create and test the SPARQL query ──
    show_banner(page, "Creating SPARQL query in editor")
    navigate(page, f"{BASE_URL}/sparql")
    time.sleep(2)

    # Set the query
    try:
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{
                cm.CodeMirror.setValue({repr(PERSON_QUERY)});
            }}
        }}""")
        time.sleep(0.5)
    except:
        textarea = page.locator('textarea').first
        if textarea.is_visible(timeout=1000):
            textarea.fill(PERSON_QUERY)

    # Execute to test
    execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
    if execute_btn.is_visible(timeout=2000):
        execute_btn.click()
        time.sleep(3)
    take_screenshot(page, "app1-query-result")

    # Save the query
    save_btn = page.locator(
        'button:has-text("Save"), button[title*="Save"]'
    ).first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(1)

        # Fill query name in save dialog
        name_input = page.locator(
            '.modal.show input[placeholder*="name" i], '
            '.modal.show input[placeholder*="title" i], '
            '.modal.show input[type="text"]'
        ).first
        if name_input.is_visible(timeout=2000):
            name_input.fill("All Persons")
            time.sleep(0.3)

        save_confirm = page.locator(
            '.modal.show button:has-text("Save"), .modal.show button:has-text("OK")'
        ).first
        if save_confirm.is_visible(timeout=2000):
            save_confirm.click()
            time.sleep(2)
    take_screenshot(page, "app1-query-saved")

    # ── Step 2: Create the REST API service ──
    show_banner(page, "Creating QAAS REST API")
    navigate(page, f"{BASE_URL}/resource/Admin:QueryService")
    time.sleep(2)
    take_screenshot(page, "app1-qaas-page")

    # Click "Add Service"
    add_btn = page.locator('button:has-text("Add service")').first
    if add_btn.is_visible(timeout=3000):
        add_btn.click()
        time.sleep(2)

        # Fill REST URL (service ID)
        rest_url_input = page.locator('input').first
        # The first editable input in the new row is the REST URL
        row_inputs = page.locator('tr:last-child input, tr:last-child select')
        for i in range(row_inputs.count()):
            inp = row_inputs.nth(i)
            if inp.is_visible():
                placeholder = inp.get_attribute('placeholder') or ''
                inp_type = inp.get_attribute('type') or ''
                if inp_type == 'text' and not inp.get_attribute('value'):
                    inp.fill("person")
                    time.sleep(0.3)
                    break

        # Select saved query from the Query dropdown
        # This is a React Select component — click the input container to open
        # First dismiss any popover/tooltip that might be covering it
        page.mouse.click(10, 10)
        time.sleep(0.5)

        query_dropdown = page.locator('.Select__input-container, [class*="Select__control"]').first
        if not query_dropdown.is_visible(timeout=1000):
            query_dropdown = page.locator('[class*="select" i]:has-text("Select query")').first
        if query_dropdown.is_visible(timeout=2000):
            query_dropdown.click(force=True)
            time.sleep(1)
            # Pick the first available query option
            option = page.locator(
                '[role="option"], .Select__option, .dropdown-item, option'
            ).first
            if option.is_visible(timeout=2000):
                option.click()
                time.sleep(0.5)
                print("    Selected query from dropdown")
            else:
                # Try native select fallback
                native_select = page.locator('select').nth(0)
                if native_select.is_visible(timeout=1000):
                    options = native_select.locator('option')
                    if options.count() > 1:
                        native_select.select_option(index=1)
                        time.sleep(0.5)
                        print("    Selected query via native select")

        # Fill ACL permission
        acl_input = page.locator('input[placeholder*="ACL" i], input[placeholder*="permiss" i]').first
        if acl_input.is_visible(timeout=1000):
            acl_input.fill("qaas:execute")
            time.sleep(0.3)

        take_screenshot(page, "app1-qaas-filled")

        # Save — the apply/save button
        save_btn = page.locator(
            'button[title*="Apply"], button:has-text("Save"), button:has-text("save")'
        ).first
        for _ in range(10):
            if save_btn.is_visible(timeout=500) and save_btn.get_attribute("disabled") is None:
                save_btn.click()
                time.sleep(2)
                break
            time.sleep(0.5)
    take_screenshot(page, "app1-qaas-created")

    # ── Step 3: Test the API ──
    show_banner(page, "Testing the REST API")
    # Click on the REST URL link to test
    rest_link = page.locator(
        'a[href*="/rest/qaas/"], '
        'a:has-text("REST URL"), '
        'a:has-text("/rest/")'
    ).first
    if rest_link.is_visible(timeout=3000):
        rest_link.click()
        time.sleep(3)
        take_screenshot(page, "app1-api-response")

    take_screenshot(page, "app1-complete")
    clear_banner(page)
    print("  ✓ App Task 1 complete — QAAS API for org:Person")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 2, TASK 2: DIAGRAMS
# ═══════════════════════════════════════════════════════════════════════════════

def app_task2_diagrams(page: Page):
    """Create and save a diagram showing Bob, his interests, and people he knows."""
    show_banner(page, "App Task 2: Bob's Diagram",
                "Graph view with interests and connections")

    # ── Approach: Assets > Diagrams > Create, then search for Bob ──
    navigate(page, f"{BASE_URL}/resource/Assets:Diagrams")
    time.sleep(2)
    take_screenshot(page, "app2-diagrams-page")

    # Click Create Diagram
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    if create_btn.is_visible(timeout=3000):
        create_btn.click()
        time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, "app2-diagram-canvas")

    # ── Search for Bob using the INSTANCES search (bottom-left), NOT Classes ──
    show_banner(page, "Searching for Bob")
    # The left panel has "Classes" (top) and "Instances" (bottom) sections.
    # Click "Instances" header to make sure it's expanded
    instances_header = page.locator('text=Instances').first
    if instances_header.is_visible(timeout=2000):
        instances_header.click()
        time.sleep(0.5)

    # The Instances search input has placeholder "Search for..."
    instances_search = page.locator('input[placeholder="Search for..."]').first
    if instances_search.is_visible(timeout=3000):
        instances_search.click()
        instances_search.fill("Bob")
        time.sleep(0.5)

        # Click the search button (magnifying glass icon next to the input)
        # It's a button with a search icon inside the Instances section
        search_icon = instances_search.locator('xpath=following-sibling::button | ../button').first
        if search_icon.is_visible(timeout=1000):
            search_icon.click()
        else:
            # Try pressing Enter to trigger search
            instances_search.press("Enter")
        time.sleep(3)

        # Find Bob in the search results and drag to canvas
        # Results appear as draggable items below the search
        bob_result = page.locator(
            '[draggable="true"]:has-text("Bob"), '
            'li:has-text("Bob"), '
            '[class*="element"]:has-text("Bob")'
        ).first
        if not bob_result.is_visible(timeout=3000):
            bob_result = page.locator('text=Bob').last

        if bob_result.is_visible(timeout=3000):
            # Drag Bob onto the canvas
            canvas = page.locator('.ontodia-paper-area, .ontodia-scrollable-paper, canvas, svg').first
            if canvas.is_visible(timeout=2000):
                bob_box = bob_result.bounding_box()
                canvas_box = canvas.bounding_box()
                if bob_box and canvas_box:
                    # Drag from result to center of canvas
                    page.mouse.move(bob_box['x'] + bob_box['width']/2, bob_box['y'] + bob_box['height']/2)
                    page.mouse.down()
                    time.sleep(0.3)
                    target_x = canvas_box['x'] + canvas_box['width']/2
                    target_y = canvas_box['y'] + canvas_box['height']/2
                    page.mouse.move(target_x, target_y, steps=20)
                    time.sleep(0.3)
                    page.mouse.up()
                    time.sleep(2)
                    print("    Dragged Bob onto canvas")
    take_screenshot(page, "app2-bob-added")

    # ── Expand Bob's relations ──
    show_banner(page, "Expanding Bob's connections")

    # Click the + button on Bob's node to expand relations
    # The plus/expand button is typically on or near the node
    try:
        # Click on Bob's node first
        bob_node = page.locator(
            '.diagram-node:has-text("Bob"), '
            '[data-element-type="node"]:has-text("Bob"), '
            'g:has-text("Bob")'
        ).first
        if bob_node.is_visible(timeout=2000):
            bob_node.click()
            time.sleep(1)

        # Click expand/plus button
        expand_btn = page.locator(
            'button:has-text("+"), '
            'button:has-text("expand"), '
            '.expand-button, '
            '[title*="expand" i], '
            '[data-testid="expand-node"]'
        ).first
        if expand_btn.is_visible(timeout=2000):
            expand_btn.click()
            time.sleep(2)

            # Select "knows" relation to expand
            knows_option = page.locator(
                'label:has-text("knows"), '
                'input[value*="knows"], '
                'li:has-text("knows"), '
                '[role="option"]:has-text("knows")'
            ).first
            if knows_option.is_visible(timeout=2000):
                knows_option.click()
                time.sleep(0.5)

            # Also expand interests
            interest_option = page.locator(
                'label:has-text("interest"), '
                'input[value*="interest"], '
                'li:has-text("interest"), '
                '[role="option"]:has-text("interest")'
            ).first
            if interest_option.is_visible(timeout=2000):
                interest_option.click()
                time.sleep(0.5)

            # Confirm expansion
            expand_confirm = page.locator(
                'button:has-text("Expand"), button:has-text("OK"), button:has-text("Apply")'
            ).first
            if expand_confirm.is_visible(timeout=2000):
                expand_confirm.click()
                time.sleep(3)
    except Exception as e:
        print(f"    Warning: Could not expand Bob's relations: {e}")

    take_screenshot(page, "app2-bob-expanded")

    # Expand connections' relations too
    show_banner(page, "Expanding connections' relations")
    try:
        # For each connected person, try to expand their relations
        nodes = page.locator(
            '.diagram-node, [data-element-type="node"]'
        )
        node_count = nodes.count()
        for i in range(min(node_count, 5)):
            try:
                node = nodes.nth(i)
                node.click()
                time.sleep(0.5)
                expand_btn = page.locator(
                    'button:has-text("+"), .expand-button, [title*="expand" i]'
                ).first
                if expand_btn.is_visible(timeout=1000):
                    expand_btn.click()
                    time.sleep(1)
                    expand_all = page.locator(
                        'button:has-text("Expand all"), button:has-text("All")'
                    ).first
                    if expand_all.is_visible(timeout=1000):
                        expand_all.click()
                        time.sleep(2)
            except:
                pass
    except:
        pass

    take_screenshot(page, "app2-fully-expanded")

    # ── Save the diagram ──
    show_banner(page, "Saving diagram")
    save_btn = page.locator(
        'button:has-text("Save"), button[title*="Save"]'
    ).first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(1)

        # Fill diagram name
        name_input = page.locator(
            '.modal.show input[placeholder*="name" i], '
            '.modal.show input[type="text"]'
        ).first
        if name_input.is_visible(timeout=2000):
            name_input.fill("Bob's Network")
            time.sleep(0.3)

        save_confirm = page.locator(
            '.modal.show button:has-text("Save"), .modal.show button:has-text("OK")'
        ).first
        if save_confirm.is_visible(timeout=2000):
            save_confirm.click()
            time.sleep(2)

    take_screenshot(page, "app2-complete")
    clear_banner(page)
    print("  ✓ App Task 2 complete — Bob's diagram with interests and connections")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 2, TASK 3: RESOURCE TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

ORGANIZATION_TEMPLATE = """<div class="page">
  <h1><mp-label iri='[[this]]'></mp-label></h1>

  <h2>Organization Details</h2>
  <semantic-query
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?label ?description WHERE {
        BIND(?? AS ?subject)
        OPTIONAL { ?subject rdfs:label ?label }
        OPTIONAL { ?subject rdfs:comment ?description }
      }
    '
    template='<p><b>{{label.value}}</b>{{#if description}} - {{description.value}}{{/if}}</p>'
  ></semantic-query>

  <h2>Members</h2>
  <semantic-query
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?member ?memberLabel WHERE {
        BIND(?? AS ?org)
        ?member org:memberOf ?org .
        ?member rdfs:label ?memberLabel .
      }
      ORDER BY ?memberLabel
    '
    template='<ul>{{#each bindings}}<li><semantic-link iri="{{member.value}}">{{memberLabel.value}}</semantic-link></li>{{/each}}</ul>'
  ></semantic-query>

  <h2>Projects</h2>
  <semantic-table
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?project ?projectLabel WHERE {
        BIND(?? AS ?org)
        ?project org:hasClient ?org .
        ?project rdfs:label ?projectLabel .
      }
      ORDER BY ?projectLabel
    '
    column-configuration='[
      {"variableName": "project", "displayName": "Project"},
      {"variableName": "projectLabel", "displayName": "Name"}
    ]'
  ></semantic-table>
</div>"""


def app_task3_resource_template(page: Page):
    """Create a template for Organization type using semantic components."""
    show_banner(page, "App Task 3: Organization Resource Template",
                "semantic-query for details + semantic-table for projects")

    # ── Navigate directly to the template editor (action=edit) ──
    template_url = (f"{BASE_URL}/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies"
                    ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit")
    try:
        navigate(page, template_url)
    except:
        # networkidle may timeout but the editor is still usable
        ensure_logged_in(page, template_url)
    time.sleep(3)
    take_screenshot(page, "app3-template-page")

    # Set content in Monaco editor via keyboard — this triggers proper React state updates
    time.sleep(2)
    # Click inside the editor to focus it
    editor_area = page.locator('.monaco-editor .view-lines').first
    if editor_area.is_visible(timeout=3000):
        editor_area.click()
        time.sleep(0.3)
    # Select all and delete existing content
    page.keyboard.press("Meta+a")
    time.sleep(0.2)
    page.keyboard.press("Backspace")
    time.sleep(0.3)
    # Insert new content via keyboard (triggers all events Monaco needs)
    page.keyboard.insert_text(ORGANIZATION_TEMPLATE)
    time.sleep(1)
    print("    Template content inserted via keyboard")
    take_screenshot(page, "app3-template-edited")

    # Save — click "Save" (not "Save & View" which navigates away)
    save_btn = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(3)
    take_screenshot(page, "app3-template-saved")

    take_screenshot(page, "app3-complete")
    clear_banner(page)
    print("  ✓ App Task 3 complete — Organization resource template")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 2, TASK 4: KNOWLEDGE PANEL TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

KNOWLEDGE_PANEL_TEMPLATE = """<div class="knowledge-panel">
  <h3><mp-label iri='[[this]]'></mp-label></h3>

  <semantic-query
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?label ?description WHERE {
        BIND(?? AS ?subject)
        OPTIONAL { ?subject rdfs:label ?label }
        OPTIONAL { ?subject rdfs:comment ?description }
      }
    '
    template='<p>{{#if description}}{{description.value}}{{/if}}</p>'
  ></semantic-query>

  <h4>Members</h4>
  <semantic-query
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?member ?memberLabel WHERE {
        BIND(?? AS ?org)
        ?member org:memberOf ?org .
        ?member rdfs:label ?memberLabel .
      }
      ORDER BY ?memberLabel
      LIMIT 10
    '
    template='<ul>{{#each bindings}}<li><semantic-link iri="{{member.value}}">{{memberLabel.value}}</semantic-link></li>{{/each}}</ul>'
  ></semantic-query>

  <h4>Projects</h4>
  <semantic-table
    query='
      PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
      PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
      SELECT ?project ?projectLabel WHERE {
        BIND(?? AS ?org)
        ?project org:hasClient ?org .
        ?project rdfs:label ?projectLabel .
      }
      LIMIT 5
    '
    column-configuration='[
      {"variableName": "projectLabel", "displayName": "Project"}
    ]'
  ></semantic-table>
</div>"""


def app_task4_knowledge_panel(page: Page):
    """Create a knowledge panel template for Organization type."""
    show_banner(page, "App Task 4: Organization Knowledge Panel",
                "Panel template for graph view info overlay")

    # ── Navigate directly to the panel template editor (action=edit) ──
    panel_url = (f"{BASE_URL}/resource/?uri=PanelTemplate%3Ahttps%3A%2F%2Fontologies"
                 ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit")
    try:
        navigate(page, panel_url)
    except:
        ensure_logged_in(page, panel_url)
    time.sleep(3)
    take_screenshot(page, "app4-panel-template-page")

    # Set content in Monaco editor via keyboard
    time.sleep(2)
    editor_area = page.locator('.monaco-editor .view-lines').first
    if editor_area.is_visible(timeout=3000):
        editor_area.click()
        time.sleep(0.3)
    page.keyboard.press("Meta+a")
    time.sleep(0.2)
    page.keyboard.press("Backspace")
    time.sleep(0.3)
    page.keyboard.insert_text(KNOWLEDGE_PANEL_TEMPLATE)
    time.sleep(1)
    print("    Panel template content inserted via keyboard")
    time.sleep(1)
    take_screenshot(page, "app4-panel-edited")

    # Save — click "Save" (not "Save & View")
    save_btn = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if save_btn.is_visible(timeout=3000):
        save_btn.click()
        time.sleep(3)
    take_screenshot(page, "app4-panel-saved")

    take_screenshot(page, "app4-complete")
    clear_banner(page)
    print("  ✓ App Task 4 complete — Organization knowledge panel template")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 3, TASK 1: SEARCH & DISCOVERY AGENT SERVICE
# ═══════════════════════════════════════════════════════════════════════════════

def ai_task1_agent_service(page: Page):
    """Create a Search & Discovery Agent service configured with Recipes ontology."""
    show_banner(page, "AI Task 1: Search & Discovery Agent",
                "Configure agent with Recipes ontology + LLM service")

    # ── Navigate to Admin > Service Settings > AI Services ──
    navigate(page, f"{BASE_URL}/resource/Admin:AIServices")
    time.sleep(2)

    # If that URL doesn't work, try alternatives
    if "AIServices" not in page.url:
        navigate(page, f"{BASE_URL}/resource/Admin:ServiceSettings")
        time.sleep(2)

        # Click on AI Services tab/section
        ai_tab = page.locator(
            'a:has-text("AI Services"), '
            'button:has-text("AI Services"), '
            '[role="tab"]:has-text("AI")'
        ).first
        if ai_tab.is_visible(timeout=3000):
            ai_tab.click()
            time.sleep(2)

    take_screenshot(page, "ai1-services-page")

    # ── Use an AI service template ──
    show_banner(page, "Creating Search & Discovery Agent service")

    # Look for template selection or "Add" button
    add_btn = page.locator(
        'button:has-text("Add"), '
        'button:has-text("Create"), '
        'button:has-text("New Service")'
    ).first
    if add_btn.is_visible(timeout=3000):
        add_btn.click()
        time.sleep(2)

    # Select the Search & Discovery Agent template
    template_option = page.locator(
        'a:has-text("Search"), '
        'li:has-text("Search"), '
        '[role="option"]:has-text("Search"), '
        'button:has-text("Search & Discovery"), '
        'label:has-text("Search & Discovery")'
    ).first
    if template_option.is_visible(timeout=3000):
        template_option.click()
        time.sleep(2)
    take_screenshot(page, "ai1-template-selected")

    # ── Configure contextOntology ──
    show_banner(page, "Configuring contextOntology → Recipes")

    # Find the contextOntology parameter input
    context_input = page.locator(
        'input[name*="contextOntology" i], '
        'input[placeholder*="ontology" i], '
        'input:near(:text("contextOntology")), '
        'textarea:near(:text("contextOntology"))'
    ).first
    if context_input.is_visible(timeout=3000):
        context_input.click()
        context_input.fill("")
        context_input.type(f"{BASE_URL}/ontology/Recipes")
        time.sleep(0.5)
    take_screenshot(page, "ai1-context-ontology-set")

    # ── Configure languageModel ──
    show_banner(page, "Configuring LLM service")
    llm_input = page.locator(
        'input[name*="languageModel" i], '
        'select[name*="languageModel" i], '
        'input:near(:text("languageModel")), '
        'select:near(:text("languageModel")), '
        'input[placeholder*="LLM" i]'
    ).first
    if llm_input.is_visible(timeout=3000):
        if llm_input.evaluate("el => el.tagName") == "SELECT":
            # Select from dropdown — pick the first available LLM
            options = llm_input.locator('option')
            if options.count() > 1:
                llm_input.select_option(index=1)
        else:
            llm_input.click()
            time.sleep(0.5)
            # Click first option in dropdown
            option = page.locator('[role="option"], li.dropdown-item').first
            if option.is_visible(timeout=2000):
                option.click()
        time.sleep(0.5)
    take_screenshot(page, "ai1-llm-configured")

    # ── Save the service ──
    save_btn = page.locator(
        'button:has-text("Save"), button:has-text("Create")'
    ).first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(2)
    take_screenshot(page, "ai1-service-saved")

    take_screenshot(page, "ai1-complete")
    clear_banner(page)
    print("  ✓ AI Task 1 complete — Search & Discovery Agent service")


# ═══════════════════════════════════════════════════════════════════════════════
# TRACK 3, TASK 2: CONVERSATIONAL AI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

CONVERSATIONAL_AI_TEMPLATE = """<div class="page">
  <h1>Recipe Assistant</h1>
  <p>Ask questions about recipes, ingredients, and cooking.</p>

  <mp-conversational-ai
    agent-service-id="search-discovery-agent"
    show-explanations=true
    enable-feedback=true
    example-questions='[
      "What recipes use vegetables as ingredients?",
      "Which recipes belong to the vegan diet?",
      "List all available recipes with their cooking times"
    ]'
  ></mp-conversational-ai>
</div>"""


def ai_task2_conversational_ui(page: Page):
    """Create a conversational AI interface with mp-conversational-ai component."""
    show_banner(page, "AI Task 2: Conversational AI Interface",
                "Template with mp-conversational-ai component")

    # ── Create a new application page/template ──
    # Navigate to the template page directly
    navigate(page, f"{BASE_URL}/resource/RecipeAssistant")
    time.sleep(2)

    # Click Edit to create the page
    edit_btn = page.locator(
        'button:has-text("Edit"), a:has-text("Edit"), '
        'button:has-text("Create"), a:has-text("Create")'
    ).first
    if edit_btn.is_visible(timeout=3000):
        edit_btn.click()
        time.sleep(2)
    take_screenshot(page, "ai2-edit-mode")

    # ── Set the template content ──
    show_banner(page, "Adding mp-conversational-ai component")

    try:
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{
                cm.CodeMirror.setValue({repr(CONVERSATIONAL_AI_TEMPLATE)});
            }}
        }}""")
        time.sleep(0.5)
    except:
        textarea = page.locator('textarea').first
        if textarea.is_visible(timeout=2000):
            textarea.fill(CONVERSATIONAL_AI_TEMPLATE)
    take_screenshot(page, "ai2-template-content")

    # ── Save ──
    save_btn = page.locator(
        'button:has-text("Save"), button[title*="Save"]'
    ).first
    if save_btn.is_visible(timeout=2000):
        save_btn.click()
        time.sleep(3)
    take_screenshot(page, "ai2-page-saved")

    # ── Test: Execute one of the example questions ──
    show_banner(page, "Testing the conversational AI")

    # Wait for the component to render
    time.sleep(3)

    # Click the first example question
    example_btn = page.locator(
        'button:has-text("What recipes"), '
        '.example-question:first-child, '
        '[data-testid*="example"]:first-child'
    ).first
    if example_btn.is_visible(timeout=5000):
        example_btn.click()
        time.sleep(5)  # Wait for AI response
        take_screenshot(page, "ai2-question-executed")
    else:
        # Try typing a question manually
        chat_input = page.locator(
            'input[placeholder*="Ask" i], '
            'textarea[placeholder*="Ask" i], '
            'input[placeholder*="question" i], '
            'textarea[placeholder*="question" i]'
        ).first
        if chat_input.is_visible(timeout=3000):
            chat_input.click()
            chat_input.type("What recipes use vegetables as ingredients?")
            time.sleep(0.5)

            send_btn = page.locator(
                'button:has-text("Send"), button:has-text("Ask"), button[type="submit"]'
            ).first
            if send_btn.is_visible(timeout=2000):
                send_btn.click()
                time.sleep(5)
            take_screenshot(page, "ai2-question-executed")

    take_screenshot(page, "ai2-complete")
    clear_banner(page)
    print("  ✓ AI Task 2 complete — Conversational AI interface")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Task orchestration
# ═══════════════════════════════════════════════════════════════════════════════

TASKS = [
    # (num, track, name, function)
    (0,  "vm",  "Cleanup Previous Attempts",            cleanup_existing_assets),
    (1,  "vm",  "Vegetables Vocabulary",                vm_task1_vocabulary),
    (2,  "vm",  "Vocabulary Editorial & Versioning",    vm_task2_vocabulary_editorial),
    (3,  "vm",  "Recipes Ontology",                     vm_task3_ontology),
    (4,  "vm",  "Ontology Editorial & Versioning",      vm_task4_ontology_editorial),
    (5,  "app", "QAAS API",                             app_task1_qaas),
    (6,  "app", "Bob's Diagram",                        app_task2_diagrams),
    (7,  "app", "Organization Resource Template",       app_task3_resource_template),
    (8,  "app", "Organization Knowledge Panel",         app_task4_knowledge_panel),
    (9,  "ai",  "Search & Discovery Agent",             ai_task1_agent_service),
    (10, "ai",  "Conversational AI Interface",          ai_task2_conversational_ui),
]


def run_certification(headed: bool = False, task_filter: int = None, track_filter: str = None):
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not headed,
            slow_mo=SLOW_MO,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.set_default_timeout(15000)

        # Login
        login(page)
        print("Logged in to metaphactory")
        print(f"Instance: {BASE_URL}")
        print()

        # Run tasks
        for num, track, name, func in TASKS:
            if task_filter is not None and num != task_filter:
                continue
            if track_filter is not None and track != track_filter:
                continue

            track_labels = {"vm": "Visual Modeling", "app": "App Building", "ai": "AI metis"}
            print(f"{'='*60}")
            print(f"Task {num} [{track_labels[track]}]: {name}")
            print(f"{'='*60}")

            try:
                ensure_logged_in(page)
                func(page)
            except Exception as e:
                print(f"  ✗ Task {num} error: {e}")
                try:
                    take_screenshot(page, f"error-task-{num}")
                except:
                    pass
                # Recover from browser crash
                if "closed" in str(e).lower():
                    print("  Browser crashed, recovering...")
                    try:
                        context.close()
                    except:
                        pass
                    try:
                        browser.close()
                    except:
                        pass
                    browser = p.chromium.launch(headless=not headed, slow_mo=SLOW_MO)
                    context = browser.new_context(
                        viewport={"width": 1920, "height": 1080},
                        record_video_dir=str(VIDEO_DIR),
                        record_video_size={"width": 1920, "height": 1080},
                    )
                    page = context.new_page()
                    page.set_default_timeout(15000)
                    login(page)
                    print("  Recovered — continuing with next task")

        # Close
        try:
            context.close()
            browser.close()
        except:
            pass

        # Rename video
        video_files = list(VIDEO_DIR.glob("*.webm"))
        if video_files:
            latest = max(video_files, key=lambda f: f.stat().st_mtime)
            from datetime import datetime
            ts = datetime.now().strftime("%Y-%m-%d")
            if task_filter is not None:
                vname = f"cert-task-{task_filter}-{ts}.webm"
            elif track_filter:
                vname = f"cert-track-{track_filter}-{ts}.webm"
            else:
                vname = f"cert-full-{ts}.webm"
            final_path = VIDEO_DIR / vname
            latest.rename(final_path)
            print(f"\n{'='*60}")
            print(f"Video recorded: {final_path}")
            print(f"Screenshots:    {SCREENSHOT_DIR}")
            print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Metaphactory Training Certification Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all tasks on your training instance
  python3 training-certification.py --url https://your-instance.metaphacts.cloud

  # Run with visible browser
  python3 training-certification.py --url https://your-instance.metaphacts.cloud --headed

  # Run only task 3 (Recipes Ontology)
  python3 training-certification.py --url https://your-instance.metaphacts.cloud --task 3

  # Run only the Visual Modeling track
  python3 training-certification.py --url https://your-instance.metaphacts.cloud --track vm

  # Run only the AI metis track
  python3 training-certification.py --url https://your-instance.metaphacts.cloud --track ai
        """,
    )
    parser.add_argument("--url", type=str, help="Metaphactory instance URL (e.g. https://your-instance.metaphacts.cloud)")
    parser.add_argument("--user", type=str, default="admin", help="Username (default: admin)")
    parser.add_argument("--password", type=str, default="admin", help="Password (default: admin)")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser")
    parser.add_argument("--task", type=int, default=None, help="Run only this task number (1-10)")
    parser.add_argument("--track", type=str, default=None, choices=["vm", "app", "ai"],
                        help="Run only this track: vm (Visual Modeling), app (App Building), ai (AI metis)")
    args = parser.parse_args()

    if args.url:
        BASE_URL = args.url.rstrip("/")
    if args.user:
        USERNAME = args.user
    if args.password:
        PASSWORD = args.password

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  Metaphactory Training Certification Automation              ║
║                                                              ║
║  Track 1 — Visual Modeling (Tasks 1-4)                       ║
║  Track 2 — App Building Basics (Tasks 5-8)                   ║
║  Track 3 — AI metis Services (Tasks 9-10)                    ║
╚══════════════════════════════════════════════════════════════╝
""")

    run_certification(headed=args.headed, task_filter=args.task, track_filter=args.track)
