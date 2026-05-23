# Metaphactory Training Automation v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reliable Playwright automation library and runner that completes all 10 metaphactory certification tasks on any training instance.

**Architecture:** Split into a reusable helpers library (`mf_helpers.py`) containing battle-tested selectors/patterns from round 1, and a task runner (`mf_tasks.py`) with one function per certification task. A CLI runner (`run.py`) orchestrates execution with error recovery.

**Tech Stack:** Python 3, Playwright, headless Chromium

---

## File Structure

| File | Responsibility |
|------|---------------|
| `mf_helpers.py` | Core library: login, navigation, React form helpers, Monaco/CodeMirror editor helpers, vocabulary tree helpers, ontology editor helpers, editorial workflow helpers, modal/dropdown cleanup |
| `mf_tasks.py` | 10 task functions (one per certification task), each self-contained |
| `mf_templates.py` | Template HTML strings for Tasks 7, 8, and 10 (Organization template, Panel template, Conversational AI) |
| `run.py` | CLI runner with argparse: `--task N`, `--track vm|app|ai`, `--headed`, `--url`, `--user`, `--pass` |
| `tests/test_helpers.py` | Unit tests for helper functions (selector builders, IRI generation) |

All files in `/Users/kiptengwer/Documents/metaphactory-tutorial/v2/`.

---

### Task 1: Create the helpers library (`mf_helpers.py`)

**Files:**
- Create: `v2/mf_helpers.py`

- [ ] **Step 1: Write login and navigation helpers**

```python
# v2/mf_helpers.py
"""Metaphactory Playwright automation helpers.
Battle-tested patterns from round 1 automation."""

import time
from datetime import datetime
from playwright.sync_api import Page

SCREENSHOT_DIR = "v2/screenshots"
SLOW = 0.3  # seconds between actions


def login(page: Page, base_url: str, username: str, password: str):
    """Login to metaphactory. Works with both admin and academyuser."""
    page.goto(f"{base_url}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(1)


def navigate(page: Page, url: str):
    """Navigate with retry and session recovery. Handles networkidle timeout."""
    for attempt in range(3):
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            if "/login" in page.url:
                print("  Session expired, re-logging in")
                page.fill('input[name="username"]', "admin")
                page.fill('input[name="password"]', "admin")
                page.click('input[type="submit"]')
                page.wait_for_load_state("networkidle")
                time.sleep(1)
                page.goto(url)
                page.wait_for_load_state("networkidle")
            return
        except Exception as e:
            if attempt < 2:
                time.sleep(5)
            else:
                # networkidle timeout is OK — page is usually usable
                if "/login" in page.url:
                    raise
                return


def safe_navigate(page: Page, url: str):
    """Navigate but never raise — absorbs networkidle timeouts."""
    try:
        navigate(page, url)
    except:
        pass
    time.sleep(2)


def screenshot(page: Page, name: str):
    """Take a screenshot with auto-created directory."""
    import os
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    page.screenshot(path=f"{SCREENSHOT_DIR}/{name}.png")
    print(f"    screenshot: {name}.png")
```

- [ ] **Step 2: Write modal/dropdown cleanup helpers**

```python
# Append to v2/mf_helpers.py

def dismiss_modals(page: Page):
    """Force-close any stuck modal, dialog, or dropdown menu.
    MUST be called between multi-step UI interactions."""
    # Close dropdowns via JS
    try:
        page.evaluate("""() => {
            document.querySelectorAll('.dropdown-menu.show')
                .forEach(m => m.classList.remove('show'));
        }""")
    except:
        pass
    # Close modals via close button or Escape
    for _ in range(3):
        try:
            modal = page.locator('.modal.show, .overlay-modal.show, .create-term-dialog.show')
            if modal.is_visible(timeout=300):
                close = modal.locator('.btn-close, button:has-text("Close"), button:has-text("Cancel")').first
                if close.is_visible(timeout=300):
                    close.click(force=True)
                else:
                    page.keyboard.press('Escape')
                time.sleep(SLOW)
            else:
                break
        except:
            page.keyboard.press('Escape')
            time.sleep(SLOW)
    # Final JS cleanup
    try:
        page.evaluate("""() => {
            document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
            document.body.classList.remove('modal-open');
        }""")
    except:
        pass


def dismiss_walkthrough(page: Page):
    """Close the Welcome walkthrough carousel if it appears."""
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
        except:
            page.keyboard.press('Escape')
    time.sleep(SLOW)
```

