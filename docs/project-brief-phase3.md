# Project Brief: Mystery.AI - Phase 3: Branching Evidence Architecture & Design

## Introduction / Problem Statement

Phase 2 of Mystery.AI focuses on enhancing foundational diversity and the richness of individual evidence items. However, the current MVP and Phase 2 enhancements generate a relatively flat list of evidence. To create truly complex and engaging mysteries, the system needs to generate interconnected evidence that forms logical chains, supports partial MMO confirmations, and allows for sophisticated red herrings, as conceptualized in `ref/mmo_tree_example.mermaid` and `ref/mmo_tree_explanation.md`.

This project phase (Phase 3) is a dedicated planning and design effort. It does not involve the implementation of the branching evidence system itself, but rather the creation of a comprehensive architectural blueprint that will guide its future implementation (e.g., in a subsequent Phase 4).

## Vision & Goals

- **Vision:** To lay the architectural groundwork for Mystery.AI to generate deeply interconnected and logically structured evidence narratives, enabling more complex, subtle, and satisfying puzzle-solving experiences.
- **Primary Goal:**
    1.  **Goal 1 (Comprehensive Design Document for Branching Evidence):** Produce a detailed "Branching Evidence Architecture & Design Document" (`docs/branching-evidence-design.md`). This document will serve as the complete technical blueprint for a future implementation phase.
- **Success Metrics:**
    -   The final `docs/branching-evidence-design.md` is assessed by the primary user (author/designer) as comprehensive, clear, and actionable for guiding future implementation.
    -   The design document clearly defines data models, agent responsibilities, orchestration logic, and addresses potential challenges for the branching evidence system.
    -   The proposed design demonstrably supports the types of branching logic and evidence interdependencies illustrated in `ref/mmo_tree_example.mermaid`.

## Target Audience / Users

- **Primary User of this Phase's Output:** The development team (including AI agents and yourself) who will undertake the *implementation* of the branching evidence system in a subsequent phase.
- **Ultimate Beneficiary:** The human author/designer, who will eventually be able to generate mysteries with much richer and more complex evidence structures.

## Key Features / Scope (for the Design Document)

The "Branching Evidence Architecture & Design Document" (`docs/branching-evidence-design.md`) must cover, at a minimum:

- **Feature 1: Data Model Specifications:**
    -   Detailed Pydantic model definitions (or extensions to existing models in `core/data_models.py`) to represent:
        -   Evidence-to-evidence relationships (e.g., prerequisites, unlocks, dependencies, contradictions).
        -   Links between individual or groups of evidence items and specific sub-components of a suspect's Means, Motive, or Opportunity.
        -   The concept of "information revealed" or "truth states" achieved by uncovering particular evidence or evidence chains.
        -   Representation of branching paths, decision points, and dead ends within the evidence structure.
- **Feature 2: Agent Logic & Responsibilities:**
    -   Definition of new AI agent roles (e.g., `EvidenceTreeArchitectAgent`, `ClueWeavingAgent`) or significant modifications to the existing `EvidenceGenerationAgent`.
    -   Detailed descriptions of each agent's inputs, core processing logic, outputs, and how they will collaborate to:
        -   Plan the overall evidence tree structure for a given killer and their MMO.
        -   Generate individual evidence items that fit into this planned structure.
        -   Place true clues and red herrings strategically within the tree.
        -   Ensure logical coherence and solvability of the entire evidence web.
- **Feature 3: Orchestration Flow:**
    -   A proposed sequence for how these agents will be orchestrated.
    -   How the `CaseContext` (or a new dedicated data structure) will manage the evolving state of the evidence tree during generation.
- **Feature 4: Core Algorithms & Heuristics (Conceptual):**
    -   Conceptual description of any key algorithms or heuristics agents might use for evidence placement, pathfinding, or ensuring solvability (e.g., ensuring at least one valid path to the solution, balancing clue distribution).
- **Feature 5: Risk & Mitigation Analysis:**
    -   Identification of potential challenges and risks in implementing the proposed design.
    -   Suggested mitigation strategies.
- **Feature 6: Prototyping Insights (Optional but Encouraged):**
    -   If any small-scale code prototypes are developed during this design phase to test specific concepts, their findings and code snippets should be included or referenced.

## Known Technical Constraints or Preferences

- **Constraints:** The design must be implementable using the existing technical stack (Python, OpenAI Agents SDK, Pydantic).
- **Preferences:** The design should favor modularity and clarity to facilitate future implementation by a potentially mixed team of human and AI developers.
- **Reference Materials:** `ref/mmo_tree_example.mermaid` and `ref/mmo_tree_explanation.md` are primary inputs and inspirations for the design.

## Relevant Research (Optional)

This phase may involve research into graph theory, narrative generation techniques for branching stories, and AI planning algorithms if deemed necessary to inform the design. The existing `docs/deep-research-report-BA.md` provides foundational context.

## PM Prompt

"You are an expert Product Manager AI. We have completed Mystery.AI MVP (Epics 1-4) and are planning Phase 2 (Enhanced Foundational Diversity & Richer Individual Evidence). This **Phase 3: Branching Evidence Architecture & Design** is a dedicated *planning and design* phase to create the blueprint for a future implementation of a complex, branching evidence system.

**Core Task:** Based on this 'Project Brief: Mystery.AI - Phase 3,' your primary role is to *facilitate and document* the creation of the "Branching Evidence Architecture & Design Document" (`docs/branching-evidence-design.md`). You will not be writing PRD/Epics for implementation in *this* phase, but rather ensuring the design document itself is comprehensive and meets the goals outlined.

**Key Activities for this Phase (You will guide the user/author through these):**
1.  **Deconstruct Requirements:** Deeply analyze `ref/mmo_tree_example.mermaid` and `ref/mmo_tree_explanation.md` to extract all implicit and explicit requirements for a branching evidence system.
2.  **Data Model Design Sessions:** Facilitate brainstorming and decision-making on the Pydantic models needed to represent the evidence tree and its components.
3.  **Agent Responsibility Definition:** Guide the definition of what new agents are needed or how existing ones must evolve to handle the generation of a branching evidence structure.
4.  **Orchestration & Logic Flow Design:** Help map out how these agents would interact and the logical flow of generating an evidence tree.
5.  **Document Compilation:** Structure and compile all findings, decisions, and designs into the `docs/branching-evidence-design.md` document.

**Key Considerations for the Design Document:**
*   **Clarity & Comprehensiveness:** The document must be detailed enough for a future team to implement from.
*   **Feasibility:** The design must be realistic within the project's technical stack.
*   **Modularity:** Encourage a design that can be implemented and tested in stages if possible.

**Primary Deliverable for Phase 3:**
1.  A completed `docs/branching-evidence-design.md` document.

No PRD or traditional Epics for implementation are expected from Phase 3 itself. The design document *is* the epic work of this phase." 