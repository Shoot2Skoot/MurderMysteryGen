# Mystery.AI - Phase 2: Goals & Scope Document

## 1. Introduction

Following the successful completion and review of the Mystery.AI Minimum Viable Product (MVP), Phase 2 aims to address key areas for improvement, primarily focusing on enhancing the creative quality and diversity of the generated mystery frameworks. This document outlines the primary goals, scope, and planned epics for this phase.

## 2. Primary Goal for Phase 2

To significantly enhance the **diversity, creativity, and uniqueness** of AI-generated mystery frameworks, addressing specific repetition and thematic stereotyping issues identified from MVP testing. The outcome should be a system that produces more varied and engaging foundational mystery elements.

## 3. Key Focus Areas & Problems to Solve (from MVP Feedback)

1.  **Limited Cause of Death Variety:** The MVP tended to generate a narrow range of common causes of death (e.g., strangling, poisoning). Phase 2 will aim to broaden this significantly with more creative and thematically appropriate options.
2.  **Overall Scenario Uniqueness:** Multiple generations using the same theme sometimes resulted in core scenarios that were too similar. Phase 2 will strive to ensure greater distinctiveness between these runs.
3.  **Thematic Stereotyping:** For certain themes, generated content (especially victim/suspect occupations and personalities) leaned heavily on common tropes. Phase 2 will aim for more nuanced and less predictable thematic interpretations.

## 4. High-Level Epic Overview for Phase 2

The work for Phase 2 is planned across the following epics:

*   **Epic 5: Advanced Prompt Engineering for Content Diversification**
    *   *Focus:* Systematically refining and enhancing the instruction prompts for all content-generating AI agents to explicitly request, guide, and reward more diverse, creative, and less stereotypical outputs.
*   **Epic 6: LLM Parameter & Model Experimentation for Creative Control**
    *   *Focus:* Investigating and implementing the use of different LLM models and generation parameters (e.g., temperature, top_p) for specific agents or generation steps to control the balance between coherence and creativity/diversity.
*   **Epic 7: (Advanced PoC) Generative Augmentation & Feedback Loops for Enhanced Uniqueness**
    *   *Focus:* Exploring (as Proof-of-Concepts) more structural or process-oriented changes to the generation pipeline to further break out of common patterns and achieve a higher degree of originality.

## 5. Success Criteria & KPIs for Phase 2 (Examples)

*(These will be refined and made more specific at the start of each Epic/Story)*

*   **KPI (Cause of Death):** For a given theme, generating X mysteries should result in at least Y distinct categories of cause of death (e.g., running 10 times for "Cyberpunk" yields >5 unique CoD types).
*   **KPI (Thematic Stereotyping):** For a previously problematic theme (e.g., "Midwest Small Town"), the percentage of stereotypical roles (e.g., school teachers) generated for victims/suspects should decrease by Z% over X runs.
*   **Qualitative KPI (Overall Uniqueness):** Primary user rating for "overall scenario uniqueness" (when generating multiple mysteries with the same theme) should improve from "fair/needs improvement" to "good/excellent" on a defined scale.
*   **Qualitative KPI (Creativity):** Primary user rating for "creativity of generated elements" (victim details, MMOs, evidence) should show a noticeable improvement.
*   **Maintenance of Core Functionality:** All existing MVP functionality (pipeline completion, JSON output, player view) must remain stable and functional.

## 6. Out of Scope for Phase 2 (Unless Directly Supporting Diversity Goals)

Unless they directly contribute to the primary goal of enhancing diversity and creativity, the following are generally out of scope for this specific phase (these remain as longer-term future enhancements):

*   Implementing highly complex, multi-layered evidence branching.
*   Adding advanced puzzle generation (ciphers, etc.).
*   Building a user interface for end-players or authors.
*   Significant architectural refactoring not directly related to enabling diversity experiments.
*   Introducing new external dependencies or services (databases, complex CI/CD, etc.).

This document provides the guiding framework for Phase 2 development of Mystery.AI. 