- [ ] **Step 3: Write React form helpers**

```python
# Append to v2/mf_helpers.py

def react_type(locator, text: str, delay: int = 30):
    """Type text character-by-character to trigger React state updates.
    fill() does NOT fire React synthetic events. type() with delay does."""
    locator.click()
    time.sleep(0.1)
    locator.type(text, delay=delay)
    time.sleep(0.5)


def react_select_pick(page: Page, option_text: str):
    """Click a React Select dropdown and pick an option.
    The .Select__input-container intercepts clicks on the placeholder,
    so we must force-click it, then click the matching [role=option]."""
    # Dismiss any tooltip/popover first
    page.mouse.click(10, 10)
    time.sleep(SLOW)
    container = page.locator('.Select__input-container').first
    container.click(force=True)
    time.sleep(1)
    option = page.locator(f'[role="option"]:has-text("{option_text}")').first
    if option.is_visible(timeout=3000):
        option.click()
        time.sleep(0.5)
        return True
    return False


def unique_iri(base: str) -> str:
    """Generate a timestamp-based unique IRI to avoid conflicts with old data."""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{base}-{ts}"


def create_asset_dialog(page: Page, title: str, asset_type: str = "vocabulary"):
    """Fill the Create Vocabulary/Ontology dialog and click Create.
    Handles IRI conflicts by generating a unique IRI if needed.
    asset_type: 'vocabulary' or 'ontology'"""
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=5000)
    react_type(title_input, title)
    time.sleep(1)

    # Check if Create button is enabled
    create_btn = page.locator('.modal button:has-text("Create")').first
    time.sleep(1)
    if create_btn.get_attribute("disabled") is not None:
        # IRI conflict — uncheck suggest IRI and use unique one
        print(f"    IRI conflict, using unique IRI")
        suggest_cb = page.locator(f'input[data-testid="suggest-iri-{asset_type}"]').first
        if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
            suggest_cb.click()
            time.sleep(0.5)
        iri_input = page.locator(f'input[data-testid="suggest-iri-{asset_type}-input"]').first
        if iri_input.is_visible(timeout=2000):
            base = f"https://vocabularies.metaphacts.com/{title.lower().replace(' ', '-')}"
            if asset_type == "ontology":
                base = f"https://ontologies.metaphacts.com/{title.lower().replace(' ', '-')}"
            react_type(iri_input, unique_iri(base) + "/0.1")
            time.sleep(0.5)

    # Click Create — wait for enabled
    for _ in range(30):
        if create_btn.get_attribute("disabled") is None:
            break
        time.sleep(0.3)
    create_btn.click()
    time.sleep(3)
    dismiss_walkthrough(page)
```

- [ ] **Step 4: Write vocabulary tree helpers**

