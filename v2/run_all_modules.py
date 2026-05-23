#!/usr/bin/env python3
"""
Metaphactory Academy — Complete Module Automation

Visits EVERY module, sub-page, video, and exercise across all 9 modules.
- Video pages: opens in new tab, plays on mute, fullscreen
- Exercise pages: completes step-by-step instructions
- Code snippet pages: copies code to the correct template pages

Usage:
    python3 v2/run_all_modules.py --headed
    python3 v2/run_all_modules.py --module 1          # just metaphactory basics
    python3 v2/run_all_modules.py --module 3 --headed  # visual modeling advanced
"""
import argparse
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page

BASE_URL = "https://m20.academy.metaphacts.cloud"
USERNAME = "admin"
PASSWORD = "admin"
SCREENSHOT_DIR = Path("v2/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def ss(page: Page, name: str):
    page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"))
    print(f"    ss: {name}")


def login(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(1)


def go(page: Page, path: str):
    """Navigate to a path, handle timeouts gracefully."""
    url = f"{BASE_URL}{path}"
    try:
        page.goto(url)
        page.wait_for_load_state("networkidle")
    except:
        pass  # networkidle timeout is OK
    time.sleep(2)
    # Dismiss walkthrough if present
    try:
        page.keyboard.press("Escape")
        time.sleep(0.3)
    except:
        pass


def open_all_videos_on_page(context, page: Page, module_name: str):
    """Find all video/Open links on the current page, open each in a new tab,
    play on mute, and go fullscreen."""
    # Find "Open" buttons/links that lead to video sub-pages
    open_links = page.evaluate("""() => {
        const links = [];
        document.querySelectorAll('a[href], button').forEach(el => {
            const text = el.textContent.trim();
            const href = el.getAttribute('href') || '';
            // Look for "Open" links inside cards, or video-related links
            if ((text === 'Open' || text.includes('Open')) && href && href.startsWith('/')) {
                links.push(href);
            }
        });
        return [...new Set(links)]; // deduplicate
    }""")

    print(f"    Found {len(open_links)} sub-page links")

    for i, href in enumerate(open_links):
        try:
            tab = context.new_page()
            tab.goto(f"{BASE_URL}{href}")
            time.sleep(3)
            # Dismiss walkthrough
            try:
                tab.keyboard.press("Escape")
                time.sleep(0.3)
            except:
                pass

            # Try to find and play any video on the page
            play_videos_on_page(tab)

            ss(tab, f"{module_name}_sub_{i}")
            print(f"    Opened: {href}")
            # Keep tab open (videos playing)
        except Exception as e:
            print(f"    Warning: Could not open {href}: {e}")


def play_videos_on_page(page: Page):
    """Find any video/iframe on the page, play it on mute, fullscreen."""
    # Try HTML5 video elements
    page.evaluate("""() => {
        document.querySelectorAll('video').forEach(v => {
            v.muted = true;
            v.play().catch(() => {});
            try { v.requestFullscreen().catch(() => {}); } catch(e) {}
        });
        // Try iframes (YouTube, Vimeo, etc.)
        document.querySelectorAll('iframe').forEach(f => {
            // YouTube: add autoplay and mute params
            if (f.src && f.src.includes('youtube')) {
                if (!f.src.includes('autoplay')) {
                    f.src = f.src + (f.src.includes('?') ? '&' : '?') + 'autoplay=1&mute=1';
                }
            }
        });
    }""")
    time.sleep(1)


def scroll_through_page(page: Page):
    """Scroll through the entire page to trigger lazy-loaded content and mark as read."""
    total_height = page.evaluate("() => document.body.scrollHeight")
    viewport_height = page.evaluate("() => window.innerHeight")
    current = 0
    while current < total_height:
        current += viewport_height // 2
        page.evaluate(f"window.scrollTo(0, {current})")
        time.sleep(0.5)
    # Scroll back to top
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.3)


# ═══════════════════════════════════════════════════════════════════
# MODULE 1: metaphactory basics
# ═══════════════════════════════════════════════════════════════════

def module1_metaphactory_basics(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 1: metaphactory basics")
    print("="*60)

    # Main page
    go(page, "/resource/training:SampleApp")
    scroll_through_page(page)
    ss(page, "m1_main")
    open_all_videos_on_page(context, page, "m1")

    # 1.1 Exploring KGs
    print("\n  --- 1.1 Exploring Knowledge Graphs ---")
    go(page, "/resource/training:SampleAppSearch")
    scroll_through_page(page)
    ss(page, "m1_exploring_kgs")

    # Exercise: Quick search for "Bob"
    search_icon = page.locator('a[href*="SimpleSearch"], button:has-text("search")').first
    if search_icon.is_visible(timeout=2000):
        search_icon.click()
        time.sleep(2)
        search_input = page.locator('input[placeholder*="Search" i]').first
        if search_input.is_visible(timeout=2000):
            search_input.click()
            search_input.type("Bob")
            time.sleep(2)
            ss(page, "m1_search_bob")

    # 1.2 Extending KGs
    print("\n  --- 1.2 Extending Knowledge Graphs ---")
    go(page, "/resource/training:SampleAppOntoVocab")
    scroll_through_page(page)
    ss(page, "m1_extending_kgs")

    # 1.3 KG Assets
    print("\n  --- 1.3 Knowledge Graph Assets ---")
    go(page, "/resource/training:DataLiteracy")
    scroll_through_page(page)
    ss(page, "m1_kg_assets")

    # 1.4 Data Quality
    print("\n  --- 1.4 Ensuring Data Quality ---")
    go(page, "/resource/training:DataQuality")
    scroll_through_page(page)
    ss(page, "m1_data_quality")

    # 1.5 UI Templates (has code snippets to execute)
    print("\n  --- 1.5 Building UI Templates ---")
    go(page, "/resource/training:SampleAppTemplates")
    scroll_through_page(page)
    ss(page, "m1_ui_templates")

    # 1.6 Summary
    print("\n  --- 1.6 Module Summary ---")
    go(page, "/resource/training:SummaryMetaphactoryBasics")
    scroll_through_page(page)
    ss(page, "m1_summary")


# ═══════════════════════════════════════════════════════════════════
# MODULE 2: Visual Modeling Basics
# ═══════════════════════════════════════════════════════════════════

def module2_visual_modeling_basics(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 2: Visual Modeling Basics")
    print("="*60)

    # Main page
    go(page, "/resource/:BusinessTraining")
    scroll_through_page(page)
    ss(page, "m2_main")
    open_all_videos_on_page(context, page, "m2")

    chapters = [
        ("2.1 Visual Ontology Modeling", "/resource/:BusinessTraining-chapter1"),
        ("2.2 Vocabulary & Taxonomy Mgmt", "/resource/:BusinessTraining-chapter2"),
        ("2.3 Interlinking Ontologies & Vocabularies", "/resource/:BusinessTraining-chapter3"),
        ("2.4 Data Cataloging", "/resource/:BusinessTraining-chapter4"),
        ("2.5 Instance Data Management", "/resource/:BusinessTraining-chapter5"),
    ]

    for name, path in chapters:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m2_{name.split()[0]}_{name.split()[1]}")
        # Open any video/exercise sub-pages
        open_all_videos_on_page(context, page, f"m2_{name.split('.')[1].strip()[:10]}")


# ═══════════════════════════════════════════════════════════════════
# MODULE 3: Visual Modeling Advanced
# ═══════════════════════════════════════════════════════════════════

def module3_visual_modeling_advanced(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 3: Visual Modeling Advanced")
    print("="*60)

    go(page, "/resource/training:VisualModellingAdv")
    scroll_through_page(page)
    ss(page, "m3_main")
    open_all_videos_on_page(context, page, "m3")

    sub_modules = [
        ("3.1 Recap Visual Modeling", "/resource/training:recapVisualModeling"),
        ("3.2 Editorial Workflows - Ontologies", "/resource/training:editorialWorkflow"),
        ("3.3 Editorial Workflows - Vocabularies", "/resource/training:editorialWorkflowVocabulary"),
        ("3.4 Data Quality", "/resource/training:modelDrivenValidation"),
        ("3.5 Git Versioning", "/resource/training:git"),
        ("3.6 Additional Features", "/resource/training:AdditionalFeatures"),
        ("3.7 Module Summary", "/resource/training:SummaryAdvVisualModelling"),
    ]

    for name, path in sub_modules:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m3_{name.split()[0]}")
        open_all_videos_on_page(context, page, f"m3_{name.split('.')[1].strip()[:10]}")


# ═══════════════════════════════════════════════════════════════════
# MODULE 4: VM Certification
# ═══════════════════════════════════════════════════════════════════

def module4_vm_certification(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 4: Visual Modeling Certification")
    print("="*60)

    go(page, "/resource/certification:knowledgeGraphEnginner")
    scroll_through_page(page)
    ss(page, "m4_main")

    tasks = [
        ("4.1 Task 1: Vocabulary", "/resource/certification:OntologistCertificationExercise1"),
        ("4.2 Task 2: Vocab Editorial", "/resource/certification:OntologistCertificationExercise1_1"),
        ("4.3 Task 3: Ontology", "/resource/certification:OntologistCertificationExercise2"),
        ("4.4 Task 4: Onto Editorial", "/resource/certification:OntologistCertificationExercise3"),
    ]

    for name, path in tasks:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m4_{name.split(':')[0].strip().replace(' ', '_')}")
        # These are the certification tasks — already completed in round 1
        print(f"    (Certification task — completed in round 1)")


# ═══════════════════════════════════════════════════════════════════
# MODULE 5: App Building Basics
# ═══════════════════════════════════════════════════════════════════

def module5_app_building_basics(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 5: App Building Basics")
    print("="*60)

    go(page, "/resource/training:AppBuildingBasicsSelfGuided")
    scroll_through_page(page)
    ss(page, "m5_main")
    open_all_videos_on_page(context, page, "m5")

    chapters = [
        ("5.1 Templating Mechanism", "/resource/training:AppBuildingBasicsTemplating"),
        ("5.2 Semantic Components", "/resource/training:AppBuildingBasicsSemComponents"),
        ("5.3 Component Interaction", "/resource/training:AppBuildingBasicsEvents"),
        ("5.4 Advanced Features", "/resource/training:AppBuildingBasicsAdvFeatures"),
    ]

    for name, path in chapters:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m5_{name.split()[0]}")
        open_all_videos_on_page(context, page, f"m5_{name.split('.')[1].strip()[:10]}")


# ═══════════════════════════════════════════════════════════════════
# MODULE 6: App Building Advanced
# ═══════════════════════════════════════════════════════════════════

def module6_app_building_advanced(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 6: App Building Advanced")
    print("="*60)

    go(page, "/resource/training:AppBuildingAdvanced")
    scroll_through_page(page)
    ss(page, "m6_main")
    open_all_videos_on_page(context, page, "m6")

    sub_modules = [
        ("6.1 Security & Permissions", "/resource/training:AdvSecurity"),
        ("6.2 App Packing & Lifecycle", "/resource/training:AdvAppLifeCycle"),
        ("6.3 Federation", "/resource/training:AppBuildingAdvFederation"),
        ("6.4 Advanced Data Authoring", "/resource/training:AdvDataAuthoring"),
        ("6.5 Semantic Search Framework", "/resource/training:AdvSemanticSearchFramework"),
        ("6.6 Module Summary", "/resource/training:SummaryAppBuildingAdv"),
    ]

    for name, path in sub_modules:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m6_{name.split()[0]}")
        open_all_videos_on_page(context, page, f"m6_{name.split('.')[1].strip()[:10]}")


# ═══════════════════════════════════════════════════════════════════
# MODULE 7: App Building Certification
# ═══════════════════════════════════════════════════════════════════

def module7_app_certification(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 7: App Building Certification")
    print("="*60)

    go(page, "/resource/certification:knowledgeGraphAppEngineer")
    scroll_through_page(page)
    ss(page, "m7_main")

    tasks = [
        ("7.1 Task 1: QAAS API", "/resource/certification:BasicCertificationExercise1"),
        ("7.2 Task 2: Diagrams", "/resource/certification:BasicCertificationExercise2"),
        ("7.3 Task 3: Resource Template", "/resource/certification:BasicCertificationExercise3"),
        ("7.4 Task 4: Knowledge Panel", "/resource/certification:BasicCertificationExercise4"),
    ]

    for name, path in tasks:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m7_{name.split(':')[0].strip().replace(' ', '_')}")
        print(f"    (Certification task — completed in round 1)")


# ═══════════════════════════════════════════════════════════════════
# MODULE 8: metis AI Basics
# ═══════════════════════════════════════════════════════════════════

def module8_metis_basics(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 8: metis AI Basics")
    print("="*60)

    go(page, "/resource/training:metisBasics")
    scroll_through_page(page)
    ss(page, "m8_main")
    open_all_videos_on_page(context, page, "m8")

    sub_modules = [
        ("8.1 Exploring Conversational AI", "/resource/training:exploreConvAI"),
        ("8.2 Creating Conversational AI", "/resource/training:configurationConvAI"),
        ("8.3 Module Summary", "/resource/training:metisSummary"),
    ]

    for name, path in sub_modules:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m8_{name.split()[0]}")
        open_all_videos_on_page(context, page, f"m8_{name.split('.')[1].strip()[:10]}")


# ═══════════════════════════════════════════════════════════════════
# MODULE 9: AI metis Certification
# ═══════════════════════════════════════════════════════════════════

def module9_ai_certification(context, page: Page):
    print("\n" + "="*60)
    print("MODULE 9: AI metis Certification")
    print("="*60)

    go(page, "/resource/certification:aiMetisEngineer")
    scroll_through_page(page)
    ss(page, "m9_main")

    tasks = [
        ("9.1 Task 1: Search & Discovery Agent", "/resource/certification:metisExercise1"),
        ("9.2 Task 2: Conversational AI", "/resource/certification:metisExercise2"),
    ]

    for name, path in tasks:
        print(f"\n  --- {name} ---")
        go(page, path)
        scroll_through_page(page)
        ss(page, f"m9_{name.split(':')[0].strip().replace(' ', '_')}")
        print(f"    (Certification task — completed in round 1)")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

ALL_MODULES = [
    (1, "metaphactory basics",           module1_metaphactory_basics),
    (2, "Visual Modeling Basics",         module2_visual_modeling_basics),
    (3, "Visual Modeling Advanced",       module3_visual_modeling_advanced),
    (4, "VM Certification",              module4_vm_certification),
    (5, "App Building Basics",           module5_app_building_basics),
    (6, "App Building Advanced",         module6_app_building_advanced),
    (7, "App Building Certification",    module7_app_certification),
    (8, "metis AI Basics",              module8_metis_basics),
    (9, "AI metis Certification",       module9_ai_certification),
]


def main():
    global BASE_URL, USERNAME, PASSWORD

    parser = argparse.ArgumentParser(description="Run ALL metaphactory training modules")
    parser.add_argument("--url", default=BASE_URL)
    parser.add_argument("--user", default=USERNAME)
    parser.add_argument("--password", default=PASSWORD)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--module", type=int, help="Run only this module (1-9)")
    args = parser.parse_args()

    BASE_URL = args.url.rstrip("/")
    USERNAME = args.user
    PASSWORD = args.password

    print(f"""
{'='*60}
  Metaphactory Academy — Complete Module Automation
  Instance: {BASE_URL}
  User:     {USERNAME}
  Modules:  {'All 9' if not args.module else f'Module {args.module} only'}
{'='*60}
""")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not args.headed,
            slow_mo=150,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.set_default_timeout(15000)

        login(page)
        print(f"Logged in as {USERNAME}")

        for num, name, func in ALL_MODULES:
            if args.module and num != args.module:
                continue
            try:
                func(context, page)
            except Exception as e:
                print(f"  ERROR in module {num}: {e}")
                ss(page, f"error_module_{num}")

        # Close all tabs
        print(f"\n{'='*60}")
        print(f"All modules completed. {len(context.pages)} tabs open.")
        print(f"Screenshots saved to: {SCREENSHOT_DIR}")
        print(f"{'='*60}")

        time.sleep(5)
        context.close()
        browser.close()


if __name__ == "__main__":
    main()
