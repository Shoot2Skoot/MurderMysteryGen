# Epic 5: Advanced Prompt Engineering for Content Diversification

**Goal:** To systematically refine and enhance the instruction prompts for all content-generating AI agents within the Mystery.AI system. The objective is to significantly increase the diversity, creativity, and originality of generated mystery elements (victim details, suspect profiles, MMOs, evidence), reducing repetition and thematic stereotyping.

**Rationale:** Based on MVP testing, while the core generation mechanics are functional, the creative output shows a tendency towards common tropes and repetition, especially in causes of death and character roles within certain themes. Improving prompt engineering is the most direct way to address this and enhance the quality and uniqueness of the generated mystery frameworks.

**Key Performance Indicators (KPIs) for this Epic:**
-   Increased range of unique "Cause of Death" outputs per theme over X runs.
-   Reduced percentage of "stereotypical" occupations/personalities for a given theme (qualitative assessment or defined metrics).
-   Higher qualitative rating for "overall scenario uniqueness" by the primary user/reviewer when generating multiple mysteries with the same theme.
-   Reduction in directly repeated phrases or narrative elements across different generations of the same theme.

## Stories

### Story 5.1: Diversify Victim - Cause of Death Generation

-   **User Story / Goal:** As a Developer, I want to refine the `CaseInitializationAgent`'s instructions to produce a significantly wider and more creative range of "causes of death" that are still thematically appropriate, reducing common repetitions like strangulation or simple poisoning.
-   **Detailed Requirements:**
    -   Analyze current `CaseInitializationAgent` instructions for cause of death generation.
    -   Research and document 2-3 distinct prompt engineering strategies specifically aimed at increasing output diversity for a constrained generation task (e.g., asking for lists and then selection, negative prompting, role-playing for creativity, few-shot examples showcasing variety).
    -   Select one promising strategy and update the agent's instructions to incorporate it. The prompt should explicitly ask for causes of death that are imaginative, fitting to the theme, and avoid common clichés unless a unique twist is provided.
    -   Consider adding phrasing like: "Suggest 3-5 distinct and thematically plausible causes of death, ranging from common to more unusual, then select the most compelling one for this mystery."
    -   Ensure the agent still correctly outputs the `VictimProfile` Pydantic model.
-   **Acceptance Criteria:**
    -   AC1: The `CaseInitializationAgent` instructions are updated with a new prompting strategy for cause of death.
    -   AC2: Running the full pipeline (`python -m src.mystery_ai.main --theme "TestTheme1"`) 10 times results in at least 5 identifiably different (non-trivial variations) causes of death.
    -   AC3: Running the full pipeline with 3 diverse themes (e.g., "Sci-Fi Mars Base", "1920s Circus Troupe", "Quiet Seaside Village") 5 times each, results in a qualitative assessment of "good" or "excellent" diversity in causes of death by the primary user.
    -   AC4: Generated causes of death remain thematically plausible and integrate coherently with the victim profile.
-   **Dependencies:** Completed MVP (Epics 1-4, 4.5).
-   **Status:** To Do

---

### Story 5.2: Diversify Victim - Occupation & Personality Generation

-   **User Story / Goal:** As a Developer, I want to update the `CaseInitializationAgent`'s prompts to generate more varied and less stereotypical victim occupations and personalities that are still thematically consistent.
-   **Detailed Requirements:**
    -   Analyze current `CaseInitializationAgent` instructions for occupation and personality generation.
    -   Modify prompts to explicitly ask for:
        -   "An occupation that is both thematically relevant and offers unique motivations or vulnerabilities for a victim."
        -   "A primary personality trait, and a contrasting or hidden secondary trait that could create conflict or intrigue."
        -   "Avoid common or stereotypical occupations/personalities for the given theme unless a compelling, unique angle is provided."
    -   Provide 1-2 few-shot examples *within the prompt* for a different theme, showcasing a non-stereotypical occupation/personality pairing (e.g., Theme: "Wild West Saloon" -> Victim Occupation: "Traveling Botanist studying desert flora," Personality: "Publicly shy and academic, but secretly a gambler").
    -   Instruct the agent to briefly explain how the chosen occupation and personality could make the victim a target or central to a mystery.
-   **Acceptance Criteria:**
    -   AC1: `CaseInitializationAgent` instructions updated with new strategies for occupation/personality.
    -   AC2: Generating 5 mysteries for "Midwest Small Town Suburban Neighborhood" theme results in no more than 1 victim being directly school-related (teacher, principal).
    -   AC3: Generating 5 mysteries for "Cyberpunk City" theme results in at least 3 distinct, non-clichéd victim occupations (e.g., not just "hacker" or "corporate drone" without a unique angle).
    -   AC4: Qualitative review by the primary user of 10 generated victims (across 2-3 themes) rates personality diversity and depth as "improved" or "significantly improved" compared to MVP baseline.
-   **Dependencies:** Story 5.1 (potentially, as a well-defined victim is key).
-   **Status:** To Do