```python
# Append to v2/mf_helpers.py

def tree_click_concept(page: Page, label: str):
    """Click a concept in the vocabulary tree panel. Expands collapsed parents.
    Scoped to the tree panel to avoid matching detail panel elements."""
    tree = page.locator('.ontodia-accordion').first
    node = tree.locator(f'a:has-text("{label}")').first
    if not node.is_visible(timeout=2000):
        # Expand all collapsed tree nodes
        toggles = tree.locator('.LazyTreeSelector--expandToggle')
        for i in range(toggles.count()):
            t = toggles.nth(i)
            if t.is_visible():
                t.click()
                time.sleep(0.3)
        node = tree.locator(f'a:has-text("{label}")').first
    node.click(force=True)
    time.sleep(1)
    return node


def tree_concept_menu(page: Page, label: str):
    """Open the more_vert menu for a SPECIFIC concept in the tree.
    Each concept has its own three-dot button inside span.termTree__node.
    NEVER use page.locator('button:has-text("more_vert")').first."""
    node = tree_click_concept(page, label)
    # Navigate up to the termTree__node span, then find its more_vert button
    tree_node = node.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
    menu_btn = tree_node.locator('button:has-text("more_vert")').first
    if not menu_btn.is_visible(timeout=1500):
        tree_node = node.locator('xpath=ancestor::div[contains(@class,"LazyTreeSelector--itemContent")]').first
        menu_btn = tree_node.locator('button:has-text("more_vert")').first
    menu_btn.wait_for(state="visible", timeout=3000)
    menu_btn.click()
    time.sleep(0.5)


def create_top_concept(page: Page, label: str, definition: str = ""):
    """Create a top-level concept in the vocabulary editor."""
    page.locator('button:has-text("Create top-level term")').first.click()
    time.sleep(1.5)
    pref = page.locator('input[placeholder="Enter preferred label here..."]').first
    pref.wait_for(state="visible", timeout=5000)
    pref.click()
    pref.type(label, delay=30)
    time.sleep(0.5)
    if definition:
        def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
        if def_input.is_visible(timeout=1000):
            def_input.click()
            def_input.type(definition, delay=20)
    # Save — button is enabled by default
    save = page.locator('.overlay-modal.show button[name="submit"]').first
    save.wait_for(state="visible", timeout=3000)
    time.sleep(0.3)
    save.click()
    time.sleep(1.5)
    print(f"    Created top concept: {label}")


def create_narrower_concept(page: Page, parent: str, child: str, definition: str = ""):
    """Create a narrower concept under a specific parent.
    Uses the parent's own more_vert > 'Create narrower term'."""
    tree_concept_menu(page, parent)
    narrower = page.locator('.dropdown-menu.show a:has-text("Create narrower term")').first
    if narrower.is_visible(timeout=2000):
        narrower.click()
        time.sleep(1)
    else:
        dismiss_modals(page)
        print(f"    Warning: 'Create narrower term' not found for {parent}")
        return
    pref = page.locator('input[placeholder="Enter preferred label here..."]').first
    pref.wait_for(state="visible", timeout=5000)
    pref.click()
    pref.type(child, delay=30)
    time.sleep(0.5)
    if definition:
        def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
        if def_input.is_visible(timeout=1000):
            def_input.click()
            def_input.type(definition, delay=20)
    save = page.locator('.overlay-modal.show button[name="submit"]').first
    save.wait_for(state="visible", timeout=3000)
    time.sleep(0.3)
    save.click()
    time.sleep(1.5)
    print(f"    Created narrower: {child} under {parent}")


def set_concept_status(page: Page, label: str, status: str):
    """Set a concept's editorial status via its more_vert menu.
    Status options are <button class='termSetStatusButton'>, not <a> tags.
    Available: 'In review', 'Ready for review', 'Accepted for publication', 'Request changes'."""
    tree_concept_menu(page, label)
    btn = page.locator(f'.dropdown-menu.show button.termSetStatusButton:has-text("{status}")').first
    if btn.is_visible(timeout=2000):
        btn.click()
        time.sleep(1)
        dismiss_modals(page)
        print(f"    Status: {label} -> {status}")
    else:
        dismiss_modals(page)
        print(f"    Warning: '{status}' not available for {label}")
```

- [ ] **Step 5: Write ontology editor helpers**

