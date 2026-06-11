"""
HPS Architecture Design - ADD 3.0 via Direct LLM Interaction
Assignment 2: Attribute Driven Design
Software Architecture Course

Usage:
    python hps_add_script.py [iteration]

    iteration: 1, 2, 3, 4, or "all" (default: "all")

    API key is configured below. To use a different key, set environment variable:
        $env:API_KEY = "your-api-key"
"""

import os
import sys
import time
from openai import OpenAI

# ============================================================
# Configuration
# ============================================================
BASE_URL = "https://api.ppio.com/openai"
API_KEY = os.environ.get("API_KEY", "sk_wH8DBd11bUve2ILbWWMvbrDnXBcFlomV16nvzP-Xiuc")
MODEL = "pa/gemini-3.1-pro-preview"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# ============================================================
# Prior Knowledge (ADD 3.0 + HPS full inputs)
# Must be included in every system prompt per assignment requirement.
# ============================================================
PRIOR_KNOWLEDGE = """
=== PRIOR KNOWLEDGE FOR ARCHITECTURE DESIGN ===

--- ADD 3.0 Method Definition (7 Steps) ---

Step 1 (Global, done once): Review Inputs.
  Identify which requirements will be considered as architectural drivers.
  List all inputs: use cases, quality attributes, concerns, constraints.

Step 2: Establish the iteration goal by selecting drivers.
  State the iteration goal explicitly. Select which subset of drivers
  (use cases, quality attributes, concerns, constraints) will be addressed
  in this iteration.

Step 3: Choose one or more elements of the system to refine.
  For greenfield development, start with "the system itself".
  For subsequent iterations, select specific elements produced in prior iterations.

Step 4: Choose one or more design concepts that satisfy the selected drivers.
  Identify at least two candidate design concepts (reference architectures,
  deployment patterns, tactics, frameworks). Compare pros and cons.
  Select one. All reasoning must come from prior knowledge only.

Step 5: Instantiate architectural elements, allocate responsibilities, define interfaces.
  Use a table with columns: Element Name, Responsibility, Properties.
  Define interfaces (e.g., REST API endpoints, message topics).

Step 6: Sketch views and record design decisions.
  Use Mermaid code blocks for all views.
  Iteration 1: Module view (decomposition view).
  Iteration 2: Component-and-Connector (C&C) view.
  Iteration 3: Deployment view (allocation view with availability tactics).
  Iteration 4: Development view or work assignment view.

Step 7: Perform analysis of current design and review iteration goal.
  Analyze whether the current design satisfies the selected drivers.
  Conclude whether the iteration goal is achieved.

--- HPS (Hotel Price System) Description ---

Design Purpose: Greenfield system, complete replacement of existing system.
Domain: Mature domain (hotel price management).

--- HPS Use Cases (HPS-1 through HPS-6) ---

HPS-1: Manage Hotel Information - CRUD operations for hotel information.
HPS-2: Change Prices - Modify prices (batch or individual).
HPS-3: Query Prices - Query prices by hotel, date, and other criteria.
HPS-4: Manage Hotels - CRUD operations for hotel management.
HPS-5: Synchronize with External CMS - Data synchronization with external CMS.
HPS-6: User Login & Authentication - User authentication and access control.

--- HPS Quality Attributes (QA-1 through QA-9) ---

QA-1 (Performance): Price query response time < 100ms at 95th percentile.
  Associated use case: HPS-3. Importance: High.

QA-2 (Reliability): Price change publication must achieve 100% success
  (max 3 retries on failure). Associated use case: HPS-2. Importance: High.

QA-3 (Availability): Query service uptime >= 99.9%.
  Associated use case: HPS-3. Importance: High.

QA-4 (Security): Only authenticated users can modify prices.
  Associated use cases: HPS-2, HPS-6. Importance: High.

QA-5 (Modifiability): Adding a new pricing strategy must affect < 5 files.
  Associated use case: HPS-2. Importance: Medium.

QA-6 (Testability): Price calculation logic must be unit-testable without
  database dependency. Associated use case: HPS-2. Importance: Medium.

QA-7 (Scalability): Support 10x growth in concurrent price query volume.
  Associated use case: HPS-3. Importance: Medium.

QA-8 (Interoperability): Must be compatible with external CMS data formats.
  Associated use case: HPS-5. Importance: Medium.

QA-9 (Deployability): New version deployments must not require downtime.
  Associated use case: HPS-3. Importance: Low.

--- HPS Architectural Concerns (CRN-1 through CRN-5) ---

CRN-1: The system must support multi-channel distribution (Web, Mobile, API).
CRN-2: The team is familiar with Java, Angular, and Kafka technology stack.
CRN-3: Need to support parallel team work allocation.
CRN-4: The system must provide audit logging.
CRN-5: Need continuous deployment infrastructure.

--- HPS Constraints (CON-1 through CON-6) ---

CON-1: Must be deployed on cloud infrastructure.
CON-2: Must use relational database (PostgreSQL).
CON-3: Must use Git platform for version control.
CON-4: Delivery in 6 months, MVP must be completed in 2 months.
CON-5: Must support integration with existing external CMS.
CON-6: Frontend must use Angular framework.
"""

