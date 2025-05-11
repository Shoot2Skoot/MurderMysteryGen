# Epic 6: LLM Parameter & Model Experimentation for Creative Control

**Goal:** To systematically investigate, test, and document the impact of different Large Language Model (LLM) generation parameters (e.g., temperature, top_p) and potentially different LLM models (from the approved list) on the diversity, creativity, and thematic coherence of outputs from Mystery.AI's specialized agents. The aim is to identify optimal settings or strategies for enhancing content quality.

**Rationale:** Beyond prompt engineering (Epic 5), the choice of LLM and its generation parameters can significantly influence the nature of the generated text. Understanding these effects will allow for more fine-grained control over the creative output, helping to balance novelty with plausibility and reduce repetitive or stereotypical content. This epic provides an empirical basis for these adjustments.

**Key Performance Indicators (KPIs) for this Epic:**
-   Documented trade-offs (diversity vs. coherence vs. cost vs. speed) for different parameter settings/models for key agents (e.g., `CaseInitializationAgent`, `MMOGenerationAgent`).
-   Identification of "sweet spot" parameter ranges or specific models that demonstrably improve content diversity for selected generation tasks without unacceptable degradation in coherence.
-   A set of recommended default parameters/models for agents, potentially different per agent, based on findings.
-   (If applicable) Implementation of a mechanism to easily switch or configure these parameters/models for experimentation or different generation profiles.

## Stories

### Story 6.1: Research & Document Impact of LLM Parameters on Key Agents

-   **Goal:** As a Developer, I want to research and document the theoretical and observed effects of key LLM generation parameters (primarily `temperature`, `top_p`, potentially others like `frequency_penalty`, `presence_penalty`) on the output of the `CaseInitializationAgent` and `MMOGenerationAgent`.
-   **Detailed Requirements:**
    -   Review OpenAI documentation and community best practices regarding `temperature`, `top_p`, and other relevant generation parameters.
    -   Focus on how these parameters influence creativity, randomness, factual adherence, and coherence.
    -   For `CaseInitializationAgent` (victim details) and `MMOGenerationAgent` (MMOs):
        -   Design a small set of test runs with varying `temperature` values (e.g., 0.3, 0.7, 1.0, 1.2) while keeping other settings constant.
        -   Run each agent (or the relevant part of the pipeline) multiple times with these settings for a consistent input theme.
        -   Qualitatively assess and document the impact on output diversity, creativity, and coherence (e.g., are causes of death more varied at higher temperatures? Do MMOs become less logical?).
    -   Summarize findings in a new document (e.g., `docs/research/llm_parameter_effects.md`).
-   **Acceptance Criteria:**
    -   AC1: Research document `llm_parameter_effects.md` is created, summarizing parameter effects.
    -   AC2: Document includes observations from test runs of `CaseInitializationAgent` and `MMOGenerationAgent` with at least 3 different temperature settings, showing qualitative impact on output.
    -   AC3: Clear explanation of how `temperature` and `top_p` are expected to affect content generation for this project.
-   **Dependencies:** Epic 5 (as refined prompts might interact with parameter changes).
-   **Status:** To Do

---

### Story 6.2: Implement Configurable LLM Settings per Agent

-   **Goal:** As a Developer, I want to enable the configuration of LLM model name and key generation parameters (like `temperature`) for each specialized agent, so that these can be easily adjusted for experimentation and tuning.
-   **Detailed Requirements:**
    -   Modify the agent instantiation process (likely in `main_orchestrator.py` or if agents are defined as classes, in their constructors).
    -   Allow `model` string and a `ModelSettings` object (for temperature, etc.) to be passed during agent initialization or dynamically configured before an agent run.
    -   Consider a simple configuration mechanism (e.g., a Python dictionary in a `config.py` file, or extending CLI arguments if simple enough) to specify these settings per agent type (e.g., `CaseInitializationAgent_model`, `CaseInitializationAgent_temperature`).
    -   Update `coding-standards.md` or `architecture.md` to reflect how these configurations are managed.
-   **Acceptance Criteria:**
    -   AC1: The LLM model used by `CaseInitializationAgent` can be changed via a configuration without altering its core code.
    -   AC2: The `temperature` setting for `MMOGenerationAgent` can be changed via a configuration.
    -   AC3: The system runs successfully with these new configuration points.
    -   AC4: Default settings are still applied if no specific configuration is provided for an agent.
-   **Dependencies:** Story 6.1 (to know which parameters are most relevant to make configurable).
-   **Status:** To Do

---

### Story 6.3: Comparative Testing of Different LLM Models for Key Tasks

-   **Goal:** As a Developer, I want to perform and document comparative tests using different approved LLM models (e.g., `gpt-4.1-mini` vs. `gpt-4o-mini` vs. `o4-mini`) for critical generation tasks like victim creation and MMO generation, assessing their impact on output diversity, quality, coherence, speed, and (estimated) cost.
-   **Detailed Requirements:**
    -   Leverage the configurable model settings from Story 6.2.
    -   Select 2-3 key generation tasks (e.g., Victim Profile generation, MMO generation for one suspect).
    -   For each task, run it N times (e.g., 5-10) with 2-3 different LLM models from the approved list.
    -   Keep prompts and other parameters (like temperature) consistent for a fair comparison across models for a given task.
    -   Qualitatively evaluate and document:
        -   Diversity of outputs.
        -   Perceived quality/coherence.
        -   Noticeable differences in response style or detail.
        -   (If possible) Relative speed of generation.
    -   Add findings to `docs/research/llm_parameter_effects.md` or a new `llm_model_comparison.md`.
-   **Acceptance Criteria:**
    -   AC1: Comparative test results for at least two different generation tasks using at least two different LLM models are documented.
    -   AC2: Documentation includes qualitative notes on diversity, quality, and style differences.
    -   AC3: A recommendation or summary of which models seem best suited for which tasks (balancing quality, diversity, and potential cost/speed) is provided.
-   **Dependencies:** Story 6.2.
-   **Status:** To Do

---

### Story 6.4: Define & Apply Tuned Default LLM Settings for MVP Agents

-   **Goal:** As a Developer, based on the findings from prompt engineering (Epic 5) and parameter/model experimentation (Stories 6.1-6.3), I want to define and apply an updated set of default LLM models and generation parameters for each agent in the MVP to optimize for a good balance of diversity, coherence, and cost-effectiveness.
-   **Detailed Requirements:**
    -   Consolidate findings from Epic 5 and Stories 6.1-6.3.
    -   For each agent (`CaseInitializationAgent`, `SuspectGenerationAgent`, `MMOGenerationAgent`, `MMOModificationAgent`, `EvidenceGenerationAgent`), decide on:
        -   The default LLM model string.
        -   The default `ModelSettings` (e.g., optimal temperature).
    -   Update the agent definitions or their instantiation in `main_orchestrator.py` to use these new tuned defaults.
    -   Document these chosen defaults and the rationale in `architecture.md` or `tech-stack.md`.
-   **Acceptance Criteria:**
    -   AC1: Default LLM model and `ModelSettings` are explicitly defined and applied for each of the 5 core generative agents.
    -   AC2: The system runs successfully with these new default settings.
    -   AC3: A brief rationale for the chosen default settings for each agent is documented.
-   **Dependencies:** Story 6.3, All of Epic 5.
-   **Status:** To Do

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 1.0     | Initial draft of Epic 6 and stories. | PM Agent | 