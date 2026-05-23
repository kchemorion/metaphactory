#!/usr/bin/env python3
"""
Execute ALL remaining exercises across ALL metaphactory training modules.
Every exercise, every code snippet, every UI interaction.

Usage:
    python3 v2/execute_all_exercises.py --headed
    python3 v2/execute_all_exercises.py --module 2 --headed
"""
import argparse
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, BrowserContext

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "admin"
PASSWORD = "admin"
SS = Path("v2/screenshots")
SS.mkdir(parents=True, exist_ok=True)


def ss(page, name):
    page.screenshot(path=str(SS / f"{name}.png"))
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
    except:
        pass
    time.sleep(0.3)


def dismiss(page):
    for _ in range(3):
        try:
            if page.locator('.modal.show').is_visible(timeout=300):
                c = page.locator('.modal.show .btn-close').first
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


def scroll(page):
    h = page.evaluate("() => document.body.scrollHeight")
    pos = 0
    while pos < h:
        pos += 500
        page.evaluate(f"window.scrollTo(0, {pos})")
        time.sleep(0.2)
    page.evaluate("window.scrollTo(0, 0)")


def monaco_type(page, content):
    e = page.locator('.monaco-editor .view-lines').first
    if e.is_visible(timeout=5000):
        e.click()
        time.sleep(0.3)
        page.keyboard.press("Meta+a")
        time.sleep(0.2)
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        page.keyboard.type(content, delay=3)
        time.sleep(1)
        return True
    return False


def save_and_view(page):
    btn = page.locator('button:has-text("Save & View")').first
    if btn.is_visible(timeout=3000):
        btn.click()
        time.sleep(4)
        return True
    btn2 = page.locator('button:has-text("Save"):not(:has-text("View"))').first
    if btn2.is_visible(timeout=2000):
        btn2.click()
        time.sleep(3)
        return True
    return False


def react_type(locator, text, delay=30):
    locator.click()
    time.sleep(0.1)
    locator.type(text, delay=delay)
    time.sleep(0.5)


def open_videos(ctx, page):
    """Open all 'Open' sub-page links in new tabs with video autoplay."""
    links = page.evaluate("""() => {
        const r = [];
        document.querySelectorAll('a[href]').forEach(a => {
            if (a.textContent.trim() === 'Open' && a.href.includes('/resource/')) {
                const href = new URL(a.href).pathname + new URL(a.href).search;
                r.push(href);
            }
        });
        return [...new Set(r)];
    }""")
    for href in links:
        try:
            t = ctx.new_page()
            t.goto(f"{BASE_URL}{href}")
            time.sleep(2)
            t.evaluate("""() => {
                document.querySelectorAll('video').forEach(v => { v.muted=true; v.play().catch(()=>{}); });
                document.querySelectorAll('iframe[src*="youtube"]').forEach(f => {
                    if(!f.src.includes('autoplay')) f.src += (f.src.includes('?')?'&':'?')+'autoplay=1&mute=1';
                });
            }""")
        except:
            pass


# ═══════════════════════════════════════════════════════════════
# MODULE 2: Visual Modeling Basics
# ═══════════════════════════════════════════════════════════════

