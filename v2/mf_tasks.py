"""
metaphactory Certification Task Functions (v2)

Implements all 10 certification tasks using helpers from mf_helpers.py
and templates from mf_templates.py. Each function drives a single graded task
end-to-end via sync Playwright.
"""

import time

from v2.mf_helpers import (
    navigate, safe_navigate, screenshot, dismiss_modals, dismiss_walkthrough,
    react_type, react_select_pick, unique_iri, create_asset_dialog,
    tree_click_concept, tree_concept_menu,
    create_top_concept, create_narrower_concept, set_concept_status,
    switch_ontology_tab, create_ontology_class, create_ontology_attribute,
    create_ontology_relation,
    codemirror_set, codemirror_get, codemirror_replace,
    monaco_set_via_keyboard, sparql_update, git_save,
    catalog_more_vert, catalog_action,
)

from v2.mf_templates import (
    ORGANIZATION_TEMPLATE,
    ORGANIZATION_PANEL,
    CONVERSATIONAL_AI_PAGE,
    RECIPE_INSTANCES_SPARQL,
    PERSON_QUERY,
)


# ============================================================================
# VM Task 1: Create Vocabulary
# ============================================================================

def vm_task1_vocabulary(page, base_url: str):
    """Create 'Vegetables for Recipes' vocabulary with full concept hierarchy."""
    print("=== Task 1: Create Vocabulary ===")

    # Navigate to vocabularies catalog
    navigate(page, f"{base_url}/resource/Assets:Vocabularies")
    time.sleep(2)
    dismiss_modals(page)

    # Create vocabulary titled "Vegetables for Recipes"
    print("[task1] Creating vocabulary 'Vegetables for Recipes'...")
    page.locator('button:has-text("Create"), a:has-text("Create")').first.click()
    time.sleep(1)
    create_asset_dialog(page, "Vegetables for Recipes", asset_type="vocabulary")
    time.sleep(2)
    dismiss_modals(page)
    screenshot(page, "task1_vocab_created")

    # Create top concept "Vegetables"
    print("[task1] Creating top concept 'Vegetables'...")
    create_top_concept(page, "Vegetables", "All vegetables used in recipes")
    time.sleep(1)
    screenshot(page, "task1_top_concept")

    # Save to git
    print("[task1] Saving to git (first save)...")
    git_save(page)
    time.sleep(1)

    # Create narrower concepts under Vegetables: Bean, Roots
    print("[task1] Creating narrower concepts under Vegetables...")
    create_narrower_concept(page, "Vegetables", "Bean", "Bean vegetables")
    time.sleep(0.5)
    create_narrower_concept(page, "Vegetables", "Roots", "Root vegetables")
    time.sleep(0.5)

    # Create narrower under Bean: Fava beans, Green beans
    print("[task1] Creating narrower concepts under Bean...")
    create_narrower_concept(page, "Bean", "Fava beans", "Fava bean variety")
    time.sleep(0.5)
    create_narrower_concept(page, "Bean", "Green beans", "Green bean variety")
    time.sleep(0.5)

    # Create narrower under Roots: Potato, Carrot, Onion
    print("[task1] Creating narrower concepts under Roots...")
    create_narrower_concept(page, "Roots", "Potato", "Potato root vegetable")
    time.sleep(0.5)
    create_narrower_concept(page, "Roots", "Carrot", "Carrot root vegetable")
    time.sleep(0.5)
    create_narrower_concept(page, "Roots", "Onion", "Onion root vegetable")
    time.sleep(0.5)

    screenshot(page, "task1_all_concepts")

    # Set all 8 concepts "In review"
    all_concepts = [
        "Vegetables", "Bean", "Roots",
        "Fava beans", "Green beans",
        "Potato", "Carrot", "Onion",
    ]

    print("[task1] Setting all concepts to 'In review'...")
    for concept in all_concepts:
        try:
            set_concept_status(page, concept, "In review")
            print(f"  -> '{concept}' set to In review")
        except Exception as e:
            print(f"  [warn] Failed to set '{concept}' to In review: {e}")
            dismiss_modals(page)

    screenshot(page, "task1_in_review")

    # Set all 8 concepts "Accepted for publication"
    print("[task1] Setting all concepts to 'Accepted for publication'...")
    for concept in all_concepts:
        try:
            set_concept_status(page, concept, "Accepted for publication")
            print(f"  -> '{concept}' accepted for publication")
        except Exception as e:
            print(f"  [warn] Failed to set '{concept}' to Accepted: {e}")
            dismiss_modals(page)

    screenshot(page, "task1_accepted")

    # Save to git (final)
    print("[task1] Saving to git (final save)...")
    git_save(page)
    time.sleep(1)

    screenshot(page, "task1_complete")
    print("=== Task 1 Complete ===")


