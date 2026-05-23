# Metaphactory Training - Complete Module Catalog

Crawled from: https://m20.academy.metaphacts.cloud

---

# Metaphactory Basics

## Main

**Page:** `/resource/training:SampleApp`

metaphactory basics
Goal

What are the capabilities of knowledge graphs? How are they able to support your business' particular use case? This metaphactory Basics module will provide an introductory overview of metaphactory and showcase how innovative knowledge graph-based apps facilitate intuitive data exploration, search and visualization. These tools transform your data into knowledge, which can be shared across the organization and empower intelligent decision-making.

Understanding the use case

This use case focuses on structuring and managing organizational knowledge to improve collaboration, decision-making, and efficiency. Valuable information about people, roles, and projects often remains inaccessible or scattered across different sources. Efficiently capturing and integrating this knowledge helps streamline project assignments and resource planning.

For the purpose of this case, a knowledge graph has been created and loaded into this instance. This knowledge graph covers an ontology, a vocabulary, and instance data.

Learning outcome

Throughout this guided tutorial, you will learn:

key How knowledge graphs can be applied to business use cases.

key How to browse a knowledge graph.

key How to use out-of-box components to search and visualize data.

key How to create or extend a knowledge graph.

key How to check for data quality in a knowledge graph.

key Which customizations are possible and can be included in use-case specific apps.

Structure
Exploring knowledge graphs

Exploring knowledge graphs through search
Exploring knowledge graphs visually
Exploring knowledge graphs using pathfinder

Open

 15 minutes

Extending knowledge graphs

Instance data management
Visual instance authoring

Open

 15 minutes

Knowledge graph assets

Browsing ontologies
Browsing vocabularies
Physical datasource schema and mappings

Open

 20 minutes

Ensuring data quality

Using ontologies to validate data
Using custom test cases to validate data
Exploring the results of validation reports
Validating knowledge graph assets

Open

 20 minutes

Building a simple user interface template

Creating a table
Creating a chart
Creating a form
Creating a conversational AI interface

Open

 45 minutes

Module summary

Module highlights

Open

 5 minutes

---

## Exploring KGs

**Page:** `/resource/training:SampleAppSearch`

Exploring knowledge graphs

metaphactory enables end users to experience and consume data in context. To do that, metaphactory abstracts from the underlying complexity of a knowledge graph, allowing users to consume data intuitively and in context, as well as connect the dots between individual pieces of information.

The following sections highlight the features that support this functionality.

Quick search

Users can explore the knowlege graph by using one of our search options for data exploration.

While most of them require some additional configuration, the out-of-the-box quick search is the quickest way to start navigating your data.

Click on the search located in the application header.
When a search page is loaded, enter the keyword "Bob", and find the relevant results below the search box.

Semantic search

Without the ability to locate and retrieve information from your knowledge graph, you won't be able to extract meaningful insights from it, thus rendering your data useless. metaphactory's semantic search framework enables users to easily retrieve data through a customizable enviroment where they can define an initial query, refine results using facets and visualize them in different ways.

metaphactory provides a unified search framework for querying our use-case data. To use this semantic search, use the link below and enter a specific keyword or explore the graph by selecting one of the domains. In both cases, you can use facets to further refine your search results by expanding relations and looking at related resources.

You can also check the code, as well as try to configure one yourself. This component offers several customizations in both the search profile and the result visualizations.

link Use the search interface to explore the knowledge graph

Visual exploration

Diagrams are a type of asset created at runtime, designed to capture and save graph views of subsets of instance data along with their relationships.

To create a new diagram at runtime, navigate to Assets > Diagrams in the application header. Here, you can view a list of previously saved diagrams or create a new one by clicking on Create in the page header. On the empty canvas, select instances from the left panel and drag them onto the canvas. Click the Save diagram button to persist the diagram under the name you specify.

link Create a new diagram

You can also visualize an existing diagram for the project 'Dimensions Knowledge Graph'.

link Go to the diagram: Dimensions Knowlege Graph Project

Pathfinder

The pathfinding interface allows you to discover paths between two instances in a knowledge graph. metaphactory provides an abstraction over pathfinding features of the underlying graph database and allows to interactively work with the results.

You can access the pathfinding interface from the graph view of a resource or from a persisted diagram; the Pathfinder button is located in the graph view toolbar. On the Pathfinder panel, you can specify both start and end nodes, control the number of resulting paths, explore the results and finally visualize the paths on the canvas.

Building on our initial example, we are interested to discover the paths between the project Dimensions Knowledge Graph and Bob.

link Discover paths between the project Dimensions Knowledge Graph (start node) and Bob (end node)

Documentation

Learn more about the semantic search framework.
Using wizards to bootstrap a search interface.
Technical details on the semantic search component.
Learn more about Pathfinding.
Pathfinding Developer Documentation (recommended for application engineers).

---

## Extending KGs

**Page:** `/resource/training:SampleAppOntoVocab`

Extending knowledge graphs

Data authoring involves the creation, modification and deletion of instances of classes in the knowledge graph. In metaphactory, this can be done entirely model-driven using ontologies.

Below, we included two possible configurations for data authoring in metaphactory along with examples of our use case. Additionally metaphactory provides the highly configurable semantic form component for data authoring, which will be introduced in next steps of this session.

Instance data management

Instance data management is accessible on the resource page of any class in the Instance Usage tab. For example:

Click on the search located in the metaphactory header, and enter 'Project'.
Follow the first link in the result set, whose type is class.
Navigate to the tab "Instance Usage".
Use the Edit button next to an existing instance of this class to edit that instance.
Use the New Instance button to create a new instance for this class.

The following link opens the built-in instance manager for the Project class.

link Add a new project.

Visual instance authoring

Visual instance authoring is an intuitive graphical user interface seamlessly integrating graph visualization capabilities. This interface enables users to choose ontology classes for which instances need to be created. The instance's attributes are entered into a form, and the resulting instance data, along with its associated relations (if applicable), is presented on the canvas.

The following interface shows an example for all of the classes in the organization ontology.

link Add a new organization using the visual instance authoring interface

Documentation

Learn more about Instance data management.
Learn more about visual instance authoring.
Learn more about the graph visualization component.

---

## KG Assets

**Page:** `/resource/training:DataLiteracy`

Knowledge graph assets

metaphactory aims at improving data literacy by providing a machine-interpretable and human-understandable view of your data through intuitive exploration, search and visualization interfaces, all built based on an underlying, common semantic model. In this section, we explore metaphactory's ontology and vocabulary editors in the context of our use case to demonstrate how you can use metaphactory to create a shared understanding of data.

Ontologies

Ontologies in metaphactory are managed as knowledge graph assets.

Navigate to the Assets menu item located in the application header.
Select Ontologies from the dropdown to view the Ontology Catalog, which shows the ontologies that are loaded in the platform.
Open the Organization ontology.
Use the Add all classes button (located at the bottom of the canvas) to populate the diagram with all available classes.
If you wish you can save this as the default diagram.
link Open Organization ontology in the ontology editor

Vocabularies

Vocabularies are also managed as knowledge graph assets in metaphactory. Vocabularies are controlled term collections capturing business-relevant terminology such as synonyms, hyponyms, spelling, and language variations.

Navigate to the Assets menu item located in the application header.
Select Vocabularies from the dropdown to view the Vocabulary Catalog, which shows the vocabularies that are loaded in the platform.
Open the Role vocabulary to view the hierarchy of terms defined in this asset.
link Open Role vocabulary

Physical datasource schema and mappings

Physical Datasource Schemas define the organization's data and its underlying structure, and they are a key part of our new Enterprise Information Architecture (EIA) solution. This solution is designed to establish a semantic knowledge model that integrates enterprise information from multiple data sources and enables answering EIA-specific questions

The solution consists of two main components: physical datasource ontologies, used to represent diverse data sources, such as SQL and JSON, and schema ontology mappings, which define how elements in a physical data schema correspond to classes, attributes and relations in an ontology

To find more details about the set up and how the EIA solution works go to the documentation.

Physical Datasource Schemas
Navigate to the Assets > Physical Datasource Schemas menu item in the application header.
Explore the northwind datasource.
Schema Ontology Mappings
Navigate to the Assets > Physical Datasource Schemas > Mappings menu item in the application header.
Explore the northwind-mappings between northwind datasource and the Organization ontology.

Documentation

Learn more about metaphactory's visual ontology editor.
Blog post: "Connecting the best of both worlds - ontologies and vocabularies in metaphactory".
Learn more about the vocabulary editor.
Blog post: "Vocabulary management with metaphactory".
Build a connected enterprise information architecture with a semantic model.

---

## Data Quality

**Page:** `/resource/training:DataQuality`

Ensuring data quality

In metaphactory, it is possible to check the quality of data managed in the platform, visualize reports showing how the data quality has changed over time, and access links to the validation reports represented in table format. Examples of these validations includes missing properties, such as labels or constraint violations, and minimum and maximum cardinalities, among others.

Model-driven data validation
One way check data quality is to run the test from a specific ontology.

For example, to run a data quality test for the Organization ontology:

Open the Organization ontology.
Select Validate database from the dropdown More located in the editor header.

You could also use the option more_vert from the Ontology Catalog and select Validate database from the dropdown.

Additional data validation options

metaphactory allows you to manage and run custom test cases, which can be created, saved and executed from platform. Unlike the previous specific test, the tests defined here allow you to take full control over the constraints being checked.

Click on the settings button located in the application header.
Click on fact_checkData Quality from the menu.
Go to the "Test Case Management" tab and click play_circle Run Tests

Data validation reports

Once the data quality check has finished, you will be provided with a link to the validation report in a pop-up dialog. You can check the report right away or access it later from settingsSystem Administration >fact_checkData Quality located in the application header.

Let's open the report and explore the results for our use case.

linkOpen data quality report

Asset quality checks

metaphactory provides automatic validation of assets (i.e., ontologies and vocabularies) based on predefined SHACL rule sets. Whenever an ontology is saved in the ontology editor or a vocabulary is modified these rules are checked against the updated asset in the background.

A quality check status button at the top of the Ontology Catalog and Vocabulary Catalog shows the current status of quality checks for all the corresponding assets.

metaphactory comes with a built-in set of rules for both asset types, which can be easily modified or extended.

Documentation

Learn more about data quality.

---

## UI Templates

**Page:** `/resource/training:SampleAppTemplates`

Building a simple user interface template

You can easily build app pages through low-code templates based on standard technologies such as HTML and CSS, integrating built-in metaphactory components and enabling dynamic interaction between multiple components by means of an event system. For example, a prevalent application of this is for defining generic pages that can be automatically applied to entire sets of instances.

Some of the mentioned components and their potential use within a page include semantic tables, semantic charts, and semantic forms, among others. Below, we will review an example for each of them.

Semantic table

The purpose of this semantic table is to display a person's friends. The code below specifies a query that retrieves all the persons connected to others through the known relation.

To visualize this table within a page:

Follow the link below.
Click on edit Edit Page.
Copy the code into the template.
After clicking Save & View the table will display the query results.
link Page for the semantic table
Copy
<h5>Person friends</h5>
 <semantic-table query="
 PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
 SELECT *
 WHERE {
 ?person1 org:knows ?person2 .
 }" column-configuration='[
 {"variableName": "person1", "displayName": "Person"},
 {"variableName": "person2", "displayName": "Friend"}]'>
 </semantic-table>

Semantic chart

Building on the semantic table example, we will use the semantic chart component to create a pie chart illustrating the number of friends per person. The code below defines a query that retrieves all individuals connected to others through the known relation, while also counting the number of friends for each person.

To visualize this chart within a page:

Follow the link below.
Click on edit Edit Page.
Copy the code into the template.
After clicking Save & View the chart will display the query results.
link Page for the semantic chart
Copy
<h5>Number of Friends</h5>
 <semantic-chart type="pie" query="
 PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
 SELECT ?person1 (COUNT(?person2) AS ?known)
 WHERE { 
 ?person1 org:knows ?person2 .
 }
 GROUP BY ?person1" sets='[{"dataSetName": "Number of Friends", "category": "person1", "value": "known"}]'>
 </semantic-chart>

Semantic form

With metaphactory’s highly configurable semantic form component, you can enable end users to add new data to the knowledge graph or edit any existing data. At its simplest, it can automatically generate a form for any class or subject. Moreover, you can also use metaphactory's wizards to bootstrap forms.

As an example, the code below creates a form for a new Project instance. To visualize this form within a page:

Follow the link below.
Click on edit Edit Page.
Copy the code into the template.
After clicking Save & View you will see the authoring form ready to create a new instance data.
Copy
<h5> Project Form </h5>
 <semantic-form for-class="https://ontologies.metaphacts.com/organization-ontology/Project" new-subject-template="https://ontologies.metaphacts.com/organization-ontology/Project/newExampleProject"></semantic-form>
link Page for the Semantic Form

Conversational AI

The Conversational AI is a functionality to chat with a LLM-powered assistant that has access to tools embedded in metaphactory. Using these tools, the assistant is able to answer requests using the data sources configured in metaphactory. To find more information about the set up and how the conversational AI interface component works go to the documentation.

Building a conversational AI interface requires the creation of a template page, and then configuring the conversational AI component.