```python
# Append to v2/mf_helpers.py

def create_ontology_class(page: Page, name: str):
    """Create a class in the ontology editor."""
    page.locator('button:has-text("Create Class")').first.click()
    time.sleep(1)
    label = page.locator('input[placeholder="Enter label here..."]').first
    if label.is_visible(timeout=2000):
        label.fill(name)
        time.sleep(0.3)
    confirm = page.locator('button:has-text("Confirm")').first
    if confirm.is_visible(timeout=1500):
        confirm.click()
        time.sleep(0.5)
    print(f"    Created class: {name}")


def create_ontology_attribute(page: Page, name: str):
    """Create an attribute (datatype property) in the ontology editor."""
    page.locator('button:has-text("Create Attribute")').first.click()
    time.sleep(1)
    label = page.locator('input[placeholder="Enter label here..."]').first
    if label.is_visible(timeout=2000):
        label.fill(name)
        time.sleep(0.3)
    confirm = page.locator('button:has-text("Confirm")').first
    if confirm.is_visible(timeout=1500):
        confirm.click()
        time.sleep(0.5)
    print(f"    Created attribute: {name}")


def create_ontology_relation(page: Page, name: str):
    """Create a relation (object property) in the ontology editor."""
    page.locator('button:has-text("Create Relation")').first.click()
    time.sleep(1)
    label = page.locator('input[placeholder="Enter label here..."]').first
    if label.is_visible(timeout=2000):
        label.fill(name)
        time.sleep(0.3)
    confirm = page.locator('button:has-text("Confirm")').first
    if confirm.is_visible(timeout=1500):
        confirm.click()
        time.sleep(0.5)
    print(f"    Created relation: {name}")


def switch_ontology_tab(page: Page, tab: str):
    """Switch to Classes/Attributes/Relations tab in the ontology editor."""
    tab_btn = page.locator(f'button:has-text("{tab}")').first
    if tab_btn.is_visible(timeout=2000):
        tab_btn.click()
        time.sleep(0.5)
```

- [ ] **Step 6: Write editor helpers (CodeMirror + Monaco)**

```python
# Append to v2/mf_helpers.py

def codemirror_set(page: Page, content: str):
    """Set content in a CodeMirror editor.
    Used by: AI Services create dialog.
    CodeMirror API works perfectly — no workaround needed."""
    page.evaluate(f"""() => {{
        const cm = document.querySelector('.CodeMirror');
        if (cm && cm.CodeMirror) cm.CodeMirror.setValue({repr(content)});
    }}""")
    time.sleep(0.5)


def codemirror_get(page: Page) -> str:
    """Get content from a CodeMirror editor."""
    return page.evaluate("""() => {
        const cm = document.querySelector('.CodeMirror');
        return cm && cm.CodeMirror ? cm.CodeMirror.getValue() : '';
    }""")


def codemirror_replace(page: Page, find: str, replace: str):
    """Find and replace text in a CodeMirror editor."""
    config = codemirror_get(page)
    new_config = config.replace(find, replace)
    codemirror_set(page, new_config)


def monaco_set_via_keyboard(page: Page, content: str):
    """Set content in a Monaco editor via keyboard type().
    Monaco in metaphactory doesn't expose window.monaco.
    clipboard paste and insert_text corrupt special chars.
    type() with delay works but is slow for long content.
    Best for short templates (<500 chars)."""
    editor = page.locator('.monaco-editor .view-lines').first
    if editor.is_visible(timeout=5000):
        editor.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        page.keyboard.type(content, delay=3)
        time.sleep(1)
        return True
    return False


def sparql_update(page: Page, base_url: str, query: str):
    """Execute a SPARQL UPDATE query via the SPARQL editor.
    Uses Monaco editor to set the query."""
    safe_navigate(page, f"{base_url}/sparql")
    time.sleep(2)
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{
            editors[0].setValue({repr(query)});
            return;
        }}
        const cm = document.querySelector('.CodeMirror');
        if (cm && cm.CodeMirror) cm.CodeMirror.setValue({repr(query)});
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute"), button:has-text("Run")').first.click()
    time.sleep(3)
```

- [ ] **Step 7: Write editorial workflow helpers**