# ============================================================================
# VM Task 2: Vocabulary Editorial Workflow
# ============================================================================

def vm_task2_vocab_editorial(page, base_url: str):
    """Vocabulary editorial workflow: review, approve, publish, version, add concept."""
    print("=== Task 2: Vocabulary Editorial Workflow ===")
    print("[task2] NOTE: The review request must be started manually by the user")
    print("       before running this task. Use the catalog three-dot menu >")
    print("       'Request publication' on the vocabulary.")

    # Navigate to vocabularies catalog
    navigate(page, f"{base_url}/resource/Assets:Vocabularies")
    time.sleep(2)
    dismiss_modals(page)

    asset_name = "Vegetables for Recipes"

    # Approve the review
    print("[task2] Approving review...")
    try:
        catalog_action(page, asset_name, "Approve")
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Approve failed (review may not be active): {e}")
        dismiss_modals(page)

    # Add comment
    print("[task2] Adding review comment...")
    try:
        comment_input = page.locator(
            'textarea[placeholder*="comment"], textarea[placeholder*="Comment"], '
            'input[placeholder*="comment"]'
        ).first
        if comment_input.count() > 0:
            comment_input.click()
            react_type(comment_input, "Vocabulary looks good, approved.", delay=20)
            # Submit comment
            submit_btn = page.locator(
                'button:has-text("Submit"), button:has-text("Add comment"), '
                'button:has-text("Send")'
            ).first
            if submit_btn.count() > 0 and submit_btn.is_enabled():
                submit_btn.click()
                time.sleep(1)
    except Exception as e:
        print(f"  [warn] Comment failed: {e}")
        dismiss_modals(page)

    # Publish
    print("[task2] Publishing vocabulary...")
    try:
        catalog_action(page, asset_name, "Publish")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Publish failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task2_published")

    # Create new version
    print("[task2] Creating new version...")
    try:
        catalog_action(page, asset_name, "Create version")
        time.sleep(2)
    except Exception as e:
        # Try alternative text
        try:
            catalog_action(page, asset_name, "Create version...")
            time.sleep(2)
        except Exception as e2:
            print(f"  [warn] Create version failed: {e2}")
            dismiss_modals(page)

    screenshot(page, "task2_new_version")

    # Navigate into the vocabulary editor to add Garlic under Roots
    print("[task2] Adding 'Garlic' as narrower concept under Roots...")
    # Click into the vocabulary from catalog
    try:
        page.locator(f'a:has-text("{asset_name}")').first.click()
        time.sleep(2)
        dismiss_modals(page)
    except Exception:
        navigate(page, f"{base_url}/resource/Assets:Vocabularies")
        time.sleep(2)

    try:
        create_narrower_concept(page, "Roots", "Garlic", "Garlic root vegetable")
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Failed to add Garlic: {e}")
        dismiss_modals(page)

    # Set Garlic status through the pipeline
    try:
        set_concept_status(page, "Garlic", "In review")
        set_concept_status(page, "Garlic", "Accepted for publication")
    except Exception as e:
        print(f"  [warn] Failed to set Garlic status: {e}")
        dismiss_modals(page)

    screenshot(page, "task2_garlic_added")

    # Navigate back to catalog for review workflow
    navigate(page, f"{base_url}/resource/Assets:Vocabularies")
    time.sleep(2)
    dismiss_modals(page)

    # Start new review
    print("[task2] Starting new review...")
    try:
        catalog_action(page, asset_name, "Request publication")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Request publication failed: {e}")
        dismiss_modals(page)

    # Approve new review
    print("[task2] Approving new review...")
    try:
        catalog_action(page, asset_name, "Approve")
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Approve failed: {e}")
        dismiss_modals(page)

    # Publish new version
    print("[task2] Publishing new version...")
    try:
        catalog_action(page, asset_name, "Publish")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Publish failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task2_complete")
    print("=== Task 2 Complete ===")


# ============================================================================
# VM Task 3: Create Ontology
# ============================================================================