Follow the link below.
Click on edit Edit Page.
Copy the code into the template.
After clicking Save & View the conversational AI interface will be displyed.
Copy
<mp-conversational-ai id="conversation-ai-test" placeholder="Talk to Conversational AI..." prompt-suggestion-template="{{> tmpl}}" default-conversation-agent-iri="urn:service:conversationagent-default" options='{"explanationOptions": {"showExplanation": true}}'>
 <template id="tmpl">
 <div class="suggestion-prompt-cards">
 <div data-flex-layout="rows stretch-stretch">
 {{#bind
 example-questions=(array-of
 "List organizations."
 "List projects."
 "List organizations and their members."
 )}}

 {{#each example-questions}}
 <div data-flex-self="size-1of5 md-half sm-full" class="suggestion-prompt-card-items">
 <mp-event-trigger targets='["conversation-ai-test"]' type="ConversationalAI.Start" data='{"prompt": "{{this}}"}'>
 <button type="button" class="btn btn-secondary suggestion-prompt-card">
 <span class="suggestion-prompt-thumbnail">
 <span class="material-symbols-outlined">
 lightbulb_circle
 </span>
 </span>
 <span class="suggestion-prompt-text">{{this}}</span>
 </button>
 </mp-event-trigger>
 </div>
 {{/each}}
 {{/bind}}
 </div>
 </div>
 </template>
 </mp-conversational-ai>

link Page for the conversational AI interface
Summary

By following these step-by-step exercises, you have gained an understanding of the basics of creating simple user interface templates in metaphactory, which concludes the metaphactory Basics module. The next step in this Academy covers using a semantic knowledge model to create a common understanding of data. Follow this link to begin the next self-guided module: Visual modeling basics

Documentation

Learn more about configuration options for the semantic table component.
Learn more about semantic chart component.
Read about styling Highcharts in metaphactory.
Blog post: "Data authoring with metaphactory's semantic forms".
Learn more about semantic form component.

---

# Visual Modeling Basics

## Main

**Page:** `/resource/:BusinessTraining`

Business user tutorial to semantic knowledge modeling
Use case & problem statement

Organization and information management

Organizations collect valuable information about projects, members, their roles and others. When captured, this information can be used to create knowledge that brings awareness and support informed decisions.

However, very often, this knowledge remains locked in experts' minds or in lengthy and heterogeneously structured documents that are stored over distributed data sources. Finding and accessing such information when preparing for a new project, for example, is a time-consuming task. This makes it difficult for team members to share information and knowledge, assess the quality and trustworthiness of data, and build on existing expertise.

Tutorial goal

This tutorial aims at demonstrating how semantic knowledge modeling can create a common understanding of the data relevant for organizations, projects, roles and others; and how this knowledge can be surfaced across the entire organization. We will be using metaphactory to:

View, edit and create ontologies and vocabularies and, thus, build a semantic knowledge model for this domain.
Create and manage instance data mapped to the semantic model.

These capabilities can be applied in the same way to support many different types of use cases, from building a semantic layer for enterprise information architecture to supporting digital twin solutions.

Tutorial sample data

For the purposes of this tutorial, we have loaded instance data about organizations and people into the system, as well as the an ontology about organizations and a vocabulary describing roles.

Tutorial structure

Start the tutorial by selecting a module and clicking 'open'. We recommend beginning with the 'Visual ontology modeling' module and continuing with the modules from left-to-right, as the modules build on each other.

As a reminder, you can complete the tutorial at your own pace, pause whenever, and always pick-up where you left off.

Note: Since some videos were recorded with older versions of metaphactory, you may notice minor differences in the user interface. However, the functionality remains the same.
Visual ontology modeling

Exploring existing ontologies
Creating a new ontology

Open

 20-40 mins

Vocabulary & taxonomy management

Exploring and extending an existing vocabulary
Creating a new vocabulary

Open

 20-40 mins

Interlinking ontologies & vocabularies

Connecting a class in an ontology with a controlled vocabulary

Open

 10-20 mins

Data cataloging

Managing dataset metadata

Open

 10 mins

Instance data management

Managing instance data using model-driven semantic forms and visual instance authoring
Adding new instance data to the knowledge graph

Open

 10-20 mins

---

## Ontology Modeling

**Page:** `/resource/:BusinessTraining-chapter1`

Visual ontology modeling
Goal

At the end of this chapter the goal is:

Understand the visual ontology modelling interface
Use the visual ontology modelling interface to create ontologies
Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's visual ontology modeling interface.

Open
Part 2: Demo video

This section will demonstrate how ontologies can be created using metaphactory's visual ontology modeling interface.

Open
Part 3: Exercises

This section will guide you through the process of creating your own ontologies using a series of hands-on exercises.

Open

---

## Vocabulary Mgmt

**Page:** `/resource/:BusinessTraining-chapter2`

Vocabulary & taxonomy management
Goal

At the end of this chapter, you will have created a new vocabulary that provides status terms used for projects.

Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's vocabulary management interface.

Open
Part 2: Demo video

This section will demonstrate vocabularies can be created using metaphactory's vocabulary management interface.

Open
Part 2: Exercises

This section will guide you through the process of creating your own vocabulary using a series of hands-on exercises.

Open

---

## Interlinking

**Page:** `/resource/:BusinessTraining-chapter3`

Interlinking ontologies & vocabularies
Goal

At the end of this chapter, you will have interlinked classes in your Project ontology with the Status vocabulary, thus configuring your system to populate instances of those classes with terms from these vocabularies.

Chapter structure
Part 1: Demo video

This section will provide an overview of how ontologies and vocabularies can be interlinked in metaphactory.

Open
Part 2: Exercises

This section will guide you through the process of linking a class in your ontology with a controlled vocabulary.

Open

---

## Data Cataloging

**Page:** `/resource/:BusinessTraining-chapter4`

Data cataloging
Goal

At the end of this chapter, you will have been introduced to metaphactory's data cataloging functionality.

Chapter structure
Demo video

This section will introduce you to metaphactory's data cataloging capabilities that allow you to capture and manage metadata about your data assets.

Open

---

## Instance Data

**Page:** `/resource/:BusinessTraining-chapter5`

Instance data management
Goal

At the end of this chapter, you will have extended your knowledge graph by adding new instances.

Chapter structure
Part 1: Demo video

This section will explain how you can use metaphactory's semantic forms and visual instance authoring component to edit and add new data to your knowledge graph.

Open
Part 2: Exercises

This section will guide you through the process of adding new instance data to your knowledge graph.

Open

---

# Visual Modeling Advanced

## Main

**Page:** `/resource/training:VisualModellingAdv`

Visual modeling advanced
Goal

In this module, you'll look at advanced ontology modeling and vocabulary management features that metaphactory offers for creating a common understanding of domain data. In particular, this module explores topics related to ontology and vocabulary versioning, and goes into detail on how these may transition through a defined set of statuses to support their entire development and publishing lifecycle.

Understanding the use case

Now that you have created an ontology about a project, let's say that we have new requirements and need a new version of this ontology.

The editorial workflow has the following steps: creating a new ontology or a new version of an existing ontology, modifying it, reviewing it, and finally publishing it. After that, we will see how how to access the different versions of an ontology.

Learning outcome

Throughout this guided tutorial, you will learn:

key How to manage multiple versions of the same ontology in the same database.

key How to publish an ontology while other users are working on a new version.

key How to manipulate assets in metaphactory.

Structure
Recap visual modeling

Exploration of the Status Vocabulary
Exploration of the Project Ontology
Interlinking of the Status vocabulary and the Project Ontology

Open

 10 minutes

Editorial workflows and versioning for Ontologies

Adding yourself to editorial workflows
Creating an ontology version
Role assignments
Starting a review request
Reviewing an ontology
Publishing an ontology
Browsing the ontology model outside of the ontology editor

Open

 40 minutes

Editorial workflows and versioning for Vocabularies

Creating a vocabulary version
Role assignments
Starting a review request
Reviewing a vocabulary
Publishing a vocabulary

Open

 40 minutes

Data quality

Model-driven data validation
Asset quality checks

Open

 20 minutes

Git versioning

Knowledge graph assets on git
Saving ontologies to Git
Saving vocabularies to Git

Open

 20 minutes

Additional features

Disjunctions in relation ranges
Imports Analysis
Review policies
Initial views
Events & Notifications
Collaborative editing
Diagrams
Provenance
RDF turtle editor
Importing & Exporting Assets

Open

 15 minutes

Module summary

Module highlights

Open

 5 minutes

---

## Recap

**Page:** `/resource/training:recapVisualModeling`

Recap visual modeling

This module aims at revisiting the basics of visual modeling.

The basics of visual modeling can be revisited at Visual modeling basics .

This training session is based on the Project ontology and Status vocabulary which are created in the self-guided tutorial. These assets can be downloaded from the LMS system and imported into the training instances.

Overview

Catalogs list all existing ontologies and vocabularies in metaphactory. To open catalogs and explore or edit the assets loaded in the platform, you can follow these steps:

Navigate to the Assets menu item located in the application header.
Select Ontologies/Vocabularies from the dropdown.

To start, you can click on one of the assets and explore it. If you want to create a new assets from scratch, click on Create. Assets can also be imported to the catalog by using the Import option.

Once an asset is loaded, you can go through the main funcionalities provided by the metaphactory's editors. In case of ontologies, the editor provides capabilities for viewing and editing metadata, displaying, navigating and searching the class, property and attribute hierarchies, creating and modifying these ontology elements, and accessing Git for asset management.

On the other hand, the vocabulary editor provides: viewing and editing metadata, navigating and searching, exploring term hierarchies, modifying vocabulary term, or creating and modifying terms and collections.

Exercise 1: Exploration of the Status Vocabulary

In this exercise, we will review the Status vocabulary created in the previous session.

Navigate to the vocabularies catalog.
Open the Status vocabulary to explore its elements, including its metadata, terms and collections.

Exercise 2: Exploration of the Project Ontology

In this exercise, we will review the Project Ontology created in the previous session.

Navigate to the ontologies catalog.
Open the Project Ontology to explore its elements, including its metadata, as well as the created classes, relations and attributes.

Exercise 3: Interlinking of the Status vocabulary and the Project Ontology

In this exercise, we will review the Interlinking of the Status vocabulary and the Project Ontology .

Navigate to the ontologies catalog.
Open the Project ontology.
Review the vocabulary restriction on the Status class.
Create an instance data of the class Project and populate the has status field using the Status Vocabulary.

Summary

Throughout these exercises, you have had the chance to revisit the basics of visual modeling in metaphactory.

With these basic concepts in place, the next steps include a dive-deep into the advanced capabilities of metaphactory for visual modeling and asset management.

Documentation

Semantic Modeling Guidelines.
Learn more about metaphactory's visual ontology editor.
Learn more about metaphactory's asset management.
SHACL (Shapes Constraint Language).
OWL (Web Ontology Language).

---

## Editorial Ontologies

**Page:** `/resource/training:editorialWorkflow`

Editorial workflows and versioning for ontologies

metaphactory supports an editorial workflow for ontologies. Ontologies may transition through a defined set of statuses to support the lifecycle from development to publishing, as well as creating new versions of ontologies.

The editorial workflow may work independently of Git version control. The metaphactory UI offers the option to save an ontology to a configured Git repository in every phase of the workflow.
Workflow overview

Ontologies may transition through a defined set of statuses to support the development and publishing lifecycle:

 In development: The ontology is in active development.
 In review: The ontology is being reviewed by other knowledge graph engineers.
 Ready to be published: (Optional) Reviews are completed and the ontology has been marked as ready to be published.
 Published: The ontology has been published.
 Archived: The ontology has been replaced by a newer version of the same ontology.

To see the diagram of the editorial workflow states and transitions, please check the documentation here .

Exercise 1: Adding yourself to editorial workflows

Before being able to review ontologies, or be assigned as owners/authors of an ontology, you need to add yourself to be part of editorial workflows.

Follow the steps below to add the user knowledge-steward to editorial workflows.

Logout of metaphactory.
Login with the username: knowledge-steward and password: knowledge-steward .
Navigate to the ontologies catalog.
A banner will be displayed stating that you are not part of the editorial workflows.
Go to the user profile page and select the option to add yourself to editorial workflows.

The user knowledge-steward is now part of the editorial workflow. Note that this can also be pre-populated, or customized as described in the documentation here .

Exercise 2: Creating a new ontology version

The ontology needs to be extended to describe additional information. To do so we will create a new version of the ontology. Carry out the following steps to create a new version of the Company ontology.

Log in with the user academyuser. This user will be the owner of this ontology.
Navigate to the ontologies catalog.
Click on more_vert next to the Company ontology.
Select Create version... from the dropdown.
Check the version number and click Create.

This action will create a copy of the ontology with status in development. This ontology is now ready to be extended or modified.

Open the ontology and switch to edit mode.
We need to extend the ontology to cover information about departments and their managers. We also want to change the description for this ontology. To do so, let's make the following changes to the ontology:
Click on Info & Metadata on the left panel and edit the description in the ontology metadata form.
Click on Elements, then 
Create Class
 and add two classes named Department and Manager .
Create a relation named has department from Company to Department and set minimum count to 1.
Create a relation named managed by from Department to Manager and set minimum count to 1.
Define the class Manager as a subClassOf Person. To do so, you need to first drag the class Person to the canvas.
Add attribute label to the new classes.
Click on Product class and enable Deprecate on its knowledge panel.
Click Save changes to ontology.

Exercise 3: Using metis to extend an ontology

In this exercise, you will modify our ontology using a metaphactory's LLM-based semantic modeling assistant. Carry out the following steps to use the assistant and add descriptions to some of the classes in the Company ontology.

Navigate to the ontologies catalog.
Click on metis close to the Company ontology.

You will be redirected to the metis-guided ontology modeling interface.

Ask metis to add descriptions to the classes Manager and Department:
person: Please add descriptions to classes Manager and Department
metis will provide a preview of the changes, use the canvas to explore the suggested descriptions.
Proceed to update the ontology with the suggested changes:
person: Looks good.
metis will respond whether the changes have been succesfully made to the ontology.
Notice that, for ontologies in development, you can always switch back and forth to the editor using Ontology editor located on top of the page.
Finally, check the descriptions using the ontology editor, by navigating the knowledge panel of each class to see the Description field.

Exercise 4: Role assignments

Role assignment can be used to communicate the responsibilities of the asset, but it also provides restricted users the permissions to fulfill that role. Follow the steps below to see the permissions granted for the knowledge-steward user on the Company ontology.

Navigate to the ontologies catalog, logged in with the knowledge-steward user, and open the model to edit it.

As this user is not the owner and have not been assigned as authors yet, he cannot perform certain actions like editing. Documentation on allowed actions are available here .

Follow the steps below to assign the author role to the knowledge-steward user.

Open the ontologies catalog, logged in with the academyuser user.
Click on more_vert next to the Company ontology.
Select More and then Role assignment... from the dropdown.
Add the knowledge-steward user as Author.
Click Save and close the dialog.
Open the ontologies catalog, logged in with the knowledge-steward user, and open the model to edit it. The knowledge-steward user has the permissions to edit the Company ontology.

Now, you can login as the knowledge-steward user and edit the ontology.

Logged in with the user knowledge-steward, add an attribute start date to the class Manager .
After adding the new attribute start date, you can see on the Manager class knowledge panel when and by whom the class was last modified.

To learn more about provenance information that is automatically captured go to the documentation.

Exercise 5: Starting a review request

In this exercise, you will start the review process for the Company ontology. The aim of this step is to ask other knowledge graph engineers to evaluate the current model.

Open the ontologies catalog, logged in with the academyuser user.
Click on Start review request next to the Company ontology.

metaphactory will load the Review request form which allows you to assign reviewers for your ontology.

Click Add reviewer.
Select your user as a reviewer

Note that in the catalog and next to the Company ontology, you will see the following label indicating that there is a pending review request: 
1 reviewer
( adjust 1)

Click on 
1 reviewer
( adjust 1)
Add a comment for the review request. For example, "What do you think about my latest changes. Is it the description right?"

Exercise 6: Reviewing an ontology

The review process has already started and all the reviewers will be notified about your request. In this exercise, you will review the latest changes made in the Company ontology in order to approve (or not) them.

Navigate to the ontologies catalog.
Open the Company ontology.

At the top, you will see a form to approve or request additional changes. Also, on the left-hand side, you will see a summary of current changes/reviews

Click documentation. In this panel you can see the changes made by the modeler who requested a review.

In the tab Elements , you will see the changes made to the this version compared to its previous, and grouped by element type: classes, relations, and attributes. For example, the class Company has been modified by adding the new relations has department to the also new class Department, and so on. On the Metadata tab you will see the changes to the ontology metadata, for example the new contributor and the version info along with the type of the change.

In the tabs Reviewers and Comments of the same panel, you will see the reviewers, the status of the reviews and also comments associated to the current review, respectively.

Go to Comments and add a comment for replying to the existing one in a thread. To do that, click on the reply option shown when putting over the comment to be replied. For example: "Changes look good, but please update the description following our documentation. Thanks".
Add comments to individual elements by clicking classes, attributes and relations on the left-hand side and browsing Add your comment in their knowledge panels on the right-hand side.

Finally, if you click Overview on the right-hand side of the panel, you will see the big picture of the ontology, including the metadata, classes, relations and attributes split in tables together with basic information about each element. In this view, it is also possible to highlight changes by checking the respective box on top of the panel.

On the left panel, click cancel for informing your decision. You can provide additional comments here as well which will be added in a new thread.

Now the label next to the Company ontology will change to 
1 reviewer
( cancel 1 )
 indicating that additional changes have been requested. If you click on that label, you will see the comments thread associated to the current review as well. At this point you can replicate or add such a description requested and then publish your Company ontology.

Exercise 7: Publishing an ontology

After approving the new changes, you are now ready to publish the new version of the Company ontology.

Navigate to the ontology catalog.

You can browse 
1 reviewer
( cancel 1 )
 and then the Comments tab to read the comments made by reviewers. From there, you can resolve or reply to those comments using the options check and reply, respectively.

Click Publish

After publishing the new version, metaphactory will replace the current published version, which is then archived. Now, the ontology catalog will show only the Company ontology.

Summary

Throughout these exercises, you have had the chance to dive deeper into metaphactory's editorial workflow to improve the collaborative development of semantic models.

The next steps in this session include the editorial workflow for vocabularies.

Documentation

Learn more about metaphactory's visual ontology editor.
Learn more about metaphactory's asset management.
Learn more about metaphactory's editorial workflows and versioning for ontologies .
Learn more about browsing the ontology model outside of the ontology editor .
SHACL (Shapes Constraint Language).
OWL (Web Ontology Language).

---

## Editorial Vocabularies

**Page:** `/resource/training:editorialWorkflowVocabulary`

Editorial workflows and versioning for vocabularies

metaphactory supports an editorial workflow for vocabularies. vocabularies may transition through a defined set of statuses to support the lifecycle from development to publishing, as well as creating new versions of vocabularies.

The editorial workflow may work independently of Git version control. The metaphactory UI offers the option to save a vocabulary to a configured Git repository in every phase of the workflow.
Workflow overview

vocabularies may transition through a defined set of statuses to support the development and publishing lifecycle:

 In development: The vocabulary is in active development.
 In review: The vocabulary is being reviewed by other knowledge graph engineers.
 Ready to be published: (Optional) Reviews are completed and the vocabulary has been marked as ready to be published.
 Published: The vocabulary has been published.
 Archived: The vocabulary has been replaced by a newer version of the same vocabulary.

To see the diagram of the editorial workflow states and transitions, please check the documentation here .

Exercise 1: Creating a new vocabulary version

The vocabulary needs to be extended to describe additional information. To do so we will create a new version of the vocabulary. Carry out the following steps to create a new version of the Role vocabulary.

Log in with the user academyuser. This user will be the owner of this vocabulary.
Navigate to the vocabularies catalog.
Click on more_vert next to the Role vocabulary.
Select Create version... from the dropdown.
Check the version number and click Create.

This action will create a copy of the vocabulary with status in development. This vocabulary is now ready to be extended or modified.

Open the vocabulary.
We will extend the vocabulary to add further roles. We also want to define a description for the vocabulary. To do so, let's make the following changes to the vocabulary:
Click on Info & Metadata on the left panel, then on the edit button edit and add a description in the vocabulary metadata form.
Click on Elements, then Create top-level term and add Manager as a new top-level term.
Click on more_vert next to Manager, then Import and add Marketing Manager and Product Manager as narrower terms of Manager.
Click on more_vert next to Marketing Manager and Product Manager and select Set In Review. Also, add comments to both of them in the dialog shown on the right hand side when clicking on each new term.

Exercise 2: Role assignments

Role assignment can be used to communicate the responsibilities of the asset, but it also provides restricted users the permissions to fulfill that role. Follow the steps below to see the permissions granted for the knowledge-steward user on the Role vocabulary.

Navigate to the vocabularies catalog, logged in with the knowledge-steward user, and open the vocabulary to edit it.

As this user is not the owner and have not been assigned as authors yet, he cannot perform certain actions like editing. Documentation on allowed actions are available here .

Follow the steps below to assign the author role to the knowledge-steward user.

Open the vocabularies catalog, logged in with the academyuser user.
Click on more_vert next to the Role vocabulary.
Select More and then Role assignment... from the dropdown.
Add the knowledge-steward user as Author.
Click Save and close the dialog.

The knowledge-steward user has now the permissions to edit the Role vocabulary.

Logged in with the user knowledge-steward, open the Role vocabulary and add a new definition to the term Manager .
After adding the definition to the term, you can see when clicking on the term Manager when and by whom the term was last modified.

To learn more about provenance information that is automatically captured go to the documentation.

Exercise 3: Reviewing and publishing terms

The review process for the new terms has already started. In this exercise, you will review the latest changes made in the terms Marketing Manager and Product Manager in order to approve (or not) them.

Navigate to the vocabularies catalog.
Open the Role vocabulary, logged in with the academyuser user.
Click on the term Product Manager from Terms tree on the left.
On the Decision panel on the left-hand side, you can select your decision, by clicking on Approve , for example, also provide an additional comment in the comments field and click Comment .

At this point you can publish your Product Manager term by clicking on more_vert and selecting Set Accepted for publication.

Follow the same steps for publishing the Marketing Manager term.

Exercise 4: Starting a review request for the vocabulary

In this exercise, you will start the review process for the Role vocabulary. The goal of this step is to ask other knowledge graph engineers to evaluate the current vocabulary.

Open the vocabularies catalog.
Click on Start review request next to the Role vocabulary.

The Review request form opens, in which you can assign reviewers for your vocabulary.

Click Add reviewer.
Select your user as a reviewer
Add a comment for the review request. For example, "What do you think about my latest changes. Is it the description right?"

Note that in the catalog and next to the Role vocabulary, you will see the following label indicating that there is a pending review request: 
1 reviewer
( adjust 1)

Exercise 5: Reviewing a vocabulary

The review process has already started and all the reviewers will be notified about your request. In this exercise, you will review the latest changes made in the Role vocabulary in order to approve (or not) them.

Navigate to the vocabularies catalog.
Open the Role vocabulary.

In the top-bar menu, you will see a summary of the current review.

Click Details to see the existing comments associated to the current review.
You can select your decision, by clicking on Approve , for example, provide an additional comment in the comments field and click Submit .

At this point you can publish your Role vocabulary.

Exercise 6: Publishing an vocabulary

After approving the new changes, you are now ready to publish the new version of the Role vocabulary.

Navigate to the vocabularies catalog.
Click Publish, then Publish to publish the Role vocabulary.

After publishing the new version, metaphactory will replace the current published version, which is then archived. Now, the vocabularies catalog will show only the Role vocabulary.

Summary

Throughout these exercises, you have had the chance to dive deeper into metaphactory's editorial workflow to improve the collaborative development of vocabularies.

The next part of this session covers Git versioning in metaphactory.

Documentation

Learn more about metaphactory's asset management.
Learn more about metaphactory's editorial workflows and versioning for vocabularies .

---

## Data Quality

**Page:** `/resource/training:modelDrivenValidation`

Data quality

metaphactory supports quality checks using SHACL. In this section, you will learn how to execute data quality rules defined in an ontology within metaphactory, as well as asset quality checks for ontologies and vocabularies.

By default, this service uses metaphactory's internal SHACL engine. However, when metaphactory is deployed on top of some commercial databases (for example, GraphDB or Stardog), the service can alternatively use the database's own internal support for SHACL validation.
Overview

To open any of the asset catalogs, navigate to the Assets menu item located in the application header. Then, select Ontologies from the dropdown to view the ontology catalog, which shows the ontologies that are loaded in the platform.

From there, you can click on more_vert for one of the ontologies, go to More, and then Validate. The option is also available from within the ontology editor, More, and then Validate database.

Exercise 1: Model-driven data validation

metaphactory also supports asset lifecycle management through model-driven data validation. To try this, you will first need to generate an inconsistency in the Project ontology. Then, you can run the validation and explore its results.

Navigate to the ontology catalog and open the Project ontology .
Click on Manage Instances from Team class and add an instance named Sales.
Go back to the ontology and validate the database from the Project ontology. You should not get any violations.
Let's change the ontology as to generate a violation. To modify an ontology, you can either set the ontology to in development, or create a new version.
Now, open the ontology, switch to edit mode, and click on the has member relation. Set the minimum count to 1.
Save the changes.

The minimum count for the relation will result in an inconsistency with the already created instance of the class Team. By running data validation, you will be able to see this violation.

Click on More located in the top-right side of the ontology editor and select Validate database from the dropdown.
Follow the validation report link to explore the generated data quality report and see the violation.
Now resolve the violation by setting the minimum count of the has member relation in the ontology to 0.
Finally, back to the ontology catalog and publish the Project ontology again.

Exercise 2: Asset quality checks

metaphactory provides automatic validation of assets (i.e., ontologies and vocabularies) based on sets of SHACL rules. Whenever an ontology is saved in the ontology editor or a vocabulary is modified these rules are checked against the modified asset in the background.

A quality check status button at the top of the Ontology Catalog and Vocabulary Catalog shows the current status of quality checks for all the corresponding assets. metaphactory comes with a built-in set of rules for both asset types, which can be easily modified or extended.

In this exercise, we will extend the default checks and add a custom rule to check if all ontologies have a description.

Asset quality management can be accessed by going to Admin -> Knowledge Graph Settings -> Ontology Management. In the Asset Quality tab, open the Ontology quality rules on the left panel, add the following rule to the default ontology checks and save the file.
Copy

 @prefix : <http://www.metaphacts.com/shacl/> .
 @prefix sh: <http://www.w3.org/ns/shacl#> .
 :OwlOntologyDescriptionShape
 a sh:NodeShape ;
 sh:targetClass owl:Ontology ;
 sh:property [
 sh:path rdfs:comment ;
 sh:severity sh:Warning ;
 sh:minCount 1 ;
 sh:datatype rdf:langString ;
 sh:message "Each Ontology should have a description." ;
 sh:description "Requires rdfs:comment property" ;
 ] .
Now click on the refresh button 
Quality checkcheck_circle
replay
 on top of the editor. Once the validation is completed, click on the quality check button to see the results.
As part of the results, you should see some warning messages for the ontologies with no rdfs:comment property defined.

These quality checks are also available for vocabularies. Under Admin -> Knowledge Graph Settings -> Vocabulary Management you can view, change or extend the default vocabulary checks.

Summary

Throughout these exercises, you have had the chance to dive deeper into metaphactory's features for quality checks.

The final step in this session will cover metaphactory’s importing and exporting capabilities.

Documentation

Learn more about metaphactory's visual ontology editor.
Learn more about metaphactory's data quality service.
SHACL (Shapes Constraint Language).
OWL (Web Ontology Language).

---

## Git Versioning

**Page:** `/resource/training:git`

Git versioning

Asset management involves all the aspects of the ontology and vocabulary lifecycle in metaphactory. The starting point for asset management in metaphactory is the ontology catalog and vocabulary catalog respectively; they provide an overview of the ontologies and vocabularies currently available in the platform. In this direction, one of the features provided by the platform is the capability to put assets under version control using one or more Git repositories to track changes and keep their history. Throughout the step-by-step exercises specified below, you will learn how to use Git to store your assets.

Asset management may require some additional configurations in the platform. Enabling Git version control requires at least one Git asset storage to be configured by the platform administrator.
Git versioning applies to both ontology and vocabulary management.
Overview

To open any of the asset catalogs, navigate to the Assets menu item located in the application header. Then, select Ontologies or Vocabularies from the dropdown, which shows the assets that are loaded in the platform.

From these catalog, you will be able to access Git from the more_vert dropdown context menu, then More and then Git. These options are also available from their respective editor. To do so, click on a knowledge graph asset and go to More, and then Git (shown on the top right).

Exercise 1: Knowledge graph assets on git

You may have noticed that when creating ontologies and vocabularies, we have an option to save them to git. This action is enabled by default when Git version control is enabled. In the next exercise we will see that the ontologies created are already in Git as well as the information available from Git.

Navigate to the ontology catalog.
Click on the more_vert dropdown next to the Company v0.2.
Go to more, and then click on Git Versioning.
Note that metaphactory will by default save newly created assets to Git. When publishing ontologies, metaphactory will again update them on Git.
Exercise 2: Saving ontologies to Git

In some cases you may not decide to save an asset to Git when creating them, or you may import them from files. For these cases, you can still add them to Git at a later stage. The following exercise will show you how.

Navigate to the ontology catalog.
Click on the more_vert dropdown next to the Project.
Go to more, and then click on Save to Git.
Enter project.ttl in the Location field.

When you define the asset storage for the first time, you must enter the location where the ontology is persisted in the repository.

While entering Location, metaphactory will autocomplete the Branch field, but you can also select the main branch configured. The commit message can also be customized.

Finally, click Save to Git.

By clicking again on the more_vert dropdown and selecting Git versioning , you will see a tab named History. Here, you will be able to see the list of changes to this ontology.

Note that you may save intermediate versions of an ontology to Git. After saving them to Git once, you can go to More, and then Git to do so.
Exercise 3: Saving vocabularies to Git

Similarly to ontologies, vocabularies that are not yet on Git can be added at a later stage. Follow the below steps to do so.

Navigate to the vocabulary catalog.
Click on the more_vert dropdown next to the Role Vocabulary.

metaphactory will load the Git Versioning form which allows you to save changes to the vocabulary to a Git repository.

When you define the asset storage for the first time, you must enter the location where the vocabulary is persisted in the repository.

Enter role.ttl in the Location field.

While entering Location, metaphactory will autocomplete the Branch field, but you can also select the main branch configured. The commit message can also be customized.

Finally, click Save to Git.

By clicking again on the more_vert dropdown and selecting Git versioning , you will see a tab named History. Here, you will be able to see the list of changes to this vocabulary.

Summary

Throughout this simple exercise, you have had the chance to put an ontology under change control in Git. The next steps involve additional features in Metaphactory e.g. asset import and export and collaborative editing.

Documentation

Learn more about metaphactory's visual ontology editor.
Learn more about metaphactory's asset management.
Learn more about metaphactory's asset storage configuration.
SHACL (Shapes Constraint Language).
OWL (Web Ontology Language).

---

## Additional Features

**Page:** `/resource/training:AdditionalFeatures`

Additional Features

This module will delve into an array of advanced features in metaphactory related to ontology modelling.

Disjunctions in relation ranges

Visual ontology editor supports modeling and visualization of disjunctions in relation ranges.

Go to the Project ontology and check the OR relation there.

Create instances for the classes Team, Person, and Task where you can have either instances of Person or Team for this relation.

Imports Analysis

The imports analysis feature provides a comprehensive overview of all ontologies imported by the current ontology. This helps you identify potential issues such as missing ontologies, version conflicts, or deprecated dependencies, which is especially useful when troubleshooting modeling errors or preparing an ontology for publication. To access this feature:

Go to the ontology catalog.
Click on the more_vert next to the Organization ontology in the ontologies catalog
Click on More and then Imports Analysis

Review policies

By default, there is no requirement on reviews for an asset (ontology and vocabulary) to be set as Ready to be published or Published. This can be customized, to define a review policy, that needs to be fulfilled to allow an asset progressing from the review status. E.g., a policy can be defined, that the asset needs to be approved by at least two reviewers.

If a review policy is defined, the UI will show information about the review policy during reviewer assignment and a warning in the asset catalog, if the asset is in review, but the policy is not fulfilled.

Follow the steps below to define a policy that checks whether you have minimum 2 approvals and no change requests for an ontology

Go to the template Platform:AssetFragmentsOverrides.
Uncomment the ontologyReviewPolicyConfiguration and ontologyReviewPublishingPolicyWarning template fragments and save.
Start a review request for an ontology. You should see a message explaining the defined review policy.

Similarly, follow the steps below to define a policy that checks whether you have minimum 2 approvals and no change requests for a vocabulary

Go to the template Platform:AssetFragmentsOverrides.
Uncomment the vocabularyReviewPolicyConfiguration and vocabularyReviewPublishingPolicyWarning template fragments and save.
Start a review request for a vocabulary. You should see a message explaining the defined review policy.

Initial views

Configuration of default initial views based on ontology status. These can be configured in the settingsSystem Administration > settings_suggestSystem Settings > Assets configuration. The available options for the entries ontologyInitialViewArchived, ontologyInitialViewInDevelopment, ontologyInitialViewInReview, ontologyInitialViewPublished and ontologyInitialViewReadyToBePublished are:

editor: Editor view with center diagram and element trees.
review: Editor view with opened review sidebar.
documentation-diff: Documentation in diff view.
documentation-overview: Documentation with overview of elements.

Events & Notifications

Certain workflows or tasks may involve further steps, often requiring input from other people or external systems beyond the initiator. A typical case in metaphactory is the creation of ontologies or vocabularies, where a triggered event can automatically send email notifications or launch additional workflows in external systems. For a complete list of available events, please refer to this documentation .

Collaborative & Concurrent Editing

metaphactory enables users to collaboratively utilize the ontology modeling features through the ontology editor. However, only one editing session per ontology is supported. Changes are tracked within the session, and saving these changes will persist the entire ontology graph to the database, thereby overwriting the previous version.

The locking mechanism is for informational purposes only. Users can start an edit session at any time, regardless of other active users, and perform or save changes, which may overwrite others' work. Furthermore, users can force-acquire an editing session, for example, if they have a stale session in another browser window.

Diagrams

The Ontology Visualization Editor allows you to create a diagram visualization. Diagrams visualize specific views of an ontology, including selected classes and relations relevant to your use case. Once you've created your diagram, you can save it to ensure it appears the same way the next time you open the ontology in the editor. To save your current diagram, click Save changes to diagram in the top left. This will establish the current diagram as the new Default Diagram for the ontology, which can be also exported as part of the model.

To see more about this feature, please check the documentation here .

Provenance

You may have noticed that as knowlege graph assets are created and modified provenance information is automatically captured. This is done in order to better support collaboration and governance.

The following questions can be answered with this provenance information:

when it was initially created?
when it was last modified?
who created it?
who modified it last?

Such annotations are captured both on the asset level (i.e. the ontology and vocabulary) as well as on the elements level (e.g. a class or a term). In the metaphactory UI the provenance information is displayed in the catalogs, as well as in the ontology editor and vocabulary editor.

Let's take a look at this in the ontology catalog.

Go to the ontology catalog.
For all ontologies where provenance was captured you can see when it was created and when it last modified, as well as who created and who last modified the ontology.
Now click on one ontology e.g. the Company ontology.
And then click on a class e.g. the Industry class.
You can see the same provenance information on panel on the bottom right of the screen.

Note that this can be disabled globally in the platform.

RDF Turtle Editor

Some users may require to see the RDF data created when defining an ontology. In such cases, metaphactory provides a way to access the RDF data in Turtle format. To access this feature:
Go to the ontology catalog.
click on the more_vert next to the ontology in the ontologies catalog
click on More and then RDF Turtle Editor...

You can also make changes directly in the RDF Turtle Editor, and these modifications will be reflected in the Ontology Editor.

Importing & Exporting Assets

Additional interoperability in metaphactory is provided by the ability to import and export assets (ontologies and vocabularies). Throughout the step-by-step exercises specified below, you will learn how this can be executed in metaphactory.

metaphactory also bundles a set of rules for transforming common language constructs that can be applied during the import and export of ontologies. The following three options are available:

enrich: Augment the ontology with language constructs defined in the configured transformation rules.
transform: Transform the ontology to language constructs defined in the configured transformation rules.
keep: Import or export the ontology as is.

For more details on how these transformations can be supported, you may navigate the Ontology transformation documentation page.

Let's try:

Go to the ontology catalog.
Click on more_vert next to one of the ontologies e.g. the Company ontology.
Select Export... from the dropdown.
You can click on expand_lessAdvanced Export Options and see the available options. Note that only keep as is is avaiable as export transformations rules need to be enabled.
You can select whether the imported ontologies should also be exported, either as in separate files in "*.zip" or in one "*.trig" file.
Additionally, you can opt to include diagrams in the exported ontology. If you do, the exported file will be in "*.trig" format. When importing, the diagrams will also be included with the ontology.
SKOS-XL support

SKOS-XL allows the inclusion of external metadata on vocabulary terms, such as (but not limited to) provenance, descriptions, sources, and references. To enable it, go to Setting > Assets Configuration and change from disabled to any of the following values:

optional: SKOS-XL can be used per vocabulary
all: SKOS-XL is enabled for all vocabularies and can not be disabled

Summary

In this section, you explored additional features related to modeling in metaphactory.

---

# VM Certification

## Main

**Page:** `/resource/certification:knowledgeGraphEnginner`

Visual modeling certification for Knowledge Graph Engineers
General notes on certification process

metaphacts Academy training allows you to certify your knowledge and skills in three tracks, which correspond to the three tracks in the learning materials:

Semantic knowledge modeling
Building knowledge graph applications
metis AI

While the corresponding module provides information on certification for the other two tracks, this page focuses exclusively on the Semantic Modeling track. Please note that you may choose to pursue certification in any number of tracks-one, two, or all three-and in any order you prefer. Certification will be reviewed and graded only once hands-on tasks are completed and the theoretical quiz score is 80% or higher.

Theoretical part
You need to complete the questionnaire in one go. You can NOT save and resume later.
The questionnaire contains questions with multiple choice and/or multiple select answers.
The questionnaire will be graded automatically.
Please allocate about 0.5 - 1 hour for a questionnaire.
Hands-on tasks
You should do the hands-on exercises on your individual metaphactory instance, which you are currenly using.
Once your solution for the exercise is ready, you should copy the solution’s link from your metaphactory instance and paste it into the comment section of the corresponding hands-on assignment in the LMS. This will record that you have completed the hands-on exercise.
You can save your work and resume working on your solutions at any time until the submission deadline.
Hands-on exercises will be graded by our the metaphacts Academy team after the course end date.
Certification in Visual Modeling

Now, to the point!

To successfully achieve certification in this track, you are expected to complete the Visual modeling basics self-guided tutorial module of the metaphactory course. It is also recommended to participate in or watch in recording the Visual modeling advanced live session. Exercises for the sessions can be found in the corresponding module . If you could not attend the session, the instructions on how to access the recording were forwarded to you via email on the next day after the session.

Note that you can take part in the certification even if you did not attend the related training sessions.

As previously mentioned, certification grading will being only once your quiz is 80% or higher and all hands-on tasks for the track have been completed.

Theoretical quiz on Visual Modeling

To find the quiz:

Log in to the LMS
Find and click the training course you are currently enrolled in
Scroll down to the “Content” section and click on the quiz module
Hand-on tasks
Hands-on task 1: Vocabulary
Hands-on task 2: Vocabulary - Editorial Workflow and versioning
Hands-on task 3: Ontology
Hands-on task 4: Ontology - Editorial Workflow and versioning

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Need help with this step? This video walks you through the process: Submitting results to hands-on tasks

---

## Task 1

**Page:** `/resource/certification:OntologistCertificationExercise1`

metaphactory Visual Modeling
Certification Level: Knowledge Graph Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 1: Vocabulary
In this exercise, you will create a vocabulary for vegetables.

Description:
To create a vocabulary go to Assets > Vocabularies.
Define the title and label for the vocabulary.
Create a top level concept for Vegetables.
Save the vocabulary on git.
Create 2 concepts under the Vegetables concept (e.g. Bean and Roots).
Create 2 concepts under the Bean concept (e.g. Fava beans and Green beans).
Create 3 concepts under the Root concept (e.g. Potato, Carrot and Onion).
Set all the concepts in review .
Request changes for at least 2 concepts adding comments asking to add labels (e.g. Bohne in German for beans) and definitions in a different language for these concepts.
Make the requested changes.
Accept for publication all the approved concepts .
Save the vocabulary again on git, and check the history.
For more information you can access the documentation Help:VocabularyVisualizationAndEditing.
Expected result:

---

## Task 2

**Page:** `/resource/certification:OntologistCertificationExercise1_1`

metaphactory Visual Modeling
Certification Level: Knowledge Graph Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 2: Vocabulary - Editorial Workflow and versioning
In this exercise, you will start a review of the vocabulary for vegetables, publish it and create a new version with additional changes to the vocabulary.

Description:
To start a review for the vocabulary created, go to Assets > Vocabularies .
Add yourself as reviewer.
Open the vocabulary, review the changes and accept them.
Publish the vocabulary.
Create a new version of the vocabulary.
The new version of the vocabulary should define the new term:
Garlic
Start a new review of the latest changes.
Add comments for the reviewer.
Reply feedback from the reviewer.
Publish the new vocabulary.
For more information you can access the documentation Help:EditorialWorkflowsAndVersioning.
Expected result:

New version:

New vocabulary:

---

## Task 3

**Page:** `/resource/certification:OntologistCertificationExercise2`

metaphactory Visual Modeling
Certification Level: Knowledge Graph Engineer (Associate)

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 3: Ontology
In this exercise, you will create a ontology for recipes.

Description:
To create an ontology, go to Assets > Ontologies. Name it as Recipes
Open the ontology and import the Organization ontology to reuse some of its classes.
The ontology should define classes, relations and attributes for the given use case:
The ontology should define recipes.
Recipes have a label, description, and cooking time attribute.
Recipes can belong to different diet types (e.g. vegan, paleo, etc).
Diets have at least a label attribute.
Recipes use ingredients.
Ingredients have a relation to food.
Ingredients may have (using an OR) a relation to vegetables.
Vegetable is restricted to the vegetables vocabulary.
Ingredients have an attribute label and quantity.
Food has a label attribute.
Recipes have authors.
Authors are subclasses of org:Person.
Authors have at least a label.
Using the Instance Data Manager, create at least two recipes as illustrated below.
Validate the database and check the generated data quality report.
For more information you can access the documentation Help:VisualOntologyEditing.
Expected result:

Ontology:

Example of instance data:

Example of data quality report:

---

## Task 4

**Page:** `/resource/certification:OntologistCertificationExercise3`

metaphactory Visual Modeling
Certification Level: Knowledge Graph Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 4: Ontology - Editorial Workflow and versioning
In this exercise, you will start a review of the ontology for recipes, publish it and create a new version with additional changes to the model.

Description:
To start a review for the Recipe ontology, go to Assets > Ontologies.
Add yourself as reviewer.
Open the ontology, review the changes and accept them.
Publish the ontology.
Create a new version of the ontology.
The new version of the ontology should define the following new relation:
A menu has at least one recipe.
Start a new review of the latest changes.
Add comments for the reviewer.
Reply previous comments from the requester.
Publish the new ontology.
For more information you can access the documentation Help:EditorialWorkflowsAndVersioning.
Expected result:

New version:

New ontology:

---

# App Building Basics

## Main

**Page:** `/resource/training:AppBuildingBasicsSelfGuided`

App building basics
Goal

Data within your knowledge graph must be presented in a manner that's consumeable and comprehensible by all relevant stakeholders in order for it to have the most impact and useability. This metaphactory App Building Basics module delves into platform customization topics to support building apps for data visualization and discovery. By the end of the module, you'll know how to create a consistent design identity in metaphactory, embed custom visual and semantic components and create pages relevant for your organization's use case.

Understanding the use case

Now that you have learned how to create a unified semantic model, let's have a look at how you can leverage this model and metaphactory's low-code approach to surface information and extract insights for relavant tasks in this domain.

In this module, you'll first learn how to create a consistent look and feel for the instance data in the system by creating templates for how information should be displayed for all instances of a class in the model.

You will then work on embedding various visualization components into your pages to support knowledge consumption and discovery for our use case. This will allow you to visualize information about the persons in your graph using a semantic query, see their friends using a table, and dynamically discover their relationships using our graph visualization and event-driven components.

Ultimately, these tasks will help you create a small app that allows you to intuitively visualize relevant information, which can help accelerate decisions.

Learning outcome

Throughout this guided tutorial, you will learn:

key How to identify and create different kinds of pages.

key How to embed the built-in semantic components provided by metaphactory in your pages.

key How to customize semantic components and the page layout.

key How to enable dynamic interaction between components by triggering events.

As a reminder, you can complete the tutorial at your own pace, pause whenever, and always pick-up where you left off.

Note: Since some videos were recorded with older versions of metaphactory, you may notice minor differences in the user interface. However, the functionality remains the same.
Templating Mechanism

Creating an application page
Creating a template page
Creating a knowledge panel template

Open

 20-40 mins

Semantic Components

Structuring the layout of a template page
Embedding semantic components into a template page
Customizing components

Open

 20-40 mins

Component Interaction

Explaining the event system
Exchanging data with other components

Open

 10-20 mins

Advanced Features

Model-driven search
Defining a SPARQL query template
Creating a custom REST API
Templates reusability

Open

 10 mins

---

## Templating

**Page:** `/resource/training:AppBuildingBasicsTemplating`

Templating Mechanism
Goal

Throughout the following video and guided exercises, you will learn:

How to create an application page
How to create a template page
How to create a knowledge panel template
Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's templating mechanism.

Open
Part 2: Exercises

This section will guide you through the process of creating your own template pages with hands-on exercises.

Open

---

## Semantic Components

**Page:** `/resource/training:AppBuildingBasicsSemComponents`

Semantic Components
Goal

Throughout the following video and guided exercises, you will learn:

How to structure the layout of a template page
How to embed semantic components into a template page
How to customize semantic components
Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's semantic components.

Open
Part 2: Exercises

This section will guide you through the process of creating your own template pages with hands-on exercises.

Open

---

## Events

**Page:** `/resource/training:AppBuildingBasicsEvents`

Component Interaction
Goal

Throughout the following video and guided exercises, you will learn:

How to use metaphactory's event system
How to exchanging data with other components
Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's event system.

Open
Part 2: Exercises

This section will guide you through the process of creating your own template pages with hands-on exercises.

Open

---

## Advanced Features

**Page:** `/resource/training:AppBuildingBasicsAdvFeatures`

Advanced Features
Goal

Throughout the following video and guided exercises, you will learn:

How to create a model-driven search
How to define a SPARQL query template
How to create a custom REST API
How to reuse templates
Chapter structure
Part 1: Demo video

This section will introduce you to metaphactory's templating mechanism.

Open

---

# App Building Advanced

## Main

**Page:** `/resource/training:AppBuildingAdvanced`

App building advanced
Goal

Now that you've completed the metaphactory App Building Basics, you're ready to take your use of metaphactory a step further and explore its advanced app features and capabilities. This App Building Advanced module dives into creating advanced features for templating and interactions involving multiple components, including forms and the semantic search framework.

Understanding the use case

In this module, you will leverage metaphactory's low-code approach to extend the small knowledge visualization app that you have already built and transform it into an advanced knowledge discovery and kowledge management app. You will configure a model-driven search interface to support more advanced interaction patterns and model-driven data authoring forms to support the augmentation of the knowledge graph with new instance data. You'll also look at metaphactory's app lifecycle mechanism to get an understanding of how apps are management and deployed into production.

Learning outcome

Throughout this guided tutorial, you will learn:

key How to configure the security layer for application access and permission control.

key How lightweight applications can be deployed along with the platform.

key How to use semantic forms to create advanced authoring forms.

key How to create and customize search configurations.

key How to augment knowlege graphs using data from multiple sources.

Structure
Security & permissions

Exploring roles & validating permissions
Creating users with pre-defined roles
Composing roles with reusable role fragments

Open

 15 minutes

App packing & lifecycle

Apps & storages
Anatomy of a metaphactory setup
App mechanism & architecture
Infrastructure management (logs, repository configuration, federation)

Open

 20 minutes

Federation

Extending a knowlege graph using Wikidata

Open

 15 minutes

Advanced data authoring

Creating a manual form
Adding contraints to form fields
Using query patterns in form fields

Open

 30 minutes

Semantic search framework

Creating a search configuration using the wizard
Creating a custom search configuration
Adding custom facets
Customizing results visualization

Open

 30 minutes

Module summary

Module highlights

Open

 10 minutes

---

## Security

**Page:** `/resource/training:AdvSecurity`

Security & permissions

metaphactory includes a set of pre-defined roles and permissions for access and permission control required by applications. In this section, you will explore the pre-defined roles. Moreover, you will learn how to compose roles using fragments and thus restrict certain actions, behaviors or UI elements.

metaphactory relies on the Apache Shiro security framework to implement the security layer.

Overview

The platform bundles a set of pre-defined roles but, if required for specific application use cases, it allows you to define custom roles with respective sets of fine-granular permissions. These roles can be defined using apps or in the runtime storage. Once roles are defined, they can be mapped to users. The pre-defined roles that come with metaphactory are:

end-user: a user with minimal permissions for restricted application access.
knowledge-steward: a user that is primarily curating ontologies, vocabularies and instance data.
knowledge-graph-engineer: a user responsible for ontology management and data quality.
application-engineer: a user responsible for creating applications.
admin: a technical power user with access to most application and administration functionality.
root: role for the super user to grant full access.

metaphactory also provides a mechanism for the composition of roles by means of reusable role fragments. For example, the role end-user gives minimal permissions for restricted application access; however, if you want to give a user with an end-user role access to explore the vocabularies loaded in the platform, you can create a new custom role, let's say end-user-vocabulary, and assign it the pre-defined role end-user along with the pre-defined role fragment vocabulary-view.

If none of the reusable fragments fit your use case, you can also define fine-granular permissions and thus create new role fragments by associating permission strings to them. For example, the string sparql:default:query:select grants permission to execute SPARQL on the given default repository. The definition of custom roles fragments to assign permission strings is out of scope for this training.

Checking permissions

Roles and permissions given to a current user can be checked in metaphactory by following these steps:

Click on person located in the application header.
Select the user name from the dropdown.

On the User Profile > Platform Roles page, you will see the roles assigned. You can also check particular permissions by going to Permission Check tab.

Click on User Profile > Permission Check tab.
Enter the permission string sparql:default:query:select to check if the current configuration grants permission to execute SPARQL on the given default repository.
Press Check.

A message indicating Permitted should appear below. Otherwise, you will get Not permitted.

Exercise 1: Creating a user with pre-defined roles

In this exercise, you will create a new end user and assign it the appropriate pre-defined role. To do that, follow the steps below:

Click on settingsSystem Administration > located in the application header.
Click on admin_panel_settingsSecurity.
In the Local Users tab, create a new account by filling out the fields Principal, Password and Repeat Password.
From the Roles dropdown, select end-user.
Click Create.

You can log in into the platform with this new user and follow the steps above to check the current role and permission strings.

Exercise 2: Editing a user to grant additional permissions by using composable role fragments

The end user created above has minimal permissions for navigating the current application. For example, they do not have access to either ontologies or vocabularies. In this exercise, you will edit the end user and assign it a new role fragment to grant access to the vocabularies loaded in the platform. To do that, follow the steps below:

Click on settingsSystem Administration > located in the application header.
Click on admin_panel_settingsSecurity.
In the Local Users tab, click on the Edit button for the end user created previously.
In the Update Account form, select vocabulary-view from the Roles dropdown.
Click on Update button.

You can log in into the platform with this updated user account and validate the new permissions by exploring the vocabulary catalog.

Summary

Throughout these step-by-step exercises, you have learned how to create users in metaphactory, assign them roles, and compose roles by reusing pre-defined role fragments.

The next steps in this module include Apps packing and lifecycle, Advanced data authoring, Semantic search framework and Federation, where you will learn about the app mechanism provided by the platform, semantic components for embedding manual forms in pages, the powerful semantic search framework, and mechanisms for extending the knowledge graph using Wikidata.

Documentation

Learn more about security in metaphactory.
Blog post: "Security best practices with metaphactory".
Blog post: "SSO and Identity Management with metaphactory".

---

## App Lifecycle

**Page:** `/resource/training:AdvAppLifeCycle`

Apps packing & lifecycle

metaphactory offers simple extension points to deploy lightweight apps along with the platform without the need to change the platform binary or re-compile the platform. An app is a customer or domain-specific platform add-on and contains: application and template pages, configuration - such as RDF namespaces, system settings, etc., as well as look and feel customizations - such as CSS files, images, header and footer resources, etc. In this section, you will explore the anatomy of a basic metaphactory app.

Deploying an app by uploading a ZIP artifact works with out-of-the-box metaphactory deployment.

Overview

To navigate to the installed app in the platform, follow these steps:

Click on settingsSystem Administration > located in the application header.
Click on appsApps & Storages.

On this page, you will see all of the apps installed on this system, for example, the training-app, which includes all of the templates and settings created for this training. Moreover, each app is also associated to a storage.

A couple of actions can be executed from here. If you want to remove the training-app, you can press Remove and then restart metaphactory. This action will remove all the templates and settings included in this training app. Moreover, if you want to deploy another app using out-of-the-box metaphactory deployment, for example, a branding app including specific styling, you can press Upload & Deploy App, select the respective *.zip artifact from the file system, and restart the plataform. Finally, you also can download any app by using the Export ZIP option.

Exercise 1: Exploring the anatomy of a metaphactory app

The tree below illustrates the basic folder structure of an app:

my-app
plugin.properties - this is the only mandatory file
/config
/page-layout - Files marked in red will be read or shadowed by files from other apps, others are merged entirely
/html-head.hbs
/header.hbs
/footer.hbs
/login.hbs
/internal_server_error.hbs (and similar errors)
html-header-resources.hbs
/ui.prop - Properties will be read selectively or shadowed individually
/environment.prop - Properties will be read selectively or shadowed individually
/global.prop - Properties will be read selectively or shadowed individually
/namespaces.prop - Properties will be read selectively or shadowed individually
/assets - Entire files will be read or shadowed by files from other apps. Files will become directly available under http://platform-url.com/assets/my-styles.css
/images - Entire files will be read or shadowed by files from other apps. Files will become directly available under http://platform-url.com/images/my-image.png
/my-app-logo.png
...
/no_auth - These files are not protected, for example, images for the login pages. Files will become directly available under http://platform-url.com/no_auth/login-logo.png
...
/data
/templates - Entire files will be read or shadowed by files from other apps.
Template%3Ahttps%3A%2F%2Fontologies.metaphacts.com%2Forganization-ontology%2FPerson.html
...

In the following, you can navigate the anatomy of the training-app:

training-app
plugin.properties
/data
/templates
Template%3Ahttps%3A%2F%2Fontologies.metaphacts.com%2Forganization-ontology%2FPerson.html
http%3A%2F%2Fwww.metaphacts.com%2Fresource%2FStart.html
...

Summary

Throughout this section, you have learnt how metaphactory's lightweight app mechanism works and what apps look like.

The next steps in this module include Federation, Advanced data authoring and Semantic search framework, where you will explore advanced semantic form and search configuartions, as well as mechanisms for extending the knowledge graph using Wikidata.

Documentation

Learn more about app installation and lifecycle in metaphactory.
Blog post: "The composable enterprise powered by metaphactory".
Explore the Nobel Prize app .
Explore the Wikidata app .

---

## Federation

**Page:** `/resource/training:AppBuildingAdvFederation`

Federation

Depending on the application use case, there is often a need to query data stored in multiple RDF repositories and even augment it with information from other services. This can be done by using federation technologies and SPARQL for executing distributed queries over several endpoints. Throughout this exercise, you will learn how to execute these queries and use some services provided by metaphactory.

SPARQL 1.1 Federation implements the SERVICE call, aiming at allowing users to direct a sub-query to a specific SPARQL endpoint and combining the results with the ones from the rest of the query.

Overview

The platform incorporates two federation engines tailored towards data integration from multiple sources: Ephedra and FedX . The first is provided by metaphactory while the second one has been implemented as part of the RDF4J Framework, which is an open source modular Java framework for working with RDF data.

In particular, Ephedra operates on top of the platform repository manager and allows you to send SPARQL 1.1 federated queries over several repositories. Based on that, metaphactory offers default built services on which it is possible to execute distributed queries. For example, one of them is the Entity Lookup, which is intended for the interactive lookup of entities in the graph, i.e., to look up an entity based on relevant names for disambiguation.

Some examples of federation include the combination of data from several SPARQL endpoints, the enrichment of local data with information from other (hybrid) data sources, database agnostic search through an entity lookup service, and transparent federation of a Linked Data Browser.

Exercise 1: Getting information from external RDF datasets

In this exercise by executing a federated query on metaphactory's Wikidata demo system, you will obtain additional information about significant events whose inception year matches the Roy's year of birth.

Open the SPARQL editor.
Copy and paste the snippet below.
Copy

PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
SELECT DISTINCT ?event ?label ?description ?inception_date
WHERE {
 <https://ontologies.metaphacts.com/organization-ontology/Person/instances/20f4b8a7-0a99-421f-a52c-747d89d77996> org:hasBirthday ?date .
 SERVICE <https://wikidata.metaphacts.com/sparql> {
 ?event a <http://www.wikidata.org/prop/novalue/P793> .
 ?event <http://www.wikidata.org/prop/direct/P571> ?inception_date .
 ?event rdfs:label ?label .
 ?event schema:description ?description .
 FILTER(year(?inception_date) = year(?date)) .
 FILTER(LANG(?label) = "en" && LANG(?description) = "en") .
 }
}
 

The whole federated query is executed on the Wikidata side (https://wikidata.metaphacts.com/sparql) and returned to your metaphactory instance with significant events incepted in 1982 together with their labels and description (in English)

Summary

Throughout these step-by-step exercises, you have learnt how federation is implemented in metaphactory and how it can also be used to augment and extend your data.

The next step includes Advanced data authoring.

Documentation

Learn more about federation in metaphactory.
Blog post: "Federation in metaphactory".
SPARQL 1.1. Federation.
Explore the Wikidata app .

---

## Data Authoring

**Page:** `/resource/training:AdvDataAuthoring`

Advanced data authoring

As introduced in the previous metaphactory Basics module, data authoring involves the creation, modification and deletion of instances of classes in the knowledge graph. While this can be done entirely model-driven using ontologies or using auto-generated forms in an application page, the manual definition of fields make the form look and behave exactly as required. Throughout the step-by-step exercises specified below, you will learn how to configure a form defining manual fields and using query patterns.

When a manual field definition is given, that manual definition completely overrides any auto-generated field definition for a field with the same identifier.

Overview

metaphactory's Semantic Form is a highly configurable component for creating of authoring forms. The semantic-form component has the option to specify field definitions manually by means of the attribute fields, which expects a JSON object array of field definitions. Moreover, these definitions provide an abstraction over the ontology by specifying SPARQL patterns as well as specifying certain validation constraints such as datatypes, cardinalities or pattern matches against existing database entries. The following code shows a blueprint for a manual form, which will be used as a template for the next exercises.

Copy

 <semantic-form
 fields='[
 {
 "id": "name",
 "label": "Name",
 <!-- define 1 or more patterns -->
 "READPATTERN": "SELECT $value WHERE { $subject <http://www.w3.org/2000/01/rdf-schema#label> ?value }"
 "WRITEPATTERN": "INSERT { $subject <http://www.w3.org/2000/01/rdf-schema#label> ?value } WHERE {}"
 },
 {...} ]'>
 <!-- define placeholders and input type for each field -->
 <semantic-form-INPUTTYPE for="name"> </semantic-form-INPUTTYPE>
 <!--...-->
 <!-- define buttons, or form helpers --> 
 <button> Submit </button>
 <!--...-->
 </semantic-form>

Exercise 1: Creating a form using manual fields

This first exercise aims at wrapping an input field within a form and creating a new graph with triples defining me as a org:Person, and my name. To do that, you will define a new field and a child element semantic-form-text-input. Follow the steps below:

Open a new application page in the Template editor.
Copy and paste the snippet in the page and save.

You will see the new form with the field Full Name, which is the label of the field specified in the snippet, together with the form buttons submit and reset.

Revisiting the code, you can observe that the semantic-form set an IRI for the new individual, new-subject-template, and an action to be executed after submitting the new values, post-action. Moreover, the attribute fields define the datatype for the field and an insertPattern query to update the new triples.

Copy

 <div class="page">
 <div class='page__body'>

 <semantic-form 
 form-id='basic-example' 
 new-subject-template='http://www.example.com/person/id/{{me}}'
 post-action='redirect'
 fields='[
 {
 "id": "me",
 "label": "Full Name",
 "xsdDatatype": "xsd:string",
 "insertPattern": "INSERT { ?subject a org:Person; rdfs:label ?value } WHERE {}"
 }]'>

 <semantic-form-text-input for="me" placeholder='Enter your name'></semantic-form-text-input>

 <div class="semantic-form-footer-buttons">
 <button name="submit" class="btn btn-primary">Submit</button>
 <button name="reset" class="btn btn-secondary">Reset</button>
 </div>
 </semantic-form> 
 </div>
