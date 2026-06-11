"""
软件架构作业2 - ADD 3.0 Hotel Pricing System (HPS) Architecture Design
使用 Direct LLM Interaction（隐式单步推理）+ gemini-3.1-pro-preview

成员A：编写脚本与基础架构，执行迭代1
成员B：执行迭代2、迭代3
成员C：执行迭代4，整合报告

使用前请确保：
  pip install openai
"""

import time
import os
from openai import OpenAI

# ============================================================
# 配置
# ============================================================
BASE_URL = "https://api.ppio.com/openai"
API_KEY = os.environ.get("HPS_API_KEY", "")  # 建议通过环境变量传入
MODEL = "pa/gemini-3.1-pro-preview"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# ============================================================
# 先验知识（Prior Knowledge）—— 必须完整粘贴，禁止遗漏或添加
# ============================================================
PRIOR_KNOWLEDGE = r"""
=== ADD 3.0 Method (Steps 1-7) ===

Step 1 - Review Inputs:
The first step of the ADD method is to review the inputs and identify which requirements will be considered as architectural drivers.

Step 2 - Establish the Iteration Goal by Selecting Drivers:
Design rounds typically take the form of a series of design iterations, each focusing on achieving a specific goal. The goal typically involves designing to satisfy a subset of the drivers.

Step 3 - Choose One or More Elements of the System to Refine:
This step is the beginning of the core design activities. The elements you choose are those that participate in satisfying the specific drivers. For greenfield development, you can start by establishing the system context and then selecting the only available element—the system itself—to decompose and refine. For existing systems or subsequent design iterations of a greenfield system, you typically choose to refine elements that have been identified in previous iterations.

Step 4 - Choose One or More Design Concepts That Satisfy the Selected Drivers:
This step requires you to identify alternatives among the design concepts that can be used to achieve the iteration goal, and select one of them.

Step 5 - Instantiate Architectural Elements, Allocate Responsibilities, and Define Interfaces:
This step requires you to instantiate architectural elements based on the selected design concepts, allocate responsibilities, and define interfaces.

Step 6 - Sketch Views and Record Design Decisions:
Sketch appropriate views (module, component-and-connector, allocation) to record the design decisions made so far.

Step 7 - Perform Analysis of Current Design and Review Iteration Goal:
Analyze whether the current design satisfies the selected drivers and review whether the iteration goal has been achieved.

=== HPS: Hotel Pricing System - Design Purpose ===

This project can be treated as greenfield development because it involves completely replacing an existing system. The purpose of the design activity is to make initial decisions to support building the system from scratch.

=== HPS: Primary Functionality (Use Cases) ===

| Use Case ID       | Description |
| :---------------- | :---------- |
| HPS-1: Login      | A user (business user or administrator) provides credentials at the login window. The system validates these credentials through the user identity service, and if successful, grants access to the system. After logging in, the user can only query and change prices for hotels they are authorized for. |
| HPS-2: Change Price | A user selects a specific hotel for which they have the right to change prices, and selects a date to change the base price or fixed price. At this point, all prices calculated based on the base price are calculated. The system allows price change simulation before actually changing prices. When prices are changed, they are pushed to the channel management system and are available for external systems to query. |
| HPS-3: Query Price | A user or external system queries the price of a specified hotel through the user interface or query API. |
| HPS-4: Manage Hotels | An administrator adds, changes, or modifies hotel information. This includes editing the hotel's tax rates, available prices, and room types. |
| HPS-5: Manage Prices | An administrator adds, changes, or modifies prices. This includes defining calculation business rules for different prices. |
| HPS-6: Manage Users | An administrator changes the permissions of a specified user. |

=== HPS: Quality Attributes ===

| ID   | Quality Attribute | Scenario [Associated Use Case] | Importance to Customer | Difficulty of Implementation |
| :--- | :---------------- | :----------------------------- | :--------------------- | :--------------------------- |
| Q-1  | Performance       | During normal operation, the base price for a specific hotel and date is changed; prices for all prices and room types of the hotel are published (ready for query) within 100 milliseconds. [HPS-2] | High | High |
| Q-2  | Reliability       | A user makes multiple price changes for a specified hotel; 100% of the price changes are successfully published (available for query) and received by the channel management system. [HPS-2] | High | High |
| Q-3  | Availability      | The SLA for price queries must reach 99.9% outside of maintenance windows. [All] | High | High |
| Q-4  | Scalability       | The system initially supports at least 100,000 price queries per day through its API, and should be able to handle up to 1,000,000 with an average latency increase of no more than 20%. [HPS-3] | High | High |
| Q-5  | Security          | A user logs into the system through the frontend. The user's credentials are validated through the user identity service, and after login, they can only see the functions they are authorized to use. [All] | High | Medium |
| Q-6  | Modifiability     | Add a price query endpoint to the system that uses a non-REST protocol (e.g., gRPC). The new endpoint does not require changes to the core components of the system. [All] | Medium | Medium |
| Q-7  | Deployability     | The application is migrated between non-production environments as part of the development process. No code changes are required. [All] | Medium | Medium |
| Q-8  | Monitorability    | System operators wish to measure the performance and reliability of price publication during runtime. The system provides a mechanism that allows 100% of these metrics to be collected as needed. [HPS-2] | Medium | Medium |
| Q-9  | Testability       | 100% of the system and its elements should support integration testing independent of external systems. [All] | Medium | Medium |

=== HPS: Architectural Concerns ===

| ID    | Concern |
| :---- | :------- |
| CRN-1 | Establish the overall initial system structure. |
| CRN-2 | Leverage the team's knowledge of Java technologies, Angular framework, and Kafka. |
| CRN-3 | Allocate work to development team members. |
| CRN-4 | Avoid introducing technical debt. |
| CRN-5 | Establish continuous deployment infrastructure. |

=== HPS: Constraints ===

| ID    | Constraint |
| :---- | :--------- |
| CON-1 | Users must interact with the system through web browsers on different platforms (Windows, OSX, Linux) and different devices. |
| CON-2 | Users are managed through a cloud provider identity service, and resources are hosted in the cloud. |
| CON-3 | The code must be hosted on a proprietary Git-based platform that is already used by other projects in the company. |
| CON-4 | The initial version of the system must be delivered within 6 months, but an initial version (MVP) must be demonstrated to internal stakeholders within at most 2 months. |
| CON-5 | The system must initially interact with existing systems through REST APIs, but may need to support other protocols in the future. |
| CON-6 | The system should be designed with a cloud-native approach as a priority. |
"""