def vm_task3_ontology(page, base_url: str):
    """Create Recipes ontology with classes, attributes, relations, and instance data."""
    print("=== Task 3: Create Ontology ===")

    # Navigate to ontologies catalog
    navigate(page, f"{base_url}/resource/Assets:Ontologies")
    time.sleep(2)
    dismiss_modals(page)

    # Create ontology
    print("[task3] Creating 'Recipes' ontology...")
    page.locator('button:has-text("Create"), a:has-text("Create")').first.click()
    time.sleep(1)
    create_asset_dialog(page, "Recipes", asset_type="ontology")
    time.sleep(2)
    dismiss_modals(page)
    screenshot(page, "task3_ontology_created")

    # Create classes
    classes = ["Recipe", "Diet", "IngredientUsage", "Vegetable", "Protein", "Seasoning", "Author"]
    print("[task3] Creating classes...")
    for cls in classes:
        try:
            create_ontology_class(page, cls)
            print(f"  -> Created class: {cls}")
        except Exception as e:
            print(f"  [warn] Failed to create class '{cls}': {e}")
            dismiss_modals(page)

    screenshot(page, "task3_classes")

    # Create attributes (deduplicated)
    attributes = ["label", "description", "difficulty", "cookingTime", "quantity", "units"]
    print("[task3] Creating attributes...")
    for attr in attributes:
        try:
            create_ontology_attribute(page, attr)
            print(f"  -> Created attribute: {attr}")
        except Exception as e:
            print(f"  [warn] Failed to create attribute '{attr}': {e}")
            dismiss_modals(page)

    screenshot(page, "task3_attributes")

    # Create relations
    relations = ["belongsToDiet", "hasIngredientUsage", "hasItem", "hasAuthor"]
    print("[task3] Creating relations...")
    for rel in relations:
        try:
            create_ontology_relation(page, rel)
            print(f"  -> Created relation: {rel}")
        except Exception as e:
            print(f"  [warn] Failed to create relation '{rel}': {e}")
            dismiss_modals(page)

    screenshot(page, "task3_relations")

    # Save ontology
    print("[task3] Saving ontology to git...")
    try:
        git_save(page)
    except Exception as e:
        print(f"  [warn] Git save failed: {e}")
        dismiss_modals(page)

    # Create instances via SPARQL
    print("[task3] Creating recipe instances via SPARQL...")
    try:
        sparql_update(page, base_url, RECIPE_INSTANCES_SPARQL)
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] SPARQL update failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task3_instances")

    # Navigate to data quality and screenshot
    print("[task3] Navigating to data quality...")
    navigate(page, f"{base_url}/resource/Admin:DataQuality")
    time.sleep(3)
    dismiss_modals(page)
    screenshot(page, "task3_data_quality")

    print("=== Task 3 Complete ===")


# ============================================================================
# VM Task 4: Ontology Editorial Workflow
# ============================================================================

def vm_task4_onto_editorial(page, base_url: str):
    """Ontology editorial workflow: publish, version, add class+relation, re-publish."""
    print("=== Task 4: Ontology Editorial Workflow ===")

    # Navigate to ontologies catalog
    navigate(page, f"{base_url}/resource/Assets:Ontologies")
    time.sleep(2)
    dismiss_modals(page)

    asset_name = "Recipes"

    # Request publication
    print("[task4] Requesting publication...")
    try:
        catalog_action(page, asset_name, "Request publication")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Request publication failed: {e}")
        dismiss_modals(page)

    # Approve
    print("[task4] Approving review...")
    try:
        catalog_action(page, asset_name, "Approve")
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Approve failed: {e}")
        dismiss_modals(page)

    # Publish
    print("[task4] Publishing ontology...")
    try:
        catalog_action(page, asset_name, "Publish")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Publish failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task4_published")

    # Create new version
    print("[task4] Creating new version...")
    try:
        catalog_action(page, asset_name, "Create version")
        time.sleep(2)
    except Exception as e:
        try:
            catalog_action(page, asset_name, "Create version...")
            time.sleep(2)
        except Exception as e2:
            print(f"  [warn] Create version failed: {e2}")
            dismiss_modals(page)

    screenshot(page, "task4_new_version")

    # Navigate into the ontology to add Menu class and hasRecipe relation
    print("[task4] Opening ontology to add Menu class and hasRecipe relation...")
    try:
        page.locator(f'a:has-text("{asset_name}")').first.click()
        time.sleep(2)
        dismiss_modals(page)
    except Exception:
        navigate(page, f"{base_url}/resource/Assets:Ontologies")
        time.sleep(2)

    # Add Menu class
    try:
        create_ontology_class(page, "Menu")
        print("  -> Created class: Menu")
    except Exception as e:
        print(f"  [warn] Failed to create class 'Menu': {e}")
        dismiss_modals(page)

    # Add hasRecipe relation
    try:
        create_ontology_relation(page, "hasRecipe")
        print("  -> Created relation: hasRecipe")
    except Exception as e:
        print(f"  [warn] Failed to create relation 'hasRecipe': {e}")
        dismiss_modals(page)

    # Save ontology
    print("[task4] Saving ontology to git...")
    try:
        git_save(page)
    except Exception as e:
        print(f"  [warn] Git save failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task4_additions")

    # Navigate back to catalog for review workflow
    navigate(page, f"{base_url}/resource/Assets:Ontologies")
    time.sleep(2)
    dismiss_modals(page)

    # Review and publish new version
    print("[task4] Requesting publication for new version...")
    try:
        catalog_action(page, asset_name, "Request publication")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Request publication failed: {e}")
        dismiss_modals(page)

    print("[task4] Approving new version...")
    try:
        catalog_action(page, asset_name, "Approve")
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Approve failed: {e}")
        dismiss_modals(page)

    print("[task4] Publishing new version...")
    try:
        catalog_action(page, asset_name, "Publish")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Publish failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task4_complete")
    print("=== Task 4 Complete ===")


