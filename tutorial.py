#!/usr/bin/env python3
"""
MIGx Knowledge Graph — Comprehensive Metaphactory Tutorial (Video Recording)

Records a screen-capture video of building the complete MIGx KG through the
metaphactory 5.10.0 web interface. Covers ALL asset types in the gold layer:
  - Namespace registration
  - Common foundation (SPARQL INSERT)
  - Ontologies with classes, attributes (domain+type), relations (domain+range), owl:imports
  - Vocabularies with hierarchical concepts (broader/narrower), definitions
  - SHACL shapes (Data Import)
  - Instance data (Manage Instances UI + Data Import)
  - Competency Questions (Data Import)
  - SPARQL query execution
  - DCAT Dataset cards
  - Data Quality / SHACL validation
  - Cross-domain verification diagram

Prerequisites:
    pip install playwright
    playwright install chromium
    GraphDB running at localhost:7200 with empty 'migx-kg-metaphactory' repo
    metaphactory running at localhost:10214 pointed at that repo

Usage:
    python3 tutorial.py              # full tutorial, headless + video
    python3 tutorial.py --headed     # watch live in a browser window
    python3 tutorial.py --phase 2    # run only phase 2
"""
import argparse
import os
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, expect

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
BASE_URL = "http://localhost:10214"
GRAPHDB_URL = "http://localhost:7200"
USERNAME = "admin"
PASSWORD = "admin"
GOLD_DIR = Path("/Users/kiptengwer/Documents/MIGxKG/gold")
VIDEO_DIR = Path(__file__).parent / "recordings"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"
SLOW_MO = 200  # ms between actions for readability


# ═══════════════════════════════════════════════════════════════════════════════
# DATA DEFINITIONS — comprehensive gold layer content
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class OntologyDef:
    title: str
    iri: str
    imports: list = field(default_factory=list)
    classes: list = field(default_factory=list)
    # (name, domain_class, datatype) — datatype properties
    attributes: list = field(default_factory=list)
    # (name, domain_class, range_class) — object properties
    relations: list = field(default_factory=list)


@dataclass
class ConceptDef:
    label: str
    definition: str = ""
    broader: str = ""  # parent concept label (empty = top-level)


@dataclass
class VocabularyDef:
    title: str
    iri: str
    concepts: list = field(default_factory=list)  # list of ConceptDef