</div>

Exercise 2: Adding additional fields to a form

To take even more control over the fields that a form displays, you will add cardinality constraints and two additional fields configured to autosuggest values.

Open the previous page to edit.
Copy and paste the next snippet to add min/max cardinality constraints for the first field me.
Copy

<semantic-form 
 fields='[
 { 
 "id": "me", 
 <!--SNIP-->
 "minOccurs": "1",
 "maxOccurs": "1",
 <!--SNIP-->
 "label": "...",
 }"
 }]'>

</semantic-form> 

Copy and paste the snippet below to add two more fields: one using the autosuggestionPattern query to search for persons and another one using valueSetPattern which prefetch values.
Copy

 <semantic-form 
 fields='[
 { 
 "id": "me",
 "..." 
 }, 
 {
 "id": "knows",
 "label": "Knows",
 "autosuggestionPattern": 
 "SELECT ?value ?label WHERE {
 ?value a <https://ontologies.metaphacts.com/organization-ontology/Person>;
 <http://www.w3.org/2000/01/rdf-schema#label> ?label .
 FILTER(REGEX(STR(?label), ?__token__, \"i\")) } LIMIT 30", 
 "minOccurs": "0", 
 "insertPattern": "INSERT { $subject <https://ontologies.metaphacts.com/organization-ontology/knows> ?value } WHERE {}"
 },
 {
 "id": "project",
 "label": "Project",
 "maxOccurs": "1",
 "insertPattern": "INSERT { $subject <https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn> ?value } WHERE {}",
 "valueSetPattern": "SELECT $value $label WHERE { 
 $value a <https://ontologies.metaphacts.com/organization-ontology/Project>; rdfs:label $label .
 }"
 } 
 ]'>

 <!-- ... -->
 </semantic-form> 
 