```python
# Append to v2/mf_helpers.py

def git_save(page: Page):
    """Save vocabulary/ontology to git via More > Git versioning."""
    more = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
    if more.is_visible(timeout=3000):
        more.click()
        time.sleep(0.5)
        git = page.locator('.dropdown-menu.show a:has-text("Git versioning")').first
        if git.is_visible(timeout=2000):
            git.click()
            time.sleep(2)
            # Click Save/Commit in the dialog
            save = page.locator('.modal.show button:has-text("Save"), .modal.show button:has-text("Commit")').first
            if save.is_visible(timeout=3000):
                save.click()
                time.sleep(2)
            # Close the git dialog — it stays open after save
            dismiss_modals(page)
            print("    Saved to git")
        else:
            dismiss_modals(page)


def catalog_more_vert(page: Page, asset_name: str):
    """Click more_vert for a specific asset on the catalog listing page.
    Returns True if the dropdown opened."""
    btns = page.locator('button:has-text("more_vert")')
    for i in range(btns.count()):
        btn = btns.nth(i)
        if btn.is_visible():
            parent = btn.evaluate(
                "el => el.closest('tr, div')?.textContent?.substring(0, 60)")
            if parent and asset_name.lower() in parent.lower():
                btn.click()
                time.sleep(1)
                return True
    return False


def catalog_action(page: Page, asset_name: str, action: str) -> bool:
    """Execute an action from the catalog more_vert menu.
    Actions: 'Create version...', 'Start review request', 'Publish', 'Export', 'Delete', etc."""
    if catalog_more_vert(page, asset_name):
        opt = page.locator(f'.dropdown-menu.show a:has-text("{action}")').first
        if opt.is_visible(timeout=2000):
            opt.click()
            time.sleep(2)
            return True
        # Try in More submenu
        more_sub = page.locator('.dropdown-menu.show a:has-text("More")').first
        if more_sub.is_visible(timeout=1000):
            more_sub.hover()
            time.sleep(1)
            opt = page.locator(f'.dropdown-menu.show a:has-text("{action}")').first
            if opt.is_visible(timeout=2000):
                opt.click()
                time.sleep(2)
                return True
        dismiss_modals(page)
    return False
```

- [ ] **Step 8: Commit helpers library**

```bash
cd /Users/kiptengwer/Documents/metaphactory-tutorial
git add v2/mf_helpers.py
git commit -m "feat: metaphactory automation helpers library v2"
```

---

### Task 2: Create template strings (`mf_templates.py`)

**Files:**
- Create: `v2/mf_templates.py`

- [ ] **Step 1: Write template content for Tasks 7, 8, 10**

