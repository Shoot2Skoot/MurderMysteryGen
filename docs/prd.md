# Mystery.AI Product Requirements Document (PRD)

## Intro

This document outlines the product requirements for the Minimum Viable Product (MVP) of "Mystery.AI." Mystery.AI is an AI-driven agentic system designed to assist in the creation of "murder mystery in a box" style games. The MVP focuses on establishing the core generation logic for mystery narratives, specifically leveraging the Means, Motive, and Opportunity (MMO) framework. The initial output will be structured data representing the foundational elements of a mystery, intended for review and use by the primary user (the system designer/author) to validate the generation capabilities. This PRD is informed by the `docs/project-brief.md` which details the overall vision and initial scope.

## Goals and Context

- **Project Objectives:**
    - To develop an AI-driven agentic system (Mystery.AI) capable of autonomously generating the foundational logical framework (Means, Motive, Opportunity, and initial evidence) for murder mystery scenarios.
    - To enable the primary user (system designer/author) to rapidly prototype and iterate on diverse mystery concepts by automating the creation of core narrative elements.
    - To produce a well-structured data output (e.g., JSON) detailing the victim, multiple suspects (including their full and then modified MMOs), the designated killer, and a small set of initial evidence pieces for each suspect.
    - To validate the feasibility and effectiveness of using the OpenAI Agents SDK for orchestrating a multi-agent system for this creative generation task.

- **Measurable Outcomes:**
    - The system consistently generates a complete set of core mystery elements (victim profile, specified number of suspect profiles (2-3) with full MMOs, one designated killer, and non-killer suspects with appropriately weakened MMOs, plus 2-3 initial evidence pieces per suspect) based on minimal thematic input.
    - The generated structured data output is consistently well-formed, complete, and easily parsable, suitable for review and further use by the primary user.
    - The implemented multi-agent workflow executes reliably, demonstrating successful handoffs and data propagation between specialized agents (e.g., Case Setup Agent, MMO Generation Agent, Evidence Generation Agent).

- **Success Criteria (MVP):**
    - The system can successfully generate at least 5 unique and logically plausible core mystery structures (victim, 2-3 suspects with MMOs, killer, evidence) within a 1-hour operational period, with distinct variations based on simple input changes.
    - The primary user assesses the generated MMO logic and initial evidence as "sufficiently coherent and usable as a creative starting point" in at least 70% of the generated outputs.
    - The agent orchestration completes the end-to-end generation process for a single mystery without unrecoverable errors in >90% of attempts.

- **Key Performance Indicators (KPIs) (MVP):**
    - **Generation Completion Rate:** Percentage of initiated generation runs that successfully produce a complete set of structured mystery data.
    - **MMO Coherence Rating (Manual):** Average rating (scale 1-5, by primary user) of the logical consistency and plausibility of the generated MMO frameworks for all suspects.
    - **Evidence Relevance Rating (Manual):** Average rating (scale 1-5, by primary user) of the relevance and logical connection of generated evidence pieces to the respective suspect's MMO.
    - **Time per Full Generation:** Average time taken for the system to generate one complete mystery framework from start to finish.

## Scope and Requirements (MVP / Current Version)

### Functional Requirements (High-Level)

- **Case Initialization:**
    - The system must allow for the input of a basic theme or setting for the mystery (e.g., "Cyberpunk," "Pirate Ship").
    - The system must generate core victim details: Name, Occupation, Personality, and Cause of Death, aligned with the provided theme.
- **Suspect Generation & MMO Framework:**
    - The system must generate a configurable number of unique suspect profiles (e.g., 2-3 suspects).
    - For each suspect, the system must generate a plausible and distinct Means (how they could have committed the crime), Motive (why they would have committed the crime), and Opportunity (when/where they could have committed the crime), all consistent with the case theme and victim details.
- **Killer Selection & MMO Modification:**
    - The system must be able to designate one suspect as the definitive killer.
    - For all non-killer suspects, the system must automatically weaken or invalidate one of their three MMO elements (Means, Motive, or Opportunity) to make them less viable as the killer, while still maintaining them as strong red herrings. The specific element to weaken could be chosen randomly or based on a simple heuristic.