Finally, add the two input children, semantic-form-select-input and semantic-form-autocomplete-input, corresponding to the two fields defined previously.
Press Save & View
Copy

 <semantic-form 
 fields='[
 { 
 "id": "me",
 "..." 
 }, 
 {
 "id": "knows",
 "..."
 },
 {
 "id": "project",
 "..."
 } 
 ]'>
 <!---SNIP--->
 <semantic-form-select-input for="project" placeholder='Select your project'>
 </semantic-form-select-input>
 <semantic-form-autocomplete-input for="knows" placeholder='Enter a name'>
 </semantic-form-autocomplete-input>
 <!---SNIP--->

 <!--...-->
 </semantic-form> 
 

Exercise 3: Adding query patterns to a form

Follow the below steps:

Open the previous page to edit.
Remove the new-subject-template and add subject and the URI of the person previously generated.
Copy

 <semantic-form 
 <!-- ... -->
 <!-- REMOVE: new-subject-template='http://www.example.com/person/id/{{me}}'-->
 subject='%%%%%INSERT YOUR OWN PREVIOUSLY GENERATED PERSON URI HERE%%%%%',
 <!--...--> 
 fields='[{ ... }]'>
 <!--...-->
 </semantic-form> 
 
Copy and paste the snippet below to add select and delete patterns to the form.
Press Save & View

