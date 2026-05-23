# metaphactory training automation

Playwright automation for the [metaphactory](https://metaphacts.com/) training
and certification tasks. It drives the metaphactory UI end-to-end — creating
vocabularies and ontologies, editing SKOS concept trees, running SPARQL,
editing page/panel templates, configuring QaaS and AI services, and walking the
editorial/git workflow — using a battle-tested helper library that encodes the
platform's framework-specific quirks.

Verified against **metaphactory 5.10.0** (local Docker) and cloud training
instances.

## Layout

| Path | What it is |
|------|-----------|
| `v2/` | The maintained version: helper library + task runner (start here) |
| `v2/mf_helpers.py` | Reusable helpers (login, React forms, tree navigation, editors, editorial workflow) |
| `v2/mf_tasks.py` | One function per certification task |
| `v2/mf_templates.py` | HTML/SPARQL template strings for the templating tasks |
| `v2/run.py` | CLI runner (`--task`, `--track`, `--url`, `--headed`) |
| `metaphactory-automation/` | Claude Code **skill** packaging the helpers + the gotchas (see below) |
| `module-catalog.md` | Full crawl of the training modules and their example markup |
| `tutorial.py`, `training-certification.py` | Earlier monolithic scripts (round 1) |
| `explore-*.py`, `debug-*.py` | One-off exploration/diagnostic scripts |
| `cleanup-*.py`, `nuke-*.py` | Data cleanup utilities |
| `screenshots/`, `recordings/`, `cert-*/` | Captured runs |
| `docs/` | Implementation plans |

## Prerequisites

```bash
pip install playwright
playwright install chromium
```

A reachable metaphactory instance. For local Docker:

```
http://localhost:10214   (login: admin / admin)
```

## Usage

```bash
cd v2

# Run everything against a target instance, watching the browser
python3 run.py --url http://localhost:10214 --user admin --pass admin --headed

# A single certification task
python3 run.py --task 1

# Only one track
python3 run.py --track vm     # vocabulary/ontology tasks
python3 run.py --track app    # app-building tasks
python3 run.py --track ai     # AI / conversational tasks
```

Screenshots land in `v2/screenshots/`, videos in `v2/recordings/`. On failure,
an `error-task-N.png` is captured.

## Why a custom helper library

metaphactory mixes several UI frameworks, and naive Playwright silently fails on
each. The non-obvious rules baked into `v2/mf_helpers.py`:

- **React forms ignore `fill()`** — it doesn't fire React's `onChange`, so
  buttons stay disabled. Type character-by-character (`react_type`).
- **Every tree concept owns its own `more_vert` button** — a global
  `.first` hits the wrong concept. Scope to the concept's `termTree__node`.
- **CodeMirror ≠ Monaco.** The SPARQL editor and service config are CodeMirror
  (`.CodeMirror.setValue` works); page/panel templates are Monaco, where
  `window.monaco` is undefined and only `keyboard.type` reliably enters text.
- **Always `dismiss_modals()` between steps** — stale overlays eat the next
  click.
- **`networkidle` never settles** — wrap waits and continue.
- **IRI conflicts** from ghost data linger after deletes — use a unique IRI.

These patterns are also packaged as a reusable Claude Code skill in
[`metaphactory-automation/`](metaphactory-automation/) — `SKILL.md` (overview +
quick reference), `mf_helpers.py` (the helper library), `reference.md` (full
selector tables and failure→fix guide), and `example.py` (runnable end-to-end
example).

Install it for Claude Code by copying that folder into your skills directory:

```bash
cp -r metaphactory-automation ~/.claude/skills/
```

## Notes

- Selectors are confirmed for metaphactory 5.10.0. On other versions, re-probe
  (e.g. `.CodeMirror` vs `.monaco-editor` counts) before trusting them.
- Editorial-workflow tasks may require two roles (author + reviewer) and some
  manual steps.
- Credentials default to `admin`/`admin` (training defaults) — override via the
  CLI flags for any real instance.