ROLE_PROMPT = """
You are a software architect who strictly follows the ADD 3.0 method.
You must obey the following rules:

1. You MUST NOT introduce any external domain knowledge beyond the "Prior Knowledge" provided above.
2. You MUST NOT use any few-shot examples or hand-crafted demonstration outputs.
3. You MUST NOT reinterpret the requirements or add extra requirements beyond what is specified.
4. ALL design decisions MUST explicitly reference prior knowledge (e.g., "According to QA-2's scenario", "Based on CON-4's time constraint").
5. Each iteration MUST output steps in order: Step 2 -> Step 3 -> Step 4 -> Step 5 -> Step 6 -> Step 7.
6. ALL views MUST be generated using Mermaid code blocks.
7. Output must be in English, though minor grammatical imperfections are acceptable.
"""

SYSTEM_PROMPT = PRIOR_KNOWLEDGE + "\n\n" + ROLE_PROMPT


# ============================================================
# User Prompts for each iteration
# ============================================================

USER_PROMPT_ITER1 = """
Iteration Goal: Establishing an Overall System Structure (per assignment).

Please follow ADD 3.0 steps strictly. Output Step 2 through Step 7.

Step 2: Select the iteration goal and list the drivers (from HPS inputs) that this iteration will satisfy. Explain why.

Step 3: According to ADD for greenfield development, select "the system itself" as the only element to refine. Justify.

Step 4: Identify at least two alternative design concepts (reference architectures, deployment patterns) from the prior knowledge. Compare them with pros/cons, then select one. Provide explicit rationale referencing constraints (e.g., CON-1, CON-2, CON-6) or quality attributes.

Step 5: Instantiate architectural elements. Use a table with columns: Element Name, Responsibility, Properties (e.g., stateless, framework). Define interfaces (e.g., REST endpoints, message channels).

Step 6: Sketch the overall system structure using Mermaid code (module view or context diagram).

Step 7: Analyze whether the current design satisfies the selected drivers. Conclude if the iteration goal is achieved.
"""

USER_PROMPT_ITER2 = """
Based on the previous iteration's output (especially the elements defined in Step 5), proceed.

Iteration Goal: Identifying Structures to Support Primary Functionality.

Drivers: HPS-2 (Change Prices), HPS-3 (Query Prices), HPS-4 (Manage Hotels).

Step 2: State the goal and select the above use cases as drivers.

Step 3: Choose specific elements from the previous iteration's architecture that need refinement to support these use cases. Name them.

Step 4: Select design concepts (e.g., domain objects, message queues, frameworks like Spring/Kafka). Compare alternatives (e.g., Kafka vs RabbitMQ) and choose based on CRN-2 (team knowledge) and quality attributes.

Step 5: Instantiate refined elements. Allocate responsibilities (e.g., PriceCalculationService, HotelRepository). Define their interfaces.

Step 6: Draw a C&C view (component-and-connector) using Mermaid to show how components interact for price change and query.

Step 7: Analyze if the primary functionality can now be realized.
"""