---

### Story 5.3: Diversify Suspect Profile Generation

-   **User Story / Goal:** As a Developer, I want to enhance the `SuspectGenerationAgent`'s instructions to produce more unique suspect archetypes, descriptions, and relationships to the victim, avoiding repetition and thematic clichés.
-   **Detailed Requirements:**
    -   Analyze current `SuspectGenerationAgent` instructions.
    -   Modify prompts to ask for:
        -   "A set of 2-3 suspects with diverse archetypes/roles within the theme. Ensure they are not all cut from the same cloth."
        -   "For each suspect, describe a primary characteristic and a less obvious secondary characteristic or a secret they might harbor."
        -   "Define relationships to the victim that create a variety of potential conflict points (e.g., professional rivalry, romantic entanglement, familial duty, ideological opposition, chance encounter with consequence)."
        -   "Avoid making all suspects direct peers or all having the same type of grievance."
    -   Provide 1-2 few-shot examples of diverse suspect groups for a sample theme within the prompt.
-   **Acceptance Criteria:**
    -   AC1: `SuspectGenerationAgent` instructions are updated.
    -   AC2: Generating 5 full mystery contexts, the set of suspect descriptions and relationships for each mystery is qualitatively assessed by the primary user as "more diverse" or "more unique" than MVP baseline.
    -   AC3: Across 5 generated mysteries, there is a wider array of suspect archetypes and relationship dynamics observed.
-   **Dependencies:** Story 5.2 (potentially, diverse victims might inspire diverse suspects).
-   **Status:** To Do

---

### Story 5.4: Enhance Creativity and Variety in MMO Generation

-   **User Story / Goal:** As a Developer, I want to refine the `MMOGenerationAgent`'s prompts to inspire more creative, thematically rich, and varied Means, Motives, and Opportunities for each suspect.
-   **Detailed Requirements:**
    -   Analyze current `MMOGenerationAgent` instructions.
    -   Modify prompts to emphasize:
        -   **Thematic Integration:** "How could this suspect's Means/Motive/Opportunity be *uniquely tied* to the [Theme] setting and the specific details of the victim and suspect?"
        -   **Originality:** "Propose a Means that is clever or less common for this type of crime. Suggest a Motive that is nuanced or unexpected. Describe an Opportunity that required specific insight or access."
        -   **Plausibility Constraint:** "While being creative, ensure the MMO remains logically plausible within the established context."
    -   Consider asking the agent to briefly justify its choice for one of the MMO elements, explaining *why it's a strong or interesting fit*.
    -   Experiment with asking for 2-3 alternative ideas for one MMO element, then having it select the best one.
-   **Acceptance Criteria:**
    -   AC1: `MMOGenerationAgent` instructions are updated.
    -   AC2: Qualitative review of 10 generated suspect MMOs (across 3-4 mysteries) shows a noticeable increase in thematic specificity and creative reasoning compared to MVP baseline.
    -   AC3: Fewer generic MMO explanations (e.g., "had a gun," "wanted money," "was there").
-   **Dependencies:** Story 5.3.
-   **Status:** To Do

---

### Story 5.5: Diversify Evidence Descriptions and Types

-   **User Story / Goal:** As a Developer, I want to update the `EvidenceGenerationAgent`'s instructions to produce more varied types of evidence and more evocative descriptions, for both direct clues and red herrings.
-   **Detailed Requirements:**
    -   Analyze current `EvidenceGenerationAgent` instructions.
    -   Modify prompts to:
        -   Suggest a wider range of evidence categories to draw from: "Consider physical objects, digital traces, witness observations (direct or overheard), circumstantial links, or even psychological clues."
        -   Encourage more evocative and detailed descriptions: "Describe the evidence in a way that hints at its significance or creates a small puzzle for the investigator, rather than just stating a fact."
        -   For Red Herrings: "Create red herring evidence that is subtly misleading, perhaps by pointing to a *plausible but ultimately incorrect* interpretation of a non-killer's original MMO, or by having a double meaning."
        -   Ask the agent to ensure evidence items generated for a single case (even for different suspects) are not too similar in their *type* and how they are discovered/presented.
-   **Acceptance Criteria:**
    -   AC1: `EvidenceGenerationAgent` instructions are updated.
    -   AC2: Qualitative review of evidence lists from 5 generated mysteries shows a greater variety in the *types* of evidence presented.
    -   AC3: Evidence descriptions are rated by the primary user as more engaging and less formulaic.
    -   AC4: Red herrings are perceived as more thoughtfully constructed and less obviously misleading.
-   **Dependencies:** Story 5.4.
-   **Status:** To Do

## Change Log

| Change | Date | Version | Description | Author |
| ------ | ---- | ------- | ----------- | ------ |
|        |      | 1.0     | Initial draft of Epic 5 and stories. | PM Agent |
|        |      | 1.1     | Fleshed out Detailed Requirements and ACs for Stories 5.2-5.5. | PM Agent | 