# ============================================================
# 角色提示（Role Prompt）
# ============================================================
ROLE_PROMPT = r"""
You are a software architect who strictly follows the ADD 3.0 method.
You must follow these rules:
1. It is FORBIDDEN to introduce any external domain knowledge (you may ONLY use the content in the "Prior Knowledge" section above).
2. It is FORBIDDEN to use any few-shot examples or hand-crafted demonstration outputs.
3. It is FORBIDDEN to reinterpret the requirements or add extra requirements beyond what is stated in the Prior Knowledge.
4. All design decisions must explicitly reference the Prior Knowledge (e.g., "According to Q-2's scenario", "According to CON-4's time constraint").
5. Each iteration must output in the strict order of Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7. If any step is skipped, the output is invalid.
6. All views must be generated using Mermaid code blocks (```mermaid ... ```).
7. The output must be in English, but minor grammatical imperfections are acceptable.
"""

# ============================================================
# 系统指令（System Prompt）= 先验知识 + 角色提示
# ============================================================
SYSTEM_PROMPT = PRIOR_KNOWLEDGE.strip() + "\n\n" + ROLE_PROMPT.strip()

# ============================================================
# 各迭代 User Prompt
# ============================================================
USER_PROMPT_ITER1 = r"""
Iteration Goal: Establishing an Overall System Structure (per assignment).

Please follow ADD 3.0 steps strictly. Output Step 2 through Step 7.

Step 2: Select the iteration goal and list the drivers (from HPS inputs) that this iteration will satisfy. Explain why.

Step 3: According to ADD for greenfield development, select "the system itself" as the only element to refine. Justify.

Step 4: Identify at least two alternative design concepts (reference architectures, deployment patterns) from the prior knowledge. Compare them with pros/cons, then select one. Provide explicit rationale referencing constraints (e.g., CON-1, CON-2, CON-6) or quality attributes.

Step 5: Instantiate architectural elements. Use a table with columns: Element Name, Responsibility, Properties (e.g., stateless, framework). Define interfaces (e.g., REST endpoints, message channels).

Step 6: Sketch the overall system structure using Mermaid code (module view or context diagram).

Step 7: Analyze whether the current design satisfies the selected drivers. Conclude if the iteration goal is achieved.
"""

