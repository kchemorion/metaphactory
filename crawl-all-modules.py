#!/usr/bin/env python3
"""Crawl metaphactory training instance and extract all module/task content."""

from playwright.sync_api import sync_playwright
import re

BASE = "https://m20.academy.metaphacts.cloud"

PAGES = [
    # metaphactory basics
    ("Metaphactory Basics", "Main", "/resource/training:SampleApp"),
    ("Metaphactory Basics", "Exploring KGs", "/resource/training:SampleAppSearch"),
    ("Metaphactory Basics", "Extending KGs", "/resource/training:SampleAppOntoVocab"),
    ("Metaphactory Basics", "KG Assets", "/resource/training:DataLiteracy"),
    ("Metaphactory Basics", "Data Quality", "/resource/training:DataQuality"),
    ("Metaphactory Basics", "UI Templates", "/resource/training:SampleAppTemplates"),
    # Visual modeling basics
    ("Visual Modeling Basics", "Main", "/resource/:BusinessTraining"),
    ("Visual Modeling Basics", "Ontology Modeling", "/resource/:BusinessTraining-chapter1"),
    ("Visual Modeling Basics", "Vocabulary Mgmt", "/resource/:BusinessTraining-chapter2"),
    ("Visual Modeling Basics", "Interlinking", "/resource/:BusinessTraining-chapter3"),
    ("Visual Modeling Basics", "Data Cataloging", "/resource/:BusinessTraining-chapter4"),
    ("Visual Modeling Basics", "Instance Data", "/resource/:BusinessTraining-chapter5"),
    # Visual modeling advanced
    ("Visual Modeling Advanced", "Main", "/resource/training:VisualModellingAdv"),
    ("Visual Modeling Advanced", "Recap", "/resource/training:recapVisualModeling"),
    ("Visual Modeling Advanced", "Editorial Ontologies", "/resource/training:editorialWorkflow"),
    ("Visual Modeling Advanced", "Editorial Vocabularies", "/resource/training:editorialWorkflowVocabulary"),
    ("Visual Modeling Advanced", "Data Quality", "/resource/training:modelDrivenValidation"),
    ("Visual Modeling Advanced", "Git Versioning", "/resource/training:git"),
    ("Visual Modeling Advanced", "Additional Features", "/resource/training:AdditionalFeatures"),
    # VM Certification
    ("VM Certification", "Main", "/resource/certification:knowledgeGraphEnginner"),
    ("VM Certification", "Task 1", "/resource/certification:OntologistCertificationExercise1"),
    ("VM Certification", "Task 2", "/resource/certification:OntologistCertificationExercise1_1"),
    ("VM Certification", "Task 3", "/resource/certification:OntologistCertificationExercise2"),
    ("VM Certification", "Task 4", "/resource/certification:OntologistCertificationExercise3"),
    # App building basics
    ("App Building Basics", "Main", "/resource/training:AppBuildingBasicsSelfGuided"),
    ("App Building Basics", "Templating", "/resource/training:AppBuildingBasicsTemplating"),
    ("App Building Basics", "Semantic Components", "/resource/training:AppBuildingBasicsSemComponents"),
    ("App Building Basics", "Events", "/resource/training:AppBuildingBasicsEvents"),
    ("App Building Basics", "Advanced Features", "/resource/training:AppBuildingBasicsAdvFeatures"),
    # App building advanced
    ("App Building Advanced", "Main", "/resource/training:AppBuildingAdvanced"),
    ("App Building Advanced", "Security", "/resource/training:AdvSecurity"),
    ("App Building Advanced", "App Lifecycle", "/resource/training:AdvAppLifeCycle"),
    ("App Building Advanced", "Federation", "/resource/training:AppBuildingAdvFederation"),
    ("App Building Advanced", "Data Authoring", "/resource/training:AdvDataAuthoring"),
    ("App Building Advanced", "Semantic Search", "/resource/training:AdvSemanticSearchFramework"),
    # App Certification
    ("App Certification", "Main", "/resource/certification:knowledgeGraphAppEngineer"),
    ("App Certification", "Task 1", "/resource/certification:BasicCertificationExercise1"),
    ("App Certification", "Task 2", "/resource/certification:BasicCertificationExercise2"),
    ("App Certification", "Task 3", "/resource/certification:BasicCertificationExercise3"),
    ("App Certification", "Task 4", "/resource/certification:BasicCertificationExercise4"),
    # AI / metis
    ("AI metis Basics", "Main", "/resource/training:metisBasics"),
    ("AI metis Basics", "Explore ConvAI", "/resource/training:exploreConvAI"),
    ("AI metis Basics", "Config ConvAI", "/resource/training:configurationConvAI"),
    # AI Certification
    ("AI Certification", "Main", "/resource/certification:aiMetisEngineer"),
    ("AI Certification", "Task 1", "/resource/certification:metisExercise1"),
    ("AI Certification", "Task 2", "/resource/certification:metisExercise2"),
]

def clean_text(text: str) -> str:
    """Clean extracted text: collapse whitespace, remove excessive blank lines."""
    # Collapse multiple spaces/tabs to single space
    text = re.sub(r'[^\S\n]+', ' ', text)
    # Collapse 3+ newlines to 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    results = {}  # module -> [(submodule, content)]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()
        page.set_default_timeout(15000)

        # Login
        print("Logging in...")
        page.goto(f"{BASE}/login")
        page.fill('input[name="username"], #username, input[type="text"]', "admin")
        page.fill('input[name="password"], #password, input[type="password"]', "admin")
        page.click('button[type="submit"], input[type="submit"], .btn-primary')
        page.wait_for_load_state("networkidle")
        print("Logged in successfully.")

        for module, submodule, path in PAGES:
            url = BASE + path
            print(f"Crawling: [{module}] {submodule} -> {path}")
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                # Wait a moment for dynamic content
                page.wait_for_timeout(2000)

                # Try to get main content area, fall back to body
                content_el = None
                for selector in [
                    ".page-content",
                    ".page__body",
                    "main",
                    '[role="main"]',
                    ".container-fluid",
                    "#main-content",
                    ".page",
                    "body",
                ]:
                    el = page.query_selector(selector)
                    if el:
                        content_el = el
                        break

                if content_el:
                    text = content_el.inner_text()
                else:
                    text = page.inner_text("body")

                text = clean_text(text)

                if module not in results:
                    results[module] = []
                results[module].append((submodule, path, text))
                print(f"  -> Got {len(text)} chars")

            except Exception as e:
                print(f"  -> ERROR: {e}")
                if module not in results:
                    results[module] = []
                results[module].append((submodule, path, f"[ERROR: {e}]"))

        browser.close()

    # Write output
    outpath = "/Users/kiptengwer/Documents/metaphactory-tutorial/module-catalog.md"
    with open(outpath, "w") as f:
        f.write("# Metaphactory Training - Complete Module Catalog\n\n")
        f.write("Crawled from: https://m20.academy.metaphacts.cloud\n\n")
        f.write("---\n\n")

        for module in dict.fromkeys(m for m, _, _ in PAGES):  # preserve order
            f.write(f"# {module}\n\n")
            for submodule, path, text in results.get(module, []):
                f.write(f"## {submodule}\n\n")
                f.write(f"**Page:** `{path}`\n\n")
                f.write(text)
                f.write("\n\n---\n\n")

    print(f"\nDone! Output written to {outpath}")
    # Print file size
    import os
    size = os.path.getsize(outpath)
    print(f"File size: {size:,} bytes")

if __name__ == "__main__":
    main()
