"""
Template strings for metaphactory page templates and SPARQL queries.

These use the ACTUAL property names from the training instance:
- org:hasMember (not memberOf) — confirmed via instance statements
- org:isInvolvedIn (not hasClient/hasProject) — confirmed via instance statements
- default-conversation-agent-iri uses urn:service: prefix
- mp-conversational-ai needs id, placeholder, default-conversation-agent-iri, options
- mp-event-trigger fires ConversationalAI.Start with prompt data
"""

# ---------------------------------------------------------------------------
# Task 7: Resource Template for Organization
# ---------------------------------------------------------------------------

ORGANIZATION_TEMPLATE = """<div>
<h3><mp-label iri="[[this]]"></mp-label></h3>
<semantic-query query="SELECT ?label WHERE { ?? rdfs:label ?label }" template="<p><b>Label:</b> {{label.value}}</p>"></semantic-query>
<semantic-query query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?memberLabel WHERE { ?? org:hasMember ?member . ?member rdfs:label ?memberLabel }" template="<p><b>Members:</b> {{#each bindings}}{{memberLabel.value}}{{#unless @last}}, {{/unless}}{{/each}}</p>"></semantic-query>
<h4>Project Portfolio</h4>
<semantic-table query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?name WHERE { ?? org:isInvolvedIn ?project . ?project rdfs:label ?name }" column-configuration='[{"variableName": "name", "displayName": "name"}]'></semantic-table>
</div>"""

# ---------------------------------------------------------------------------
# Task 8: Knowledge Panel Template for Organization
# ---------------------------------------------------------------------------

ORGANIZATION_PANEL = """<div>
<h3><mp-label iri="[[this]]"></mp-label></h3>
<semantic-query query="SELECT ?label WHERE { ?? rdfs:label ?label }" template="<p><b>Label:</b> {{label.value}}</p>"></semantic-query>
<semantic-query query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?memberLabel WHERE { ?? org:hasMember ?member . ?member rdfs:label ?memberLabel }" template="<p><b>Members:</b> {{#each bindings}}{{memberLabel.value}}{{#unless @last}}, {{/unless}}{{/each}}</p>"></semantic-query>
<h4>Projects</h4>
<semantic-table query="PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/> SELECT ?name WHERE { ?? org:isInvolvedIn ?project . ?project rdfs:label ?name }" column-configuration='[{"variableName": "name", "displayName": "name"}]'></semantic-table>
</div>"""

# ---------------------------------------------------------------------------
# Task 10: Conversational AI Page
# ---------------------------------------------------------------------------

CONVERSATIONAL_AI_PAGE = """<div class="page">
<h1>Conversational AI</h1>
<mp-conversational-ai id="recipe-ai" placeholder="Talk to the Recipe Search and Discovery Agent..." default-conversation-agent-iri="urn:service:agent-searchanddiscovery-recipes" options='{"explanationOptions": {"showExplanation": true}}'></mp-conversational-ai>
<mp-event-trigger targets='["recipe-ai"]' type="ConversationalAI.Start" data='{"prompt": "Show all the recipes and their ingredients and quantities"}'><button class="btn btn-outline-primary m-1">Show all the recipes and their ingredients and quantities</button></mp-event-trigger>
<mp-event-trigger targets='["recipe-ai"]' type="ConversationalAI.Start" data='{"prompt": "Which recipes belong to the vegan diet?"}'><button class="btn btn-outline-primary m-1">Which recipes belong to the vegan diet?</button></mp-event-trigger>
</div>"""

# ---------------------------------------------------------------------------
# Task 3: Recipe Instance Data (SPARQL INSERT)
# ---------------------------------------------------------------------------

