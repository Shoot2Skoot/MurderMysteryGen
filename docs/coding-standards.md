# Mystery.AI - Coding Standards (MVP)

This document outlines the coding standards and best practices to be followed during the development of the Mystery.AI MVP. Adhering to these standards will help ensure code quality, consistency, maintainability, and ease of collaboration (even with AI developer agents).

## 1. General Python Standards

-   **PEP 8:** All Python code should adhere to the PEP 8 style guide.
    -   Use an auto-formatter like Black to ensure compliance.
-   **Type Hinting:** All functions, methods, and variables should have type hints (PEP 484).
    -   Use Pydantic models for complex data structures passed between agents or functions.
-   **Docstrings (Google Style):**
    -   All public modules, classes, functions, and methods should have clear docstrings (PEP 257) using Google style.
    -   Example (Google Style):
        ```python
        def my_function(param1: int, param2: str) -> bool:
            """Does something interesting.

            Args:
                param1 (int): The first parameter.
                param2 (str): The second parameter.

            Returns:
                bool: True if successful, False otherwise.
            """
            # ... implementation ...
            return True
        ```
-   **Readability:** Prioritize clear and readable code over overly clever or obscure implementations.
-   **Modularity:** Write small, focused functions and classes with single responsibilities.
-   **Error Handling:** Use `try-except` blocks for operations that might fail (e.g., LLM calls, file I/O). Log errors appropriately.
-   **Logging:** Use the standard Python `logging` module for all application logging. Do not use `print()` statements for debugging information in committed code.
-   **Naming Conventions:**
    -   Modules and Packages: `snake_case` (e.g., `case_initializer.py`, `mystery_ai.core`).
    -   Classes: `PascalCase` (e.g., `VictimProfile`, `CaseInitializationAgent`).
    -   Functions and Methods: `snake_case` (e.g., `generate_mmo()`, `run_pipeline()`).
    -   Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_THEME = "Noir"`).
    -   Variables: `snake_case`.

## 2. OpenAI Agents SDK Specifics

-   **Import Convention:**
    -   The SDK is installed as `openai-agents`.
    -   Import it in Python as `agents`. Example: `from agents import Agent, Runner, ModelSettings, trace`.
-   **Module Naming Conflict:** **Do NOT name any local Python module `agents.py`**. This will conflict with the SDK import. The directory `src/mystery_ai/agents/` is acceptable as it forms part of a package path.
-   **Agent Definition:**
    -   Define each specialized agent as an instance of `agents.Agent`.
    -   Provide clear and concise `instructions` for each agent.
    -   Use descriptive `name` parameters for agents (e.g., `"Case Initialization Agent"`).
    -   Specify the LLM model using the `model="model_name_string"` parameter (e.g., `model="gpt-4.1-mini"`).
    -   For other model parameters like temperature, top_p, etc., use the `model_settings` parameter, passing an `agents.ModelSettings` object (e.g., `model_settings=ModelSettings(temperature=0.7)`).
-   **Structured Outputs:**
    -   When an agent's primary output is structured data, **always use Pydantic models** defined in `src/mystery_ai/core/data_models.py` as the `output_type` for the agent.
    -   Ensure these Pydantic models strictly adhere to OpenAI's supported types for structured JSON output (primitives, Enums, Lists of supported types, nested Pydantic models). Refer to [OpenAI Structured Outputs Guide](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses).
    -   Pydantic `default` and `default_factory` can be used in models specified as `output_type`; the LLM will be informed of optional fields, and Pydantic will apply defaults if omitted in the LLM's JSON response.
-   **Agent Execution:**
    -   Use `agents.Runner.run()` (for `async`) or `agents.Runner.run_sync()` (for synchronous code) to execute agents.
    -   The `RunConfig` object within `Runner.run()` can be used to customize tracing for a specific run (e.g., `RunConfig(tracing_disabled=True)` or `RunConfig(trace_config=...)`).
-   **Error Handling for Agent Runs:** Wrap calls to `Runner.run()` in `try-except` blocks.
-   **Tracing Customization:**
    -   Leverage the SDK's tracing capabilities. When initiating a trace for a significant workflow (e.g., a full mystery generation), use `with agents.trace(...)` context manager.
    -   Specify `workflow_name` for logical grouping (e.g., `"MysteryGenerationMVP"`).
    -   Consider using `trace_id` (e.g., a UUID generated for the session) and `group_id` (if applicable for related sub-traces).
    -   Add relevant `metadata` to traces for better context (e.g., input theme, key configuration parameters).
    -   Refer to the [OpenAI Agents SDK Tracing Documentation](https://openai.github.io/openai-agents-python/tracing/) for details on `trace()`, `RunConfig`, and trace properties.
    -   Be mindful of sensitive data in traces as per SDK documentation (`RunConfig.trace_include_sensitive_data`).

## 3. Pydantic Model Standards

-   **Location:** Core Pydantic data models for the foundational mystery generation reside in `src/mystery_ai/core/data_models.py`. Pydantic data models specific to the Branching Evidence System (e.g., `BranchingCaseContext` and its components) will reside in `src/mystery_ai/core/data_models_branching.py`.
-   **Clarity:** Models should be clearly named (`PascalCase`) and fields should have descriptive names and type hints.
-   **Field Descriptions:** Use `Field(description="...")` for all Pydantic model fields.
-   **OpenAI Constraints:** Models used for `output_type` in agents must adhere to OpenAI's structured output limitations.
-   **Defaults:** Use `default=...` or `default_factory=...` for optional fields. `default_factory=list` for mutable list defaults.
-   **Model Configuration:** For top-level context models like `CaseContext` or `BranchingCaseContext` that aggregate many sub-models, consider using `model_config = {"extra": "ignore"}` to allow for graceful handling of unexpected fields from LLM responses or other sources.

## 4. Version Control (Git)

-   **Commit Messages:** Write clear, concise, and informative commit messages (e.g., Google style or Conventional Commits).
-   **Branching:** Use a feature-branching workflow.
-   **Pull Requests (if applicable):** Ensure PRs are reviewed.
-   **.gitignore:** Keep updated.

## 5. Testing

-   (Brief, details in `testing-strategy.md`)
-   Strive for testable code. Unit and integration tests are expected.

Adherence to these standards will be reviewed periodically. 