The snippet adds select patterns for all of the fields in the form: me, knows and project. Moreover, it inserts delete patterns to remove the data ahead of its re-insertion.

Copy

 <semantic-form 
 <!--...--> 
 fields='[
 {
 "id": "me",
 "...",
 <!---SNIP--->
 "selectPattern": "SELECT ?value WHERE { $subject a org:Person; rdfs:label ?value }",
 "deletePattern": "DELETE { $subject a org:Person; rdfs:label ?value} WHERE {}"
 <!---SNIP--->
 },
 {
 "id": "knows",
 "...",
 <!---SNIP--->
 "selectPattern": "SELECT ?value WHERE { $subject a org:Person; <https://ontologies.metaphacts.com/organization-ontology/knows> ?value }",
 "deletePattern": "DELETE { $subject a org:Person; <https://ontologies.metaphacts.com/organization-ontology/knows> ?value} WHERE {}"
 <!---SNIP--->
 },
 {
 "id": "project",
 "...",
 <!---SNIP--->
 "selectPattern": "SELECT ?value WHERE { $subject a org:Person; <https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn> ?value }",
 "deletePattern": "DELETE { $subject a org:Person; <https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn> ?value} WHERE {}"
 <!---SNIP--->
 } 
 ]'>
 <!--...-->
 </semantic-form> 
 