RECIPE_INSTANCES_SPARQL = """PREFIX recipe: <http://ontologies.metaphacts.com/recipes/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

INSERT DATA {
  recipe:VeganDiet a recipe:Diet ; rdfs:label "Vegan" .
  recipe:MediterraneanDiet a recipe:Diet ; rdfs:label "Mediterranean" .
  recipe:AuthorAnna a recipe:Author ; rdfs:label "Anna Smith" .
  recipe:AuthorMarco a recipe:Author ; rdfs:label "Marco Rossi" .
  recipe:CarrotVeg a recipe:Vegetable ; rdfs:label "Carrot" .
  recipe:PotatoVeg a recipe:Vegetable ; rdfs:label "Potato" .
  recipe:OnionVeg a recipe:Vegetable ; rdfs:label "Onion" .
  recipe:GreenBeansVeg a recipe:Vegetable ; rdfs:label "Green beans" .
  recipe:ChickenProtein a recipe:Protein ; rdfs:label "Chicken breast" .
  recipe:TofuProtein a recipe:Protein ; rdfs:label "Tofu" .
  recipe:BasilSeasoning a recipe:Seasoning ; rdfs:label "Basil" .
  recipe:GarlicSeasoning a recipe:Seasoning ; rdfs:label "Garlic" .
  recipe:OliveOilSeasoning a recipe:Seasoning ; rdfs:label "Olive oil" .
  recipe:IU_Pasta_Carrot a recipe:IngredientUsage ; rdfs:label "Carrots" ; recipe:quantity "200" ; recipe:units "grams" ; recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Pasta_GreenBeans a recipe:IngredientUsage ; rdfs:label "Green beans" ; recipe:quantity "150" ; recipe:units "grams" ; recipe:hasItem recipe:GreenBeansVeg .
  recipe:IU_Pasta_Basil a recipe:IngredientUsage ; rdfs:label "Fresh basil" ; recipe:quantity "10" ; recipe:units "leaves" ; recipe:hasItem recipe:BasilSeasoning .
  recipe:IU_Pasta_OliveOil a recipe:IngredientUsage ; rdfs:label "Olive oil" ; recipe:quantity "3" ; recipe:units "tablespoons" ; recipe:hasItem recipe:OliveOilSeasoning .
  recipe:IU_Soup_Potato a recipe:IngredientUsage ; rdfs:label "Potatoes" ; recipe:quantity "300" ; recipe:units "grams" ; recipe:hasItem recipe:PotatoVeg .
  recipe:IU_Soup_Carrot a recipe:IngredientUsage ; rdfs:label "Carrots" ; recipe:quantity "200" ; recipe:units "grams" ; recipe:hasItem recipe:CarrotVeg .
  recipe:IU_Soup_Onion a recipe:IngredientUsage ; rdfs:label "Onion" ; recipe:quantity "1" ; recipe:units "piece" ; recipe:hasItem recipe:OnionVeg .
  recipe:IU_Soup_Garlic a recipe:IngredientUsage ; rdfs:label "Garlic cloves" ; recipe:quantity "3" ; recipe:units "cloves" ; recipe:hasItem recipe:GarlicSeasoning .
  recipe:PastaPrimavera a recipe:Recipe ; rdfs:label "Pasta Primavera" ; recipe:description "Fresh spring vegetables tossed with pasta in olive oil and basil" ; recipe:difficulty "Easy" ; recipe:cookingTime "25 minutes" ; recipe:belongsToDiet recipe:VeganDiet, recipe:MediterraneanDiet ; recipe:hasIngredientUsage recipe:IU_Pasta_Carrot, recipe:IU_Pasta_GreenBeans, recipe:IU_Pasta_Basil, recipe:IU_Pasta_OliveOil ; recipe:hasAuthor recipe:AuthorAnna .
  recipe:VegetableSoup a recipe:Recipe ; rdfs:label "Vegetable Soup" ; recipe:description "Hearty soup with root vegetables, onion and garlic" ; recipe:difficulty "Medium" ; recipe:cookingTime "45 minutes" ; recipe:belongsToDiet recipe:VeganDiet ; recipe:hasIngredientUsage recipe:IU_Soup_Potato, recipe:IU_Soup_Carrot, recipe:IU_Soup_Onion, recipe:IU_Soup_Garlic ; recipe:hasAuthor recipe:AuthorMarco .
}"""

# ---------------------------------------------------------------------------
# Task 5: SPARQL query for QAAS API (all org:Person instances)
# ---------------------------------------------------------------------------

PERSON_QUERY = """PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?label WHERE {
    ?person a org:Person .
    OPTIONAL { ?person rdfs:label ?label }
}
ORDER BY ?label"""