# ============================================================================
# App Task 5: Query-as-a-Service (QAAS)
# ============================================================================

def app_task5_qaas(page, base_url: str):
    """Set up SPARQL query and expose it as a REST service via QAAS."""
    print("=== Task 5: Query-as-a-Service ===")

    # Navigate to SPARQL editor
    print("[task5] Opening SPARQL editor...")
    navigate(page, f"{base_url}/sparql")
    time.sleep(2)
    dismiss_modals(page)

    # Set the PERSON_QUERY in CodeMirror
    print("[task5] Setting SPARQL query...")
    codemirror_set(page, PERSON_QUERY)
    time.sleep(0.5)

    # Execute the query
    print("[task5] Executing query...")
    run_btn = page.locator(
        'button:has-text("Execute"), button:has-text("Run"), '
        'button[title="Execute"], button[title="Run query"]'
    ).first
    run_btn.click()
    time.sleep(3)
    screenshot(page, "task5_query_result")

    # Save the query
    print("[task5] Saving query...")
    save_btn = page.locator(
        'button:has-text("Save"), button[title="Save"]'
    ).first
    save_btn.click()
    time.sleep(1)

    # Fill query name in save dialog if present
    try:
        query_name_input = page.locator(
            'input[placeholder*="query name"], input[placeholder*="name"], '
            'input[name="queryName"]'
        ).first
        if query_name_input.count() > 0:
            query_name_input.click()
            query_name_input.fill("")
            react_type(query_name_input, "person")
            time.sleep(0.5)
            # Confirm save
            page.locator(
                'button:has-text("Save"), button:has-text("OK"), button:has-text("Confirm")'
            ).first.click()
            time.sleep(1)
    except Exception as e:
        print(f"  [info] Save dialog handling: {e}")
        dismiss_modals(page)

    screenshot(page, "task5_query_saved")

    # Navigate to Admin:QueryService
    print("[task5] Navigating to Query Service admin...")
    navigate(page, f"{base_url}/resource/Admin:QueryService")
    time.sleep(2)
    dismiss_modals(page)

    # Click "Add service"
    print("[task5] Adding new service...")
    add_btn = page.locator(
        'button:has-text("Add service"), button:has-text("Add Service"), '
        'a:has-text("Add service")'
    ).first
    add_btn.click()
    time.sleep(1)

    # Fill REST URL "person"
    print("[task5] Filling service configuration...")
    try:
        url_input = page.locator(
            'input[placeholder*="URL"], input[placeholder*="url"], '
            'input[name="url"], input[placeholder*="REST"]'
        ).first
        if url_input.count() > 0:
            url_input.click()
            url_input.fill("")
            react_type(url_input, "person")
            time.sleep(0.5)
    except Exception as e:
        print(f"  [warn] URL input failed: {e}")

    # Use react_select_pick to select the saved query
    print("[task5] Selecting saved query...")
    try:
        react_select_pick(page, "person")
        time.sleep(0.5)
    except Exception as e:
        print(f"  [warn] Query selection failed: {e}")
        dismiss_modals(page)

    # Fill ACL permission
    print("[task5] Setting ACL permission...")
    try:
        acl_input = page.locator(
            'input[placeholder*="permission"], input[placeholder*="ACL"], '
            'input[name="acl"], input[name="permission"]'
        ).first
        if acl_input.count() > 0:
            acl_input.click()
            acl_input.fill("")
            react_type(acl_input, "qaas:execute")
            time.sleep(0.5)
    except Exception as e:
        print(f"  [warn] ACL input failed: {e}")

    # Save service configuration
    print("[task5] Saving service...")
    save_btn = page.locator(
        'button:has-text("Save"), button:has-text("Create"), button[type="submit"]'
    ).first
    if save_btn.count() > 0 and save_btn.is_enabled():
        save_btn.click()
        time.sleep(2)

    dismiss_modals(page)
    screenshot(page, "task5_complete")
    print("=== Task 5 Complete ===")


