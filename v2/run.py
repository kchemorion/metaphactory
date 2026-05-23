#!/usr/bin/env python3
"""
Metaphactory Training Certification Automation v2

Usage:
    python3 v2/run.py --headed                          # all tasks, visible browser
    python3 v2/run.py --task 1 --headed                 # single task
    python3 v2/run.py --track vm --headed               # Visual Modeling tasks only
    python3 v2/run.py --track app --headed              # App Building tasks only
    python3 v2/run.py --track ai --headed               # AI metis tasks only
    python3 v2/run.py --url https://other.instance.com  # different instance
"""
import argparse
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from v2.mf_helpers import login, screenshot, dismiss_modals
from v2.mf_tasks import (
    vm_task1_vocabulary, vm_task2_vocab_editorial,
    vm_task3_ontology, vm_task4_onto_editorial,
    app_task5_qaas, app_task6_diagram,
    app_task7_resource_template, app_task8_knowledge_panel,
    ai_task9_agent, ai_task10_conversational_ai,
)

TASKS = [
    (1,  "vm",  "Vegetables Vocabulary",          vm_task1_vocabulary),
    (2,  "vm",  "Vocab Editorial & Versioning",   vm_task2_vocab_editorial),
    (3,  "vm",  "Recipes Ontology",               vm_task3_ontology),
    (4,  "vm",  "Onto Editorial & Versioning",    vm_task4_onto_editorial),
    (5,  "app", "QAAS API",                       app_task5_qaas),
    (6,  "app", "Bob's Diagram",                  app_task6_diagram),
    (7,  "app", "Organization Resource Template",  app_task7_resource_template),
    (8,  "app", "Organization Knowledge Panel",    app_task8_knowledge_panel),
    (9,  "ai",  "Search & Discovery Agent",        ai_task9_agent),
    (10, "ai",  "Conversational AI Interface",     ai_task10_conversational_ai),
]


def main():
    parser = argparse.ArgumentParser(
        description="Metaphactory Training Certification Automation v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--url", default="https://m20.academy.metaphacts.cloud",
                        help="Metaphactory instance URL")
    parser.add_argument("--user", default="admin", help="Username (default: admin)")
    parser.add_argument("--password", default="admin", help="Password (default: admin)")
    parser.add_argument("--headed", action="store_true", help="Show browser window")
    parser.add_argument("--task", type=int, help="Run only this task (1-10)")
    parser.add_argument("--track", choices=["vm", "app", "ai"],
                        help="Run only this track")
    parser.add_argument("--slow-mo", type=int, default=200,
                        help="Milliseconds between Playwright actions (default: 200)")
    args = parser.parse_args()

    base_url = args.url.rstrip("/")

    print(f"""
{'='*60}
  Metaphactory Certification Automation v2
  Instance: {base_url}
  User:     {args.user}
  Mode:     {'headed' if args.headed else 'headless'}
{'='*60}
""")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not args.headed,
            slow_mo=args.slow_mo,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="v2/recordings",
            record_video_size={"width": 1920, "height": 1080},
        )
        context.grant_permissions(["clipboard-read", "clipboard-write"])
        page = context.new_page()
        page.set_default_timeout(15000)

        # Login
        login(page, base_url, args.user, args.password)
        print(f"Logged in as {args.user}\n")

        # Run tasks
        results = []
        for num, track, name, func in TASKS:
            if args.task is not None and num != args.task:
                continue
            if args.track is not None and track != args.track:
                continue

            track_label = {"vm": "Visual Modeling", "app": "App Building", "ai": "AI metis"}[track]
            print(f"{'─'*60}")
            print(f"Task {num} [{track_label}]: {name}")
            print(f"{'─'*60}")

            try:
                func(page, base_url)
                print(f"  ✓ PASS\n")
                results.append((num, name, "PASS"))
            except Exception as e:
                print(f"  ✗ FAIL: {e}\n")
                screenshot(page, f"error-task-{num}")
                dismiss_modals(page)
                results.append((num, name, f"FAIL: {e}"))

                # Recover from browser crash
                if "closed" in str(e).lower() or "target" in str(e).lower():
                    print("  Browser crashed, recovering...")
                    try:
                        context.close()
                    except:
                        pass
                    try:
                        browser.close()
                    except:
                        pass
                    browser = p.chromium.launch(
                        headless=not args.headed,
                        slow_mo=args.slow_mo,
                    )
                    context = browser.new_context(
                        viewport={"width": 1920, "height": 1080},
                        record_video_dir="v2/recordings",
                    )
                    context.grant_permissions(["clipboard-read", "clipboard-write"])
                    page = context.new_page()
                    page.set_default_timeout(15000)
                    login(page, base_url, args.user, args.password)

        # Summary
        print(f"\n{'='*60}")
        print("RESULTS SUMMARY")
        print(f"{'='*60}")
        passed = sum(1 for _, _, r in results if r == "PASS")
        total = len(results)
        for num, name, result in results:
            status = "✓" if result == "PASS" else "✗"
            print(f"  {status} Task {num}: {name}")
        print(f"\n  {passed}/{total} passed")
        print(f"{'='*60}")

        # Cleanup
        try:
            context.close()
            browser.close()
        except:
            pass


if __name__ == "__main__":
    main()