Summary

Throughout these step-by-step exercises, you have learned how to create a form with manual field definitions.

The next steps in this module includes Semantic search component, where you will learn about how to create a new search configuration.

Documentation

Learn more about semantic form in metaphactory.
Blog post: "Data authoring with metaphactory's semantic forms".

---

## Semantic Search

**Page:** `/resource/training:AdvSemanticSearchFramework`

Semantic search framework

metaphactory's semantic search is a customizable and composable framework for defining complex information needs, refining results using facets and visualizing them in different ways. In this section, you'll learn how to create a basic search page and customize it according to your use case.

Overview

The semantic search environment (semantic-search) represents the main wrapper component defining the parameters of the whole search scenario. The environment consists of a few sections: the search profile (search-profile), which defines the categories and relations that are used across other search components, the search definition components (for example, the semantic-search-query-universal component), allowing the user to express information needs and generate the initial query, the faceted filtering components, which allow the user to further refine the search request by means of different faceted views, and the results visualization components that visualize the search results in different ways.

To start working on a new search, you can create and edit a new application page. In that page, you can write a search configuration from scratch starting with a skeleton, which looks like this:

Copy
<semantic-search id="search1" search-profile="...">
 <!-- 1. search profile configuration -->
 <semantic-search-query-universal id="search-definition">
 <!-- 2. search definition -->
 </semantic-search-query-universal>

 <!-- 3. faceting -->
 <semantic-search-facet-store id="facet"></semantic-search-facet-store>
 <semantic-search-facet-group></semantic-search-facet-group>

 <semantic-search-result-holder>
 <semantic-search-result>
 <!-- 4. result visualization -->
 <!-- it is possible to use any semantic-* visualization component to
 visualize search results, e.g semantic-table -->
 <semantic-table id="table" query="..."></semantic-table>
 </semantic-search-result>
 </semantic-search-result-holder>
 </semantic-search>

Otherwise, you can start using the metaphactory wizard to help you with bootstrapping your search configuration. The wizard is invoked using the Configuration Wizards dropdown at the top of the Page Editor. After selecting Search Wizard..., you can click on Create new configuration to start configuring a fresh search. Note that you can also continue a previous search configuration or load it from an external JSON file.

Exercise 1: Creating a search page using the search wizard with default settings

The aim of this exercise is to use the search wizard to create a search configuration with the default settings, meaning you will configure your search with a model-driven search profile which will be created at runtime, based on the domain (or domains) selected. To do that, follow the next steps:

Edit a new application page.
Invoke the search wizard and start creating a new configuration.
For Step 1 in the Configuration process, keep the value as set by default.
Do the same for Count Query Optimization.
Go to next step by clicking on Next: Select classes
Navigate the Agent in Available classes for selection hierarchy and select Person.
Click on Use selected classes → to add this target domain to the configuration.
Go to the next step by clicking on Next: Generate configuration.
You can explore the configuration generated and/or go to next step Next: Insert configuration.

Your search configuration will be inserted into your application page, which should look like this:

Copy
{{> Platform:SearchResultsFragments::defaultStyle}}
 <semantic-search id="search1" search-profile='{
 "loadByDomains": [
 "<https://ontologies.metaphacts.com/organization-ontology/Person>"
 ]
}'>
 <semantic-search-query-universal id="universal-search">
 </semantic-search-query-universal>
 <semantic-search-facet-store id="facet"></semantic-search-facet-store>
 <semantic-search-result-group template="{{> searchResultGroupTemplate}}">
 <template id="searchResultGroupTemplate">
 <div class="searchTopMenu">
 {{> Platform:SearchResultsFragments::startButton}}
 {{> Platform:SearchResultsFragments::clearDomain}}
 </div>
 {{> Platform:SearchResultsFragments::searchResultGroupTemplate
 showDomainSelector=false
 showExplorationFacets=true
 }}
 </template>
 </semantic-search-result-group>
 </semantic-search>
Press Save & View in the Page Editor to save the configuration.

You will see your search page, displaying all the people instantiating the domain https://ontologies.metaphacts.com/organization-ontology/Person with the default result visualization. Moreover, on top of them you will see all of the facets to refine the search results. Since this search has been configured as model-driven, all of the relevant properties based on the specified domain will be automatically loaded.

Exercise 2: Editing a search configuration to add a new class

In this exercise, you will experiment with the search wizard option to continue the previous configuration by adding a new domain (class) to the search profile. To do that, follow the next steps:

Edit the application page.
Invoke the search wizard and select Continue previous configuration from Insert search dialog.

In the Configuration process you will see step 1 with the same default settings and step 2 Select classes marked in bold indicating that there is already a selection.

Go to next step by clicking on Next: Select classes.
Select the class Project from Available classes for selection hierarchy.
Click on Use selected classes → to add this target domain to the configuration.
Go to next step by clicking on Next: Generate configuration.
You can explore the configuration generated and/or go to next step Next: Insert configuration.

Your search configuration will be inserted into your application page. It should look like the one below, where the only change is that the class https://ontologies.metaphacts.com/organization-ontology/Project has been added to the search profile:

