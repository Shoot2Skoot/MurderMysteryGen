# Project Brief: Mystery.AI

## Introduction / Problem Statement

Creating compelling, complex, and logically sound murder mystery puzzle games, particularly for a printed format, is a highly time-consuming and creatively demanding process. This project aims to develop an AI-driven agentic system, "Mystery.AI," to significantly augment and streamline this creation process. The system will leverage the Means, Motive, and Opportunity (MMO) framework and the OpenAI Agents SDK to generate intricate plot structures, diverse character profiles, and interconnected webs of evidence.

The primary opportunity is to empower a human author/designer to:
1.  Rapidly prototype and iterate on numerous mystery concepts.
2.  Offload the generation of complex foundational logic and detailed content (e.g., suspect alibis, evidence descriptions, character backstories).
3.  Achieve a higher degree of plot intricacy and logical consistency than might be feasible through purely manual methods at scale.
4.  Ultimately, serve as a powerful drafting and content generation tool to produce unique, "hand-crafted" feeling murder mystery experiences for a print-based format, potentially without overtly advertising the AI's role in the generation.

The problem being solved is the bottleneck of manual effort and the challenge of maintaining deep narrative coherence in highly complex mystery designs.

## Vision & Goals

- **Vision:** To create a sophisticated AI-powered system that serves as an expert co-creator for designing and drafting high-quality, complex, and logically sound murder mystery games for a printed format, significantly reducing manual effort while enhancing creative possibilities and narrative depth.
- **Primary Goals (for the initial phase focusing on Proof-of-Concepts):**
    -   **Goal 1 (PoC: Minimal Viable Mystery Core):** Demonstrate that a small team of AI agents, orchestrated via the OpenAI Agents SDK, can collaboratively generate a rudimentary but complete and solvable micro-mystery (1 victim, 2 suspects, 1 killer with a clear motive, 2-3 pieces of supporting printed evidence) based on the MMO framework by [End of Q3 2024].
    -   **Goal 2 (PoC: Suspect Profile Generator & MMO Integrity Check):** Develop and validate AI agents capable of generating multiple distinct suspect profiles, each with a complete and plausible Means, Motive, and Opportunity (MMO) for a given crime, and implement an "MMO Logic Integrity Agent" to ensure these profiles are internally consistent and structurally sound by [End of Q3 2024].
    -   **Goal 3 (PoC: Single Evidence Thread Weaver):** Successfully create an AI agent (or agents) that can, given a defined killer and a specific MMO element (e.g., Means), generate a coherent, logical chain of 3-4 pieces of printable evidence that would lead a player to understand that specific MMO element by [End of Q3 2024].
- **Success Metrics (Initial Ideas for PoCs, evaluated qualitatively):**
    -   **Mystery Core Solvability:** Can a human reviewer solve the PoC#1 micro-mystery using only the AI-generated evidence?
    -   **MMO Plausibility & Consistency:** Are the suspect MMOs generated in PoC#2 believable, distinct, and logically sound upon human review? Does the MMO Logic Integrity Agent correctly identify inconsistencies?
    -   **Evidence Chain Logic:** Does the evidence chain from PoC#3 create a clear and logical path to the intended conclusion? Is it appropriately subtle (not too obvious, not too obscure)?
    -   **Adherence to MMO Framework:** Do the outputs of all PoCs demonstrate correct application and understanding of the MMO principles?
    -   **Content Quality for Print:** Is the textual content generated for evidence (e.g., diary entries, letters) of a quality that could serve as a strong first draft for a printed game artifact, upon human review?

## Target Audience / Users

- **Ultimate Target Audience:** End players of the printed murder mystery games.
    -   **Characteristics (based on initial research):** Adults and young adults who enjoy immersive, narrative-driven, collaborative puzzle-solving experiences (e.g., fans of Hunt A Killer, Unsolved Case Files, true crime, escape rooms).
    -   **Needs (as players of the final product):**
        -   Engaging and challenging, yet fair and solvable mysteries.
        -   High-quality, immersive printed materials and evidence.
        -   Coherent and believable narratives, characters, and plot developments.
        -   A satisfying sense of discovery and accomplishment.

- **Initial Primary User (MVP & Early Development Focus):** The human author/designer (yourself) utilizing Mystery.AI as an advanced content generation and drafting tool to create experiences for the ultimate target audience.
    -   **Needs (as a creator for the end players):**
        -   Efficiently explore and iterate on multiple mystery concepts tailored to the end players' desires.
        -   Reduce the manual effort of creating complex plot logic, character backstories, and detailed evidence suitable for a high-quality player experience.
        -   Maintain high levels of narrative coherence and logical consistency across intricate plotlines to ensure player satisfaction and solvability.
        -   Receive AI-generated content in a structured and usable format for further refinement and incorporation into final print-ready game materials.
        -   Control over the AI's creative direction and the ability to guide/correct its outputs to meet the standards for the end players.