# ============================================================================
# App Task 6: Diagram
# ============================================================================

def app_task6_diagram(page, base_url: str):
    """Create a diagram: search for Bob, drag onto canvas, expand, save."""
    print("=== Task 6: Create Diagram ===")

    # Navigate to diagrams
    navigate(page, f"{base_url}/resource/Assets:Diagrams")
    time.sleep(2)
    dismiss_modals(page)

    # Click Create
    print("[task6] Creating new diagram...")
    page.locator('button:has-text("Create"), a:has-text("Create")').first.click()
    time.sleep(3)

    # Dismiss walkthrough
    dismiss_walkthrough(page)
    time.sleep(1)

    screenshot(page, "task6_diagram_opened")

    # Use Instances search (NOT Classes) -- look for "Instances" tab or toggle
    print("[task6] Switching to Instances search...")
    try:
        instances_tab = page.locator(
            'a:has-text("Instances"), button:has-text("Instances"), '
            '[role="tab"]:has-text("Instances"), .nav-link:has-text("Instances")'
        ).first
        if instances_tab.count() > 0:
            instances_tab.click()
            time.sleep(0.5)
    except Exception as e:
        print(f"  [info] Instances tab: {e}")

    # Type "Bob" in search input (placeholder "Search for...")
    print("[task6] Searching for 'Bob'...")
    search_input = page.locator(
        'input[placeholder*="Search for"], input[placeholder*="search"], '
        'input[type="search"]'
    ).first
    search_input.wait_for(timeout=5000)
    search_input.click()
    search_input.fill("")
    react_type(search_input, "Bob")
    time.sleep(0.5)

    # Click search button or press Enter
    try:
        search_btn = page.locator(
            'button:has-text("Search"), button[title="Search"], '
            'button[aria-label="Search"]'
        ).first
        if search_btn.count() > 0:
            search_btn.click()
        else:
            page.keyboard.press("Enter")
    except Exception:
        page.keyboard.press("Enter")

    time.sleep(2)
    screenshot(page, "task6_bob_search")

    # Drag Bob result onto canvas
    print("[task6] Dragging Bob onto canvas...")
    try:
        bob_result = page.locator(
            '[class*="search-result"]:has-text("Bob"), '
            '[class*="element"]:has-text("Bob"), '
            'li:has-text("Bob"), '
            'a:has-text("Bob")'
        ).first
        bob_result.wait_for(timeout=5000)

        # Find the canvas/paper area
        canvas = page.locator(
            '.ontodia-paper, [class*="paper"], canvas, '
            '.ontodia-canvas, [class*="Canvas"]'
        ).first

        # Perform drag and drop
        bob_result.drag_to(canvas)
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Drag failed, trying double-click: {e}")
        try:
            bob_result = page.locator('*:has-text("Bob")').first
            bob_result.dblclick()
            time.sleep(2)
        except Exception:
            pass

    screenshot(page, "task6_bob_on_canvas")

    # Click expand (+) on Bob node
    print("[task6] Expanding Bob node...")
    try:
        expand_btn = page.locator(
            '[class*="expand"], button:has-text("+"), '
            '[class*="ontodia"] button, [title*="expand"], '
            '[title*="Expand"]'
        ).first
        if expand_btn.count() > 0:
            expand_btn.click()
            time.sleep(2)
    except Exception as e:
        print(f"  [warn] Expand failed: {e}")

    screenshot(page, "task6_bob_expanded")

    # Save diagram
    print("[task6] Saving diagram...")
    try:
        save_btn = page.locator(
            'button:has-text("Save"), button[title="Save"]'
        ).first
        save_btn.click()
        time.sleep(1)

        # Fill diagram name if prompted
        name_input = page.locator(
            'input[placeholder*="name"], input[placeholder*="Name"], '
            'input[name="name"], input[name="title"]'
        ).first
        if name_input.count() > 0:
            name_input.click()
            name_input.fill("")
            react_type(name_input, "Bob Diagram")
            time.sleep(0.5)
            page.locator(
                'button:has-text("Save"), button:has-text("OK"), button:has-text("Confirm")'
            ).first.click()
            time.sleep(2)
    except Exception as e:
        print(f"  [warn] Save failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task6_complete")
    print("=== Task 6 Complete ===")