```python
# v2/mf_templates.py
"""HTML template strings for metaphactory page templates.
These use the ACTUAL property names from the training instance data:
- org:hasMember (not memberOf)
- org:isInvolvedIn (not hasClient/hasProject)
"""

ORGANIZATION_TEMPLATE = """<div>
<h3><mp-label iri="[[this]]"></mp-label></h3>
<semantic-query query="SELECT ?label WHERE { ?? rdfs:label ?label }" template="<p><b>Label:</b> {{label.value}}</p>"></semantic-query>
<semantic-query query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?memberLabel WHERE { ?? org:hasMember ?member . ?member rdfs:label ?memberLabel }" template="<p><b>Members:</b> {{#each bindings}}{{memberLabel.value}}{{#unless @last}}, {{/unless}}{{/each}}</p>"></semantic-query>
<h4>Project Portfolio</h4>
<semantic-table query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?name WHERE { ?? org:isInvolvedIn ?project . ?project rdfs:label ?name }" column-configuration='[{"variableName": "name", "displayName": "name"}]'></semantic-table>
</div>"""

ORGANIZATION_PANEL = """<div>
<h3><mp-label iri="[[this]]"></mp-label></h3>
<semantic-query query="SELECT ?label WHERE { ?? rdfs:label ?label }" template="<p><b>Label:</b> {{label.value}}</p>"></semantic-query>
<semantic-query query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?memberLabel WHERE { ?? org:hasMember ?member . ?member rdfs:label ?memberLabel }" template="<p><b>Members:</b> {{#each bindings}}{{memberLabel.value}}{{#unless @last}}, {{/unless}}{{/each}}</p>"></semantic-query>
<h4>Projects</h4>
<semantic-table query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?name WHERE { ?? org:isInvolvedIn ?project . ?project rdfs:label ?name }" column-configuration='[{"variableName": "name", "displayName": "name"}]'></semantic-table>
</div>"""

CONVERSATIONAL_AI_PAGE = """<div class="page">
<h1>Conversational AI</h1>
<mp-conversational-ai id="recipe-ai" placeholder="Talk to the Recipe Search and Discovery Agent..." default-conversation-agent-iri="urn:service:agent-searchanddiscovery-recipes" options='{"explanationOptions": {"showExplanation": true}}'></mp-conversational-ai>
<mp-event-trigger targets='["recipe-ai"]' type="ConversationalAI.Start" data='{"prompt": "Show all the recipes and their ingredients and quantities"}'><button class="btn btn-outline-primary m-1">Show all the recipes and their ingredients and quantities</button></mp-event-trigger>
<mp-event-trigger targets='["recipe-ai"]' type="ConversationalAI.Start" data='{"prompt": "Which recipes belong to the vegan diet?"}'><button class="btn btn-outline-primary m-1">Which recipes belong to the vegan diet?</button></mp-event-trigger>
</div>"""

RECIPE_INSTANCES_SPARQL = """PREFIX recipe: <http://ontologies.metaphacts.com/recipes/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {
  recipe:VeganDiet a recipe:Diet ; rdfs:label "Vegan" .
  recipe:MediterraneanDiet a recipe:Diet ; rdfs:label "Mediterranean" .
  recipe:AuthorAnna a recipe:Author ; rdfs:label "Anna Smith" .
  recipe:AuthorMarco a recipe:Author ; rdfs:label "Marco Rossi" .
  recipe:CarrotVeg a recipe:Vegetable ; rdfs:label "Carrot" .
  recipe:PotatoVeg a recipe:Vegetable ; rdfs:label "Potato" .
  recipe:OnionVeg a recipe:Vegetable ; rdfs:label "Onion" .
  recipe:GreenBeansVeg a recipe:Vegetable ; rdfs:label "Green beans" .
  recipe:ChickenProtein a recipe:Protein ; rdfs:label "Chicken breast" .
  recipe:TofuProtein a recipe:Protein ; rdfs:label "Tofu" .
  recipe:BasilSeasoning a recipe:Seasoning ; rdfs:label "Basil" .
  recipe:GarlicSeasoning a recipe:Seasoning ; rdfs:label "Garlic" .
  recipe:OliveOilSeasoning a recipe:Seasoning ; rdfs:label "Olive oil" .
  recipe:IU_Pasta_Carrot a recipe:IngredientUsage ; rdfs:label "Carrots" ; recipe:quantity "200" ; recipe:units "grams" ; recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Pasta_GreenBeans a recipe:IngredientUsage ; rdfs:label "Green beans" ; recipe:quantity "150" ; recipe:units "grams" ; recipe:hasItem recipe:GreenBeansVeg .
  recipe:IU_Pasta_Basil a recipe:IngredientUsage ; rdfs:label "Fresh basil" ; recipe:quantity "10" ; recipe:units "leaves" ; recipe:hasItem recipe:BasilSeasoning .
  recipe:IU_Pasta_OliveOil a recipe:IngredientUsage ; rdfs:label "Olive oil" ; recipe:quantity "3" ; recipe:units "tablespoons" ; recipe:hasItem recipe:OliveOilSeasoning .
  recipe:IU_Soup_Potato a recipe:IngredientUsage ; rdfs:label "Potatoes" ; recipe:quantity "300" ; recipe:units "grams" ; recipe:hasItem recipe:PotatoVeg .
  recipe:IU_Soup_Carrot a recipe:IngredientUsage ; rdfs:label "Carrots" ; recipe:quantity "200" ; recipe:units "grams" ; recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Soup_Onion a recipe:IngredientUsage ; rdfs:label "Onion" ; recipe:quantity "1" ; recipe:units "piece" ; recipe:hasItem recipe:OnionVeg .
  recipe:IU_Soup_Garlic a recipe:IngredientUsage ; rdfs:label "Garlic cloves" ; recipe:quantity "3" ; recipe:units "cloves" ; recipe:hasItem recipe:GarlicSeasoning .
  recipe:PastaPrimavera a recipe:Recipe ; rdfs:label "Pasta Primavera" ; recipe:description "Fresh spring vegetables tossed with pasta in olive oil and basil" ; recipe:difficulty "Easy" ; recipe:cookingTime "25 minutes" ; recipe:belongsToDiet recipe:VeganDiet, recipe:MediterraneanDiet ; recipe:hasIngredientUsage recipe:IU_Pasta_Carrot, recipe:IU_Pasta_GreenBeans, recipe:IU_Pasta_Basil, recipe:IU_Pasta_OliveOil ; recipe:hasAuthor recipe:AuthorAnna .
  recipe:VegetableSoup a recipe:Recipe ; rdfs:label "Vegetable Soup" ; recipe:description "Hearty soup with root vegetables, onion and garlic" ; recipe:difficulty "Medium" ; recipe:cookingTime "45 minutes" ; recipe:belongsToDiet recipe:VeganDiet ; recipe:hasIngredientUsage recipe:IU_Soup_Potato, recipe:IU_Soup_Carrot, recipe:IU_Soup_Onion, recipe:IU_Soup_Garlic ; recipe:hasAuthor recipe:AuthorMarco .
}"""
```