## Key Features / Scope (High-Level Ideas for MVP)

The MVP will focus on developing and validating the core AI agentic system's ability to generate foundational elements of a murder mystery, corresponding to the three initial Proof-of-Concept (PoC) streams. The output will be structured data and text content suitable for a human author to then craft into a final printed game.

- **Feature 1: Foundational Mystery Element Generation (Corresponds to PoC #1 - Minimal Viable Mystery Core)**
    -   Ability for an agent team to generate a complete, solvable micro-mystery including:
        -   Basic case setup (Victim, Setting).
        -   A small number of suspects (e.g., 2-3).
        -   Clear designation of one killer.
        -   A single, clear MMO element (e.g., Motive) for the killer.
        -   A small set (e.g., 2-3) of interconnected, printable evidence items that establish this MMO element and identify the killer.
    -   Output: Structured data defining these elements and text content for the evidence.

- **Feature 2: Suspect Profile & MMO Framework Integrity (Corresponds to PoC #2 - Suspect Profile Generator & MMO Integrity Check)**
    -   AI agents capable of generating multiple (e.g., 3-5) distinct suspect profiles for a given crime setup.
    -   Each suspect profile to include a fully fleshed-out and plausible Means, Motive, and Opportunity (MMO).
    -   An "MMO Logic Integrity Agent" that validates the completeness, internal consistency, and structural soundness of these generated MMO profiles.
    -   Output: Structured data for suspect profiles (including MMOs) and validation reports/status.

- **Feature 3: Coherent Evidence Thread Weaving (Corresponds to PoC #3 - Single Evidence Thread Weaver)**
    -   AI agent(s) that can take a predefined killer and a specific MMO element (e.g., Means, Motive, or Opportunity) as input.
    -   Generation of a logical, coherent chain of several (e.g., 3-5) pieces of printable evidence.
    -   This evidence chain should clearly and logically lead a player to understand the specified MMO element for the killer.
    -   The system should ensure clues are "fair" and the path is solvable.
    -   Output: Structured data defining the evidence items and their connections, and text content for each piece of evidence.

- **Feature 4 (System-Wide): Structured Data Output & Coherence Mechanisms (Underpinning all PoCs)**
    -   Establishment of a clear, structured data model for representing all mystery components (case, suspects, MMOs, evidence, relationships).
    -   Implementation of initial coherence-checking mechanisms (e.g., the brainstormed "Red Team Agent," "MMO Logic Integrity Agent," "Ripple Effect Analyzer Agent" in their most basic forms) to support the generation and validation within the PoCs.
    -   Output: The Mystery.AI system's ability to produce its outputs as well-defined structured data (e.g., JSON, Pydantic models) that can be reviewed and utilized by the human author.

## Known Technical Constraints or Preferences

- **Constraints:**
    -   **Primary SDK:** OpenAI Agents SDK (Python).
    -   **Target LLMs:** GPT-4.1 (and its variants like mini, nano), o3, o4-mini. The system should be designed with the potential for tiered model usage (more powerful models for critical reasoning, less powerful for simpler tasks) to manage cost and performance.
    -   **Development Environment:** Python 3.12.3 within a virtual environment (venv).
    -   **Output Format:** Initially focused on structured data (e.g., JSON, Pydantic models) and text content that can be used to create physical, printed game materials.
    -   **No Direct User Input (for generation):** The end-to-end mystery generation pipeline should be automated and not require interactive user input during the generation process itself (though user prompts may initiate a generation).
    -   **Qualitative Evals Initially:** Success of PoCs will be determined by human qualitative review against defined criteria, acknowledging the difficulty of automated evals for creative, narrative content.

- **Preferences:**
    -   **Modular Agent Design:** Preference for specialized agents, each excelling at a specific task, to enhance maintainability and allow for iterative improvement.
    -   **Human-in-the-Loop (HITL) for Design/Refinement:** The system is envisioned as a powerful drafting tool for a human author, who will provide creative direction, review, and polish AI-generated content.
    -   **Iterative Development through PoCs:** Approach development through focused Proof-of-Concepts to test core functionalities and learn quickly.

- **Risks:**
    -   **Maintaining Narrative Coherence:** Ensuring logical consistency, character believability, and plot integrity across a complex, multi-agent generated narrative remains the primary technical risk.
    -   **Cost Management:** Use of powerful LLMs can be expensive; a strategy for tiered model usage and efficient prompting will be essential.
    -   **SDK Limitations/Maturity:** As a newer SDK, there might be unforeseen limitations or fewer established best practices for highly complex, multi-agent narrative systems.
    -   **Complexity of "Fair Puzzle" Generation:** Ensuring that AI-generated clues and red herrings lead to a solvable yet challenging mystery is a complex design task.
    -   **Subjectivity of "Good" Mystery:** Defining and achieving a "good" or "engaging" mystery is inherently subjective and will require significant human judgment and iteration.
    -   **Scalability of Coherence Mechanisms:** The proposed coherence agents (Red Team, MMO Logic Integrity, Ripple Effect Analyzer) may become bottlenecks or computationally intensive as mystery complexity grows.

## Relevant Research (Optional)

Comprehensive research was conducted during the Business Analysis phase and has been compiled into the **`deep-research-report-BA.md`** document located in the `MurderMysteryGen/docs/` directory. This report covers:
-   Detailed market analysis of "murder mystery in a box" games, including key players, target audiences, and opportunities.
-   Competitor analysis focusing on strengths, weaknesses, and areas for differentiation.
-   In-depth assessment of the OpenAI Agents SDK's capabilities and limitations for complex narrative generation.
-   Exploration of AI techniques for puzzle design, narrative structuring (MMO framework), and achieving coherence.
-   Consideration of multi-agent architectural patterns and cost optimization strategies.
-   Investigation of evaluation strategies for narrative AI, emphasizing qualitative human-led assessment for PoCs.
-   Insights into the craft of professional mystery writing, including clue planting, red herring design, and plot structuring.
-   Synthesis on key challenges and approaches for data representation, print-focused content generation, and AI-human collaborative workflows.

Key takeaways informing this Project Brief include the validation of the MMO framework, the necessity of a structured data model for mystery components, the critical role of human oversight in evaluation and creative polish, and the design of specialized AI agents (including coherence checkers) to manage narrative complexity.

## PM Prompt

"You are an expert Product Manager AI. Your task is to take the following Project Brief for 'Mystery.AI' and develop a detailed Product Requirements Document (PRD) and initial draft Epics for the defined Proof-of-Concept (PoC) features.

**Project Vision:** To create a sophisticated AI-powered system that serves as an expert co-creator for designing and drafting high-quality, complex, and logically sound murder mystery games for a printed format. The ultimate goal is to produce engaging experiences for end players, with the initial development phase focusing on the human author as the primary user of the AI tool.

**Core Task:** Translate the high-level MVP features (which are the PoCs) into detailed requirements. Focus on:
1.  **PoC 1: Minimal Viable Mystery Core:** Requirements for agents to generate a basic, solvable micro-mystery (1 victim, 2 suspects, 1 killer, 1 MMO element for killer, 2-3 pieces of evidence). Define expected inputs (e.g., theme/setting placeholders) and outputs (structured data for case elements, text for evidence).
2.  **PoC 2: Suspect Profile Generator & MMO Integrity Check:** Requirements for agents to generate multiple distinct suspect profiles with full MMOs. Detail the inputs (crime setup) and outputs (structured suspect profiles, validation status from MMO Logic Integrity Agent). Specify criteria for "plausible" and "internally consistent" MMOs.
3.  **PoC 3: Single Evidence Thread Weaver:** Requirements for agents to generate a coherent chain of 3-5 evidence items for a specific MMO element of a given killer. Define inputs (killer, specific MMO element) and outputs (structured evidence chain, text content). Address "fair clue" principles.
4.  **System-Wide: Structured Data & Coherence:** Requirements for the underlying data model (JSON/Pydantic) that will store all mystery components. Define how this data structure supports the PoCs and enables coherence checks. Detail the initial functional requirements for the conceptual coherence agents (Red Team, MMO Logic Integrity, Ripple Effect Analyzer) as they apply to validating PoC outputs.

**Key Considerations for PRD & Epics:**
*   **User (Author-Creator):** The system should empower the author with control and provide outputs that are useful as first drafts for a printed game.
*   **MMO Framework:** This is central to the logic.
*   **Printed Output:** Generated content (text for clues, letters, reports) must be suitable for this medium.
*   **OpenAI Agents SDK:** The system will be built using this SDK.
*   **Iterative Development:** The PRD should acknowledge that these PoCs are for learning and will inform future iterations.
*   **Qualitative Evaluation:** Success metrics for PoCs are primarily qualitative human reviews. The PRD should define what aspects will be reviewed.

**Deliverables:**
1.  `prd.md` covering the scope of the three PoCs.
2.  Initial draft Epic markdown files (e.g., `epic1-MinimalMysteryCore.md`, `epic2-SuspectProfiler.md`, `epic3-EvidenceWeaver.md`) outlining user stories and acceptance criteria for each PoC.

Refer to the full Project Brief for details on goals, audience, constraints, and research. Focus on defining the 'what' for these initial PoCs, enabling the subsequent Architecture phase to define the 'how'." 