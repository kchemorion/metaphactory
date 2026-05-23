#!/usr/bin/env python3
"""Create recipe instances via SPARQL INSERT."""
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://m20.academy.metaphacts.cloud"
NS = "http://ontologies.metaphacts.com/recipes/"

INSERT_QUERY = f"""
PREFIX recipe: <{NS}>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {{

  # ── Diets ──
  recipe:VeganDiet a recipe:Diet ;
    rdfs:label "Vegan" .
  recipe:MediterraneanDiet a recipe:Diet ;
    rdfs:label "Mediterranean" .

  # ── Authors ──
  recipe:AuthorAnna a recipe:Author ;
    rdfs:label "Anna Smith" .
  recipe:AuthorMarco a recipe:Author ;
    rdfs:label "Marco Rossi" .

  # ── Vegetables (from vocabulary) ──
  recipe:CarrotVeg a recipe:Vegetable ;
    rdfs:label "Carrot" .
  recipe:PotatoVeg a recipe:Vegetable ;
    rdfs:label "Potato" .
  recipe:OnionVeg a recipe:Vegetable ;
    rdfs:label "Onion" .
  recipe:GreenBeansVeg a recipe:Vegetable ;
    rdfs:label "Green beans" .

  # ── Proteins ──
  recipe:ChickenProtein a recipe:Protein ;
    rdfs:label "Chicken breast" .
  recipe:TofuProtein a recipe:Protein ;
    rdfs:label "Tofu" .

  # ── Seasonings ──
  recipe:BasilSeasoning a recipe:Seasoning ;
    rdfs:label "Basil" .
  recipe:GarlicSeasoning a recipe:Seasoning ;
    rdfs:label "Garlic" .
  recipe:OliveOilSeasoning a recipe:Seasoning ;
    rdfs:label "Olive oil" .

  # ── Ingredient Usages for Recipe 1 ──
  recipe:IU_Pasta_Carrot a recipe:IngredientUsage ;
    rdfs:label "Carrots" ;
    recipe:quantity "200" ;
    recipe:units "grams" ;
    recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Pasta_GreenBeans a recipe:IngredientUsage ;
    rdfs:label "Green beans" ;
    recipe:quantity "150" ;
    recipe:units "grams" ;
    recipe:hasItem recipe:GreenBeansVeg .
  recipe:IU_Pasta_Basil a recipe:IngredientUsage ;
    rdfs:label "Fresh basil" ;
    recipe:quantity "10" ;
    recipe:units "leaves" ;
    recipe:hasItem recipe:BasilSeasoning .
  recipe:IU_Pasta_OliveOil a recipe:IngredientUsage ;
    rdfs:label "Olive oil" ;
    recipe:quantity "3" ;
    recipe:units "tablespoons" ;
    recipe:hasItem recipe:OliveOilSeasoning .

  # ── Ingredient Usages for Recipe 2 ──
  recipe:IU_Soup_Potato a recipe:IngredientUsage ;
    rdfs:label "Potatoes" ;
    recipe:quantity "300" ;
    recipe:units "grams" ;
    recipe:hasItem recipe:PotatoVeg .
  recipe:IU_Soup_Carrot a recipe:IngredientUsage ;
    rdfs:label "Carrots" ;
    recipe:quantity "200" ;
    recipe:units "grams" ;
    recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Soup_Onion a recipe:IngredientUsage ;
    rdfs:label "Onion" ;
    recipe:quantity "1" ;
    recipe:units "piece" ;
    recipe:hasItem recipe:OnionVeg .
  recipe:IU_Soup_Garlic a recipe:IngredientUsage ;
    rdfs:label "Garlic cloves" ;
    recipe:quantity "3" ;
    recipe:units "cloves" ;
    recipe:hasItem recipe:GarlicSeasoning .

  # ── Recipe 1: Pasta Primavera ──
  recipe:PastaPrimavera a recipe:Recipe ;
    rdfs:label "Pasta Primavera" ;
    recipe:description "Fresh spring vegetables tossed with pasta in olive oil and basil" ;
    recipe:difficulty "Easy" ;
    recipe:cookingTime "25 minutes" ;
    recipe:belongsToDiet recipe:VeganDiet ;
    recipe:belongsToDiet recipe:MediterraneanDiet ;
    recipe:hasIngredientUsage recipe:IU_Pasta_Carrot ;
    recipe:hasIngredientUsage recipe:IU_Pasta_GreenBeans ;
    recipe:hasIngredientUsage recipe:IU_Pasta_Basil ;
    recipe:hasIngredientUsage recipe:IU_Pasta_OliveOil ;
    recipe:hasAuthor recipe:AuthorAnna .

  # ── Recipe 2: Vegetable Soup ──
  recipe:VegetableSoup a recipe:Recipe ;
    rdfs:label "Vegetable Soup" ;
    recipe:description "Hearty soup with root vegetables, onion and garlic" ;
    recipe:difficulty "Medium" ;
    recipe:cookingTime "45 minutes" ;
    recipe:belongsToDiet recipe:VeganDiet ;
    recipe:hasIngredientUsage recipe:IU_Soup_Potato ;
    recipe:hasIngredientUsage recipe:IU_Soup_Carrot ;
    recipe:hasIngredientUsage recipe:IU_Soup_Onion ;
    recipe:hasIngredientUsage recipe:IU_Soup_Garlic ;
    recipe:hasAuthor recipe:AuthorMarco .
}}
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=200)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.set_default_timeout(30000)

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill('input[name="username"]', "academyuser")
    page.fill('input[name="password"]', "m20")
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Navigate to SPARQL editor
    page.goto(f"{BASE_URL}/sparql")
    page.wait_for_load_state("networkidle")
    time.sleep(2)

    # Set the INSERT query in Monaco editor
    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{
            editors[0].setValue({repr(INSERT_QUERY)});
        }} else {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{ cm.CodeMirror.setValue({repr(INSERT_QUERY)}); }}
        }}
    }}""")
    time.sleep(1)
    page.screenshot(path="cert-screenshots/instances-query.png")

    # Execute
    execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
    execute_btn.click()
    time.sleep(5)

    page.screenshot(path="cert-screenshots/instances-result.png")
    print("INSERT DATA executed")

    # Verify: count recipe instances
    verify_query = f"""PREFIX recipe: <{NS}>
SELECT ?recipe ?label WHERE {{
    ?recipe a recipe:Recipe .
    ?recipe <http://www.w3.org/2000/01/rdf-schema#label> ?label .
}}"""

    page.evaluate(f"""() => {{
        const editors = window.monaco?.editor?.getEditors?.();
        if (editors && editors.length > 0) {{ editors[0].setValue({repr(verify_query)}); }}
    }}""")
    time.sleep(0.5)
    execute_btn.click()
    time.sleep(3)

    results = page.evaluate("""() => {
        const cells = document.querySelectorAll('table td');
        return Array.from(cells).map(c => c.textContent.trim()).filter(t => t.length > 3);
    }""")
    print(f"\n=== RECIPE INSTANCES ===")
    for r in results[:20]:
        print(f"  {r}")

    page.screenshot(path="cert-screenshots/instances-verified.png")
    time.sleep(2)
    browser.close()