- **Initial Evidence Generation:**
    - For the designated killer, the system must generate a small set (e.g., 2-3 pieces) of distinct evidence items that directly support their established Means, Motive, and Opportunity.
    - For each non-killer suspect, the system must generate a smaller set (e.g., 1-2 pieces) of "red herring" evidence items that point towards their original (now weakened) MMO elements, creating misdirection.
    - Evidence items should be described textually and be logically connected to the suspect and their MMO.
- **Structured Data Output:**
    - The system must produce a comprehensive structured data output (e.g., JSON format) containing all generated case elements:
        - Theme/Setting.
        - Victim details (Name, Occupation, Personality, Cause of Death).
        - List of all Suspects, including for each:
            - Name, brief profile.
            - Original Means, Motive, Opportunity.
            - Indication if they are the killer.
            - If not the killer, their modified/weakened MMO.
        - List of all generated Evidence items, including for each:
            - Description of the evidence.
            - Which suspect it relates to.
            - How it connects to that suspect's Means, Motive, or Opportunity.
- **Agent-Based Orchestration:**
    - The system's generation process must be orchestrated using the OpenAI Agents SDK, employing multiple distinct agents with specialized roles (e.g., a "Case Setup Agent," an "MMO Generation Agent," an "Evidence Generation Agent," and a "Killer Selection & MMO Modification Agent").
    - The system must implement basic, reliable handoff logic to pass data and control between these agents as they collaboratively build the mystery.

### Non-Functional Requirements (NFRs)

- **Performance:**
    - **Generation Time:** The system should aim to generate a complete mystery framework (as defined in functional requirements) within a reasonable timeframe for a single user (e.g., ideally under 5-10 minutes per generation, TBD based on initial agent performance).
    - **Resource Usage:** The system should operate efficiently on a standard developer machine without excessive CPU or memory consumption during a single generation run.
- **Scalability:**
    - Not a primary concern for MVP. The system is designed for single-user, iterative generation. Future scalability will be assessed if the tool evolves towards concurrent use or larger batch processing.
- **Reliability/Availability:**
    - **Generation Success Rate:** The agent orchestration should complete the end-to-end generation process without unrecoverable errors in >90% of attempts (as per success criteria).
    - **Error Handling:** Basic error handling should be implemented within agents to manage common issues (e.g., unexpected LLM responses, data validation failures) and provide informative error messages to the console/log.
- **Security:**
    - **API Key Management:** OpenAI API keys must be handled securely (e.g., via environment variables, not hardcoded).
    - **Data Security:** The generated mystery data, while not containing real PII for the MVP, should be managed with good practice (e.g., if stored temporarily, ensure appropriate permissions). Not a major concern for transient MVP output.
- **Maintainability:**
    - **Code Clarity:** Agent code (instructions, logic) should be clear, well-organized, and understandable to facilitate iteration and debugging.
    - **Modularity:** Agents should be designed with distinct responsibilities to promote modularity and independent development/testing where possible.
    - **Configuration:** Key parameters (e.g., number of suspects, model names) should be easily configurable.
- **Usability/Accessibility (for Primary User - Developer):**
    - **Ease of Execution:** The system should be executable with a simple command or script.
    - **Output Clarity:** The structured data output (JSON) must be well-formatted and easily human-readable for review and debugging.
    - **Logging:** Sufficient logging should be implemented to trace agent activity and diagnose issues during generation.
