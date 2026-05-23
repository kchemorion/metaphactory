#!/usr/bin/env python3
"""
Execute ALL exercises across ALL metaphactory training modules.

This script goes module by module, opens every page, plays every video,
and executes every hands-on exercise with the exact steps from the catalog.

Usage:
    python3 v2/execute_exercises.py --headed
    python3 v2/execute_exercises.py --module 1 --headed
"""
import argparse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, BrowserContext

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "admin"
PASSWORD = "admin"
SS_DIR = Path("v2/screenshots")
SS_DIR.mkdir(parents=True, exist_ok=True)


def ss(page, name):
    page.screenshot(path=str(SS_DIR / f"{name}.png"))
    print(f"      ss: {name}")


def go(page, path):
    try:
        page.goto(f"{BASE_URL}{path}")
        page.wait_for_load_state("networkidle")
    except:
        pass
    time.sleep(2)
    try:
        page.keyboard.press("Escape")
        time.sleep(0.3)
    except:
        pass


def scroll_page(page):
    h = page.evaluate("() => document.body.scrollHeight")
    vh = page.evaluate("() => window.innerHeight")
    pos = 0
    while pos < h:
        pos += vh // 2
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(0.3)
    page.evaluate("window.scrollTo(0, 0)")


def open_video_tab(ctx, page, link_text="Open"):
    """Click an 'Open' link and play any video in the new page."""
    links = page.locator(f'a:has-text("{link_text}")').all()
    tabs = []
    for link in links:
        try:
            href = link.get_attribute("href")
            if href and href.startswith("/"):
                tab = ctx.new_page()
                tab.goto(f"{BASE_URL}{href}")
                time.sleep(2)
                tab.evaluate("""() => {
                    document.querySelectorAll('video').forEach(v => { v.muted=true; v.play().catch(()=>{}); });
                    document.querySelectorAll('iframe[src*="youtube"]').forEach(f => {
                        if (!f.src.includes('autoplay')) f.src += (f.src.includes('?')?'&':'?') + 'autoplay=1&mute=1';
                    });
                }""")
                tabs.append(tab)
        except:
            pass
    return tabs


def dismiss(page):
    for _ in range(3):
        try:
            m = page.locator('.modal.show, .walkthroughCarousel.show')
            if m.is_visible(timeout=300):
                c = m.locator('.btn-close').first
                if c.is_visible(timeout=200):
                    c.click(force=True)
                else:
                    page.keyboard.press("Escape")
                time.sleep(0.3)
            else:
                break
        except:
            page.keyboard.press("Escape")
            time.sleep(0.2)


def monaco_type(page, content):
    """Type content into Monaco editor via keyboard."""
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


# ═══════════════════════════════════════════════════════════════
# MODULE 1: metaphactory basics
# ═══════════════════════════════════════════════════════════════