Copy
<!-- ... -->
 <semantic-search id="search1" search-profile='{
 "loadByDomains": [
 "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "<https://ontologies.metaphacts.com/organization-ontology/Project>"
 ]
}'>

 <div class="search">
 <!-- ... -->
 </div>
 </semantic-search>

Alternatively, it is possible to specify the reference ontology as part of the search-profile, so that the search domains (defined in loadByDomains) as well as their relations and attributes are scoped to that ontology and its imports.

Copy
<semantic-search id="search1" search-profile='{ "ontology": "https://ontologies.metaphacts.com/organization-ontology/0.1" , "loadByDomains": [ ... ]}'>
 <div class="search">
 <!-- ... -->
 </div>
</semantic-search>
Exercise 3: Creating a search page using the search wizard and selecting attributes and relations

As an alternative to the model-driven search configuration, you can choose the manual option to take control of the attributes and relations that should be added to the configuration for the domains selected. To try that, follow the steps below:

Edit a new application page.
Invoke the search wizard and start creating a new configuration.
For step 1 in the Configuration process, uncheck the Model-Driven Search Profile option.
Go to next step by clicking on Next: Select classes.
Navigate the Agent in Available classes for selection hierarchy and select Person, Project, Organization and Role.
Click on Use selected classes → to add this target domain to the configuration.
Go to next step by clicking on Next: Select relations and attributes.
Select the following relations and attributes from Attributes and relations : knows, hasMember, isInvolvedIn and hasRole .
Click on Use selected → to add these relations and properties to the configuration.
Go to next step by clicking on Next: Generate configuration.
You can explore the configuration generated and/or go to next step Next: Insert configuration.

Your search configuration will be inserted into your application page, which should look like the snippet below. Unlike the previous exercises, you will only be able to navigate through the instances of the specific domains and relations defined in categories and relations.

Copy

<div class="page">
 <div class="page__body">
 {{> Platform:SearchResultsFragments::defaultStyle}}
<semantic-search id="search1" search-profile='{
 "categories": [
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/Organization>",
 "label": "Organization"
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "label": "Person"
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/Project>",
 "label": "Project"
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/Role>",
 "label": "Role"
 }
 ],
 "relations": [
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/hasMember>",
 "label": "hasMember",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Organization>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "inverse": {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/hasMember-inverse>",
 "label": "hasMember (inverse)"
 }
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/hasRole>",
 "label": "hasRole",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Role>",
 "inverse": {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/hasRole-inverse>",
 "label": "hasRole (inverse)"
 }
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn>",
 "label": "isInvolvedIn",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Organization>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Project>",
 "inverse": {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn-inverse>",
 "label": "isInvolvedIn (inverse)"
 }
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn>",
 "label": "isInvolvedIn",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Project>",
 "inverse": {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn-inverse>",
 "label": "isInvolvedIn (inverse)"
 }
 },
 {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/knows>",
 "label": "knows",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Person>",
 "inverse": {
 "iri": "<https://ontologies.metaphacts.com/organization-ontology/knows-inverse>",
 "label": "knows (inverse)"
 }
 }
 ]
}' categories='{
 "<https://ontologies.metaphacts.com/organization-ontology/Role>": [
 {
 "queryPattern": "$subject ?__relation__ ?__value__",
 "kind": "hierarchy",
 "treePatterns": {
 "kind": "simple",
 "scheme": "https://vocabularies.metaphacts.com/role-vocabulary/0.1"
 }
 }
 ]
}'>
 <div class="search">
 <!-- ... -->
 </div>
 </semantic-search>
 </div>
</div>
 

Exercise 4: Adding a custom facet to a search page

In this exercise, you will use search query patterns for defining more complex relations, which require special bindings depending on the pattern. Follow the steps below to configure a new relation:

Edit the application page with the search definition of the exercise above.
Copy and add the next snippet to the configuration. The code there adds a new facet to filter projects by the roles associated to their members.

The snippet adds a new object relations with a queryPattern, and the special variable to be substituted by user selected values ?__value__, while the ?subject variable refers to the result projection variable, and should be always present in the query pattern. Finally, this new relation must be added to the search-profile.

Copy

 <semantic-search
 id="search1"
 relations='{
 "<http://www.metaphacts.com/ontology/sample/rolesInProject>": [{
 "kind": "resource",
 "queryPattern": "
 $subject ^<https://ontologies.metaphacts.com/organization-ontology/isInvolvedIn> ?person .
 ?person <https://ontologies.metaphacts.com/organization-ontology/hasRole> ?__value__ .
 "
 }]
 }'
 search-profile='{ 
 "categories": [ ... ],
 "relations": [
 {
 "iri": "<http://www.metaphacts.com/ontology/sample/rolesInProject>",
 "label": "hasRoleInProject",
 "hasDomain": "<https://ontologies.metaphacts.com/organization-ontology/Project>",
 "hasRange": "<https://ontologies.metaphacts.com/organization-ontology/Role>"
 }]
 }'>
 
 <div class="search">
 ...
 </div> 

 </semantic-search>
 

Exercise 5: Customizing the results visualization of a search page

The semantic search framework provides a default result visualization that can be customized. In order to visualize a search result, in this exercise you will use a semantic-search-result together with visualization components. To do that, follow the steps below:

Edit the application page with the search defintion.
First of all, copy the snippet below to add facets on top of the results.
Copy

<div class="page">
 <div class="page__body">
 <semantic-search id="search1"
 search-profile='{ ... }'>

 <div class="search">
 <semantic-search-query-universal id="universal-search">
 </semantic-search-query-universal>

 <!-- SNIPPET -->
 <div class='domainSelectorAndFacets'>
 <semantic-search-facet-store id="facet"></semantic-search-facet-store>
 <semantic-search-facet-group variant='horizontal'></semantic-search-facet-group>
 </div>
 <!-- SNIPPET -->

 </div>
 </semantic-search>
 </div>
</div>
 
Replace the default <semantic-search-result-group> ... </semantic-search-result-group> with the snippet below to add a new <semantic-search-result-holder> ... </semantic-search-result-holder> including a standard semantic-table, which will project Person instances, and their dates of birth.
Copy

<div class="page">
 <div class="page__body">
 <semantic-search id="search1"
 search-profile='{ ... }'>

 <div class="search">
 <semantic-search-query-universal id="universal-search">
 </semantic-search-query-universal>
 <div class='domainSelectorAndFacets'>
 <semantic-search-facet-store id="facet"></semantic-search-facet-store>
 <semantic-search-facet-group variant='horizontal'></semantic-search-facet-group>
 </div>

 <!-- SNIPPET -->
 <semantic-search-result-holder>
 <semantic-search-result>
 <semantic-table id='search-result-table'
 query='SELECT DISTINCT * WHERE { 
 ?subject a ?type .
 OPTIONAL { 
 ?subject <https://ontologies.metaphacts.com/organization-ontology/hasBirthday> ?dob 
 }
 }'
 options='{"showFilter": false}'
 no-result-template='<i>No results found</i>'
 class='SearchCardResult--table'
 prefetch-labels='false'>
 </semantic-table>
 </semantic-search-result>
 </semantic-search-result-holder>
 <!-- SNIPPET -->
 
 </div>
 </semantic-search>
 </div>
</div>
 

Finally, we will customize the table above by using the parameter tuple-template, which is the most advanced table configuration that provides the ability to have visualizations different from the standard.

Add the parameter tuple-template='{{> template}}' to the table.
Add the <template id='template'> definition as shown in the snippet below.
Copy