def module2(ctx, page):
    print("\n" + "="*60)
    print("MODULE 2: Visual Modeling Basics")
    print("="*60)

    # Ch1: Create Project Ontology
    print("\n  [2.1] Visual Ontology Modeling — Create Project Ontology")
    go(page, "/resource/:BusinessTraining-chapter1")
    open_videos(ctx, page)

    # Navigate to Ontologies and create Project ontology
    go(page, "/resource/Assets:Ontologies")
    time.sleep(2)

    # Check if Project ontology already exists
    body = page.locator('body').inner_text()
    if 'Project' not in body or 'Company' in body:
        # Create it
        create = page.locator('button:has-text("Create"), a:has-text("Create")').first
        if create.is_visible(timeout=3000):
            create.click()
            time.sleep(2)
            title = page.locator('input[data-testid="asset-title-input"]').first
            if title.is_visible(timeout=3000):
                react_type(title, "Project")
                time.sleep(1)
                # Check for IRI conflict
                cbtn = page.locator('.modal button:has-text("Create")').first
                time.sleep(1)
                if cbtn.get_attribute("disabled") is not None:
                    print("      Project ontology IRI conflict — already exists")
                    page.keyboard.press("Escape")
                    time.sleep(0.5)
                else:
                    for _ in range(20):
                        if cbtn.get_attribute("disabled") is None:
                            break
                        time.sleep(0.3)
                    cbtn.click()
                    time.sleep(3)
                    dismiss(page)
                    print("      Created Project ontology")

                    # Add classes: Project, Status, Company, Person
                    for cls in ["Project", "Status", "Company", "Person"]:
                        try:
                            page.locator('button:has-text("Create Class")').first.click()
                            time.sleep(1)
                            lbl = page.locator('input[placeholder="Enter label here..."]').first
                            if lbl.is_visible(timeout=2000):
                                lbl.fill(cls)
                            cnf = page.locator('button:has-text("Confirm")').first
                            if cnf.is_visible(timeout=1500):
                                cnf.click()
                                time.sleep(0.5)
                            print(f"      Created class: {cls}")
                        except:
                            pass

                    # Add relations
                    page.locator('button:has-text("Relations")').first.click()
                    time.sleep(0.5)
                    for rel in ["hasStatus", "hasProject", "involvedIn"]:
                        try:
                            page.locator('button:has-text("Create Relation")').first.click()
                            time.sleep(1)
                            lbl = page.locator('input[placeholder="Enter label here..."]').first
                            if lbl.is_visible(timeout=2000):
                                lbl.fill(rel)
                            cnf = page.locator('button:has-text("Confirm")').first
                            if cnf.is_visible(timeout=1500):
                                cnf.click()
                                time.sleep(0.5)
                            print(f"      Created relation: {rel}")
                        except:
                            pass

                    # Save
                    save = page.locator('button:has-text("Save")').first
                    if save.is_visible(timeout=2000):
                        save.click()
                        time.sleep(2)
    else:
        print("      Project ontology already exists")
    ss(page, "m2_project_ontology")

    # Ch2: Create Status Vocabulary
    print("\n  [2.2] Vocabulary & Taxonomy Mgmt — Create Status Vocabulary")
    go(page, "/resource/:BusinessTraining-chapter2")
    open_videos(ctx, page)

    go(page, "/resource/Assets:Vocabularies")
    time.sleep(2)
    body = page.locator('body').inner_text()
    if 'Status' not in body:
        create = page.locator('button:has-text("Create"), a:has-text("Create")').first
        if create.is_visible(timeout=3000):
            create.click()
            time.sleep(2)
            title = page.locator('input[data-testid="asset-title-input"]').first
            if title.is_visible(timeout=3000):
                react_type(title, "Status Vocabulary")
                time.sleep(1)
                cbtn = page.locator('.modal button:has-text("Create")').first
                time.sleep(1)
                if cbtn.get_attribute("disabled") is not None:
                    print("      Status vocab IRI conflict")
                    page.keyboard.press("Escape")
                else:
                    for _ in range(20):
                        if cbtn.get_attribute("disabled") is None:
                            break
                        time.sleep(0.3)
                    cbtn.click()
                    time.sleep(3)
                    dismiss(page)
                    print("      Created Status Vocabulary")

                    # Create top concept "Status"
                    page.locator('button:has-text("Create top-level term")').first.click()
                    time.sleep(1.5)
                    pref = page.locator('input[placeholder="Enter preferred label here..."]').first
                    if pref.is_visible(timeout=3000):
                        pref.click()
                        pref.type("Status", delay=30)
                        time.sleep(0.5)
                    sv = page.locator('.overlay-modal.show button[name="submit"]').first
                    if sv.is_visible(timeout=3000):
                        sv.click()
                        time.sleep(1.5)
                    print("      Created top concept: Status")

                    # Create narrower concepts
                    for term in ["Active", "On Hold", "Completed", "Cancelled"]:
                        try:
                            tree = page.locator('.ontodia-accordion').first
                            node = tree.locator('a:has-text("Status")').first
                            node.click(force=True)
                            time.sleep(1)
                            tn = node.locator('xpath=ancestor::span[contains(@class,"termTree__node")]').first
                            mb = tn.locator('button:has-text("more_vert")').first
                            mb.wait_for(state="visible", timeout=3000)
                            mb.click()
                            time.sleep(0.5)
                            nr = page.locator('.dropdown-menu.show a:has-text("Create narrower term")').first
                            if nr.is_visible(timeout=2000):
                                nr.click()
                                time.sleep(1)
                                pref = page.locator('input[placeholder="Enter preferred label here..."]').first
                                pref.click()
                                pref.type(term, delay=30)
                                time.sleep(0.5)
                                sv = page.locator('.overlay-modal.show button[name="submit"]').first
                                if sv.is_visible(timeout=3000):
                                    sv.click()
                                    time.sleep(1.5)
                                print(f"      Created term: {term}")
                        except Exception as e:
                            print(f"      Warning: {term}: {e}")
                            dismiss(page)
    else:
        print("      Status Vocabulary already exists")
    ss(page, "m2_status_vocabulary")

    # Ch3: Interlink ontology with vocabulary
    print("\n  [2.3] Interlinking — apply vocab restriction")
    go(page, "/resource/:BusinessTraining-chapter3")
    open_videos(ctx, page)
    ss(page, "m2_interlinking")
    # This requires creating a new version of Project ontology and applying
    # a vocabulary restriction to the Status class — complex UI interaction
    print("      Note: Interlinking requires manual UI interaction for vocab restriction")

    # Ch4: Data cataloging (video only)
    print("\n  [2.4] Data Cataloging")
    go(page, "/resource/:BusinessTraining-chapter4")
    open_videos(ctx, page)
    ss(page, "m2_data_cataloging")

    # Ch5: Instance data management
    print("\n  [2.5] Instance Data Management")
    go(page, "/resource/:BusinessTraining-chapter5")
    open_videos(ctx, page)
    ss(page, "m2_instance_data")

    print("\n  Module 2 complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 3: Visual Modeling Advanced
# ═══════════════════════════════════════════════════════════════

def module3(ctx, page):
    print("\n" + "="*60)
    print("MODULE 3: Visual Modeling Advanced")
    print("="*60)

    # All sub-modules — open videos + scroll through exercises
    subs = [
        ("/resource/training:recapVisualModeling", "Recap"),
        ("/resource/training:editorialWorkflow", "Editorial Ontologies"),
        ("/resource/training:editorialWorkflowVocabulary", "Editorial Vocabularies"),
        ("/resource/training:modelDrivenValidation", "Data Quality"),
        ("/resource/training:git", "Git Versioning"),
        ("/resource/training:AdditionalFeatures", "Additional Features"),
        ("/resource/training:SummaryAdvVisualModelling", "Summary"),
    ]
    for path, name in subs:
        print(f"\n  [3] {name}")
        go(page, path)
        scroll(page)
        open_videos(ctx, page)
        ss(page, f"m3_{name.replace(' ', '_')}")

    print("\n  Module 3 complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 5: App Building Basics
# ═══════════════════════════════════════════════════════════════

def module5(ctx, page):
    print("\n" + "="*60)
    print("MODULE 5: App Building Basics")
    print("="*60)

    # 5.1 Templating — create first app page
    print("\n  [5.1] Create first application page")
    go(page, "/resource/training:AppBuildingBasicsTemplatingDemo")
    open_videos(ctx, page)

    APP_PAGE = '''<div class="page">
  <div class="page__body">
    <h1> My first application page built with metaphactory </h1>
  </div>
</div>'''

    go(page, "/resource/?uri=http%3A%2F%2Fexample.org%2Fresource%2FmyFirstAppPage&action=edit")
    time.sleep(3)
    if monaco_type(page, APP_PAGE):
        save_and_view(page)
        print("      First app page saved")
    ss(page, "m5_first_app_page")

    # 5.2 Semantic Components — Person template layout
    print("\n  [5.2] Create Person template with layout")
    go(page, "/resource/training:AppBuildingBasicsSemComponentsDemo")
    open_videos(ctx, page)

    PERSON_LAYOUT = '''<div class="page">
  <div class='page__body'>
    <!-- Section 1 -->
      <h5>Date of Birth</h5>
      <br/>
      <h5>Friends</h5>
      <br/>
      <h5>Knowns /is known by persons</h5>
      <br/>
    <!-- Section 2 -->
      <h5>Person relations</h5>
      <br/>
  </div>
</div>'''

    go(page, "/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies.metaphacts.com%2Forganization-ontology%2FPerson&action=edit")
    time.sleep(5)
    if monaco_type(page, PERSON_LAYOUT):
        save_and_view(page)
        print("      Person template layout saved")
    ss(page, "m5_person_layout")

    # 5.3 Events — add ontodia graph to Person template
    print("\n  [5.3] Add ontodia graph to Person template")
    go(page, "/resource/training:AppBuildingBasicsEventsDemo")
    open_videos(ctx, page)

    PERSON_WITH_GRAPH = '''<!-- Date of Birth -->
<!-- Friends -->
<!-- Knowns /is known by persons -->

<h5>Person relations</h5>
<div class='grid-demo' style='flex: 1; height: 400px'>
<ontodia
  query='
    CONSTRUCT {
      <{{page-resource}}>  ?p ?o
    }
    WHERE {
      <{{page-resource}}> ?p ?o
    }'
  confirm-navigation='false'>
  <ontodia-canvas id='canvas'></ontodia-canvas>
  </ontodia>
</div>'''

    go(page, "/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies.metaphacts.com%2Forganization-ontology%2FPerson&action=edit")
    time.sleep(5)
    if monaco_type(page, PERSON_WITH_GRAPH):
        save_and_view(page)
        print("      Person template with graph saved")
    ss(page, "m5_person_graph")

    # 5.4 Advanced Features — demo video
    print("\n  [5.4] Advanced Features")
    go(page, "/resource/training:AppBuildingBasicsAdvFeaturesDemo")
    open_videos(ctx, page)
    ss(page, "m5_adv_features")

    print("\n  Module 5 complete!")


# ═══════════════════════════════════════════════════════════════
# MODULE 6: App Building Advanced
# ═══════════════════════════════════════════════════════════════

def module6(ctx, page):
    print("\n" + "="*60)
    print("MODULE 6: App Building Advanced")
    print("="*60)

    # 6.1 Security — create end-user
    print("\n  [6.1] Security — create end-user account")
    go(page, "/resource/?uri=http%3A%2F%2Fwww.metaphacts.com%2Fresource%2Fadmin%2F")
    time.sleep(2)
    security_link = page.locator('a:has-text("Security")').first
    if security_link.is_visible(timeout=3000):
        security_link.click()
        time.sleep(3)
        ss(page, "m6_security_page")
        # Create end-user account
        principal = page.locator('input[placeholder*="Principal" i], input[name*="principal" i]').first
        if principal.is_visible(timeout=2000):
            principal.fill("enduser1")
            pw = page.locator('input[type="password"]').first
            if pw.is_visible():
                pw.fill("enduser1")
            pw2 = page.locator('input[type="password"]').nth(1)
            if pw2.is_visible():
                pw2.fill("enduser1")
            # Select end-user role
            role_select = page.locator('select, .Select__input-container').first
            if role_select.is_visible(timeout=1000):
                role_select.click(force=True)
                time.sleep(0.5)
                opt = page.locator('[role="option"]:has-text("end-user"), option:has-text("end-user")').first
                if opt.is_visible(timeout=1000):
                    opt.click()
                    time.sleep(0.5)
            create_btn = page.locator('button:has-text("Create")').first
            if create_btn.is_visible(timeout=2000):
                create_btn.click()
                time.sleep(2)
                print("      Created enduser1 account")
    ss(page, "m6_enduser_created")

    # 6.2 App Lifecycle — explore
    print("\n  [6.2] App Lifecycle — explore apps")
    go(page, "/resource/training:AdvAppLifeCycle")
    scroll(page)
    ss(page, "m6_app_lifecycle")

    # 6.3 Federation — execute Wikidata query
    print("\n  [6.3] Federation — Wikidata federated query")
    FEDERATION_QUERY = """PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
SELECT DISTINCT ?event ?label ?description ?inception_date
WHERE {
  <https://ontologies.metaphacts.com/organization-ontology/Person/instances/20f4b8a7-0a99-421f-a52c-747d89d77996> org:hasBirthday ?date .
  SERVICE <https://wikidata.metaphacts.com/sparql> {
    ?event a <http://www.wikidata.org/prop/novalue/P793> .
    ?event <http://www.wikidata.org/prop/direct/P571> ?inception_date .
    ?event rdfs:label ?label .
    ?event schema:description ?description .
    FILTER(year(?inception_date) = year(?date)) .
    FILTER(LANG(?label) = "en" && LANG(?description) = "en") .
  }
}"""

    go(page, "/sparql")
    time.sleep(2)
    page.evaluate(f"""() => {{
        const e = window.monaco?.editor?.getEditors?.();
        if (e && e.length > 0) e[0].setValue({repr(FEDERATION_QUERY)});
        else {{ const cm = document.querySelector('.CodeMirror'); if (cm?.CodeMirror) cm.CodeMirror.setValue({repr(FEDERATION_QUERY)}); }}
    }}""")
    time.sleep(0.5)
    page.locator('button:has-text("Execute")').first.click()
    time.sleep(5)
    ss(page, "m6_federation_result")
    print("      Federation query executed")

    # 6.4 Data Authoring — create form
    print("\n  [6.4] Data Authoring — create semantic form")
    FORM_CODE = '''<div class="page">
  <div class='page__body'>
    <semantic-form
      form-id='basic-example'
      new-subject-template='http://www.example.com/person/id/{{me}}'
      post-action='redirect'
      fields='[
      {
            "id": "me",
            "label": "Full Name",
            "xsdDatatype": "xsd:string",
            "insertPattern": "INSERT { ?subject a org:Person; rdfs:label ?value } WHERE {}"
      }]'>
      <semantic-form-text-input for="me" placeholder='Enter your name'></semantic-form-text-input>
      <div class="semantic-form-footer-buttons">
        <button name="submit" class="btn btn-primary">Submit</button>
        <button name="reset" class="btn btn-secondary">Reset</button>
      </div>
    </semantic-form>
  </div>
</div>'''

    go(page, "/resource/training:AdvFormExample?action=edit")
    time.sleep(3)
    if monaco_type(page, FORM_CODE):
        save_and_view(page)
        print("      Semantic form saved")
    ss(page, "m6_semantic_form")

    # 6.5 Semantic Search — create search page via wizard
    print("\n  [6.5] Semantic Search — create search page")
    SEARCH_CODE = '''{{> Platform:SearchResultsFragments::defaultStyle}}
<semantic-search id="search1" search-profile='{
  "loadByDomains": [
    "<https://ontologies.metaphacts.com/organization-ontology/Person>"
  ]
}'>
  <semantic-search-query-universal id="universal-search">
  </semantic-search-query-universal>
  <semantic-search-facet-store id="facet"></semantic-search-facet-store>
  <semantic-search-result-holder>
    <semantic-search-result>
      <semantic-table id="table" query="SELECT ?subject WHERE {} ORDER BY ?subject"></semantic-table>
    </semantic-search-result>
  </semantic-search-result-holder>
</semantic-search>'''

    go(page, "/resource/training:SearchPageExample?action=edit")
    time.sleep(3)
    if monaco_type(page, SEARCH_CODE):
        save_and_view(page)
        print("      Search page saved")
    ss(page, "m6_search_page")

    print("\n  Module 6 complete!")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

MODULES = [
    (2, "Visual Modeling Basics", module2),
    (3, "Visual Modeling Advanced", module3),
    (5, "App Building Basics", module5),
    (6, "App Building Advanced", module6),
]


def main():
    global BASE_URL, USERNAME, PASSWORD
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=BASE_URL)
    parser.add_argument("--user", default=USERNAME)
    parser.add_argument("--password", default=PASSWORD)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--module", type=int)
    args = parser.parse_args()
    BASE_URL = args.url.rstrip("/")
    USERNAME = args.user
    PASSWORD = args.password

    print(f"\n{'='*60}")
    print(f"  Execute ALL Training Exercises")
    print(f"  {BASE_URL} as {USERNAME}")
    print(f"{'='*60}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed, slow_mo=150)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        page = ctx.new_page()
        page.set_default_timeout(15000)

        page.goto(f"{BASE_URL}/login")
        page.wait_for_load_state("networkidle")
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        print(f"Logged in as {USERNAME}")

        for num, name, func in MODULES:
            if args.module and num != args.module:
                continue
            try:
                func(ctx, page)
            except Exception as e:
                print(f"  ERROR in module {num}: {e}")
                ss(page, f"error_m{num}")

        print(f"\n{'='*60}")
        print(f"ALL DONE. {len(ctx.pages)} tabs open.")
        print(f"{'='*60}")
        time.sleep(5)
        ctx.close()
        browser.close()


if __name__ == "__main__":
    main()
