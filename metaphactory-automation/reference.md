# metaphactory Automation — Deep Reference

Battle-tested selectors and quirks for driving the metaphactory UI with
Playwright. Verified against metaphactory **5.10.0** (local Docker) and cloud
training instances. Load this only when you need detail beyond SKILL.md.

---

## The framework quirks (why naive Playwright fails)

metaphactory mixes several UI frameworks. Each needs a different technique.

| Surface | Framework | Reliable technique | What fails |
|---------|-----------|--------------------|------------|
| Login form | plain HTML | `fill()` | — |
| Vocabulary/ontology forms | React | `react_type()` (char-by-char) | `fill()` (no onChange) |
| Type/relation pickers | react-select | force-click `.Select__input-container` then `[role=option]` | clicking the `<input>` |
| SPARQL editor, service config | CodeMirror | `el.CodeMirror.setValue()` via JS | — |
| Page/panel templates | Monaco | `keyboard.type()` after select-all | `window.monaco`, `insert_text`, paste |
| Tree concept menus | custom | per-node `more_vert` | `.first` global |
| Catalog rows | custom (divs) | iterate `more_vert`, match container text | `tr`/card selectors |

### React forms
`page.fill()` sets the DOM value but does NOT fire React's synthetic
`onChange`. The component state stays empty, validation never runs, and the
Create/Save button stays `disabled`. Type character-by-character with a ~30ms
delay (`react_type`). Faster than ~15ms drops events. **Never** `fill('')` a
React input to "clear" it first — that corrupts the controlled state and
disables the form.

### react-select dropdowns
The visible `.Select__input-container` div sits on top of the real `<input>`
and swallows clicks. Force-click the container, wait ~1s for the menu, then
click `[role="option"]:has-text(...)`. Dismiss stray tooltips first with a
`page.mouse.click(10,10)`.

### CodeMirror vs Monaco — they are NOT interchangeable
- **CodeMirror** powers the **SPARQL editor** (`/sparql`), the **AI service
  config** dialog, and Turtle editors. The instance is on the DOM node:
  `document.querySelector('.CodeMirror').CodeMirror.setValue(text)`. Clean and
  reliable. Use `codemirror_set/get/replace`.
- **Monaco** powers **page templates and panel templates** (`?action=edit`).
  `window.monaco` is **undefined** in metaphactory's build, so
  `monaco.editor.getModels()` does not exist. `insert_text()` and clipboard
  paste corrupt `<`, `>`, `{`, `}` (exactly the chars templates need). The only
  reliable path: click editor → `Ctrl/Cmd+A` → `Backspace` → `keyboard.type()`
  with a small delay. Slow; for >5KB chunk the content.

Verify which editor a page uses before automating:
`page.locator('.CodeMirror').count()` vs `page.locator('.monaco-editor').count()`.

### Modals block everything
Leftover modals, dropdown menus, and react-select menus intercept the next
click and produce silent failures. Call `dismiss_modals()` between every
multi-step action. It presses Escape, removes `.dropdown-menu.show`, clicks
close buttons on `.modal.show`/`.overlay-modal.show`, and strips
`.modal-backdrop`.

### networkidle never settles
metaphactory keeps background requests open, so
`wait_for_load_state("networkidle")` times out routinely even though the page
is fully usable. Always wrap it in try/except and continue. Navigate with
`wait_until="domcontentloaded"`.

### IRI conflicts from ghost data
Deleting a vocabulary/ontology leaves data behind in git-backed asset storage;
`DROP GRAPH` does **not** remove it. Re-creating the same title yields an
"already exists" conflict and the Create button stays disabled. Detect it
(button disabled after typing the title) and supply a timestamped unique IRI
(`unique_iri()`), after unchecking the "suggest IRI" box.

---

## Page URL map (`/resource/<id>`)

| Area | URL |
|------|-----|
| Start | `/resource/Start` |
| SPARQL editor | `/sparql` |
| Vocabularies catalog | `/resource/Assets:Vocabularies` |
| Ontologies catalog | `/resource/Assets:Ontologies` |
| Diagrams | `/resource/Assets:Diagrams` |
| Datasets / Named Graphs | `/resource/Assets:Datasets`, `/resource/Assets:NamedGraphs` |
| Query Service (QaaS) | `/resource/Admin:QueryService` |
| AI Services | `/resource/Admin:AIServices` (agents: `?service-type=agents`) |
| All Services | `/resource/Admin:AllServices` |
| Instance Data Manager | `/resource/Admin:InstanceDataManager` |
| Namespaces | `/resource/Admin:Namespaces` |
| Data Import/Export | `/resource/Admin:DataImportExport` |
| Data Quality (SHACL) | `/resource/Admin:DataQuality` |
| Edit any page template | `/resource/<PageId>?action=edit` |
| Edit a panel template | `Template:<...>` / `PanelTemplate:<...>` with `?action=edit` |

---

## Verified selectors

### Login
`input[name="username"]`, `input[name="password"]`, `input[type="submit"]`
(value "Login"). Success → redirect to `/resource/Start`.

### Create-asset dialog (vocabulary / ontology)
- Title: `input[data-testid="asset-title-input"]` (React — use `react_type`)
- Suggest-IRI checkbox: `input[data-testid="suggest-iri-vocabulary"]` /
  `...-ontology`
- Manual IRI (appears only after unchecking suggest):
  `input[data-testid="suggest-iri-vocabulary-input"]`
- Create button: `.modal button:has-text("Create")` (disabled until valid)
- Open the dialog from the catalog's `button:has-text("Create")`.

