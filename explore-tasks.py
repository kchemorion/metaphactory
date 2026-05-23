#!/usr/bin/env python3
"""Explore the actual task/exercise detail pages."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "academyuser"
PASSWORD = "m20"

TASK_PAGES = [
    # KG Engineer Certification (Visual Modeling)
    ("VM-Cert Task 1: Vocabulary", "/resource/certification:OntologistCertificationExercise1"),
    ("VM-Cert Task 2: Vocabulary Editorial", "/resource/certification:OntologistCertificationExercise1_1"),
    ("VM-Cert Task 3: Ontology", "/resource/certification:OntologistCertificationExercise2"),
    ("VM-Cert Task 4: Ontology Editorial", "/resource/certification:OntologistCertificationExercise3"),
    # KG App Engineer Certification
    ("App-Cert Task 1: QAAS API", "/resource/certification:BasicCertificationExercise1"),
    ("App-Cert Task 2: Diagrams", "/resource/certification:BasicCertificationExercise2"),
    ("App-Cert Task 3: Resource Template", "/resource/certification:BasicCertificationExercise3"),
    ("App-Cert Task 4: Knowledge Panel", "/resource/certification:BasicCertificationExercise4"),
    # AI metis Certification
    ("AI-Cert Task 1: S&D Agent", "/resource/certification:metisExercise1"),
    ("AI-Cert Task 2: Conversational AI", "/resource/certification:metisExercise2"),
]

# Also explore the self-guided tutorial sub-pages
TUTORIAL_SUBPAGES = [
    # metaphactory basics sub-modules
    ("Basics: Exploring KGs", "/resource/training:SampleAppSearch"),
    ("Basics: Extending KGs", "/resource/training:SampleAppOntoVocab"),
    ("Basics: KG Assets", "/resource/training:DataLiteracy"),
    ("Basics: Data Quality", "/resource/training:DataQuality"),
    ("Basics: UI Templates", "/resource/training:SampleAppTemplates"),
    # Visual Modeling basics sub-modules
    ("VM-Basics: Ontology Modeling", "/resource/:BusinessTraining-chapter1"),
    ("VM-Basics: Vocabulary Mgmt", "/resource/:BusinessTraining-chapter2"),
    ("VM-Basics: Interlinking", "/resource/:BusinessTraining-chapter3"),
    ("VM-Basics: Data Cataloging", "/resource/:BusinessTraining-chapter4"),
    ("VM-Basics: Instance Data", "/resource/:BusinessTraining-chapter5"),
    # Visual Modeling advanced sub-modules
    ("VM-Adv: Recap", "/resource/training:recapVisualModeling"),
    ("VM-Adv: Editorial Ontologies", "/resource/training:editorialWorkflow"),
    ("VM-Adv: Editorial Vocabularies", "/resource/training:editorialWorkflowVocabulary"),
    ("VM-Adv: Data Quality", "/resource/training:modelDrivenValidation"),
    ("VM-Adv: Git Versioning", "/resource/training:git"),
    ("VM-Adv: Additional Features", "/resource/training:AdditionalFeatures"),
    # App Building basics sub-modules
    ("App-Basics: Templating", "/resource/training:AppBuildingBasicsTemplating"),
    ("App-Basics: Semantic Comps", "/resource/training:AppBuildingBasicsSemComponents"),
    ("App-Basics: Events", "/resource/training:AppBuildingBasicsEvents"),
    ("App-Basics: Adv Features", "/resource/training:AppBuildingBasicsAdvFeatures"),
    # App Building advanced sub-modules
    ("App-Adv: Security", "/resource/training:AdvSecurity"),
    ("App-Adv: App Lifecycle", "/resource/training:AdvAppLifeCycle"),
    ("App-Adv: Federation", "/resource/training:AppBuildingAdvFederation"),
    ("App-Adv: Data Authoring", "/resource/training:AdvDataAuthoring"),
    ("App-Adv: Semantic Search", "/resource/training:AdvSemanticSearchFramework"),
    # metis sub-modules
    ("metis: Explore ConvAI", "/resource/training:exploreConvAI"),
    ("metis: Config ConvAI", "/resource/training:configurationConvAI"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, slow_mo=50)
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

    # First: certification task detail pages
    print("=" * 80)
    print("CERTIFICATION TASK DETAIL PAGES")
    print("=" * 80)

    for task_name, task_path in TASK_PAGES:
        print(f"\n{'─'*60}")
        print(f"TASK: {task_name}")
        print(f"URL: {BASE_URL}{task_path}")
        print(f"{'─'*60}")

        page.goto(f"{BASE_URL}{task_path}")
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        safe_name = task_name.replace(" ", "_").replace(":", "").replace("/", "_")
        page.screenshot(path=f"cert-screenshots/task-{safe_name}.png", full_page=True)

        body_text = page.locator('body').inner_text()
        # Strip nav content
        content = body_text.split("Edit Page")[-1] if "Edit Page" in body_text else body_text
        print(content[:3000])

    # Then: a quick scan of tutorial sub-pages (just headings, not full text)
    print("\n\n" + "=" * 80)
    print("TUTORIAL SUB-PAGES (headings only)")
    print("=" * 80)

    for sub_name, sub_path in TUTORIAL_SUBPAGES:
        page.goto(f"{BASE_URL}{sub_path}")
        page.wait_for_load_state("networkidle")
        time.sleep(1)

        headings = page.locator('h1, h2, h3, h4')
        h_texts = []
        for i in range(headings.count()):
            try:
                text = headings.nth(i).inner_text().strip()
                if text and len(text) < 150:
                    h_texts.append(text)
            except:
                pass
        print(f"\n{sub_name}: {' | '.join(h_texts[:10])}")

    browser.close()
    print("\n\nDONE")