- **Other Constraints:**
    - **Technology Stack:** Must use Python and **exclusively the OpenAI Agents SDK for all AI agent functionality and LLM interaction.**
    - **LLM Usage:** Primarily targets `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, or `o4-mini` models, as specified in the Project Brief, **configured and utilized via the OpenAI Agents SDK.** Cost implications of model choice should be kept in mind for future iterations, but functionality is prioritized for MVP.

### User Experience (UX) Requirements (High-Level)

- **Primary User (Developer) Interaction:**
    - **Execution:** The system generation process shall be initiated via a straightforward command-line interface (CLI) command or by running a primary Python script.
    - **Input:** Initial thematic input (e.g., "Cyberpunk") should be specifiable as a simple argument to the execution command/script.
    - **Feedback (During Run):** Console output should provide basic status updates on which major agent/stage is currently active (e.g., "Initializing Case...", "Generating Suspect MMOs...", "Generating Evidence..."). Detailed logs should capture more granular activity.
    - **Output (Post Run):** The primary output will be a structured data file (JSON) that is clearly named and easily accessible. The content of this file must be well-formatted for human readability and programmatic parsing.
- **Secondary User (End Player):**
    - Not applicable for MVP. The MVP does not produce a playable game or interface for end players.

### Integration Requirements (High-Level)

- **OpenAI Agents SDK:** The system must be built **exclusively** using the OpenAI Agents SDK for all agent definitions, LLM interactions, model configuration, and orchestration. All calls to language models will be managed through the Agents SDK's `Agent` and `Runner` constructs.
- **OpenAI Models (via Agents SDK):** The system will utilize OpenAI language models (e.g., `gpt-4.1-mini`, `o4-mini`, etc.) as configured and accessed **through the capabilities of the OpenAI Agents SDK**. Secure API key management is required, as per the SDK's requirements for authentication.
- **External Systems/Services:** No other external system integrations are required for the MVP.
- _(See `docs/api-reference.md` for technical details - for MVP, this primarily refers to the patterns and interfaces defined by the OpenAI Agents SDK itself, rather than direct base API calls)._

### Testing Requirements (High-Level)

- **Manual Review:** The primary method for validating the quality and coherence of generated mystery content (MMOs, evidence) for the MVP will be manual review by the system designer/author.
- **Unit/Integration Tests (Code):** While comprehensive test suites are future work, foundational unit tests for critical helper functions and basic integration tests for agent handoff mechanisms are encouraged to ensure code stability. (Specifics TBD during development).
- **Structured Output Validation:** The generated JSON output should be validated against a defined schema (even if simple initially) to ensure consistent structure and presence of key data elements.
- _(See `docs/testing-strategy.md` for details - this document will be developed later to outline a more comprehensive testing approach beyond MVP)._

## Epic Overview (MVP / Current Version)

- **Epic 1: Core Agent Setup & Case Initialization**
    - **Goal:** Establish the basic multi-agent framework using the OpenAI Agents SDK, define the initial agent roles, and implement the capability to initialize a new mystery case with a theme and generate victim details.
- **Epic 2: Suspect & MMO Generation**
    - **Goal:** Develop the agent(s) responsible for generating 2-3 unique suspect profiles and, for each suspect, creating a plausible and distinct Means, Motive, and Opportunity (MMO) consistent with the initialized case.
- **Epic 3: Killer Selection, MMO Modification & Initial Evidence Generation**
    - **Goal:** Implement the logic for an agent to designate one suspect as the killer, appropriately weaken an MMO element for all non-killer suspects, and then generate a small, distinct set of initial evidence pieces (both direct and red herring) for all suspects.
- **Epic 4: Structured Data Output & Orchestration Finalization**
    - **Goal:** Ensure all generated mystery components (victim, suspects with original/modified MMOs, killer, evidence) are correctly aggregated and formatted into a final, well-structured JSON output. Finalize and test the end-to-end agent orchestration for a complete generation run.

## Key Reference Documents

- `docs/project-brief.md`
- `docs/deep-research-report-BA.md`
- `docs/epic1.md` (To be created)
- `docs/epic2.md` (To be created)
- `docs/epic3.md` (To be created)
- `docs/epic4.md` (To be created)
- `docs/architecture.md` (To be created by Architect)
- `docs/tech-stack.md` (To be created by Architect, will detail Python, OpenAI Agents SDK, specific models)
- `docs/data-models.md` (To be created, will detail the JSON schema for output)
- `docs/testing-strategy.md` (To be created, will elaborate on MVP testing and beyond)

## Post-MVP / Future Enhancements

- **Advanced Puzzle Generation:** Incorporate diverse puzzle types (ciphers, logic puzzles, physical evidence interactions).
- **Deep Narrative & Storytelling:** Expand beyond core logic to generate rich character backstories, dialogue, atmospheric descriptions, and a more compelling narrative flow.
- **Multi-Layered Evidence Branching:** Develop more complex, non-linear evidence trees with multiple paths and dependencies, as visualized in `mmo_tree_example.mermaid`.
- **Sophisticated Coherence & Logic Checking:** Implement advanced AI agents or mechanisms for ensuring deep narrative coherence, plot consistency, and solvability (e.g., "Red Team Agent," "MMO Logic Integrity Agent," "Ripple Effect Analyzer").
- **User-Defined Prompts & Customization:** Allow end-users (secondary audience) to provide detailed prompts to guide mystery generation (e.g., specific characters, settings, plot twists).
- **Physical Evidence Design Assistance:** AI tools to suggest or even draft elements for physical evidence (e.g., mock document layouts, image concepts).
- **Evaluation & Refinement Tools:** Develop more robust automated and semi-automated evaluation frameworks for assessing mystery quality, coherence, and engagement.
- **Interactive Gameplay Interface:** A web-based or application interface for players to interact with the generated mysteries digitally.
- **Knowledge Graph Integration:** Explore using knowledge graphs to manage and reason about narrative elements for improved consistency and complexity.
- **Dynamic Difficulty Adjustment:** Mechanisms to tailor the complexity and solvability of mysteries.
- **Thematic Depth & Variety:** Expand the AI's ability to generate mysteries across a wider range of themes and styles with more nuanced understanding.
- **"Human-in-the-loop" Refinement UI:** A tool for the primary user to easily review, edit, and refine AI-generated content.

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 0.1     | Initial PRD draft | PM Agent |

## Initial Architect Prompt

This section provides a comprehensive summary of technical infrastructure decisions, constraints, and considerations for the Architect to reference when designing the system architecture for the Mystery.AI MVP. The primary goal of the MVP is to develop a Python-based agentic system using the OpenAI Agents SDK to generate the foundational logic for murder mysteries, outputting structured JSON data.

### Technical Infrastructure

- **Starter Project/Template:** None. The project will be built from scratch.
- **Hosting/Cloud Provider:** Not applicable for MVP, as the system is a local command-line tool. Future web interface is desired but no provider preferences at this stage.
- **Frontend Platform:** Not applicable for MVP. Future web interface preferences are open (React-based or tools like Streamlit/Gradio).
- **Backend Platform:** The core system will be a Python application. No additional backend framework (like Django/Flask) is required for the MVP's command-line execution and data output.
- **Database Requirements:** No database is required for the MVP. Generated mystery data will be output as transient structured data files (JSON).

### Technical Constraints

- **Primary Technology:** The system **must exclusively use Python and the OpenAI Agents SDK** for all AI agent functionality, LLM interaction, model configuration, and orchestration. Direct calls to base OpenAI APIs are to be avoided; all model interaction must be through the Agents SDK.
- **LLM Models:** The system should be designed to work with OpenAI models such as `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`, `o3`, or `o4-mini`, configured and accessed via the Agents SDK.
- **Development Environment:** Standard Python `venv` will be used. Standard linting/formatting tools (e.g., Black, Ruff) are expected.
- **Output Format:** The primary output of the MVP must be a well-structured JSON file detailing all generated mystery components. A clear schema for this JSON should be defined (and will be documented in `docs/data-models.md`).

### Deployment Considerations

- **Deployment:** Not applicable for MVP (local execution).
- **CI/CD:** Not applicable for MVP.
- **Environments:** Primarily a local development environment.

### Local Development & Testing Requirements

- **Execution:** The system must be executable via a simple CLI command or by running a main Python script.
- **Input:** Basic thematic input should be specifiable via CLI argument.
- **Logging:** Implement sufficient console logging to trace agent activity, handoffs, and key decision points during a generation run. The OpenAI Agents SDK's built-in tracing capabilities should be leveraged.
- **Testing (Code):** Encourage foundational unit tests for critical helper functions and basic integration tests for agent handoffs, though comprehensive test suites are post-MVP.
- **Testing (Generated Content):** Initial validation of generated content will be through manual review of the JSON output by the primary user. Automated checks for schema adherence of the JSON output are required.

### Other Technical Considerations

- **Modularity:** Design agents with clear, distinct responsibilities to promote modularity and ease of iteration.
- **Configuration:** Key operational parameters (e.g., number of suspects to generate, specific LLM model to use for an agent) should be easily configurable (e.g., via a configuration file or CLI arguments).
- **Security:** Ensure OpenAI API keys are managed securely (e.g., environment variables) and not exposed in the codebase. 