# ─────────────────────────────────────────────────────────────────────────────
# Namespace registry (Phase 0)
# ─────────────────────────────────────────────────────────────────────────────
NAMESPACES = [
    ("common",              "https://purl.migx.ch/common/"),
    ("knowledge",           "https://knowledge.migx.ch/"),
    ("migx-ent",            "https://purl.migx.ch/ontology/enterprise/"),
    ("cptEnt",              "https://purl.migx.ch/terminology/enterprise/"),
    ("migx-org-o",          "https://purl.migx.ch/ontology/organization/"),
    ("migx-org-i",          "https://purl.migx.ch/instance/organization/"),
    ("migx-org-s",          "https://purl.migx.ch/shape/organization/"),
    ("migx-person-o",       "https://purl.migx.ch/ontology/person/"),
    ("migx-person-i",       "https://purl.migx.ch/instance/person/"),
    ("migx-person-s",       "https://purl.migx.ch/shape/person/"),
    ("migx-employee-o",     "https://purl.migx.ch/ontology/employee/"),
    ("migx-employee-i",     "https://purl.migx.ch/instance/employee/"),
    ("migx-employee-s",     "https://purl.migx.ch/shape/employee/"),
    ("onItSys",             "https://purl.migx.ch/ontology/it_system/"),
    ("cptItSys",            "https://purl.migx.ch/terminology/it_system/"),
    ("shItSys",             "https://purl.migx.ch/shapes/it_system/"),
    ("migx-it-i",           "https://purl.migx.ch/instance/it_system/"),
    ("migx-skill-o",        "https://purl.migx.ch/ontology/skill/"),
    ("migx-skill-t",        "https://purl.migx.ch/terminology/skill/"),
    ("migx-skill-s",        "https://purl.migx.ch/shape/skill/"),
    ("migx-skill-i",        "https://purl.migx.ch/instance/skill/"),
    ("migx-proficiency-t",  "https://purl.migx.ch/terminology/proficiency-level/"),
    ("migx-project",        "https://purl.migx.ch/ontology/project/"),
    ("migx-project-i",      "https://purl.migx.ch/instance/project/"),
    ("migx-project-s",      "https://purl.migx.ch/shape/project/"),
    ("migx-account-s",      "https://purl.migx.ch/shape/account/"),
    ("migx-account-i",      "https://purl.migx.ch/instance/account/"),
    ("itsm-o",              "https://purl.migx.ch/ontology/itsm/"),
    ("cptITSM",             "https://purl.migx.ch/terminology/itsm/"),
    ("itsm-s",              "https://purl.migx.ch/shape/itsm/"),
    ("csa-o",               "https://purl.migx.ch/ontology/csa/"),
    ("csa-t",               "https://purl.migx.ch/terminology/csa/"),
    ("migx-pos",            "https://purl.migx.ch/terminology/position/"),
    ("migx-site-i",         "https://purl.migx.ch/instance/site/"),
    ("migx-seg-t",          "https://purl.migx.ch/terminology/segment/"),
    ("migx-svc-t",          "https://purl.migx.ch/terminology/service/"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Enterprise Ontology (Phase 2) — core of the KG
# ─────────────────────────────────────────────────────────────────────────────
ENTERPRISE_ONTOLOGY = OntologyDef(
    title="MIGx Enterprise Ontology",
    iri="https://purl.migx.ch/ontology/enterprise/",
    imports=[
        "http://www.w3.org/2004/02/skos/core",
        "http://xmlns.com/foaf/0.1/",
        "https://schema.org/",
        "http://www.w3.org/ns/org#",
    ],
    classes=[
        "Organization", "Person", "Employee", "Role", "Position",
        "Department", "Team", "BusinessUnit", "OfficeSite",
        "Project", "ProjectAssignment", "Service", "Solution",
        "Account", "Contact", "Skill", "SkillCategory",
        "SkillAssessment", "Certification", "Education",
        "ITSystem", "BusinessProcess", "MarketSegment",
        "GovernanceStructure", "Policy",
    ],
    attributes=[
        ("skillLevel",              "SkillAssessment",    "integer"),
        ("dealId",                  "Project",            "string"),
        ("dealName",                "Project",            "string"),
        ("startDate",               "Project",            "date"),
        ("endDate",                 "Project",            "date"),
        ("timeAllocationPercentage","ProjectAssignment",  "decimal"),
        ("assignmentRole",          "ProjectAssignment",  "string"),
        ("certificationDate",       "Certification",      "date"),
    ],
    relations=[
        ("isPerson",         "Employee",           "Person"),
        ("hasRole",          "Employee",           "Position"),
        ("memberOf",         "Employee",           "Organization"),
        ("worksAt",          "Person",             "OfficeSite"),
        ("hasClient",        "Project",            "Organization"),
        ("hasDeliveryLead",  "Project",            "Person"),
        ("hasSkill",         "Person",             "Skill"),
        ("belongsToCategory","Skill",              "SkillCategory"),
        ("hasContact",       "Account",            "Contact"),
        ("providesService",  "Organization",       "Service"),
        ("hasProjectAssignment","Person",           "ProjectAssignment"),
        ("forProject",       "ProjectAssignment",  "Project"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# Enterprise Terminology (Phase 3)
# ─────────────────────────────────────────────────────────────────────────────
ENTERPRISE_VOCAB = VocabularyDef(
    title="Enterprise Terminology",
    iri="https://purl.migx.ch/terminology/enterprise/",
    concepts=[
        ConceptDef("Enterprise Domain", "Top-level concept for enterprise domain"),
        ConceptDef("Organization",     "Legal entity or business unit",          "Enterprise Domain"),
        ConceptDef("Person",           "Individual associated with the enterprise","Enterprise Domain"),
        ConceptDef("Employee",         "Person employed by the organization",    "Enterprise Domain"),
        ConceptDef("Role",             "Organizational role or function",         "Enterprise Domain"),
        ConceptDef("Position",         "Job position within the organization",   "Enterprise Domain"),
        ConceptDef("Department",       "Organizational subdivision",             "Enterprise Domain"),
        ConceptDef("Team",             "Working group within a department",      "Enterprise Domain"),
        ConceptDef("Project",          "Time-bounded initiative with deliverables","Enterprise Domain"),
        ConceptDef("Service",          "Offering provided by the organization",  "Enterprise Domain"),
        ConceptDef("Skill",            "Competency or knowledge area",           "Enterprise Domain"),
        ConceptDef("Account",          "Client account in CRM",                  "Enterprise Domain"),
        ConceptDef("OfficeSite",       "Physical office location",               "Enterprise Domain"),
        ConceptDef("ITSystem",         "Software application or platform",       "Enterprise Domain"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# IT System Ontology (Phase 4)
# ─────────────────────────────────────────────────────────────────────────────
IT_SYSTEM_ONTOLOGY = OntologyDef(
    title="IT Systems Inventory Ontology",
    iri="https://purl.migx.ch/ontology/it_system/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[
        "Application", "Integration", "DataFlow",
        "SystemCategory", "LifecycleStatus", "DataClassification",
        "ImpactLevel", "IntegrationMethod", "IntegrationDirection",
        "SyncFrequency", "DataField",
    ],
    attributes=[
        ("applicationName",  "Application",   "string"),
        ("vendorName",       "Application",   "string"),
        ("ssoEnabled",       "Application",   "boolean"),
        ("deploymentModel",  "Application",   "string"),
    ],
    relations=[
        ("hasCategory",          "Application",   "SystemCategory"),
        ("hasLifecycleStatus",   "Application",   "LifecycleStatus"),
        ("hasDataClassification","Application",   "DataClassification"),
        ("hasImpact",            "Application",   "ImpactLevel"),
        ("businessOwner",        "Application",   "Person"),
        ("technicalOwner",       "Application",   "Person"),
        ("integrationOwner",     "Integration",   "Person"),
        ("sourceSystem",         "Integration",   "Application"),
        ("targetSystem",         "Integration",   "Application"),
        ("hasIntegrationMethod", "Integration",   "IntegrationMethod"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# IT System Terminology (Phase 5)
# ─────────────────────────────────────────────────────────────────────────────
IT_SYSTEM_VOCAB = VocabularyDef(
    title="IT System Terminology",
    iri="https://purl.migx.ch/terminology/it_system/",
    concepts=[
        ConceptDef("Application",          "IT application providing business functionality"),
        ConceptDef("Integration",          "Data integration connecting two or more systems"),
        ConceptDef("DataFlow",             "Unidirectional flow of data between systems"),
        ConceptDef("SystemCategory",       "Functional category classifying IT systems"),
        ConceptDef("IT",                   "Information Technology systems",          "SystemCategory"),
        ConceptDef("BI",                   "Business Intelligence and analytics",     "SystemCategory"),
        ConceptDef("Finance",              "Financial management systems",            "SystemCategory"),
        ConceptDef("HR",                   "Human Resources systems",                "SystemCategory"),
        ConceptDef("CRM",                  "Customer Relationship Management",       "SystemCategory"),
        ConceptDef("ResourceManagement",   "Resource planning and allocation",       "SystemCategory"),
        ConceptDef("LifecycleStatus",      "Phase of an IT system in its lifecycle"),
        ConceptDef("Active",               "System is in active production use",     "LifecycleStatus"),
        ConceptDef("Deprecated",           "System marked for phase-out",            "LifecycleStatus"),
        ConceptDef("Decommissioned",       "System permanently retired",             "LifecycleStatus"),
        ConceptDef("DataClassification",   "Sensitivity level of data handled"),
        ConceptDef("Internal",             "Internal use only",                      "DataClassification"),
        ConceptDef("Confidential",         "Restricted access required",             "DataClassification"),
        ConceptDef("ImpactLevel",          "Business impact if system unavailable"),
        ConceptDef("CriticalImpact",       "Immediate business disruption",          "ImpactLevel"),
        ConceptDef("HighImpact",           "Significant operational impact",         "ImpactLevel"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# Skills Ontology (Phase 6) — extends enterprise
# ─────────────────────────────────────────────────────────────────────────────
SKILLS_ONTOLOGY = OntologyDef(
    title="MIGx Skills Ontology",
    iri="https://purl.migx.ch/ontology/skill/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[
        "SkillProficiency", "ProficiencyLevel",
    ],
    attributes=[
        ("proficiencyDate",  "SkillProficiency",  "date"),
        ("verifiedBy",       "SkillProficiency",  "string"),
    ],
    relations=[
        ("hasEducation",          "Person",          "Education"),
        ("holdsCertification",    "Person",          "Certification"),
        ("hasDomainExpertise",    "Person",          "Domain"),
        ("hasExperienceWith",     "Person",          "Technology"),
        ("acquiredThrough",       "Skill",           "Education"),
        ("validatedBy",           "Skill",           "Certification"),
        ("hasSkillProficiency",   "Person",          "SkillProficiency"),
        ("forSkill",              "SkillProficiency", "Skill"),
        ("atProficiencyLevel",    "SkillProficiency", "ProficiencyLevel"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# Skills Terminology (Phase 7) — 4 top-level skill families
# ─────────────────────────────────────────────────────────────────────────────
SKILLS_VOCAB = VocabularyDef(
    title="MIGx Skills Terminology",
    iri="https://purl.migx.ch/terminology/skill/",
    concepts=[
        ConceptDef("Business Analysis",    "BA skills: requirements, process modeling, stakeholder management"),
        ConceptDef("Business Intelligence","BI skills: reporting, data visualization, dashboards"),
        ConceptDef("Data and AI",          "Data engineering, machine learning, AI/ML skills"),
        ConceptDef("Enterprise IT",        "Infrastructure, DevOps, cloud, security skills"),
        ConceptDef("Requirements Engineering","Elicitation, analysis, documentation",  "Business Analysis"),
        ConceptDef("Process Modeling",     "BPMN, workflow design",                     "Business Analysis"),
        ConceptDef("Power BI",            "Microsoft Power BI platform",                "Business Intelligence"),
        ConceptDef("Tableau",             "Tableau visualization platform",             "Business Intelligence"),
        ConceptDef("Python",              "Python programming language",                "Data and AI"),
        ConceptDef("Machine Learning",    "ML algorithms and model training",           "Data and AI"),
        ConceptDef("Knowledge Graphs",    "Semantic web, RDF, SPARQL, OWL",            "Data and AI"),
        ConceptDef("Cloud Architecture",  "AWS, Azure, GCP infrastructure",            "Enterprise IT"),
        ConceptDef("DevOps",             "CI/CD, containers, automation",              "Enterprise IT"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# ITSM Ontology (Phase 8) — IT Service Management governance
# ─────────────────────────────────────────────────────────────────────────────
ITSM_ONTOLOGY = OntologyDef(
    title="IT Service Management Ontology",
    iri="https://purl.migx.ch/ontology/itsm/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[
        "GovernedDocument", "Policy", "StandardOperatingProcedure",
        "OperationalGuide", "ServiceArea", "PriorityLevel",
        "AccessRequest", "ApprovalRule", "AITool",
        "CollaborationTool", "DataClassificationLevel",
        "AuthenticationMethod", "DeviceType", "EscalationRole",
        "SecurityIncidentType", "SoftwareCategory", "LifecycleProcess",
    ],
    attributes=[
        ("documentId",    "GovernedDocument",  "string"),
        ("responseTime",  "PriorityLevel",     "string"),
        ("resolutionTime","PriorityLevel",     "string"),
        ("usagePolicy",   "AITool",            "string"),
    ],
    relations=[
        ("governs",              "GovernedDocument",   "ServiceArea"),
        ("derivesAuthorityFrom", "GovernedDocument",   "GovernedDocument"),
        ("hasPriority",          "AccessRequest",      "PriorityLevel"),
        ("requiresApproval",     "AccessRequest",      "ApprovalRule"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# ITSM Terminology (Phase 9)
# ─────────────────────────────────────────────────────────────────────────────
ITSM_VOCAB = VocabularyDef(
    title="ITSM Terminology",
    iri="https://purl.migx.ch/terminology/itsm/",
    concepts=[
        ConceptDef("IT Service Management",  "Top-level concept for ITSM domain"),
        ConceptDef("GovernedDocument",   "Formal IT governance document",           "IT Service Management"),
        ConceptDef("Policy",             "IT Security Policy (POL-IS-XX)",          "GovernedDocument"),
        ConceptDef("SOP",                "Standard Operating Procedure (SOP-IS-XX)","GovernedDocument"),
        ConceptDef("OperationalGuide",   "How-to guide for IT operations",         "GovernedDocument"),
        ConceptDef("ServiceArea",        "Domain of IT support capability",         "IT Service Management"),
        ConceptDef("ITServiceManagement","General ITSM services",                  "ServiceArea"),
        ConceptDef("IdentityAccessMgmt", "Identity and access management",          "ServiceArea"),
        ConceptDef("SecurityOperations", "Security monitoring and response",        "ServiceArea"),
        ConceptDef("PriorityLevel",      "Ticket priority classification",          "IT Service Management"),
        ConceptDef("P1 Critical",        "Critical: 1h response, 4h resolution",   "PriorityLevel"),
        ConceptDef("P2 High",            "High: 4h response, 8h resolution",       "PriorityLevel"),
        ConceptDef("P3 Medium",          "Medium: 8h response, 24h resolution",    "PriorityLevel"),
        ConceptDef("P4 Low",             "Low: 24h response, 72h resolution",      "PriorityLevel"),
        ConceptDef("AITool",             "AI platform with usage classification",   "IT Service Management"),
        ConceptDef("EscalationRole",     "IT governance escalation chain role",     "IT Service Management"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# CSA Ontology (Phase 10) — Computer Software Assurance
# ─────────────────────────────────────────────────────────────────────────────
CSA_ONTOLOGY = OntologyDef(
    title="CSA Ontology",
    iri="https://purl.migx.ch/ontology/csa/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[
        "ValidationPhase", "ValidationActivity",
    ],
    attributes=[],
    relations=[
        ("timelyPrecedes",  "ValidationActivity",  "ValidationActivity"),
        ("timelyFollows",   "ValidationActivity",  "ValidationActivity"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# CSA Terminology (Phase 11)
# ─────────────────────────────────────────────────────────────────────────────
CSA_VOCAB = VocabularyDef(
    title="CSA Terminology",
    iri="https://purl.migx.ch/terminology/csa/",
    concepts=[
        ConceptDef("Computer Software Assurance",  "Top-level CSA concept"),
        ConceptDef("Concept Phase",         "Initial qualification planning",      "Computer Software Assurance"),
        ConceptDef("Project Phase",         "System development and testing",      "Computer Software Assurance"),
        ConceptDef("Operation Phase",       "Production use and maintenance",      "Computer Software Assurance"),
        ConceptDef("Retirement Phase",      "System decommissioning",             "Computer Software Assurance"),
        ConceptDef("Requirements",          "Functional and non-functional requirements", "Project Phase"),
        ConceptDef("RiskAssessment",        "Risk analysis and evaluation",        "Concept Phase"),
        ConceptDef("ValidationPlanning",    "Planning validation activities",      "Concept Phase"),
        ConceptDef("Verification",          "Testing and verification activities", "Project Phase"),
        ConceptDef("Release",              "Software release management",          "Project Phase"),
        ConceptDef("ChangeManagement",     "Change control processes",             "Operation Phase"),
        ConceptDef("PeriodicReview",       "Regular system reviews",               "Operation Phase"),
        ConceptDef("Decommissioning",      "System shutdown and disposal",         "Retirement Phase"),
        ConceptDef("DataMigration",        "Data transfer to replacement systems", "Retirement Phase"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# Supporting Ontologies (Phase 12) — Person, Employee, Project
# ─────────────────────────────────────────────────────────────────────────────
PERSON_ONTOLOGY = OntologyDef(
    title="Person Ontology",
    iri="https://purl.migx.ch/ontology/person/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[],
    attributes=[],
    relations=[],
)

EMPLOYEE_ONTOLOGY = OntologyDef(
    title="Employee Ontology",
    iri="https://purl.migx.ch/ontology/employee/",
    imports=[
        "https://purl.migx.ch/ontology/enterprise/",
        "https://purl.migx.ch/ontology/person/",
    ],
    classes=[],
    attributes=[
        ("oid", "Employee", "string"),
    ],
    relations=[],
)

PROJECT_ONTOLOGY = OntologyDef(
    title="Project Ontology",
    iri="https://purl.migx.ch/ontology/project/",
    imports=["https://purl.migx.ch/ontology/enterprise/"],
    classes=[],
    attributes=[
        ("dealId",      "Project",  "string"),
        ("dealName",    "Project",  "string"),
        ("startDate",   "Project",  "date"),
        ("endDate",     "Project",  "date"),
        ("probability", "Project",  "decimal"),
        ("stage",       "Project",  "string"),
    ],
    relations=[
        ("hasClient",        "Project",  "Organization"),
        ("hasDeliveryLead",  "Project",  "Person"),
        ("hasOwner",         "Project",  "Person"),
        ("hasServiceType",   "Project",  "Service"),
    ],
)

# ─────────────────────────────────────────────────────────────────────────────
# Files to upload via Data Import (Phase 13-15)
# ─────────────────────────────────────────────────────────────────────────────
SHAPE_FILES = [
    ("gold/organization/organization-s.ttl", "https://purl.migx.ch/shape/organization"),
    ("gold/person/person-s.ttl",             "https://purl.migx.ch/shape/person"),
    ("gold/employee/employee-s.ttl",         "https://purl.migx.ch/shape/employee"),
    ("gold/it_system/it_system-s.ttl",       "https://purl.migx.ch/shapes/it_system"),
    ("gold/skills/skills-s.ttl",             "https://purl.migx.ch/shape/skill"),
    ("gold/project/project-s.ttl",           "https://purl.migx.ch/shape/project"),
    ("gold/account/account-s.ttl",           "https://purl.migx.ch/shape/account"),
    ("gold/itsm/itsm-s.ttl",                "https://purl.migx.ch/shape/itsm"),
]

INSTANCE_FILES = [
    ("gold/organization/organization-i.ttl",     "https://purl.migx.ch/instance/organization"),
    ("gold/organization/migx_sites-i.ttl",       "https://purl.migx.ch/instance/site"),
    ("gold/person/person-i.ttl",                 "https://purl.migx.ch/instance/person"),
    ("gold/employee/employee-i.ttl",             "https://purl.migx.ch/instance/employee"),
    ("gold/project/project-i.ttl",               "https://purl.migx.ch/instance/project"),
    ("gold/project/project_assignment-i.ttl",    "https://purl.migx.ch/instance/project/assignment"),
    ("gold/skills/skills-i.ttl",                 "https://purl.migx.ch/instance/skill"),
    ("gold/account/account-i.ttl",               "https://purl.migx.ch/instance/account"),
    ("gold/account/account_contact-i.ttl",       "https://purl.migx.ch/instance/account_contact"),
    ("gold/account/account_mapping-i.ttl",       "https://purl.migx.ch/instance/account_mapping"),
    ("gold/it_system/it_system-i.ttl",           "https://purl.migx.ch/instance/it_system"),
]

TERMINOLOGY_FILES = [
    ("gold/organization/enterprise-t.ttl",       "https://purl.migx.ch/terminology/enterprise"),
    ("gold/organization/migx_positions-t.ttl",   "https://purl.migx.ch/terminology/position"),
    ("gold/organization/professional_services-t.ttl", "https://purl.migx.ch/terminology/service"),
    ("gold/organization/segment-t.ttl",          "https://purl.migx.ch/terminology/segment"),
    ("gold/it_system/it_system-t.ttl",           "https://purl.migx.ch/terminology/it_system"),
    ("gold/skills/skills-t.ttl",                 "https://purl.migx.ch/terminology/skill"),
    ("gold/skills/proficiency_level-t.ttl",      "https://purl.migx.ch/terminology/proficiency-level"),
    ("gold/itsm/itsm-t.ttl",                    "https://purl.migx.ch/terminology/itsm"),
    ("gold/csa/csa-t.ttl",                      "https://purl.migx.ch/terminology/csa"),
    ("gold/csa/csa-gsk-t.ttl",                  "https://purl.migx.ch/terminology/csa-gsk"),
]

CQ_AND_SQ_FILES = [
    ("gold/organization/enterprise-cq.ttl",  "https://purl.migx.ch/competency-questions/enterprise"),
    ("gold/organization/enterprise-sq.ttl",  "https://purl.migx.ch/sparql/enterprise"),
    ("gold/it_system/it_system-cq.ttl",      "https://purl.migx.ch/terminology/it_system/competency-question"),
    ("gold/it_system/it_system-sq.ttl",      "https://purl.migx.ch/sparql/it_system"),
    ("gold/skills/skills-cq.ttl",            "https://purl.migx.ch/terminology/skill/competency-question"),
    ("gold/skills/skills-sq.ttl",            "https://purl.migx.ch/sparql/skill"),
    ("gold/itsm/itsm-cq.ttl",               "https://purl.migx.ch/terminology/itsm/competency-question"),
    ("gold/itsm/itsm-sq.ttl",               "https://purl.migx.ch/sparql/itsm"),
    ("gold/csa/csa-cq.ttl",                 "https://purl.migx.ch/terminology/csa/competency-question"),
    ("gold/csa/csa-sq.ttl",                 "https://purl.migx.ch/sparql/csa"),
]

ONTOLOGY_FILES = [
    ("gold/common.ttl",                      "https://purl.migx.ch/common"),
    ("gold/organization/enterprise-o.ttl",   "https://purl.migx.ch/ontology/enterprise"),
    ("gold/organization/organization-o.ttl", "https://purl.migx.ch/ontology/organization"),
    ("gold/person/person-o.ttl",             "https://purl.migx.ch/ontology/person"),
    ("gold/employee/employee-o.ttl",         "https://purl.migx.ch/ontology/employee"),
    ("gold/it_system/it_system-o.ttl",       "https://purl.migx.ch/ontology/it_system"),
    ("gold/skills/skills-o.ttl",             "https://purl.migx.ch/ontology/skill"),
    ("gold/project/project-o.ttl",           "https://purl.migx.ch/ontology/project"),
    ("gold/itsm/itsm-o.ttl",                "https://purl.migx.ch/ontology/itsm"),
    ("gold/csa/csa-o.ttl",                  "https://purl.migx.ch/ontology/csa"),
]

# ─────────────────────────────────────────────────────────────────────────────
# Representative SPARQL queries to demonstrate (Phase 16)
# ─────────────────────────────────────────────────────────────────────────────
DEMO_QUERIES = [
    (
        "Enterprise: Organization Structure",
        """PREFIX migx-ent: <https://purl.migx.ch/ontology/enterprise/>
PREFIX org: <http://www.w3.org/ns/org#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <https://schema.org/>

SELECT ?employee ?name ?jobTitle ?org ?orgName WHERE {
    ?employee a migx-ent:Employee ;
        migx-ent:isPerson ?person ;
        schema:jobTitle ?jobTitle ;
        org:memberOf ?org .
    ?person foaf:name ?name .
    ?org rdfs:label ?orgName .
} LIMIT 20""",
    ),
    (
        "IT Systems: Application Portfolio",
        """PREFIX onItSys: <https://purl.migx.ch/ontology/it_system/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?app ?appName ?category ?status WHERE {
    ?app a onItSys:Application ;
        skos:prefLabel ?appName ;
        onItSys:hasCategory ?cat ;
        onItSys:hasLifecycleStatus ?st .
    ?cat skos:prefLabel ?category .
    ?st skos:prefLabel ?status .
} ORDER BY ?category""",
    ),
    (
        "Skills: Team Capability Heatmap",
        """PREFIX migx-ent: <https://purl.migx.ch/ontology/enterprise/>
PREFIX migx-skill-o: <https://purl.migx.ch/ontology/skill/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?personName ?skillName ?level WHERE {
    ?person a migx-ent:Person ;
        foaf:name ?personName ;
        migx-ent:hasSkillProficiency ?sp .
    ?sp migx-skill-o:forSkill ?skill ;
        migx-skill-o:atProficiencyLevel ?pl .
    ?skill skos:prefLabel ?skillName .
    ?pl skos:prefLabel ?level .
} ORDER BY ?personName LIMIT 30""",
    ),
    (
        "Cross-Domain: Count all triples per named graph",
        """SELECT ?graph (COUNT(*) AS ?triples) WHERE {
    GRAPH ?graph { ?s ?p ?o }
} GROUP BY ?graph ORDER BY DESC(?triples)""",
    ),
]


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show_banner(page: Page, text: str, sub: str = ""):
    """Inject a visible overlay banner at the top of the page."""
    sub_html = f'<div style="font-size:16px;margin-top:4px;opacity:0.8">{sub}</div>' if sub else ""
    page.evaluate(f"""() => {{
        let b = document.getElementById('tutorial-banner');
        if (!b) {{
            b = document.createElement('div');
            b.id = 'tutorial-banner';
            b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;'
                + 'background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;'
                + 'padding:18px 32px;font:bold 22px/1.3 system-ui;text-align:center;'
                + 'box-shadow:0 4px 20px rgba(0,0,0,0.4);border-bottom:3px solid #0f3460;'
                + 'pointer-events:none';
            document.body.prepend(b);
        }}
        b.innerHTML = `{text}{sub_html}`;
    }}""")
    time.sleep(2.5)


def clear_banner(page: Page):
    page.evaluate("() => { let b = document.getElementById('tutorial-banner'); if(b) b.remove(); }")


def take_screenshot(page: Page, name: str):
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SCREENSHOT_DIR / f"{name}.png"), full_page=False)


def _dismiss_import_modal(page: Page):
    """Force-close the Import ontology modal if it's still open."""
    for attempt in range(3):
        try:
            modal = page.locator('.import-ontology-modal.show')
            if modal.is_visible(timeout=500):
                # Try close button, then Escape, then JS removal
                close_btn = modal.locator('.btn-close, [class*="close"], button:has-text("Cancel"), button:has-text("Close")').first
                if close_btn.is_visible(timeout=300):
                    close_btn.click(force=True)
                    time.sleep(0.5)
                else:
                    page.keyboard.press('Escape')
                    time.sleep(0.5)

                # If still visible, force-remove via JS
                if modal.is_visible(timeout=300):
                    page.evaluate("""() => {
                        document.querySelectorAll('.import-ontology-modal.show').forEach(m => m.remove());
                        document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
                        document.body.classList.remove('modal-open');
                        document.body.style.removeProperty('overflow');
                        document.body.style.removeProperty('padding-right');
                    }""")
                    time.sleep(0.3)
            else:
                break
        except:
            # Last resort: JS cleanup
            try:
                page.evaluate("""() => {
                    document.querySelectorAll('.import-ontology-modal').forEach(m => m.remove());
                    document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
                    document.body.classList.remove('modal-open');
                    document.body.style.removeProperty('overflow');
                    document.body.style.removeProperty('padding-right');
                }""")
                time.sleep(0.3)
            except:
                break


def dismiss_walkthrough(page: Page):
    """Close the 'Welcome to...' walkthrough carousel if it appears."""
    for _ in range(5):
        try:
            modal = page.locator('.walkthroughCarousel.show, .modal.show')
            if modal.is_visible(timeout=1000):
                close_btn = page.locator('.modal.show .btn-close, .modal.show [class*="close"]')
                if close_btn.count() > 0 and close_btn.first.is_visible(timeout=500):
                    close_btn.first.click(force=True)
                else:
                    page.mouse.click(10, 10)
                    if modal.is_visible(timeout=500):
                        page.keyboard.press('Escape')
            else:
                break
        except:
            page.keyboard.press('Escape')
    time.sleep(0.3)


def login(page: Page):
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', USERNAME)
    page.fill('input[name="password"]', PASSWORD)
    page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle")
    time.sleep(1)


def ensure_logged_in(page: Page, target_url: str = ""):
    """Re-login if the session has expired (redirected to login page)."""
    if "/login" in page.url:
        print("  Session expired — re-logging in")
        page.fill('input[name="username"]', USERNAME)
        page.fill('input[name="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_load_state("networkidle")
        time.sleep(1)
        # Re-navigate to the intended target if provided
        if target_url and target_url not in page.url:
            page.goto(target_url)
            page.wait_for_load_state("networkidle")
            time.sleep(1)


def navigate(page: Page, url: str):
    """Navigate to a URL, retry on transient errors, re-login if session expired."""
    for attempt in range(3):
        try:
            page.goto(url)
            page.wait_for_load_state("networkidle")
            ensure_logged_in(page, url)
            return
        except Exception as e:
            if "ERR_CONNECTION" in str(e) and attempt < 2:
                wait = 10 * (attempt + 1)
                print(f"  Server unavailable, waiting {wait}s (attempt {attempt + 1}/3)...")
                time.sleep(wait)
            else:
                raise


def safe_click(page: Page, selector: str, timeout: int = 3000):
    """Click an element, waiting for it to be visible first."""
    try:
        el = page.locator(selector).first
        el.wait_for(state="visible", timeout=timeout)
        el.click()
        return True
    except:
        return False


def safe_fill(page: Page, selector: str, value: str, timeout: int = 3000):
    """Fill a field, waiting for it to be visible first."""
    try:
        el = page.locator(selector).first
        el.wait_for(state="visible", timeout=timeout)
        el.fill(value)
        return True
    except:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 0: LOGIN & NAMESPACE REGISTRATION
# ═══════════════════════════════════════════════════════════════════════════════

def phase_0_namespaces(page: Page):
    show_banner(page, "Phase 0: Namespace Registration", "Admin > Namespaces — registering all custom prefixes")
    take_screenshot(page, "p00-start")

    navigate(page, f"{BASE_URL}/resource/Admin:Namespaces")
    time.sleep(2)
    take_screenshot(page, "p00-namespace-page")

    registered = 0
    for prefix, namespace in NAMESPACES:
        try:
            # Scroll to bottom where the registration form is
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(0.3)

            # Exact placeholder selectors from DOM exploration
            prefix_input = page.locator('input[placeholder="Prefix"]').first
            prefix_input.wait_for(state="visible", timeout=2000)
            # Use click + clear + type (not fill) to trigger form validation events
            prefix_input.click()
            prefix_input.fill("")
            prefix_input.type(prefix)

            ns_input = page.locator('input[placeholder="Namespace"]').first
            ns_input.click()
            ns_input.fill("")
            ns_input.type(namespace)
            time.sleep(0.5)

            # Wait for "Set Namespace" button to become enabled
            set_btn = page.locator('button:has-text("Set Namespace")').first
            set_btn.wait_for(state="visible", timeout=2000)
            # Button may be disabled until validation fires; wait briefly
            for _ in range(10):
                if set_btn.get_attribute("disabled") is None:
                    break
                time.sleep(0.2)

            if set_btn.get_attribute("disabled") is None:
                set_btn.click()
                time.sleep(0.5)

                # Handle override confirmation dialog (exact data-testid from DOM exploration)
                try:
                    confirm_btn = page.locator('[data-testid="confirmation-dialog-button-confirm"]').first
                    if confirm_btn.is_visible(timeout=2000):
                        confirm_btn.click()
                        time.sleep(0.5)
                except Exception:
                    pass  # No override dialog — prefix was new
            else:
                print(f"  Warning: Set Namespace button stayed disabled for {prefix}")

            registered += 1
            if registered in [1, len(NAMESPACES)]:
                take_screenshot(page, f"p00-ns-{prefix}")
        except Exception as e:
            print(f"  Warning: Could not register {prefix}: {e}")

    # Scroll to top to show the full namespace table
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1)
    take_screenshot(page, "p00-all-namespaces")
    print(f"  Registered {registered}/{len(NAMESPACES)} namespaces")


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1: COMMON FOUNDATION (Data Import)
# ═══════════════════════════════════════════════════════════════════════════════

def phase_1_common(page: Page):
    show_banner(page, "Phase 1: Common Foundation", "Uploading common.ttl via Data Import")

    common_file = GOLD_DIR / "common.ttl"
    if not common_file.exists():
        print(f"  ERROR: {common_file} not found, skipping")
        return

    upload_ttl_file(page, str(common_file), "https://purl.migx.ch/common")
    take_screenshot(page, "p01-common-uploaded")

    # Verify in Named Graphs
    navigate(page, f"{BASE_URL}/resource/Assets:NamedGraphs")
    time.sleep(2)
    take_screenshot(page, "p01-named-graphs-verify")

    # Quick SPARQL verification
    run_sparql_query(page, "SELECT (COUNT(*) AS ?triples) WHERE { ?s ?p ?o }", "p01-verify-count")


def upload_ttl_file(page: Page, file_path: str, named_graph: str = ""):
    """Upload a TTL file via the Data Import page."""
    navigate(page, f"{BASE_URL}/resource/Admin:DataImportExport")
    time.sleep(1)

    # Expand Advanced Options if needed
    try:
        advanced = page.locator('text=Advanced Options, text=Advanced, [data-toggle="collapse"]:has-text("Advanced")').first
        if advanced.is_visible(timeout=1000):
            advanced.click()
            time.sleep(0.5)
    except:
        pass

    # Set target named graph if specified
    if named_graph:
        try:
            ng_input = page.locator('input[placeholder*="NamedGraph" i], input[placeholder*="named graph" i], input[placeholder*="IRI" i]').first
            if ng_input.is_visible(timeout=1000):
                ng_input.fill(named_graph)
        except:
            pass

    # Upload the file
    file_input = page.locator('input[type="file"]').first
    file_input.set_input_files(file_path)
    time.sleep(2)

    # Wait for upload to complete
    time.sleep(3)
    print(f"  Uploaded: {Path(file_path).name} → {named_graph or '(default graph)'}")


def run_sparql_query(page: Page, query: str, screenshot_name: str = ""):
    """Execute a SPARQL query in the metaphactory SPARQL editor."""
    navigate(page, f"{BASE_URL}/sparql")
    time.sleep(2)

    # Set the query in the CodeMirror editor
    try:
        page.evaluate(f"""() => {{
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) {{
                cm.CodeMirror.setValue({repr(query)});
            }}
        }}""")
        time.sleep(0.5)
    except:
        # Fallback: try textarea
        textarea = page.locator('textarea').first
        if textarea.is_visible(timeout=1000):
            textarea.fill(query)

    # Click Execute
    execute_btn = page.locator('button:has-text("Execute"), button:has-text("Run")').first
    if execute_btn.is_visible(timeout=2000):
        execute_btn.click()
        time.sleep(3)

    if screenshot_name:
        take_screenshot(page, screenshot_name)


# ═══════════════════════════════════════════════════════════════════════════════
# ONTOLOGY CREATION HELPER (used by Phases 2, 4, 6, 8, 10, 12)
# ═══════════════════════════════════════════════════════════════════════════════

def create_ontology(page: Page, onto: OntologyDef, phase_prefix: str):
    """Create an ontology through the metaphactory Ontology Editor UI."""
    show_banner(page, f"Creating Ontology: {onto.title}",
                f"Classes: {len(onto.classes)} | Attributes: {len(onto.attributes)} | Relations: {len(onto.relations)}")

    # Navigate to Ontologies
    navigate(page, f"{BASE_URL}/resource/Assets:Ontologies")
    time.sleep(2)

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)
    take_screenshot(page, f"{phase_prefix}-create-dialog")

    # Fill title (exact data-testid from DOM exploration)
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=3000)
    title_input.click()
    title_input.type(onto.title)
    time.sleep(0.5)

    # Uncheck "Suggest IRI" and set custom IRI — auto-suggest leaves the Create button
    # disabled due to async validation. We append a fragment to avoid conflict with
    # the registered namespace (which is the bare IRI ending in /).
    suggest_cb = page.locator('input[data-testid="suggest-iri-ontology"]').first
    if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
        suggest_cb.click()
        time.sleep(0.5)

    iri_input = page.locator('input[data-testid="suggest-iri-ontology-input"]').first
    if iri_input.is_visible(timeout=2000):
        # Build a non-conflicting IRI: append CamelCase title as fragment
        fragment = onto.title.replace(" ", "")
        custom_iri = onto.iri.rstrip("/") + "/" + fragment
        iri_input.click()
        iri_input.fill("")
        iri_input.type(custom_iri)
        time.sleep(0.5)

    # Click Create in dialog — wait for it to become enabled
    dialog_create = page.locator('.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")').first
    if dialog_create.is_visible(timeout=3000):
        for _ in range(15):
            if dialog_create.get_attribute("disabled") is None:
                break
            time.sleep(0.3)
        if dialog_create.get_attribute("disabled") is None:
            dialog_create.click()
        else:
            print(f"  Warning: Create button stayed disabled for {onto.title}")
            page.keyboard.press("Escape")
            return
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, f"{phase_prefix}-editor-open")

    # Note: owl:imports are set via the full Data Import (Phase 13) since
    # the Import Ontology modal requires ontologies to already be loaded.
    # The UI editor is used for creating classes, attributes, and relations.

    # ── Create classes ──
    # Safety: ensure no modal is blocking before creating classes
    _dismiss_import_modal(page)
    if onto.classes:
        show_banner(page, f"Creating {len(onto.classes)} Classes", onto.title)
        # Make sure we're on Classes tab
        try:
            classes_tab = page.locator('[role="tab"]:has-text("Classes"), button:has-text("Classes")').first
            if classes_tab.is_visible(timeout=1000):
                classes_tab.click()
                time.sleep(0.5)
        except:
            pass

        for i, cls_name in enumerate(onto.classes):
            try:
                create_cls = page.locator('button:has-text("Create Class")').first
                create_cls.click()
                time.sleep(1)

                # Fill label in the right panel or inline dialog
                label_input = page.locator('input[placeholder="Enter label here..."]').first
                if label_input.is_visible(timeout=2000):
                    label_input.fill(cls_name)
                    time.sleep(0.3)

                # Confirm if available (some versions show a confirm button)
                try:
                    confirm = page.locator('button:has-text("Confirm")').first
                    if confirm.is_visible(timeout=1500):
                        confirm.click()
                        time.sleep(0.5)
                except:
                    time.sleep(0.3)
            except Exception as e:
                print(f"  Warning: Could not create class {cls_name}: {e}")

            if i == 0 or i == len(onto.classes) - 1:
                take_screenshot(page, f"{phase_prefix}-class-{cls_name}")

    # ── Create attributes (datatype properties) ──
    if onto.attributes:
        show_banner(page, f"Creating {len(onto.attributes)} Attributes", f"Datatype properties with domain and type")
        try:
            attrs_tab = page.locator('[role="tab"]:has-text("Attributes"), button:has-text("Attributes")').first
            if attrs_tab.is_visible(timeout=2000):
                attrs_tab.click()
                time.sleep(0.5)
        except:
            pass

        for i, (attr_name, domain_cls, dtype) in enumerate(onto.attributes):
            try:
                create_attr = page.locator('button:has-text("Create Attribute")').first
                create_attr.click()
                time.sleep(1)

                # Fill label in right panel
                label_input = page.locator('input[placeholder="Enter label here..."]').first
                if label_input.is_visible(timeout=2000):
                    label_input.fill(attr_name)
                    time.sleep(0.3)

                # Confirm if available
                try:
                    confirm = page.locator('button:has-text("Confirm")').first
                    if confirm.is_visible(timeout=1500):
                        confirm.click()
                        time.sleep(0.5)
                except:
                    time.sleep(0.3)
            except Exception as e:
                print(f"  Warning: Could not create attribute {attr_name}: {e}")

            if i == 0:
                take_screenshot(page, f"{phase_prefix}-attr-{attr_name}")

    # ── Create relations (object properties) ──
    if onto.relations:
        show_banner(page, f"Creating {len(onto.relations)} Relations", f"Object properties with domain and range")
        try:
            rels_tab = page.locator('[role="tab"]:has-text("Relations"), button:has-text("Relations")').first
            if rels_tab.is_visible(timeout=2000):
                rels_tab.click()
                time.sleep(0.5)
        except:
            pass

        for i, (rel_name, domain_cls, range_cls) in enumerate(onto.relations):
            try:
                create_rel = page.locator('button:has-text("Create Relation")').first
                create_rel.click()
                time.sleep(1)

                # Fill label in right panel
                label_input = page.locator('input[placeholder="Enter label here..."]').first
                if label_input.is_visible(timeout=2000):
                    label_input.fill(rel_name)
                    time.sleep(0.3)

                # Confirm if available
                try:
                    confirm = page.locator('button:has-text("Confirm")').first
                    if confirm.is_visible(timeout=1500):
                        confirm.click()
                        time.sleep(0.5)
                except:
                    time.sleep(0.3)
            except Exception as e:
                print(f"  Warning: Could not create relation {rel_name}: {e}")

            if i == 0:
                take_screenshot(page, f"{phase_prefix}-rel-{rel_name}")

    # ── Apply layout and save ──
    try:
        layout_btn = page.locator('button:has-text("Hierarchical"), [title*="layout" i]').first
        if layout_btn.is_visible(timeout=1000):
            layout_btn.click()
            time.sleep(2)
    except:
        pass

    take_screenshot(page, f"{phase_prefix}-canvas-overview")

    # Save
    try:
        save_btn = page.locator('button:has-text("Save"), [title*="Save"]').first
        if save_btn.is_visible(timeout=2000):
            save_btn.click()
            time.sleep(2)
            take_screenshot(page, f"{phase_prefix}-saved")
    except:
        pass

    clear_banner(page)


# ═══════════════════════════════════════════════════════════════════════════════
# VOCABULARY CREATION HELPER (used by Phases 3, 5, 7, 9, 11)
# ═══════════════════════════════════════════════════════════════════════════════

def create_vocabulary(page: Page, vocab: VocabularyDef, phase_prefix: str):
    """Create a vocabulary through the metaphactory Vocabulary Editor UI."""
    # Separate top-level and narrower concepts
    top_concepts = [c for c in vocab.concepts if not c.broader]
    narrower_map = {}  # parent_label -> [child concepts]
    for c in vocab.concepts:
        if c.broader:
            narrower_map.setdefault(c.broader, []).append(c)

    show_banner(page, f"Creating Vocabulary: {vocab.title}",
                f"Top-level: {len(top_concepts)} | Narrower: {len(vocab.concepts) - len(top_concepts)}")

    # Navigate to Vocabularies
    navigate(page, f"{BASE_URL}/resource/Assets:Vocabularies")
    time.sleep(2)

    # Click Create
    create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
    create_btn.click()
    time.sleep(2)

    # Fill title (exact data-testid from DOM exploration)
    title_input = page.locator('input[data-testid="asset-title-input"]').first
    title_input.wait_for(state="visible", timeout=3000)
    title_input.click()
    title_input.type(vocab.title)
    time.sleep(0.5)

    # Uncheck "Suggest IRI" and set custom IRI — auto-suggest leaves the Create button
    # disabled due to async validation. Append a fragment to avoid namespace conflicts.
    suggest_cb = page.locator('input[data-testid="suggest-iri-vocabulary"]').first
    if suggest_cb.is_visible(timeout=1000) and suggest_cb.is_checked():
        suggest_cb.click()
        time.sleep(0.5)

    iri_input = page.locator('input[data-testid="suggest-iri-vocabulary-input"]').first
    if iri_input.is_visible(timeout=2000):
        fragment = vocab.title.replace(" ", "")
        custom_iri = vocab.iri.rstrip("/") + "/" + fragment
        iri_input.click()
        iri_input.fill("")
        iri_input.type(custom_iri)
        time.sleep(0.5)

    # Click Create in dialog — wait for it to become enabled
    dialog_create = page.locator('.modal button:has-text("Create"), [role="dialog"] button:has-text("Create")').first
    if dialog_create.is_visible(timeout=3000):
        for _ in range(15):
            if dialog_create.get_attribute("disabled") is None:
                break
            time.sleep(0.3)
        if dialog_create.get_attribute("disabled") is None:
            dialog_create.click()
        else:
            print(f"  Warning: Create button stayed disabled for {vocab.title}")
            page.keyboard.press("Escape")
            return
    time.sleep(3)
    dismiss_walkthrough(page)
    take_screenshot(page, f"{phase_prefix}-editor-open")

    # ── Create top-level concepts ──
    for i, concept in enumerate(top_concepts):
        try:
            create_term = page.locator('button:has-text("Create top-level term")').first
            create_term.click()
            time.sleep(1)

            # Exact placeholders from DOM exploration — use type() to trigger validation
            pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
            pref_input.click()
            pref_input.fill("")
            pref_input.type(concept.label)
            time.sleep(0.5)

            # Fill definition if available
            if concept.definition:
                def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
                if def_input.is_visible(timeout=500):
                    def_input.click()
                    def_input.type(concept.definition)

            # Save — scope to the modal dialog (not the editor toolbar Save)
            save_btn = page.locator('.overlay-modal.show button[name="submit"], [role="dialog"].show button[name="submit"]').first
            for _ in range(10):
                if save_btn.get_attribute("disabled") is None:
                    break
                time.sleep(0.3)
            save_btn.click()
            time.sleep(1)
        except Exception as e:
            print(f"  Warning: Could not create concept {concept.label}: {e}")
            # Close stuck modal if present
            try:
                page.keyboard.press('Escape')
                time.sleep(0.5)
            except:
                pass

        if i == 0:
            take_screenshot(page, f"{phase_prefix}-first-concept")

    # ── Create narrower concepts using "Create narrower term" menu ──
    for parent_label, children in narrower_map.items():
        show_banner(page, f"Creating narrower terms under: {parent_label}",
                    f"{len(children)} child concept(s)")
        clear_banner(page)

        for child in children:
            try:
                created_as_narrower = False

                # 1. Click the parent concept in the tree (target <a> in tree panel)
                parent_node = page.locator(f'a:has(span:text-is("{parent_label}"))').first
                if not parent_node.is_visible(timeout=2000):
                    parent_node = page.locator(f'a:has-text("{parent_label}")').first
                if parent_node.is_visible(timeout=1000):
                    parent_node.click(force=True)
                    time.sleep(1)

                    # 2. Click the more_vert (three-dot) menu button
                    menu_btn = page.locator('button:has-text("more_vert")').first
                    if menu_btn.is_visible(timeout=2000):
                        menu_btn.click()
                        time.sleep(0.5)

                        # 3. Click "Create narrower term..." from dropdown
                        narrower_option = page.locator('.dropdown-menu.show a:has-text("Create narrower term")').first
                        if narrower_option.is_visible(timeout=1000):
                            narrower_option.click()
                            time.sleep(1)

                            # 4. Fill preferred label
                            pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
                            if pref_input.is_visible(timeout=3000):
                                pref_input.click()
                                pref_input.fill("")
                                pref_input.type(child.label)
                                time.sleep(0.3)

                                # Fill definition
                                if child.definition:
                                    def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
                                    if def_input.is_visible(timeout=500):
                                        def_input.click()
                                        def_input.type(child.definition)

                                # 5. Save — scope to modal
                                save_btn = page.locator('.overlay-modal.show button[name="submit"], [role="dialog"].show button[name="submit"]').first
                                for _ in range(10):
                                    if save_btn.get_attribute("disabled") is None:
                                        break
                                    time.sleep(0.3)
                                if save_btn.get_attribute("disabled") is None:
                                    save_btn.click()
                                    time.sleep(1)
                                    created_as_narrower = True
                        else:
                            # Close the dropdown if narrower option not found
                            page.keyboard.press("Escape")
                            time.sleep(0.3)

                if created_as_narrower:
                    continue

                # Fallback: create as top-level and note the broader wasn't set
                create_term = page.locator('button:has-text("Create top-level term")').first
                if create_term.is_visible(timeout=1000):
                    create_term.click()
                    time.sleep(1)
                    pref_input = page.locator('input[placeholder="Enter preferred label here..."]').first
                    pref_input.click()
                    pref_input.fill("")
                    pref_input.type(child.label)
                    if child.definition:
                        def_input = page.locator('textarea[placeholder="Enter definition here..."]').first
                        if def_input.is_visible(timeout=500):
                            def_input.click()
                            def_input.type(child.definition)
                    save_btn = page.locator('.overlay-modal.show button[name="submit"], [role="dialog"].show button[name="submit"]').first
                    for _ in range(10):
                        if save_btn.get_attribute("disabled") is None:
                            break
                        time.sleep(0.3)
                    if save_btn.get_attribute("disabled") is None:
                        save_btn.click()
                        time.sleep(1)
                    print(f"  Note: Created {child.label} as top-level (narrower creation under {parent_label} failed)")

            except Exception as e:
                print(f"  Warning: Could not create narrower concept {child.label}: {e}")
                try:
                    page.keyboard.press('Escape')
                    time.sleep(0.5)
                except:
                    pass

    take_screenshot(page, f"{phase_prefix}-vocabulary-complete")
    clear_banner(page)


# ═══════════════════════════════════════════════════════════════════════════════
# BATCH DATA IMPORT HELPER (used by Phases 13-15)
# ═══════════════════════════════════════════════════════════════════════════════

def batch_upload_files(page: Page, file_list: list, category_name: str, phase_prefix: str):
    """Upload multiple TTL files from the gold layer via Data Import."""
    show_banner(page, f"Data Import: {category_name}", f"{len(file_list)} file(s)")

    uploaded = 0
    for rel_path, named_graph in file_list:
        abs_path = GOLD_DIR.parent / rel_path  # GOLD_DIR is gold/, rel_path starts with gold/
        if not abs_path.exists():
            # Try from GOLD_DIR parent
            abs_path = Path("/Users/kiptengwer/Documents/MIGxKG") / rel_path
        if not abs_path.exists():
            print(f"  SKIP: {rel_path} not found")
            continue

        upload_ttl_file(page, str(abs_path), named_graph)
        uploaded += 1

        if uploaded == 1 or uploaded == len(file_list):
            take_screenshot(page, f"{phase_prefix}-upload-{uploaded}")

    print(f"  Uploaded {uploaded}/{len(file_list)} {category_name} files")
    clear_banner(page)


# ═══════════════════════════════════════════════════════════════════════════════
# PHASE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def phase_2_enterprise_ontology(page: Page):
    create_ontology(page, ENTERPRISE_ONTOLOGY, "p02")

def phase_3_enterprise_terminology(page: Page):
    create_vocabulary(page, ENTERPRISE_VOCAB, "p03")

def phase_4_it_system_ontology(page: Page):
    create_ontology(page, IT_SYSTEM_ONTOLOGY, "p04")

def phase_5_it_system_terminology(page: Page):
    create_vocabulary(page, IT_SYSTEM_VOCAB, "p05")

def phase_6_skills_ontology(page: Page):
    create_ontology(page, SKILLS_ONTOLOGY, "p06")

def phase_7_skills_terminology(page: Page):
    create_vocabulary(page, SKILLS_VOCAB, "p07")

def phase_8_itsm_ontology(page: Page):
    create_ontology(page, ITSM_ONTOLOGY, "p08")

def phase_9_itsm_terminology(page: Page):
    create_vocabulary(page, ITSM_VOCAB, "p09")

def phase_10_csa_ontology(page: Page):
    create_ontology(page, CSA_ONTOLOGY, "p10")

def phase_11_csa_terminology(page: Page):
    create_vocabulary(page, CSA_VOCAB, "p11")


def phase_12_supporting_ontologies(page: Page):
    """Create Person, Employee, and Project ontologies (lightweight, mostly imports)."""
    show_banner(page, "Phase 12: Supporting Ontologies", "Person, Employee, Project — import-based extensions")

    for onto, prefix in [
        (PERSON_ONTOLOGY,   "p12a"),
        (EMPLOYEE_ONTOLOGY, "p12b"),
        (PROJECT_ONTOLOGY,  "p12c"),
    ]:
        create_ontology(page, onto, prefix)


def phase_13_upload_all_ontologies(page: Page):
    """Upload the FULL gold-layer ontology files via Data Import (complete content)."""
    show_banner(page, "Phase 13: Full Ontology Data Import",
                "Uploading complete ontology TTL files with all classes, properties, and DCAT metadata")
    batch_upload_files(page, ONTOLOGY_FILES, "Ontology Files", "p13")


def phase_14_upload_terminologies(page: Page):
    """Upload full terminology files (1000+ skill concepts, etc.)."""
    show_banner(page, "Phase 14: Full Terminology Data Import",
                "Uploading complete terminology files with all concepts and hierarchies")
    batch_upload_files(page, TERMINOLOGY_FILES, "Terminology Files", "p14")


def phase_15_upload_shapes(page: Page):
    """Upload all SHACL shape files via Data Import."""
    show_banner(page, "Phase 15: SHACL Shapes Import",
                "Uploading validation shapes for all domains")
    batch_upload_files(page, SHAPE_FILES, "SHACL Shape Files", "p15")

    # Navigate to Data Quality to show SHACL is available
    navigate(page, f"{BASE_URL}/resource/Admin:DataQuality")
    time.sleep(2)
    take_screenshot(page, "p15-data-quality-page")


def phase_16_upload_instances(page: Page):
    """Upload all instance data files."""
    show_banner(page, "Phase 16: Instance Data Import",
                "Organizations, persons, employees, projects, skills, accounts, IT systems")
    batch_upload_files(page, INSTANCE_FILES, "Instance Files", "p16")


def phase_17_upload_cqs_and_sparql(page: Page):
    """Upload competency questions and SPARQL query files."""
    show_banner(page, "Phase 17: CQs & SPARQL Queries Import",
                "Competency questions and SPARQL query definitions for all domains")
    batch_upload_files(page, CQ_AND_SQ_FILES, "CQ & SQ Files", "p17")


def phase_18_sparql_demo(page: Page):
    """Run representative SPARQL queries to demonstrate cross-domain intelligence."""
    show_banner(page, "Phase 18: SPARQL Workbench", "Running cross-domain intelligence queries")

    for i, (title, query) in enumerate(DEMO_QUERIES):
        show_banner(page, f"SPARQL Query: {title}", f"Query {i+1} of {len(DEMO_QUERIES)}")
        run_sparql_query(page, query, f"p18-query-{i+1}")
        time.sleep(2)


def phase_19_dcat_datasets(page: Page):
    """Create DCAT dataset cards via Assets > Datasets."""
    show_banner(page, "Phase 19: DCAT Dataset Catalog",
                "Creating dataset cards for discoverability and governance")

    navigate(page, f"{BASE_URL}/resource/Assets:Datasets")
    time.sleep(2)
    take_screenshot(page, "p19-datasets-page")

    # Create a representative dataset card
    datasets_to_create = [
        ("MIGx Enterprise Ontology", "Comprehensive ontology for the MIGx enterprise ecosystem", ["Enterprise", "Ontology", "MIGx"]),
        ("IT Systems Inventory",     "IT application portfolio with integrations and data flows",  ["IT Systems", "CMDB", "Applications"]),
        ("Skills Assessment Data",   "Employee skill assessments and proficiency levels",           ["Skills", "Competency", "Talent"]),
    ]

    for title, desc, keywords in datasets_to_create:
        try:
            create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
            if create_btn.is_visible(timeout=2000):
                create_btn.click()
                time.sleep(1)

                # Fill title
                title_input = page.locator('input[placeholder*="title" i], input[type="text"]').first
                if title_input.is_visible(timeout=1000):
                    title_input.fill(title)

                # Fill description
                desc_input = page.locator('textarea, input[placeholder*="description" i]')
                if desc_input.count() > 0 and desc_input.first.is_visible(timeout=500):
                    desc_input.first.fill(desc)

                # Create
                confirm_btn = page.locator('.modal button:has-text("Create"), dialog button:has-text("Create")').first
                if confirm_btn.is_visible(timeout=1000):
                    confirm_btn.click()
                    time.sleep(2)

                take_screenshot(page, f"p19-dataset-{title[:10].replace(' ', '_')}")
                # Navigate back to datasets list
                navigate(page, f"{BASE_URL}/resource/Assets:Datasets")
                time.sleep(1)
        except Exception as e:
            print(f"  Warning: Could not create dataset {title}: {e}")

    take_screenshot(page, "p19-datasets-complete")


def phase_20_named_graphs_review(page: Page):
    """Review all named graphs to show complete KG deployment."""
    show_banner(page, "Phase 20: Named Graphs Review",
                "Viewing all deployed named graphs and triple counts")

    navigate(page, f"{BASE_URL}/resource/Assets:NamedGraphs")
    time.sleep(2)
    take_screenshot(page, "p20-named-graphs-overview")

    # Count total triples
    run_sparql_query(page,
        "SELECT (COUNT(*) AS ?total) WHERE { ?s ?p ?o }",
        "p20-total-triples")

    # Count per graph
    run_sparql_query(page,
        "SELECT ?g (COUNT(*) AS ?n) WHERE { GRAPH ?g { ?s ?p ?o } } GROUP BY ?g ORDER BY DESC(?n)",
        "p20-triples-per-graph")


def phase_21_verification_diagram(page: Page):
    """Create a cross-domain verification diagram."""
    show_banner(page, "Phase 21: Verification Diagram",
                "Visual overview of the complete knowledge graph")

    navigate(page, f"{BASE_URL}/resource/Assets:Diagrams")
    time.sleep(2)

    # Create new diagram
    try:
        create_btn = page.locator('button:has-text("Create"), a:has-text("Create")').first
        create_btn.click()
        time.sleep(3)
        dismiss_walkthrough(page)

        # Try to add all classes
        try:
            add_all = page.locator('button:has-text("Add all"), text=Add all classes').first
            if add_all.is_visible(timeout=2000):
                add_all.click()
                time.sleep(3)
        except:
            pass

        # Apply layout
        try:
            layout = page.locator('button:has-text("Hierarchical"), [title*="layout" i]').first
            if layout.is_visible(timeout=1000):
                layout.click()
                time.sleep(3)
        except:
            pass

        take_screenshot(page, "p21-verification-diagram")
    except Exception as e:
        print(f"  Warning: Diagram creation failed: {e}")

    show_banner(page, "Tutorial Complete!",
                "Full MIGx Knowledge Graph deployed in metaphactory")
    take_screenshot(page, "p21-tutorial-complete")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Phase orchestration
# ═══════════════════════════════════════════════════════════════════════════════

PHASES = [
    (0,  "Namespace Registration",       phase_0_namespaces),
    (1,  "Common Foundation",            phase_1_common),
    (2,  "Enterprise Ontology",          phase_2_enterprise_ontology),
    (3,  "Enterprise Terminology",       phase_3_enterprise_terminology),
    (4,  "IT System Ontology",           phase_4_it_system_ontology),
    (5,  "IT System Terminology",        phase_5_it_system_terminology),
    (6,  "Skills Ontology",              phase_6_skills_ontology),
    (7,  "Skills Terminology",           phase_7_skills_terminology),
    (8,  "ITSM Ontology",               phase_8_itsm_ontology),
    (9,  "ITSM Terminology",            phase_9_itsm_terminology),
    (10, "CSA Ontology",                 phase_10_csa_ontology),
    (11, "CSA Terminology",              phase_11_csa_terminology),
    (12, "Supporting Ontologies",        phase_12_supporting_ontologies),
    (13, "Full Ontology Data Import",    phase_13_upload_all_ontologies),
    (14, "Full Terminology Data Import", phase_14_upload_terminologies),
    (15, "SHACL Shapes Import",          phase_15_upload_shapes),
    (16, "Instance Data Import",         phase_16_upload_instances),
    (17, "CQs & SPARQL Import",         phase_17_upload_cqs_and_sparql),
    (18, "SPARQL Workbench Demo",        phase_18_sparql_demo),
    (19, "DCAT Dataset Catalog",         phase_19_dcat_datasets),
    (20, "Named Graphs Review",          phase_20_named_graphs_review),
    (21, "Verification Diagram",         phase_21_verification_diagram),
]


def run_tutorial(headed: bool = False, phase_filter: int = None):
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=not headed,
            slow_mo=SLOW_MO,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(VIDEO_DIR),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.set_default_timeout(15000)  # 15s default instead of 30s

        # Login
        login(page)
        print("Logged in to metaphactory")

        # Run phases
        for num, name, func in PHASES:
            if phase_filter is not None and num != phase_filter:
                continue

            print(f"\n{'='*60}")
            print(f"Phase {num}: {name}")
            print(f"{'='*60}")

            try:
                # Check if session expired before each phase
                ensure_logged_in(page)
                func(page)
                print(f"  ✓ Phase {num} complete")
            except Exception as e:
                print(f"  ✗ Phase {num} error: {e}")
                try:
                    take_screenshot(page, f"error-phase-{num}")
                except:
                    pass
                # If page/context/browser crashed, try full recovery
                if "closed" in str(e).lower():
                    print("  Browser crashed, launching new browser...")
                    try:
                        context.close()
                    except:
                        pass
                    try:
                        browser.close()
                    except:
                        pass
                    browser = p.chromium.launch(
                        headless=not headed,
                        slow_mo=SLOW_MO,
                    )
                    context = browser.new_context(
                        viewport={"width": 1920, "height": 1080},
                        record_video_dir=str(VIDEO_DIR),
                        record_video_size={"width": 1920, "height": 1080},
                    )
                    page = context.new_page()
                    page.set_default_timeout(15000)
                    login(page)
                    print("  Recovered — continuing with next phase")

        # Close
        try:
            context.close()
            browser.close()
        except:
            pass

        # Rename video to a meaningful name
        video_files = list(VIDEO_DIR.glob("*.webm"))
        if video_files:
            latest = max(video_files, key=lambda f: f.stat().st_mtime)
            from datetime import datetime
            ts = datetime.now().strftime("%Y-%m-%d")
            if args.phase is not None:
                name = f"migx-kg-tutorial-phase-{args.phase}-{ts}.webm"
            else:
                name = f"migx-kg-tutorial-full-{ts}.webm"
            final_path = VIDEO_DIR / name
            latest.rename(final_path)
            print(f"\n{'='*60}")
            print(f"Video recorded: {final_path}")
            print(f"Screenshots:    {SCREENSHOT_DIR}")
            print(f"{'='*60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MIGx KG Metaphactory Tutorial")
    parser.add_argument("--headed", action="store_true", help="Run with visible browser")
    parser.add_argument("--phase", type=int, default=None, help="Run only this phase number")
    args = parser.parse_args()

    run_tutorial(headed=args.headed, phase_filter=args.phase)