- [ ] **Step 2: Commit**

```bash
git add v2/mf_templates.py
git commit -m "feat: template strings for metaphactory page templates"
```

---

### Task 3: Create task functions (`mf_tasks.py`)

**Files:**
- Create: `v2/mf_tasks.py`

This is the largest file. Each task is a self-contained function using the helpers from `mf_helpers.py`. I'll define the function signatures and key steps — the implementation uses the helpers directly.

- [ ] **Step 1: Write VM Tasks 1-4 (Vocabulary + Ontology)**

Write functions `vm_task1_vocabulary`, `vm_task2_vocab_editorial`, `vm_task3_ontology`, `vm_task4_onto_editorial` using the helpers. Each function takes `(page, base_url)` as arguments.

Key patterns per task:
- **Task 1**: `create_asset_dialog` → `create_top_concept` → `create_narrower_concept` (x7) → `set_concept_status` (x8 "In review") → `set_concept_status` (x2 "Request changes") → `set_concept_status` (x8 "Accepted for publication") → `git_save`
- **Task 2**: `catalog_action("Start review request")` → approve inside ontology → `catalog_action("Publish")` → `catalog_action("Create version...")` → add Garlic → review → publish
- **Task 3**: `create_asset_dialog` (ontology) → `switch_ontology_tab("Classes")` → create 7 classes → `switch_ontology_tab("Attributes")` → create 6 attrs → `switch_ontology_tab("Relations")` → create 4 relations → `sparql_update` (instances)
- **Task 4**: Same editorial pattern as Task 2 but for ontology, adding Menu class + hasRecipe relation

- [ ] **Step 2: Write App Tasks 5-8 (QAAS, Diagram, Templates)**

Functions: `app_task5_qaas`, `app_task6_diagram`, `app_task7_resource_template`, `app_task8_knowledge_panel`

Key patterns:
- **Task 5**: SPARQL editor → save query → Admin:QueryService → Add Service → React Select for query → fill ACL → Save
- **Task 6**: Assets:Diagrams → Create → Instances search → drag Bob → expand connections
- **Task 7**: Navigate to `Template:...Organization&action=edit` → `monaco_set_via_keyboard(ORGANIZATION_TEMPLATE)` → Save
- **Task 8**: Navigate to `PanelTemplate:...Organization&action=edit` → `monaco_set_via_keyboard(ORGANIZATION_PANEL)` → Save

- [ ] **Step 3: Write AI Tasks 9-10 (Agent + Conversational AI)**

Functions: `ai_task9_agent`, `ai_task10_conversational_ai`

Key patterns:
- **Task 9**: Admin:AIServices → Create → select `agent-searchanddiscovery` template → `codemirror_replace` (contextOntology, languageModel, service ID) → Create
- **Task 10**: Navigate to `RecipeAssistant?action=edit` → `monaco_set_via_keyboard(CONVERSATIONAL_AI_PAGE)` → Save & View → click example question

- [ ] **Step 4: Commit**

```bash
git add v2/mf_tasks.py
git commit -m "feat: 10 certification task functions"
```

---

### Task 4: Create CLI runner (`run.py`)

**Files:**
- Create: `v2/run.py`

- [ ] **Step 1: Write the CLI runner**