USER_PROMPT_ITER2 = r"""
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

USER_PROMPT_ITER3 = r"""
Based on the architecture from iteration 2, now address reliability and availability.

Iteration Goal: Addressing Reliability and Availability Quality Attributes.

Drivers: Q-2 (100% price change publication success) and Q-3 (99.9% uptime for queries).

Step 2: Select Q-2 and Q-3 as drivers.

Step 3: Choose elements to refine: the price publication component and the query API component from iteration 2.

Step 4: Select design concepts for availability (e.g., active redundancy, failover, retry tactics). Refer to tactics from prior knowledge. Compare two alternatives (e.g., load-balanced cluster vs. active-passive). Choose one and justify.

Step 5: Instantiate redundant elements (e.g., load balancer, replicated application instances, database replica). Define health check interfaces.

Step 6: Draw a deployment view (allocation view) using Mermaid, showing physical nodes and redundancy.

Step 7: Analyze whether Q-2 and Q-3 can be met. If not, propose adjustments.
"""

USER_PROMPT_ITER4 = r"""
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
# LLM 调用函数（含时间戳日志 + token 消耗记录）
# ============================================================
def call_llm(iteration_name: str, user_prompt: str, prev_output: str = "") -> str:
    """
    调用 LLM 并记录完整日志。

    Args:
        iteration_name: 迭代名称，如 "iter1"
        user_prompt: 本次迭代的 User Prompt
        prev_output: 前一次迭代的 Assistant Response（迭代2~4需要）

    Returns:
        Assistant 的回复文本
    """
    # 构造实际发送的 user message
    # 如果有前次输出，附加在 user prompt 之前
    if prev_output:
        full_user_msg = (
            f"The following is the output from the previous iteration:\n\n"
            f"--- BEGIN PREVIOUS ITERATION OUTPUT ---\n{prev_output}\n--- END PREVIOUS ITERATION OUTPUT ---\n\n"
            f"{user_prompt}"
        )
    else:
        full_user_msg = user_prompt

    # 时间戳
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"log_{iteration_name}.txt"

    # 写入请求日志
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== ITERATION: {iteration_name} ===\n")
        f.write(f"=== TIMESTAMP: {timestamp} ===\n\n")
        f.write("=== SYSTEM PROMPT ===\n")
        f.write(SYSTEM_PROMPT + "\n\n")
        f.write("=== USER PROMPT ===\n")
        f.write(full_user_msg + "\n\n")

    print(f"[{timestamp}] Calling LLM for {iteration_name}...")

    # 调用 API
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": full_user_msg},
        ],
    )

    # 提取回复
    answer = response.choices[0].message.content

    # 提取 token 消耗
    usage = response.usage
    token_info = ""
    if usage:
        token_info = (
            f"Prompt tokens: {usage.prompt_tokens}\n"
            f"Completion tokens: {usage.completion_tokens}\n"
            f"Total tokens: {usage.total_tokens}\n"
        )

    # 写入回复日志
    end_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=== ASSISTANT RESPONSE ===\n")
        f.write(answer + "\n\n")
        f.write(f"=== TOKEN USAGE ===\n{token_info}\n")
        f.write(f"=== RESPONSE TIMESTAMP: {end_timestamp} ===\n")

    print(f"[{end_timestamp}] {iteration_name} complete. Tokens: {token_info.strip() if token_info else 'N/A'}")

    return answer