USER_PROMPT_ITER3 = """
Based on the architecture from iteration 2, now address reliability and availability.

Iteration Goal: Addressing Reliability and Availability Quality Attributes.

Drivers: QA-2 (100% price change publication success) and QA-3 (99.9% uptime for queries).

Step 2: Select QA-2 and QA-3 as drivers.

Step 3: Choose elements to refine: the price publication component and the query API component from iteration 2.

Step 4: Select design concepts for availability (e.g., active redundancy, failover, retry tactics). Refer to tactics from prior knowledge. Compare two alternatives (e.g., load-balanced cluster vs. active-passive). Choose one and justify.

Step 5: Instantiate redundant elements (e.g., load balancer, replicated application instances, database replica). Define health check interfaces.

Step 6: Draw a deployment view (allocation view) using Mermaid, showing physical nodes and redundancy.

Step 7: Analyze whether QA-2 and QA-3 can be met. If not, propose adjustments.
"""

USER_PROMPT_ITER4 = """
Based on all previous iterations, address development and operations.

Iteration Goal: Addressing Development and Operations.

Drivers: CRN-2 (Java/Angular/Kafka knowledge), CRN-3 (team work allocation), CRN-5 (continuous deployment infrastructure). Also CON-4 (6 months delivery, MVP in 2 months) and CON-3 (Git platform).

Step 2: Select these drivers.

Step 3: Choose elements to refine: the build/deployment pipeline, module organization for team allocation.

Step 4: Select design concepts: Git branching strategy, CI/CD pipeline (e.g., Jenkins/GitHub Actions), containerization (Docker), environment promotion. Compare alternatives based on team familiarity.

Step 5: Instantiate development-related elements: version control repository, CI jobs, deployment environments (dev, staging, prod). Assign responsibilities.

Step 6: Draw a development view or work assignment view using Mermaid (e.g., showing modules assigned to teams, pipeline stages).

Step 7: Analyze whether the design supports MVP in 2 months and full release in 6 months, and avoids technical debt.
"""


# ============================================================
# Core function: call LLM and log everything
# ============================================================
def call_llm(iteration_name, user_prompt):
    """Send request to LLM with full system prompt and log the interaction."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"log_{iteration_name}.txt"

    # Write request to log file
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"--- {timestamp} - {iteration_name} ---\n")
        f.write("=== SYSTEM PROMPT ===\n")
        f.write(SYSTEM_PROMPT + "\n\n")
        f.write("=== USER PROMPT ===\n")
        f.write(user_prompt + "\n\n")

    print(f"[{timestamp}] Sending {iteration_name} request to {MODEL}...")

    # Call the API
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    answer = response.choices[0].message.content

    # Log token usage if available
    token_info = ""
    if hasattr(response, 'usage') and response.usage:
        token_info = (
            f"\n=== TOKEN USAGE ===\n"
            f"Prompt tokens: {response.usage.prompt_tokens}\n"
            f"Completion tokens: {response.usage.completion_tokens}\n"
            f"Total tokens: {response.usage.total_tokens}\n"
        )

    # Append response to log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=== ASSISTANT RESPONSE ===\n")
        f.write(answer + "\n")
        if token_info:
            f.write(token_info)

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {iteration_name} complete -> {log_file}")
    if token_info:
        print(f"    Token usage: {response.usage.total_tokens} total")

    return answer


# ============================================================
# Main execution
# ============================================================
def run_iteration(n):
    """Run a single iteration by number."""
    prompts = {
        1: ("iter1", USER_PROMPT_ITER1),
        2: ("iter2", USER_PROMPT_ITER2),
        3: ("iter3", USER_PROMPT_ITER3),
        4: ("iter4", USER_PROMPT_ITER4),
    }
    if n not in prompts:
        print(f"Error: iteration {n} not valid. Choose from 1, 2, 3, 4.")
        sys.exit(1)

    name, prompt = prompts[n]
    print(f"\n{'='*60}")
    print(f"Starting iteration {n}: {name}")
    print(f"{'='*60}")
    call_llm(name, prompt)


if __name__ == "__main__":
    # Determine which iteration(s) to run
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg == "all":
            for i in range(1, 5):
                run_iteration(i)
        else:
            try:
                n = int(arg)
                run_iteration(n)
            except ValueError:
                print(f"Usage: python {sys.argv[0]} [1|2|3|4|all]")
                sys.exit(1)
    else:
        # Default: run all iterations sequentially
        for i in range(1, 5):
            run_iteration(i)

    print(f"\n{'='*60}")
    print("All iterations completed. Log files generated:")
    for i in range(1, 5):
        print(f"  - log_iter{i}.txt")
    print(f"{'='*60}")