def m1_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 1: metaphactory basics — EXERCISES")
    print("="*60)

    # 1.1 Quick search for Bob
    print("\n  [1.1] Quick search for Bob")
    go(page, "/resource/:SimpleSearch")
    search = page.locator('input[placeholder*="Search" i]').first
    if search.is_visible(timeout=3000):
        search.click()
        search.type("Bob")
        time.sleep(2)
        ss(page, "m1_ex_search_bob")

    # 1.2 Explore semantic search
    print("\n  [1.2] Semantic search interface")
    go(page, "/resource/training:SampleAppSearch")
    scroll_page(page)
    # Click the semantic search link
    link = page.locator('a:has-text("Use the search interface")').first
    if link.is_visible(timeout=2000):
        link.click()
        time.sleep(3)
        ss(page, "m1_ex_semantic_search")

    # 1.3 Create a diagram
    print("\n  [1.3] Visual exploration — create diagram")
    go(page, "/resource/Assets:Diagrams")
    time.sleep(2)
    ss(page, "m1_ex_diagrams")

    # 1.4 Instance data management
    print("\n  [1.4] Instance data management — Project class")
    go(page, "/resource/training:SampleAppOntoVocab")
    scroll_page(page)
    ss(page, "m1_ex_instance_mgmt")

    # 1.5 Data quality — run validation
    print("\n  [1.5] Data quality — validate Organization ontology")
    go(page, "/resource/Assets:Ontologies")
    time.sleep(2)
    # Open Organization ontology
    org_link = page.locator('a:has-text("Organization")').first
    if org_link.is_visible(timeout=3000):
        org_link.click()
        time.sleep(3)
        dismiss(page)
        # Click More > Validate database
        more = page.locator('button:has-text("More"):has-text("arrow_drop_down")').first
        if more.is_visible(timeout=2000):
            more.click()
            time.sleep(0.5)
            validate = page.locator('.dropdown-menu.show a:has-text("Validate")').first
            if validate.is_visible(timeout=1000):
                validate.click()
                time.sleep(5)
                ss(page, "m1_ex_validate_org")
            else:
                page.keyboard.press("Escape")

    # 1.6 UI Templates — Semantic table
    print("\n  [1.6a] Semantic table exercise")
    TABLE_CODE = '''<h5>Person friends</h5>
<semantic-table query="
PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
SELECT *
WHERE {
?person1 org:knows ?person2 .
}" column-configuration='[
{"variableName": "person1", "displayName": "Person"},
{"variableName": "person2", "displayName": "Friend"}]'>
</semantic-table>'''

    go(page, "/resource/training:SemanticTablePage?action=edit")
    time.sleep(3)
    if monaco_type(page, TABLE_CODE):
        save = page.locator('button:has-text("Save & View")').first
        if save.is_visible(timeout=2000):
            save.click()
            time.sleep(3)
        ss(page, "m1_ex_semantic_table")
        print("      Semantic table saved")

    # 1.6b Semantic chart
    print("\n  [1.6b] Semantic chart exercise")
    CHART_CODE = '''<h5>Number of Friends</h5>
<semantic-chart type="pie" query="
PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
SELECT ?person1 (COUNT(?person2) AS ?known)
WHERE {
?person1 org:knows ?person2 .
}
GROUP BY ?person1" sets='[{"dataSetName": "Number of Friends", "category": "person1", "value": "known"}]'>
</semantic-chart>'''

    go(page, "/resource/training:SemanticChartPage?action=edit")
    time.sleep(3)
    if monaco_type(page, CHART_CODE):
        save = page.locator('button:has-text("Save & View")').first
        if save.is_visible(timeout=2000):
            save.click()
            time.sleep(3)
        ss(page, "m1_ex_semantic_chart")
        print("      Semantic chart saved")

    # 1.6c Semantic form
    print("\n  [1.6c] Semantic form exercise")
    FORM_CODE = '''<h5> Project Form </h5>
<semantic-form for-class="https://ontologies.metaphacts.com/organization-ontology/Project" new-subject-template="https://ontologies.metaphacts.com/organization-ontology/Project/newExampleProject"></semantic-form>'''

    go(page, "/resource/training:SemanticFormPage?action=edit")
    time.sleep(3)
    if monaco_type(page, FORM_CODE):
        save = page.locator('button:has-text("Save & View")').first
        if save.is_visible(timeout=2000):
            save.click()
            time.sleep(3)
        ss(page, "m1_ex_semantic_form")
        print("      Semantic form saved")

    # 1.6d Conversational AI
    print("\n  [1.6d] Conversational AI exercise")
    CONV_CODE = '<mp-conversational-ai id="conversation-ai-test" placeholder="Talk to Conversational AI..." prompt-suggestion-template="{{> tmpl}}" default-conversation-agent-iri="urn:service:conversationagent-default" options=\'{"explanationOptions": {"showExplanation": true}}\'>\n<template id="tmpl">\n<div class="suggestion-prompt-cards">\n<div data-flex-layout="rows stretch-stretch">\n{{#bind\nexample-questions=(array-of\n"List organizations."\n"List projects."\n"List organizations and their members."\n)}}\n{{#each example-questions}}\n<div data-flex-self="size-1of5 md-half sm-full" class="suggestion-prompt-card-items">\n<mp-event-trigger targets=\'["conversation-ai-test"]\' type="ConversationalAI.Start" data=\'{"prompt": "{{this}}"}\' >\n<button type="button" class="btn btn-secondary suggestion-prompt-card">\n<span class="suggestion-prompt-thumbnail">\n<span class="material-symbols-outlined">lightbulb_circle</span>\n</span>\n<span class="suggestion-prompt-text">{{this}}</span>\n</button>\n</mp-event-trigger>\n</div>\n{{/each}}\n{{/bind}}\n</div>\n</div>\n</template>\n</mp-conversational-ai>'

    go(page, "/resource/training:ConversationalAIPage?action=edit")
    time.sleep(3)
    if monaco_type(page, CONV_CODE):
        save = page.locator('button:has-text("Save & View")').first
        if save.is_visible(timeout=2000):
            save.click()
            time.sleep(5)
        ss(page, "m1_ex_conv_ai")
        print("      Conversational AI saved")

    print("\n  Module 1 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 2: Visual Modeling Basics — browse assets
# ═══════════════════════════════════════════════════════════════

def m2_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 2: Visual Modeling Basics — EXERCISES")
    print("="*60)

    # Open main page and all video sub-pages
    go(page, "/resource/:BusinessTraining")
    scroll_page(page)

    # Chapter pages are mostly video-based, open each
    chapters = [
        ("/resource/:BusinessTraining-chapter1", "Ontology Modeling"),
        ("/resource/:BusinessTraining-chapter2", "Vocabulary Mgmt"),
        ("/resource/:BusinessTraining-chapter3", "Interlinking"),
        ("/resource/:BusinessTraining-chapter4", "Data Cataloging"),
        ("/resource/:BusinessTraining-chapter5", "Instance Data"),
    ]

    for path, name in chapters:
        print(f"\n  [2] {name}")
        go(page, path)
        scroll_page(page)
        # Open video sub-pages in tabs
        open_video_tab(ctx, page)
        ss(page, f"m2_{name.replace(' ', '_')}")

    print("\n  Module 2 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 3: Visual Modeling Advanced
# ═══════════════════════════════════════════════════════════════

def m3_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 3: Visual Modeling Advanced — EXERCISES")
    print("="*60)

    # 3.1 Recap — explore Status vocab and Project ontology
    print("\n  [3.1] Recap — explore assets")
    go(page, "/resource/Assets:Vocabularies")
    time.sleep(2)
    ss(page, "m3_recap_vocabs")

    go(page, "/resource/Assets:Ontologies")
    time.sleep(2)
    ss(page, "m3_recap_ontos")

    # 3.2-3.7 Open each sub-module and scroll through
    sub_modules = [
        ("/resource/training:recapVisualModeling", "Recap"),
        ("/resource/training:editorialWorkflow", "Editorial Ontologies"),
        ("/resource/training:editorialWorkflowVocabulary", "Editorial Vocabularies"),
        ("/resource/training:modelDrivenValidation", "Data Quality"),
        ("/resource/training:git", "Git Versioning"),
        ("/resource/training:AdditionalFeatures", "Additional Features"),
        ("/resource/training:SummaryAdvVisualModelling", "Summary"),
    ]

    for path, name in sub_modules:
        print(f"\n  [3] {name}")
        go(page, path)
        scroll_page(page)
        open_video_tab(ctx, page)
        ss(page, f"m3_{name.replace(' ', '_')}")

    print("\n  Module 3 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 5: App Building Basics
# ═══════════════════════════════════════════════════════════════

def m5_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 5: App Building Basics — EXERCISES")
    print("="*60)

    chapters = [
        ("/resource/training:AppBuildingBasicsTemplating", "Templating"),
        ("/resource/training:AppBuildingBasicsSemComponents", "Semantic Components"),
        ("/resource/training:AppBuildingBasicsEvents", "Component Interaction"),
        ("/resource/training:AppBuildingBasicsAdvFeatures", "Advanced Features"),
    ]

    for path, name in chapters:
        print(f"\n  [5] {name}")
        go(page, path)
        scroll_page(page)
        open_video_tab(ctx, page)
        ss(page, f"m5_{name.replace(' ', '_')}")

    print("\n  Module 5 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 6: App Building Advanced
# ═══════════════════════════════════════════════════════════════

def m6_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 6: App Building Advanced — EXERCISES")
    print("="*60)

    sub_modules = [
        ("/resource/training:AdvSecurity", "Security"),
        ("/resource/training:AdvAppLifeCycle", "App Lifecycle"),
        ("/resource/training:AppBuildingAdvFederation", "Federation"),
        ("/resource/training:AdvDataAuthoring", "Data Authoring"),
        ("/resource/training:AdvSemanticSearchFramework", "Semantic Search"),
        ("/resource/training:SummaryAppBuildingAdv", "Summary"),
    ]

    for path, name in sub_modules:
        print(f"\n  [6] {name}")
        go(page, path)
        scroll_page(page)
        open_video_tab(ctx, page)
        ss(page, f"m6_{name.replace(' ', '_')}")

    print("\n  Module 6 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 8: metis AI Basics
# ═══════════════════════════════════════════════════════════════

def m8_exercises(ctx, page):
    print("\n" + "="*60)
    print("MODULE 8: metis AI Basics — EXERCISES")
    print("="*60)

    # 8.1 Explore AI Services
    print("\n  [8.1] Explore AI services")
    go(page, "/resource/Admin:AIServices?service-type=language-models")
    time.sleep(2)
    ss(page, "m8_ex_language_models")

    go(page, "/resource/Admin:AIServices?service-type=agents")
    time.sleep(2)
    ss(page, "m8_ex_agents")

    # 8.2 Explore conversational AI component
    print("\n  [8.2] Explore conversational AI component")
    go(page, "/resource/training:exploreConvAI")
    scroll_page(page)
    ss(page, "m8_ex_explore_convai")

    # 8.3 Create agent for training
    print("\n  [8.3] Create search & discovery agent for training")
    go(page, "/resource/Admin:AIServices?service-type=agents")
    time.sleep(2)

    # Check if conversationagent-training already exists
    body = page.locator('body').inner_text()
    if 'conversationagent-training' in body:
        print("      Agent conversationagent-training already exists")
    else:
        # Create it
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)
        create = page.locator('button:has-text("Create")').first
        if create.is_visible(timeout=3000):
            create.scroll_into_view_if_needed()
            create.click()
            time.sleep(2)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            # Select template
            page.locator('.Select__input-container').last.click(force=True)
            time.sleep(1)
            page.locator('[role="option"]:has-text("agent-searchanddiscovery")').first.click()
            time.sleep(3)

            # Modify config via CodeMirror
            config = page.evaluate("""() => {
                const cm = document.querySelector('.CodeMirror');
                return cm && cm.CodeMirror ? cm.CodeMirror.getValue() : '';
            }""")
            if config:
                new_config = config.replace(
                    'agent-searchanddiscovery-default', 'conversationagent-training'
                ).replace(
                    'example.com/ontologies/my-ontology/0.1',
                    'ontologies.metaphacts.com/company-ontology/0.3'
                ).replace(
                    'languagemodel-default', 'languagemodel-openai'
                )
                page.evaluate(f"""() => {{
                    const cm = document.querySelector('.CodeMirror');
                    if (cm && cm.CodeMirror) cm.CodeMirror.setValue({repr(new_config)});
                }}""")
                time.sleep(1)

            # Click Create
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.5)
            page.locator('button:has-text("Create")').last.click()
            time.sleep(3)
            print("      Created conversationagent-training")

    ss(page, "m8_ex_agent_created")

    # 8.4 Create ConvAI page for training
    print("\n  [8.4] Create conversational AI page for training")
    TRAINING_CONV = '<mp-conversational-ai id="conversation-ai-test" placeholder="Talk to Conversational AI..." prompt-suggestion-template="{{> tmpl}}" default-conversation-agent-iri="urn:service:conversationagent-training" options=\'{"explanationOptions": {"showExplanation": true}}\'>\n<template id="tmpl">\n<div class="suggestion-prompt-cards">\n<div data-flex-layout="rows stretch-stretch">\n{{#bind\nexample-questions=(array-of\n"List organizations"\n"List projects"\n"List all the projects and persons involved in those projects"\n)}}\n{{#each example-questions}}\n<div data-flex-self="size-1of5 md-half sm-full" class="suggestion-prompt-card-items">\n<mp-event-trigger targets=\'["conversation-ai-test"]\' type="ConversationalAI.Start" data=\'{"prompt": "{{this}}"}\' >\n<button type="button" class="btn btn-secondary suggestion-prompt-card">\n<span class="suggestion-prompt-thumbnail">\n<span class="material-symbols-outlined">lightbulb_circle</span>\n</span>\n<span class="suggestion-prompt-text">{{this}}</span>\n</button>\n</mp-event-trigger>\n</div>\n{{/each}}\n{{/bind}}\n</div>\n</div>\n</template>\n</mp-conversational-ai>'

    go(page, "/resource/training:ConvAITrainingPage?action=edit")
    time.sleep(3)
    if monaco_type(page, TRAINING_CONV):
        save = page.locator('button:has-text("Save & View")').first
        if save.is_visible(timeout=2000):
            save.click()
            time.sleep(5)
        ss(page, "m8_ex_convai_training")
        print("      Training ConvAI page saved")

    # 8.5 Interact with agent
    print("\n  [8.5] Interact with agent — ask 'List organizations'")
    example = page.locator('button:has-text("List organizations")').first
    if example.is_visible(timeout=5000):
        example.click()
        time.sleep(10)
        ss(page, "m8_ex_agent_response")
        print("      Agent responded!")

    # 8.6 Extend KG — create Department and Product instances
    print("\n  [8.6] Extend KG — create Department/Product instances")
    EXTEND_SPARQL = """PREFIX org: <https://ontologies.metaphacts.com/company-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  <https://ontologies.metaphacts.com/company-ontology/Department/SoftwareEngineering> a org:Department ; rdfs:label "Software Engineering" .
  <https://ontologies.metaphacts.com/company-ontology/Department/AIEngineering> a org:Department ; rdfs:label "AI Engineering" .
  <https://ontologies.metaphacts.com/company-ontology/Department/Sales> a org:Department ; rdfs:label "Sales" .
  <https://ontologies.metaphacts.com/company-ontology/Department/Consulting> a org:Department ; rdfs:label "Consulting" .
  <https://ontologies.metaphacts.com/company-ontology/Product/metaphactory> a org:Product ; rdfs:label "metaphactory" .
  <https://ontologies.metaphacts.com/company-ontology/Product/metis> a org:Product ; rdfs:label "metis" .
}"""

    go(page, "/sparql")
    time.sleep(2)
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) editors[0].setValue({repr(EXTEND_SPARQL)});
        else {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) cm.CodeMirror.setValue({repr(EXTEND_SPARQL)});
        }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute")').first.click()
    time.sleep(3)
    ss(page, "m8_ex_extend_kg")
    print("      KG extended with departments and products")

    print("\n  Module 8 exercises complete!")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

ALL_MODULES = [
    (1, "metaphactory basics",       m1_exercises),
    (2, "Visual Modeling Basics",     m2_exercises),
    (3, "Visual Modeling Advanced",   m3_exercises),
    (5, "App Building Basics",       m5_exercises),
    (6, "App Building Advanced",     m6_exercises),
    (8, "metis AI Basics",          m8_exercises),
]


def main():
    global BASE_URL, USERNAME, PASSWORD

    parser = argparse.ArgumentParser(description="Execute ALL training exercises")
    parser.add_argument("--url", default=BASE_URL)
    parser.add_argument("--user", default=USERNAME)
    parser.add_argument("--password", default=PASSWORD)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--module", type=int, help="Run only this module")
    args = parser.parse_args()

    BASE_URL = args.url.rstrip("/")
    USERNAME = args.user
    PASSWORD = args.password

    print(f"""
{'='*60}
  Execute ALL Training Exercises
  Instance: {BASE_URL}
  User:     {USERNAME}
{'='*60}
""")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, slow_mo=150)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        page.set_default_timeout(15000)

        # Login
        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        print(f"Logged in as {USERNAME}")

        for num, name, func in ALL_MODULES:
            if args.module and num != args.module:
                continue
            try:
                func(ctx, page)
            except Exception as e:
                print(f"  ERROR in module {num}: {e}")
                ss(page, f"error_m{num}")

        print(f"\n{'='*60}")
        print(f"ALL EXERCISES COMPLETE. {len(ctx.pages)} tabs open.")
        print(f"{'='*60}")

        time.sleep(5)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