# ============================================================
# 主流程：依次执行4次迭代
# ============================================================
def run_all_iterations():
    """依次执行迭代1 → 迭代2 → 迭代3 → 迭代4"""
    prev_output = ""
    total_prompt_tokens = 0
    total_completion_tokens = 0

    iterations = [
        ("iter1", USER_PROMPT_ITER1),
        ("iter2", USER_PROMPT_ITER2),
        ("iter3", USER_PROMPT_ITER3),
        ("iter4", USER_PROMPT_ITER4),
    ]

    for iter_name, prompt in iterations:
        answer = call_llm(iter_name, prompt, prev_output)
        prev_output = answer  # 下一次迭代的输入

    # 汇总 token 消耗
    print("\n" + "=" * 60)
    print("TOKEN CONSUMPTION SUMMARY")
    print("=" * 60)
    grand_total = 0
    for iter_name, _ in iterations:
        log_file = f"log_{iter_name}.txt"
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read()
                # 提取 token 信息
                if "Total tokens:" in content:
                    for line in content.split("\n"):
                        if "Total tokens:" in line:
                            try:
                                total = int(line.split(":")[-1].strip())
                                grand_total += total
                                print(f"  {iter_name}: {total} tokens")
                            except ValueError:
                                pass
    print(f"  GRAND TOTAL: {grand_total} tokens ({grand_total / 1000:.1f}K tokens)")
    print("=" * 60)


def run_single_iteration(iteration_number: int):
    """只执行某一次迭代（1-4），用于成员B、C接力执行"""
    if iteration_number < 1 or iteration_number > 4:
        print("Error: iteration_number must be 1, 2, 3, or 4")
        return

    prompts = {
        1: USER_PROMPT_ITER1,
        2: USER_PROMPT_ITER2,
        3: USER_PROMPT_ITER3,
        4: USER_PROMPT_ITER4,
    }

    iter_name = f"iter{iteration_number}"
    prompt = prompts[iteration_number]

    # 读取前一次迭代的输出
    prev_output = ""
    if iteration_number > 1:
        prev_log = f"log_iter{iteration_number - 1}.txt"
        if os.path.exists(prev_log):
            with open(prev_log, "r", encoding="utf-8") as f:
                content = f.read()
                # 提取 ASSISTANT RESPONSE 部分
                if "=== ASSISTANT RESPONSE ===" in content:
                    parts = content.split("=== ASSISTANT RESPONSE ===")
                    if len(parts) >= 2:
                        response_section = parts[1]
                        # 截取到 TOKEN USAGE 之前
                        if "=== TOKEN USAGE ===" in response_section:
                            prev_output = response_section.split("=== TOKEN USAGE ===")[0].strip()
                        else:
                            prev_output = response_section.strip()
            print(f"Loaded previous iteration output from {prev_log} ({len(prev_output)} chars)")
        else:
            print(f"Warning: {prev_log} not found. Proceeding without previous iteration output.")

    call_llm(iter_name, prompt, prev_output)


# ============================================================
# 入口
# ============================================================
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # 用法: python hps_add.py 1    → 只执行迭代1
        #       python hps_add.py 2    → 只执行迭代2（需先有 log_iter1.txt）
        #       python hps_add.py all  → 依次执行所有迭代
        arg = sys.argv[1]
        if arg == "all":
            run_all_iterations()
        else:
            try:
                n = int(arg)
                run_single_iteration(n)
            except ValueError:
                print("Usage: python hps_add.py [1|2|3|4|all]")
    else:
        # 默认：只执行迭代1（成员A的工作）
        print("Running Iteration 1 only (Member A's task).")
        print("To run other iterations: python hps_add.py [2|3|4|all]")
        print()
        run_single_iteration(1)