# ============================================================================
# App Task 7: Resource Template
# ============================================================================

def app_task7_resource_template(page, base_url: str):
    """Create Organization resource template using Monaco editor."""
    print("=== Task 7: Resource Template ===")

    # Navigate to Template:...Organization with &action=edit
    template_url = (
        f"{base_url}/resource/?uri=Template%3Ahttps%3A%2F%2Fontologies"
        ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit"
    )
    print(f"[task7] Navigating to template editor...")
    navigate(page, template_url)
    time.sleep(3)
    dismiss_modals(page)

    screenshot(page, "task7_editor_opened")

    # Set template content via Monaco
    print("[task7] Setting template content via Monaco...")
    try:
        monaco_set_via_keyboard(page, ORGANIZATION_TEMPLATE)
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Monaco set failed: {e}")

    screenshot(page, "task7_template_entered")

    # Click "Save" (NOT "Save & View")
    print("[task7] Saving template...")
    try:
        # Look for a Save button that is NOT "Save & View"
        save_buttons = page.locator('button:has-text("Save")')
        count = save_buttons.count()
        for i in range(count):
            btn = save_buttons.nth(i)
            text = btn.inner_text().strip()
            if text == "Save":
                btn.click()
                break
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Save failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task7_complete")
    print("=== Task 7 Complete ===")


# ============================================================================
# App Task 8: Knowledge Panel
# ============================================================================

def app_task8_knowledge_panel(page, base_url: str):
    """Create Organization knowledge panel template using Monaco editor."""
    print("=== Task 8: Knowledge Panel ===")

    # Navigate to PanelTemplate:...Organization with &action=edit
    panel_url = (
        f"{base_url}/resource/?uri=PanelTemplate%3Ahttps%3A%2F%2Fontologies"
        ".metaphacts.com%2Forganization-ontology%2FOrganization&action=edit"
    )
    print(f"[task8] Navigating to panel template editor...")
    navigate(page, panel_url)
    time.sleep(3)
    dismiss_modals(page)

    screenshot(page, "task8_editor_opened")

    # Set panel content via Monaco
    print("[task8] Setting panel content via Monaco...")
    try:
        monaco_set_via_keyboard(page, ORGANIZATION_PANEL)
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Monaco set failed: {e}")

    screenshot(page, "task8_panel_entered")

    # Click "Save"
    print("[task8] Saving panel...")
    try:
        save_buttons = page.locator('button:has-text("Save")')
        count = save_buttons.count()
        for i in range(count):
            btn = save_buttons.nth(i)
            text = btn.inner_text().strip()
            if text == "Save":
                btn.click()
                break
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Save failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task8_complete")
    print("=== Task 8 Complete ===")


# ============================================================================
# AI Task 9: Create AI Agent
# ============================================================================