### Vocabulary editor (SKOS tree)
- Tree panel: `.ontodia-accordion` (concepts are `<a>` inside it)
- Expand toggles: `.LazyTreeSelector--expandToggle`
- Per-concept node: `span.termTree__node` (each holds its own `more_vert`)
- Concept menu: anchor `<a>` → `ancestor::span[@class~="termTree__node"]` →
  `button:has-text("more_vert")`. **Never** use a global `more_vert`.first.
- New top concept: `button:has-text("Create top-level term")`
- Narrower: concept menu → `.dropdown-menu.show a:has-text("Create narrower term")`
- Concept form: `input[placeholder="Enter preferred label here..."]`,
  `textarea[placeholder="Enter definition here..."]`,
  save `.overlay-modal.show button[name="submit"]`
- Status: `.dropdown-menu.show button.termSetStatusButton:has-text("<status>")`
  — statuses: `In review`, `Ready for review`, `Accepted for publication`,
  `Request changes`. These are `<button>`, not `<a>`.

### Ontology editor
- Create entity buttons: `Create Class`, `Create Attribute` (datatype prop),
  `Create Relation` (object prop)
- Entity label: `input[placeholder="Enter label here..."]`
- Confirm: `button[data-testid="confirmation-dialog-button-confirm"]` (a.k.a.
  `Confirm`)
- Tabs: `button:has-text("Classes" | "Attributes" | "Relations" | "Graph")`

### SPARQL editor (`/sparql`)
- Editor: `.CodeMirror` (use `codemirror_set`)
- Run: `button:has-text("Execute")` / `Run`

### Page template editor (`?action=edit`)
- Editor: `.monaco-editor .view-lines` (use `monaco_set_via_keyboard`)
- Save: `button:has-text("Save")`

### Catalog editorial controls
- Per-row menu: iterate `button:has-text("more_vert")`, match the nearest
  `closest('tr, div, li')` text against the asset name (rows are divs, not
  `<tr>`).
- Actions live in `.dropdown-menu.show a:has-text(...)`, sometimes nested under
  a `More` submenu (hover to open). Examples: `Create version...`,
  `Start review request`, `Request publication`, `Approve`, `Publish`,
  `Export`, `Delete`.

### Git versioning
- `button:has-text("More")` → `a:has-text("Git versioning")` →
  `.modal.show button:has-text("Save")` / `Commit`.
- The dialog stays open after Save — `dismiss_modals()` to close it.

---

## Editorial workflow (vocabularies & ontologies)

Workflow controls are on the **catalog page** (per-row `more_vert`), not inside
the editor. Typical lifecycle:

1. Author content in the editor; set per-concept status to `In review` then
   `Accepted for publication` (vocab) — `set_concept_status`.
2. `git_save` to commit.
3. On the catalog: `Start review request` / `Request publication`.
4. A review banner appears inside the asset with Approve/Comment — approve it
   (may require a different reviewer user/role; the "Role assignment" item is in
   the editor's More menu).
5. On the catalog: `Publish`.
6. To revise: `Create version...`, edit, re-review, re-publish.

Editorial tasks often need two roles (author + reviewer), so full end-to-end
automation may require switching logged-in users.

---

## Recommended Playwright context

```python
browser = p.chromium.launch(headless=True, slow_mo=150)
ctx = browser.new_context(
    viewport={"width": 1920, "height": 1080},
    record_video_dir="recordings",
)
ctx.grant_permissions(["clipboard-read", "clipboard-write"])
page = ctx.new_page()
page.set_default_timeout(15000)
```

`slow_mo` makes flakiness debuggable; large viewport keeps catalog buttons in
view; clipboard permissions help any paste fallbacks; video aids post-mortems.

---

## Semantic components reference (for page/panel templates)

Templates are HTML using metaphactory web components. `[[this]]` is the current
resource IRI; `??` inside a query binds to it.

- `<mp-label iri="[[this]]">` — render a resource's label.
- `<semantic-query query="..." template="...">` — run SELECT, render Handlebars
  (`{{var.value}}`, `{{#each bindings}}`).
- `<semantic-table query="..." column-configuration='[{"variableName":"x","displayName":"X"}]'>`.
- `<semantic-search>` family — faceted search.
- `<mp-conversational-ai id="..." default-conversation-agent-iri="urn:service:agent-...">`
  — chat UI bound to an AI agent service.
- `<mp-event-trigger targets='["id"]' type="ConversationalAI.Start" data='{"prompt":"..."}'>`
  — fire a prompt into a conversational-AI component.

Always declare PREFIXes inside each query string. A full crawled component
catalog (every module's example markup) is in the source repo's
`module-catalog.md`.

---

## Common failure → fix

| Symptom | Cause | Fix |
|---------|-------|-----|
| Create/Save button stays disabled | `fill()` didn't fire React onChange | `react_type()` |
| Wrong concept gets the action | global `more_vert.first` | scope to the node (`tree_concept_menu`) |
| Template special chars mangled | Monaco + insert_text/paste | `monaco_set_via_keyboard` |
| `monaco is not defined` | `window.monaco` absent in build | keyboard typing, never the JS API |
| SPARQL setValue no-op | used Monaco API on a CodeMirror editor | `codemirror_set` |
| Next click silently ignored | leftover modal/dropdown | `dismiss_modals()` |
| Navigation hangs | networkidle never settles | wrap in try/except, `domcontentloaded` |
| "already exists", Create disabled | ghost data from deleted asset | `unique_iri()` + uncheck suggest |
| Git dialog blocks next step | dialog stays open after Save | `dismiss_modals()` after `git_save` |
