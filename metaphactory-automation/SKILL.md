---
name: metaphactory-automation
description: Use when automating, scripting, or UI-testing the metaphactory platform with Playwright — creating vocabularies/ontologies, editing SKOS concept trees, running SPARQL, editing page/panel templates, configuring AI services or QaaS, or driving the editorial/git workflow. Also use when metaphactory Playwright scripts fail with disabled buttons, wrong tree menus, mangled template text, stuck modals, or networkidle timeouts.
---

# metaphactory Automation

## Overview

metaphactory's UI mixes plain HTML, React, react-select, CodeMirror, and Monaco
on different screens. Naive Playwright (`fill()`, `.first`, `setValue`) silently
fails because each surface needs a different technique. This skill bundles a
battle-tested helper library (`mf_helpers.py`) and the selectors/quirks that
make automation reliable — learned from real failures and verified against
metaphactory 5.10.0.

**Core principle:** match the technique to the framework behind each screen.
Never assume one input/editor behaves like another.

## When to Use

- Scripting any metaphactory task: vocabularies, ontologies, SPARQL, templates,
  diagrams, QaaS/REST services, AI agents, conversational AI, editorial/git.
- Writing or fixing Playwright tests against a metaphactory instance.
- Debugging symptoms: Create/Save button stays disabled, the wrong tree concept
  gets the action, template `< > { }` get corrupted, `monaco is not defined`,
  clicks silently ignored, navigation hangs on networkidle, "already exists"
  IRI conflicts.

Not for: SPARQL/SHACL/ontology *modeling* itself (use the eaac-kg skill), or
non-metaphactory web automation.

## Quick Reference — technique per surface

| Doing this | Use | Never |
|------------|-----|-------|
| Login | `login()` (`fill` ok here) | — |
| Navigate | `navigate()` / `safe_navigate()` | bare `goto`+networkidle |
| Type into a vocab/ontology form | `react_type()` | `fill()` |
| Pick from a type/relation dropdown | `react_select_pick()` | clicking the `<input>` |
| Create vocabulary/ontology | `create_asset_dialog()` | — |
| Click/menu a tree concept | `tree_click_concept()` / `tree_concept_menu()` | global `more_vert`.first |
| Add concepts | `create_top_concept()` / `create_narrower_concept()` | — |
| Set concept status | `set_concept_status()` | — |
| Ontology class/attr/relation | `create_ontology_class/attribute/relation()` | — |
| SPARQL or service config | `codemirror_set/get/replace()`, `sparql_update()` | Monaco JS API |
| Page/panel templates | `monaco_set_via_keyboard()` | `insert_text`, paste, `window.monaco` |
| Commit | `git_save()` (then it's still open) | forgetting to close it |
| Catalog editorial actions | `catalog_action()` | `tr`/card row selectors |
| Between every step | `dismiss_modals()` | — |

## The non-negotiable gotchas

1. **React forms ignore `fill()`** — it sets the value but not React state, so
   buttons stay disabled. Type char-by-char (`react_type`, ~30ms). Never
   `fill('')` to clear.
2. **Each tree concept owns its `more_vert`** — `page.locator('button:has-text("more_vert")').first`
   hits the wrong concept. Anchor to the concept's `<a>`, walk up to
   `span.termTree__node`, then click that node's `more_vert`.
3. **CodeMirror ≠ Monaco.** SPARQL editor + service config = CodeMirror
   (`el.CodeMirror.setValue` works). Page/panel templates = Monaco, where
   `window.monaco` is undefined and paste/insert corrupt `< > { }` — only
   click→select-all→`keyboard.type` works.
4. **`dismiss_modals()` between every multi-step action** — stale overlays
   silently eat the next click.
5. **networkidle never settles** — wrap waits in try/except; use
   `domcontentloaded`.
6. **Git dialog stays open after Save** — close it (`dismiss_modals`).
7. **IRI conflicts from ghost data** — deleted assets linger in git storage;
   `DROP GRAPH` won't clear them. Detect the disabled Create button and use a
   timestamped `unique_iri()`.

## How to use

1. Copy `mf_helpers.py` next to your script (or import from this skill dir) and
   `from mf_helpers import *`.
2. Follow `example.py` — a complete login → create vocabulary → build hierarchy
   → set status → commit → SPARQL run, using the recommended browser context
   (1920×1080, clipboard perms, `slow_mo`, video).
3. For any selector, page URL, editorial-workflow detail, or semantic-component
   markup, read `reference.md`.

Default local instance: `http://localhost:10214`, `admin`/`admin`.

## Verifying changes

This skill targets a *live* UI that shifts between versions. Before trusting a
selector, probe the running instance:
`page.locator('.CodeMirror').count()` vs `.monaco-editor`, dump candidate
buttons, screenshot on failure. Re-verify against your metaphactory version —
the bundled selectors are confirmed for 5.10.0.

## Common Mistakes

- Treating the SPARQL editor and the template editor the same (one is
  CodeMirror, one is Monaco).
- Using `fill()` because the field "looks like a normal input."
- Looking for editorial controls inside the editor — they're on the catalog
  page's per-row menu.
- Skipping `dismiss_modals()` "just this once" — that's the usual flaky cause.