def ai_task9_agent(page, base_url: str):
    """Create and configure the Search and Discovery AI agent."""
    print("=== Task 9: AI Agent ===")

    # Navigate to AI Services agents page
    print("[task9] Navigating to AI Services (agents)...")
    navigate(page, f"{base_url}/resource/Admin:AIServices?service-type=agents")
    time.sleep(3)
    dismiss_modals(page)

    screenshot(page, "task9_ai_services")

    # Scroll down and click Create
    print("[task9] Scrolling and clicking Create...")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

    create_btn = page.locator(
        'button:has-text("Create"), a:has-text("Create")'
    ).first
    create_btn.click()
    time.sleep(2)
    dismiss_modals(page)

    screenshot(page, "task9_create_dialog")

    # Select template "agent-searchanddiscovery" via React Select
    print("[task9] Selecting agent template...")
    try:
        react_select_pick(page, "agent-searchanddiscovery")
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Template selection failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task9_template_selected")

    # Use codemirror_replace to fix configuration values
    print("[task9] Configuring agent via CodeMirror...")
    time.sleep(1)

    # Fix service ID: "default" -> "recipes"
    try:
        codemirror_replace(page, '"default"', '"recipes"')
        time.sleep(0.5)
    except Exception as e:
        print(f"  [warn] Service ID replace failed: {e}")

    # Fix contextOntology: example URL -> recipes ontology
    try:
        # Get current content to find the exact URL to replace
        current = codemirror_get(page)
        # Find the contextOntology value — it may vary, so search for pattern
        import re
        match = re.search(r'"contextOntology"\s*:\s*"([^"]*)"', current)
        if match:
            old_onto = match.group(1)
            codemirror_replace(
                page, old_onto,
                "http://ontologies.metaphacts.com/recipes/0.1"
            )
            print(f"  -> Replaced contextOntology: {old_onto}")
        else:
            print("  [warn] Could not find contextOntology in config")
    except Exception as e:
        print(f"  [warn] contextOntology replace failed: {e}")

    # Fix languageModel: "default" -> "openai"
    # Note: the first replace already changed "default" to "recipes",
    # so if there was another "default" for languageModel, it may also
    # have been replaced. Let's check and fix.
    try:
        current = codemirror_get(page)
        # Look for languageModel field
        match = re.search(r'"languageModel"\s*:\s*"([^"]*)"', current)
        if match:
            old_lm = match.group(1)
            if old_lm != "openai":
                codemirror_replace(page, f'"languageModel": "{old_lm}"', '"languageModel": "openai"')
                print(f"  -> Replaced languageModel: {old_lm} -> openai")
        else:
            print("  [warn] Could not find languageModel in config")
    except Exception as e:
        print(f"  [warn] languageModel replace failed: {e}")

    screenshot(page, "task9_config_updated")

    # Click Create button in the dialog
    print("[task9] Creating agent...")
    try:
        page.locator(
            'button:has-text("Create"), button:has-text("Save"), button[type="submit"]'
        ).first.click()
        time.sleep(3)
    except Exception as e:
        print(f"  [warn] Create click failed: {e}")
        dismiss_modals(page)

    screenshot(page, "task9_complete")
    print("=== Task 9 Complete ===")


# ============================================================================
# AI Task 10: Conversational AI Page
# ============================================================================

def ai_task10_conversational_ai(page, base_url: str):
    """Create conversational AI page and test with example question."""
    print("=== Task 10: Conversational AI Page ===")

    # Navigate to RecipeAssistant page in edit mode
    print("[task10] Navigating to RecipeAssistant edit page...")
    navigate(page, f"{base_url}/resource/RecipeAssistant?action=edit")
    time.sleep(3)
    dismiss_modals(page)

    screenshot(page, "task10_editor_opened")

    # Set page content via Monaco
    print("[task10] Setting page content via Monaco...")
    try:
        monaco_set_via_keyboard(page, CONVERSATIONAL_AI_PAGE)
        time.sleep(1)
    except Exception as e:
        print(f"  [warn] Monaco set failed: {e}")

    screenshot(page, "task10_content_entered")

    # Click "Save & View"
    print("[task10] Clicking Save & View...")
    try:
        save_view_btn = page.locator('button:has-text("Save & View")').first
        save_view_btn.click()
        time.sleep(3)
    except Exception as e:
        print(f"  [warn] Save & View failed: {e}")
        dismiss_modals(page)

    # Wait for page to render
    time.sleep(3)
    dismiss_modals(page)
    screenshot(page, "task10_page_rendered")

    # Click example question button
    print("[task10] Clicking example question button...")
    try:
        example_btn = page.locator(
            'button:has-text("Show all the recipes")'
        ).first
        example_btn.wait_for(timeout=10000)
        example_btn.click()
        time.sleep(2)
    except Exception as e:
        print(f"  [warn] Example button click failed: {e}")
        # Try the second button
        try:
            page.locator('button:has-text("vegan diet")').first.click()
            time.sleep(2)
        except Exception:
            pass

    # Wait for agent response
    print("[task10] Waiting for agent response...")
    time.sleep(15)

    screenshot(page, "task10_agent_response")
    screenshot(page, "task10_complete")
    print("=== Task 10 Complete ===")