<div class="page">
 <div class="page__body">
 <semantic-search id="search1"
 search-profile='{ ... }'>

 <div class="search">
 <semantic-search-query-universal id="universal-search">
 </semantic-search-query-universal>
 <div class='domainSelectorAndFacets'>
 <semantic-search-facet-store id="facet"></semantic-search-facet-store>
 <semantic-search-facet-group variant='horizontal'></semantic-search-facet-group>
 </div>

 <semantic-search-result-holder>
 <semantic-search-result>
 <semantic-table id='search-result-table'
 query='SELECT DISTINCT * WHERE { 
 ?subject a ?type .
 OPTIONAL { 
 ?subject <https://ontologies.metaphacts.com/organization-ontology/hasBirthday> ?dob 
 }
 }'
 options='{"showFilter": false}'

 <!-- SNIPPET -->
 tuple-template='{{> template}}'
 <!-- SNIPPET -->

 no-result-template='<i>No results found</i>'
 class='SearchCardResult--table'
 prefetch-labels='false'>
 
 <!-- SNIPPET -->

 <template id='template'>
 <div style='width:100%;'>
 <mp-resource-thumbnail style="width:40px" iri="{{subject.value}}">
 </mp-resource-thumbnail>
 <semantic-link iri='{{subject.value}}'></semantic-link><br />
 <div class='float-end'>
 {{> Platform:SearchResultsFragments::addToSearchButton queryFormulationComponentId="universal-search" subject=subject.value}}
 </div>
 <b>Type: </b>
 <semantic-link iri='{{type.value}}'> </semantic-link><br />
 {{#if dob}}<b>DoB: </b> {{dob.value}}{{/if}}<br />
 <hr>
 </div>
 </template>

 <!-- SNIPPET -->

 </semantic-table>
 </semantic-search-result>
 </semantic-search-result-holder>
 </div>
 </semantic-search>
 </div>
</div>
 

As you can see, the resulting code follows the search configuration shown here and includes a semantic-table component for which the tuple-template has been redefined with the template template. The default table is customized by adding the following components: a thumbnail mp-resource-thumbnail, a semantic-link for the current subject, a semantic-link for its type, the date of birth (if exists), and finally, an additional link on the right side to explore other instances related to the current ones. Note that for this last additional link, you will reuse the template fragment {{Platform:SearchResultsFragments::addToSearchButton ... }} provided the platform.

Search services

The semantic search framework relies on the following core search services which abstract database specific configurations. Note that metaphactory comes with default configurations which are database agnostic, but that can be customized for specific use cases.

This section does not cover how to configure search indexes, but you can find documentation here.

Entity lookup: it is intended for a lookup of entities. The goal is to select and disambiguate a single entity. The following example aims at looking up for an entity by using the literal "Bob", whose types could be either "Person" or "Project".
Copy

PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX entitylookup: <http://www.metaphacts.com/ontologies/platform/service/entitylookup/>
PREFIX Service: <http://www.metaphacts.com/ontologies/platform/service/>
SELECT ?subject ?type WHERE {
 SERVICE Service:entityLookup {
 ?subject entitylookup:entityName "Bob";
 entitylookup:candidateType org:Person, org:Project;
 entitylookup:type ?type.
 }
}
 
Keyword search: it performs a search based on provided keywords. Different from the previous entity lookup, this service will search on all relevant properties. The following example aims at searching for an entity by providing a date as keyword.
Copy

PREFIX org: <https://ontologies.metaphacts.com/organization-ontology/>
PREFIX Service: <http://www.metaphacts.com/ontologies/platform/service/>
PREFIX keywordsearch: <http://www.metaphacts.com/ontologies/platform/service/keywordsearch/>
SELECT ?subject ?type WHERE {
 SERVICE Service:keywordSearch {
 ?subject keywordsearch:query "1982";
 keywordsearch:candidateType org:Organization, org:Person;
 keywordsearch:limit 100;
 keywordsearch:type ?type .
 }
}
 
Summary

Throughout these step-by-step exercises, you have learnt how to configurate metaphactory's semantic search framework: using the model-driven mechanism, selecting custom categories and relations, adding new facets, and customizing the result visualization.

This is the last section in the App Building Advanced module. The next and final step is to review the module summary.

Documentation

Learn more about the semantic search framework.
Learn more about the semantic search component.
Other types of search definition interfaces: Constant search and Form-based search.
Learn more about search services and their configurations.

---

# App Certification

## Main

**Page:** `/resource/certification:knowledgeGraphAppEngineer`

Application building certification for Knowledge Graph Application Engineers
General notes on certification process

metaphacts Academy training allows you to certify your knowledge and skills in three tracks, which correspond to the three tracks in the learning materials:

Semantic knowledge modeling
Building knowledge graph applications
metis AI

While the corresponding module provides information on certification for the other two tracks, this page focuses exclusively on the Application building track. Please note that you may choose to pursue certification in any number of tracks-one, two, or all three-and in any order you prefer. Certification will be reviewed and graded only once hands-on tasks are completed and the theoretical quiz score is 80% or higher.

Theoretical part
You need to complete the questionnaire in one go. You can NOT save and resume later.
The questionnaire contains questions with multiple choice and/or multiple select answers.
The questionnaire will be graded automatically.
Please allocate about 0.5 - 1 hour for a questionnaire.
Hands-on tasks
You should do the hands-on exercises on your individual metaphactory instance, which you are currenly using.
Once your solution for the exercise is ready, you should copy the solution’s link from your metaphactory instance and paste it into the comment section of the corresponding hands-on assignment in the LMS. This will record that you have completed the hands-on exercise.
You can save your work and resume working on your solutions at any time until the submission deadline.
Hands-on exercises will be graded by our the metaphacts Academy team after the course end date.
Certification in App building

Now, to the point!

To successfully achieve certification in this track, you are expected to complete the App building basics self-guided tutorial module of the metaphactory course. If you could not attend the session, the instructions on how to access the recording were forwarded to you via email on the next day after the session.

Note that you can take part in the certification even if you did not attend the related training sessions.

As previously mentioned, certification grading will being only once your quiz is 80% or higher and all hands-on tasks for the track have been completed.

Theoretical quiz on App building

To find the quiz:

Log in to the LMS
Find and click the training course you are currently enrolled in
Scroll down to the “Content” section and click on the quiz module
Hands-on tasks
Hands-on task 1: QAAS API
Hands-on task 2: Diagrams
Hands-on task 3: Resource template
Hands-on task 4: Knowledge panel template

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Need help with this step? This video walks you through the process: Submitting results to hands-on tasks

---

## Task 1

**Page:** `/resource/certification:BasicCertificationExercise1`

metaphactory App Building Basics
Certification Level: Knowledge Graph Application Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 1: QAAS API
In this exercise you will create a Query As A Service (QAAS) API which returns all instances of org:Person.

Description:
To create the SPARQL query to be executed by the API you can go the SPARQL editor.
Define and test your query, the click Save to store it.
To create an API that executes this query, go to Admin > Query as a (REST) Service.
Click Add Service, provide the required parameters, and click Save.
Once saved, you click on the REST URL to test the API.
For more information you can access the documentation Help:QueryAsAService .
Expected result:

QAAS definition:

Testing the API:

---

## Task 2

**Page:** `/resource/certification:BasicCertificationExercise2`

metaphactory App Building Basics
Certification Level: Knowledge Graph Application Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 2: Diagrams
In this exercise, you will create and save a diagram showing Bob, his interests and the people he knows.

Description:
To create and save a diagram, navigate to Bob's resource page and switch to the Graph View.
Alternatively, go to Assets > Diagrams and click Create Diagram. On this page you can search for Bob, using the instances search option on the bottom left of the page, then you can drag and drop the Bob instance onto the canvas.
Use the plus button on the node Bob to find the people he knows (knows) as well as other relations of Bob's connections.
Expected result:

---

## Task 3

**Page:** `/resource/certification:BasicCertificationExercise3`

metaphactory App Building Basics
Certification Level: Knowledge Graph Application Engineer (Associate)

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 3: Resource template
In this exercise, you will create a template for the type Organization using at least one component.

Description:
To find the template for Organization you can go to an instance page, e.g. metaphacts, click on the Edit button, and follow the link to Applicable Templates on the middle right section of the editor (Template:https://ontologies.metaphacts.com/organization-ontology/Organization).
On this page you can use any component you like to customize the resource pages for the type Organization. In the example below, we use the semantic-query component to query the label, and members, and the semantic-table for projects.
For more information you can access the documentation Help:TemplatesAndTemplating.
Expected result:

---

## Task 4

**Page:** `/resource/certification:BasicCertificationExercise4`

metaphactory App Building Basics
Certification Level: Knowledge Graph Application Engineer

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 4: Knowledge graph template
In this exercise, you will create a knowledge panel template for the type Organization using at least one component.

Description:
To find the template for Organization you can go to an instance page, e.g. metaphacts, click on the Edit button, and follow the link to the Knowledge Panel template on the bottom right (PanelTemplate:https://ontologies.metaphacts.com/organization-ontology/Organization).
On this page you can use any component you like to customize resource pages for the type Organization. In the example below, we use the semantic-query component to query the label, and members, and the semantic-table for projects.
To test the Knowledge Panel you can go to the graph view for an instance (e.g. metaphacts) and click on the info icon on the diagram canvas.
For more information you can access the documentation Help:KnowledgePanel.
Expected result:

---

# AI metis Basics

## Main

**Page:** `/resource/training:metisBasics`

metis basics
Goal

The metis platform combines large language models (LLM) & knowledge graphs to deliver AI agents that provide generative power, semantic precision & contextual, explainable insights.

This metaphactory metis module delves into AI service topics to support LLM-based agents for search and discovery. By the end of the module, you'll know how to create AI services, and embed a conversational AI UI component for your use case.

Understanding the use case

Now that you have learned how to create a unified semantic model and how to use this model and metaphactory's low-code approach to surface information and extract insights for relavant tasks in this domain, let's have a look at how to integrate LLM-based agents to interact with your knowledge graph via natural language.

In this module, you'll first learn how to create and configure the AI services relevant for the agent. You will then work on embedding the metaphactory AI components into your pages to support knowledge search and discovery for our use case.

Learning outcome

Throughout this guided tutorial, you will learn:

key How to configure a conversation AI agent.

key How to interact with a conversation AI to explore your knowledge graphs.

Structure
Exploring your knowledge graph with a conversational AI agent

Explore AI services
Explore conversational AI component
Interact with a conversational agent

Open

 55 minutes

Create a conversational AI agent

Create a search & discovery agent service
Setting up an UI component
Expand the knowledge graph for a conversational agent

Open

 55 minutes

Model summary

Module highlights

Open

 5 minutes

---

## Explore ConvAI

**Page:** `/resource/training:exploreConvAI`

Exploring your knowledge graph with a conversational AI agent

This module aims at exploring a knowledge graph using a search & discovery agent using the metaphactory metis AI services.

Overview

metis is an AI agent platform, that assists users with semantic modeling, search, and discovery across knowledge graphs. It combines the conversational capabilities of Large Language Models (LLMs) with the precision of semantic knowledge graphs, integrating seamlessly with the functionalities of the metaphactory platform, such as semantic search and visualization.

First of all, enabling a Search & Discovery Agent requires the setup of the metis AI services: a language model (OpenAI, Gemini, Azure) service, a conversational agent service powered by the language model, and finally the frontend component mp-conversational-ai that serves as an interface to have a dialog with the Search & Discovery Agent.

In this section, we will use the metis AI services which has been already set up: urn:service:languagemodel-openai and conversationagent-default. To explore these services, go to Adminstration > AI Services.

Exercise 1: Explore AI services

In this exercise, we will review the basics of the AI services required for exploring knowledge graphs by interacting with a conversational AI agent. For this, we will use this conversational AI from the metaphactory basics session.

Navigate to Adminstration > Service Settings > AI Services > Language Models tab.
Press edit on the Actions column to edit languagemodel-openai .
Navigate to Adminstration > Service Settings > AI Services > Agents tab.
Press edit on the Actions column to edit conversationagent-default .

Exercise 2: Explore conversation AI component

In this exercise, we will review the metaphactory frontend component mp-conversational-ai which serves as an interface to have a dialog with the Search & Discovery Agent.

Navigate to conversational AI template
Open the template to edit.
Explore the component and its parameters: default-conversation-agent-iri, example-questions, and options

Exercise 3: Interact with a conversational agent

In this exercise, we will interact with the agent and review some explanatory features in metis.

Navigate to conversational AI template
Use the first example question "List organizations".
On the agent's response, expand Steps to generate this responseexpand_less
Check Detailed information, and explore the queries executed against the knowledge graph .

Summary

Throughout these exercises, you have had the chance to learn how metaphactory metis AI services power a LLM-based conversational AI agent to interact with.

In the next module, you will learn how to create your own conversational agent.

Documentation

Learn more about metaphactory's metis .
Learn more about Search & Discovery agent.
Introducing metis.

---

## Config ConvAI

**Page:** `/resource/training:configurationConvAI`

Create a conversational AI agent

This module aims at creating a new conversational agent: the AI services required and the agent interface.

Overview

metis is an AI agent platform, that assists users with semantic modeling, search, and discovery across knowledge graphs. It combines the conversational capabilities of Large Language Models (LLMs) with the precision of semantic knowledge graphs, integrating seamlessly with the functionalities of the metaphactory platform, such as semantic search and visualization.

First of all, enabling a Search & Discovery Agent requires the setup of the metis AI services: a language model (OpenAI, Gemini, Azure) service, a conversational agent service powered by the language model, and finally the frontend component mp-conversational-ai that serves as an interface to have a dialog with the Search & Discovery Agent.

In this section, we will use the language model service already set up (urn:service:languagemodel-openai) to create a new conversational agent. Also, we will extend the knowledge to interact with the agent regarding the new data.

When interacting with the search & discovery agent be aware of some possible limitations: non-determinism, potential for hallucinations, and others detailed here

Exercise 1: Create a search & discovery agent service

In this exercise, we will create a search & discovery agent to enable users to interact via natural language with your data and using the metis AI service already set up, as explained above. Then, the creation of a new agent consists of the following three steps:

Navigate to Adminstration > Service Settings > AI Services > Agents tab.
Press Create
From Template* dropdown, select agent-searchanddiscovery (AI Services) option.

In the Configuration* part, you will see the standard template for setting this service, which can be customized accordingly. Next, you will need to configure the current search & discovery agent with both a language model (defined as a separate service), and the domain ontology that your agent should use as context for entity linking and SPARQL translation.

In the Configuration* part:
Change default IRI of the service to urn:service:conversationagent-training
Change default label to "Default Search & Discovery Agent for training"
Set the agent:languageModel with this IRI: urn:service:languagemodel-openai
Set the agent:contextOntology with this Company ontology IRI: https://ontologies.metaphacts.com/company-ontology/0.3
Press Save

Exercise 2: Setting up the UI Component and interacting with the agent

Once you created your first ever search & discovery agent service, in this exercise you will create the user interface to interact with that agent.

Create a new application page and open it for editing.
Copy and paste the snippet below.
Press Save
Start interacting with the agent.

On this template, you will need to point the search & discovery agent just created using the IRI of the service. Then as you can see in the snippet, the paramenter default-conversation-agent-iri is referencing to urn:service:conversationagent-training . To interact with the agent you can use the "example-questions" which have been set in the conversational ai component as well.

Copy
<mp-conversational-ai id="conversation-ai-test" placeholder="Talk to Conversational AI..." prompt-suggestion-template="{{> tmpl}}" default-conversation-agent-iri="urn:service:conversationagent-training" options='{"explanationOptions": {"showExplanation": true}}'>
 <template id="tmpl">
 <div class="suggestion-prompt-cards">
 <div data-flex-layout="rows stretch-stretch">
 {{#bind
 example-questions=(array-of
 "List organizations"
 "List projects"
 "List all the projects and persons involved in those projects"
 )}}

 {{#each example-questions}}
 <div data-flex-self="size-1of5 md-half sm-full" class="suggestion-prompt-card-items">
 <mp-event-trigger targets='["conversation-ai-test"]' type="ConversationalAI.Start" data='{"prompt": "{{this}}"}'>
 <button type="button" class="btn btn-secondary suggestion-prompt-card">
 <span class="suggestion-prompt-thumbnail">
 <span class="material-symbols-outlined">
 lightbulb_circle
 </span>
 </span>
 <span class="suggestion-prompt-text">{{this}}</span>
 </button>
 </mp-event-trigger>
 </div>
 {{/each}}
 {{/bind}}
 </div>
 </div>
 </template>
</mp-conversational-ai>

Exercise 3: Extend the knowledge graph for the conversational agent

In this exercise, you will extend the knowledge graph and will interact with the agent again to ask about the new data.

Navigate to the ontologies catalog.
Open the Company Ontology.
Click on Department and then go to Manage instances on the right-hand side panel.
Create the instances:
Sofware Engineering
AI Engineering
Sales
Consulting
Click on Product and the go to Manage instances on the right-hand side panel.
Create the instances:
metaphactory
metis

Then you can interact again with the agent from the conversational AI template created previously and ask about the extended knowledge graph. For example, some prompts may be "List products" and "List departments"

Summary

Throughout these exercises, you have had the chance to create your first conversational AI agent to interact with.

Documentation

Learn more about metaphactory's metis .
Learn more about Search & Discovery agent.
Introducing metis.

---

# AI Certification

## Main

**Page:** `/resource/certification:aiMetisEngineer`

metis AI certification for metis AI Engineer
General notes on certification process

metaphacts Academy training allows you to certify your knowledge and skills in three tracks, which correspond to the three tracks in the learning materials:

Semantic knowledge modeling
Building knowledge graph applications
metis AI

While the corresponding module provides information on certification for the other two tracks, this page focuses exclusively on the metis AI track. Please note that you may choose to pursue certification in any number of tracks-one, two, or all three-and in any order you prefer. Certification will be reviewed and graded only once hands-on tasks are completed and the theoretical quiz score is 80% or higher.

Theoretical part
You need to complete the questionnaire in one go. You can NOT save and resume later.
The questionnaire contains questions with multiple choice and/or multiple select answers.
The questionnaire will be graded automatically.
Please allocate about 0.5 - 1 hour for a questionnaire.
Hands-on tasks
You should do the hands-on exercises on your individual metaphactory instance, which you are currenly using.
Once your solution for the exercise is ready, you should copy the solution’s link from your metaphactory instance and paste it into the comment section of the corresponding hands-on assignment in the LMS. This will record that you have completed the hands-on exercise.
You can save your work and resume working on your solutions at any time until the submission deadline.
Hands-on exercises will be graded by our the metaphacts Academy team after the course end date.
Certification in metis AI

Now, to the point!

To successfully achieve certification in this track, you are expected to complete the metis AI basics module of the metaphactory course. If you could not attend the session, the instructions on how to access the recording were forwarded to you via email on the next day after the session.

Note that you can take part in the certification even if you did not attend the related training sessions.

As previously mentioned, certification grading will being only once your quiz is 80% or higher and all hands-on tasks for the track have been completed.

Theoretical quiz on metis AI

To find the quiz:

Log in to the LMS
Find and click the training course you are currently enrolled in
Scroll down to the “Content” section and click on the quiz module
Hands-on tasks
Hands-on task 1: Search & Discovery Agent service
Hands-on task 2: Conversational AI interface

For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Need help with this step? This video walks you through the process: Submitting results to hands-on tasks

---

## Task 1

**Page:** `/resource/certification:metisExercise1`

metaphactory metis AI services
Certification Level: metis AI Engineer

Certification hands-on tasks for this track are based on the knowledge and skills discussed in the Visual Modeling training module.
For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 1: Search & Discovery Agent
In this exercise, you will create a Search&Discovery Agent service.

Description:
To create that service you can go to Administration > Service Settings > All Services
On this page, you need to use one of the AI service templates available there
Customize the contextOntology parameter to point to the Recipes ontology
Customize languageModel using the existing LLM service
For more information you can access the documentation Help:SearchAndDiscoveryAgent .
Expected result:

---

## Task 2

**Page:** `/resource/certification:metisExercise2`

metaphactory metis AI services
Certification Level: metis AI Engineer

Certification hands-on tasks for this track are based on the knowledge and skills discussed in the Visual Modeling training module.
For each exercise, please do not forget to copy the URL for your solution from the metaphactory instance to the corresponding module in the LMS. If you have any questions, please feel free to reach out to Dmitry Pavlov at dp@metaphacts.com

Task 2: Conversational AI interface
In this exercise, you will create a conversational AI interface to talk with your data.

Description:
To create this UI, you need to create a new application template
On this new template, embed the mp-conversational-ai semantic component and customize it by pointing to the search and discovery agent created in the previous exercise
Finally:
Add at least 2 example questions
Show explanations
Execute at leat one of the example questios
For more information you can access the documentation Help:SearchAndDiscoveryAgent#setting-up-the-ui-component .
Expected result:

---