```python
# v2/run.py
"""Metaphactory Training Certification Automation v2.
Usage:
    python3 v2/run.py --url https://m20.academy.metaphacts.cloud --headed
    python3 v2/run.py --task 1                    # single task
    python3 v2/run.py --track vm                  # VM tasks only
    python3 v2/run.py --track app                 # App tasks only
    python3 v2/run.py --track ai                  # AI tasks only
"""
import argparse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from mf_helpers import login, screenshot, dismiss_modals
from mf_tasks import (
    vm_task1_vocabulary, vm_task2_vocab_editorial,
    vm_task3_ontology, vm_task4_onto_editorial,
    app_task5_qaas, app_task6_diagram,
    app_task7_resource_template, app_task8_knowledge_panel,
    ai_task9_agent, ai_task10_conversational_ai,
)

TASKS = [
    (1,  "vm",  "Vegetables Vocabulary",         vm_task1_vocabulary),
    (2,  "vm",  "Vocab Editorial & Versioning",  vm_task2_vocab_editorial),
    (3,  "vm",  "Recipes Ontology",              vm_task3_ontology),
    (4,  "vm",  "Onto Editorial & Versioning",   vm_task4_onto_editorial),
    (5,  "app", "QAAS API",                      app_task5_qaas),
    (6,  "app", "Bob's Diagram",                 app_task6_diagram),
    (7,  "app", "Organization Resource Template", app_task7_resource_template),
    (8,  "app", "Organization Knowledge Panel",  app_task8_knowledge_panel),
    (9,  "ai",  "Search & Discovery Agent",      ai_task9_agent),
    (10, "ai",  "Conversational AI Interface",   ai_task10_conversational_ai),
]

def main():
    parser = argparse.ArgumentParser(description="Metaphactory Certification v2")
    parser.add_argument("--url", default="https://m20.academy.metaphacts.cloud")
    parser.add_argument("--user", default="admin")
    parser.add_argument("--password", default="admin")
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--task", type=int)
    parser.add_argument("--track", choices=["vm", "app", "ai"])
    args = parser.parse_args()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, slow_mo=200)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="v2/recordings",
        )
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        page.set_default_timeout(15000)

        login(page, args.url, args.user, args.password)
        print(f"Logged in to {args.url}")

        for num, track, name, func in TASKS:
            if args.task and num != args.task:
                continue
            if args.track and track != args.track:
                continue
            print(f"\n{'='*60}")
            print(f"Task {num}: {name}")
            print(f"{'='*60}")
            try:
                func(page, args.url)
                print(f"  PASS")
            except Exception as e:
                print(f"  FAIL: {e}")
                screenshot(page, f"error-task-{num}")
                dismiss_modals(page)

        ctx.close()
        browser.close()

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add v2/run.py
git commit -m "feat: CLI runner for metaphactory certification automation"
```

---

### Task 5: Test each task individually

- [ ] **Step 1: Run Task 1 (Vocabulary)**
```bash
cd /Users/kiptengwer/Documents/metaphactory-tutorial
python3 v2/run.py --task 1 --headed
```
Expected: Vocabulary created with correct hierarchy, all concepts set in review, accepted for publication, saved to git.

- [ ] **Step 2: Run Task 3 (Ontology)**
```bash
python3 v2/run.py --task 3 --headed
```
Expected: Ontology with 7 classes, 6 attributes, 4 relations. Instances created via SPARQL.

- [ ] **Step 3: Run Task 5 (QAAS)**
```bash
python3 v2/run.py --task 5 --headed
```
Expected: SPARQL query saved, REST service created and testable.

- [ ] **Step 4: Run Task 7 (Resource Template)**
```bash
python3 v2/run.py --task 7 --headed
```
Expected: Organization template rendering Label, Members, Project Portfolio.

- [ ] **Step 5: Run Task 9 (S&D Agent)**
```bash
python3 v2/run.py --task 9 --headed
```
Expected: Agent created with Recipes ontology + OpenAI LLM.

- [ ] **Step 6: Run Task 10 (Conversational AI)**
```bash
python3 v2/run.py --task 10 --headed
```
Expected: Page with mp-conversational-ai, 2 example questions, agent responds with recipe data.

- [ ] **Step 7: Fix any failures and re-run**

- [ ] **Step 8: Run full suite**
```bash
python3 v2/run.py --headed
```
Expected: All 10 tasks pass (editorial workflow tasks 2 and 4 may need manual reviewer setup).

- [ ] **Step 9: Commit final working version**
```bash
git add -A v2/
git commit -m "feat: metaphactory certification automation v2 - all 10 tasks"
```
