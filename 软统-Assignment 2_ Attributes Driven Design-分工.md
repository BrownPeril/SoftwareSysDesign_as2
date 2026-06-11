# 软统\-Assignment 2: Attributes Driven Design\-分工

## 一、方案确认

- **所选AI范式**：Direct LLM interaction（隐式单步推理）  

- **所选LLM**：`gemini-3.1-pro-preview`（调用名：`pa/gemini-3.1-pro-preview`）  

- **API调用基础URL**：`https://api.ppio.com/openai`  

- **迭代计划**（完全按作业要求）：

    1. 建立整体系统结构

    2. 识别支持主要功能的结构

    3. 处理可靠性与可用性质量属性

    4. 处理开发与运维

- **强约束**：

    - 视图必须用 Mermaid / PlantUML

    - 不允许外部领域知识

    - 不允许 few\-shot 示例

    - 不允许任务重解释或需求增强

    - 所有决策规则必须来自系统指令中的先验知识

- 交付物（作业PDF P2）

    1. 源代码（15分）—— 实际就是提示词 \+ 调用LLM的脚本

    2. 完整对话日志（4次迭代，带时间戳）（15分）

    3. 报告（附录模板，20分）

## 二、小组分工（顺序执行，不可并行）



|成员|角色|负责迭代|具体任务|预估时间|
|---|---|---|---|---|
|**A**|脚本与基础架构|迭代1|① 编写Python调用脚本（含自动时间戳日志）\<br\>② 准备完整的先验知识文本（ADD 3\.0 \+ HPS全部输入）\<br\>③ 编写系统指令模板（固定部分）\<br\>④ 执行迭代1，生成`log_iter1.txt`及Mermaid图|90min|
|**B**|功能与质量迭代|迭代2、迭代3|① 基于A提供的脚本和模板\<br\>② 执行迭代2（依赖迭代1输出）\<br\>③ 执行迭代3（依赖迭代2输出）\<br\>④ 分别生成`log_iter2.txt`和`log_iter3.txt`|90min|
|**C**|运维与报告整合|迭代4|① 执行迭代4（依赖迭代3输出）\<br\>② 收集A、B的日志，合并为完整对话日志\<br\>③ 按附录模板撰写报告（含ADD步骤输出、Mermaid图、成本表、反思、贡献表）\<br\>④ 最终提交|90min|



> **顺序约束**：迭代1 → 迭代2 → 迭代3 → 迭代4，后一次必须使用前一次的输出作为输入（尤其是Step 3中要选择前次迭代产生的元素）。三人依次接力，C在等待B时可提前准备报告框架。
> 
> 



## 三、ADD方法在每次迭代中的严格映射（作业要求）



作业PDF第5页给出了ADD方法的7个步骤。**每次迭代必须完整输出Step 2 → Step 7**（Step 1全局只做一次，放在报告开头）。



### Step 1（全局，由C在报告中完成）

> “Review Inputs: identifying which requirements will be considered as architectural drivers\.”
> 
> 

- 输出内容：列出本次设计的所有输入——HPS的6个用例、9个质量属性、5个关注点、6个约束。说明这是一个成熟领域的绿地系统。

    

### 每次迭代中的Step 2 \~ Step 7（严格按以下定义输出）



|ADD步骤|作业PDF原文|本次迭代中必须包含的内容|
|---|---|---|
|**Step 2**|Establish the iteration goal by selecting drivers|明确写出本次迭代的目标（例如“建立整体系统结构”），并选择哪些驱动（用例/质量属性/关注点/约束）作为本次要满足的子集。|
|**Step 3**|Choose one or more elements of the system to refine|对于迭代1：选择“系统本身”（依据PDF：for greenfield development, start by establishing the system context and selecting the only available element—the system itself）。对于后续迭代：选择前次迭代中产生的具体元素进行细化。|
|**Step 4**|Choose one or more design concepts that satisfy the selected drivers|列出至少两个候选设计概念（参考架构、部署模式、战术、框架等），比较优缺点，然后选择一个。所有理由必须来自先验知识（讲义或HPS）。|
|**Step 5**|Instantiate architectural elements, allocate responsibilities, define interfaces|用**表格**形式给出：元素名称、职责、属性（如无状态/有状态、使用的框架等）。定义接口（如REST API端点、消息主题）。|
|**Step 6**|Sketch views and record design decisions|使用**Mermaid**代码块绘制视图。迭代1：模块视图（分解视图）；迭代2：C\&C视图；迭代3：部署视图（含可用性战术）；迭代4：开发视图或工作分配视图。|
|**Step 7**|Perform analysis of current design and review iteration goal|分析当前设计是否满足本次迭代所选中的驱动，并说明是否达到迭代目标。|



## 四、系统指令（System Prompt）编写要点



依据作业PDF第2页“关键点”：**1\. Prior knowledge  2\. Role Prompt**



### 4\.1 先验知识（必须完整粘贴到每条system prompt中）

需包含以下内容（由成员A提前整理成文本块）：

- ADD 3\.0方法的Step 1\~7定义（作业PDF第5页）

- HPS的设计目的（绿地系统，完全替换）

- HPS的6个用例（HPS\-1 \~ HPS\-6）

- HPS的9个质量属性（QA\-1 \~ QA\-9），包含场景、关联用例、重要度

- HPS的5个架构关注点（CRN\-1 \~ CRN\-5）

- HPS的6个约束（CON\-1 \~ CON\-6）

    

### 4\.2 角色提示（Role Prompt）模板

```Plain Text
你是一位严格遵守ADD 3.0方法的软件架构师。
你必须遵循以下规则：
1. 禁止引入任何外部领域知识（只能使用上述“先验知识”中的内容）。
2. 禁止使用任何few-shot示例或手工制作的演示输出。
3. 禁止对需求进行重新解释或增加额外要求。
4. 所有设计决策必须显式地来自先验知识（例如“根据QA-2的场景”、“根据CON-4的时间约束”）。
5. 每次迭代必须按照 Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7 的顺序输出。
6. 所有视图必须使用Mermaid代码块生成。
7. 输出必须是英文，但允许少量语法不完美。
```



## 五、源代码（15分）编写规范



### 5\.1 功能要求

- 能够向`https://api.ppio.com/openai`发送请求，模型为`pa/gemini-3.1-pro-preview`

- 每条请求包含：system prompt（先验知识\+角色提示）和 user prompt（本次迭代的具体指令）

- **自动在日志中记录时间戳**（精确到秒）

- 保存每次迭代的完整对话（system, user, assistant）到独立文件

    

### 5\.2 参考代码框架（成员A实现）

```Python
import time
from openai import OpenAI

# 配置
BASE_URL = "https://api.ppio.com/openai"
API_KEY = "你的API_KEY"   # 上课前助教分配
MODEL = "pa/gemini-3.1-pro-preview"

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# 固定的先验知识（成员A提前填入）
PRIOR_KNOWLEDGE = """
[此处粘贴 ADD 3.0 完整定义 + HPS所有用例、质量属性、关注点、约束]
"""

ROLE_PROMPT = """
你是一位严格遵守ADD 3.0方法的软件架构师。
...（按4.2节内容）
"""

SYSTEM_PROMPT = PRIOR_KNOWLEDGE + "\n\n" + ROLE_PROMPT

def call_llm(iteration_name, user_prompt):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"log_{iteration_name}.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"--- {timestamp} - {iteration_name} ---\n")
        f.write("=== SYSTEM PROMPT ===\n" + SYSTEM_PROMPT + "\n")
        f.write("=== USER PROMPT ===\n" + user_prompt + "\n")
    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )
    answer = response.choices[0].message.content
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("=== ASSISTANT RESPONSE ===\n" + answer + "\n")
    
    # 可选：记录token消耗（如response.usage）
    return answer

# 调用示例：成员A执行迭代1
user_prompt_iter1 = """...（见第六节）"""
call_llm("iter1", user_prompt_iter1)
```



### 5\.3 提交物

- 一个完整的`.py`文件（或`.ipynb`），能够依次执行4次迭代（或分别执行，但需保证脚本可重现）。

- **不需要**提交模型生成的架构方案文本（那些属于日志的一部分）。

    

## 六、各迭代用户提示词（User Prompt）模板



### 迭代1（成员A执行）

```Plain Text
Iteration Goal: Establishing an Overall System Structure (per assignment).

Please follow ADD 3.0 steps strictly. Output Step 2 through Step 7.

Step 2: Select the iteration goal and list the drivers (from HPS inputs) that this iteration will satisfy. Explain why.

Step 3: According to ADD for greenfield development, select "the system itself" as the only element to refine. Justify.

Step 4: Identify at least two alternative design concepts (reference architectures, deployment patterns) from the prior knowledge. Compare them with pros/cons, then select one. Provide explicit rationale referencing constraints (e.g., CON-1, CON-2, CON-6) or quality attributes.

Step 5: Instantiate architectural elements. Use a table with columns: Element Name, Responsibility, Properties (e.g., stateless, framework). Define interfaces (e.g., REST endpoints, message channels).

Step 6: Sketch the overall system structure using Mermaid code (module view or context diagram).

Step 7: Analyze whether the current design satisfies the selected drivers. Conclude if the iteration goal is achieved.
```



### 迭代2（成员B执行，需先读取迭代1的输出）

```Plain Text
Based on the previous iteration's output (especially the elements defined in Step 5), proceed.

Iteration Goal: Identifying Structures to Support Primary Functionality.

Drivers: HPS-2 (Change Prices), HPS-3 (Query Prices), HPS-4 (Manage Hotels).

Step 2: State the goal and select the above use cases as drivers.

Step 3: Choose specific elements from the previous iteration's architecture that need refinement to support these use cases. Name them.

Step 4: Select design concepts (e.g., domain objects, message queues, frameworks like Spring/Kafka). Compare alternatives (e.g., Kafka vs RabbitMQ) and choose based on CRN-2 (team knowledge) and quality attributes.

Step 5: Instantiate refined elements. Allocate responsibilities (e.g., PriceCalculationService, HotelRepository). Define their interfaces.

Step 6: Draw a C&C view (component-and-connector) using Mermaid to show how components interact for price change and query.

Step 7: Analyze if the primary functionality can now be realized.
```



### 迭代3（成员B执行）

```Plain Text
Based on the architecture from iteration 2, now address reliability and availability.

Iteration Goal: Addressing Reliability and Availability Quality Attributes.

Drivers: QA-2 (100% price change publication success) and QA-3 (99.9% uptime for queries).

Step 2: Select QA-2 and QA-3 as drivers.

Step 3: Choose elements to refine: the price publication component and the query API component from iteration 2.

Step 4: Select design concepts for availability (e.g., active redundancy, failover, retry tactics). Refer to tactics from prior knowledge. Compare two alternatives (e.g., load-balanced cluster vs. active-passive). Choose one and justify.

Step 5: Instantiate redundant elements (e.g., load balancer, replicated application instances, database replica). Define health check interfaces.

Step 6: Draw a deployment view (allocation view) using Mermaid, showing physical nodes and redundancy.

Step 7: Analyze whether QA-2 and QA-3 can be met. If not, propose adjustments.
```



### 迭代4（成员C执行）

```Plain Text
Based on all previous iterations, address development and operations.

Iteration Goal: Addressing Development and Operations.

Drivers: CRN-2 (Java/Angular/Kafka knowledge), CRN-3 (team work allocation), CRN-5 (continuous deployment infrastructure). Also CON-4 (6 months delivery, MVP in 2 months) and CON-3 (Git platform).

Step 2: Select these drivers.

Step 3: Choose elements to refine: the build/deployment pipeline, module organization for team allocation.

Step 4: Select design concepts: Git branching strategy, CI/CD pipeline (e.g., Jenkins/GitHub Actions), containerization (Docker), environment promotion. Compare alternatives based on team familiarity.

Step 5: Instantiate development-related elements: version control repository, CI jobs, deployment environments (dev, staging, prod). Assign responsibilities.

Step 6: Draw a development view or work assignment view using Mermaid (e.g., showing modules assigned to teams, pipeline stages).

Step 7: Analyze whether the design supports MVP in 2 months and full release in 6 months, and avoids technical debt.
```



## 七、日志收集与时间戳要求（15分）



- **每个迭代的日志文件必须包含**：

    - 请求开始的时间戳（格式：`YYYY-MM-DD HH:MM:SS`）

    - 完整的System Prompt

    - 完整的User Prompt

    - 完整的Assistant Response

- 文件命名：`log_iter1.txt`, `log_iter2.txt`, `log_iter3.txt`, `log_iter4.txt`

- 成员C最终将它们按时间顺序合并为一个`conversation_log.txt`（或保留四个文件提交，但需注明顺序）。

    

## 八、报告撰写指南（20分）



使用作业PDF第6\-7页的附录模板，输出为PDF，不超过30页。



### 8\.1 报告结构

1. **封面**：课程名、作业名、小组成员、日期、所选方式（Direct LLM \+ gemini）

2. **ADD Step 1（全局输入回顾）**：列表形式展示所有输入（用例、QA、约束、关注点）

3. **迭代1输出**：复制`log_iter1.txt`中Assistant Response的Step 2\~7，并确保Mermaid代码正确渲染。也可重新排版，但内容必须一致。

4. **迭代2输出**：同上

5. **迭代3输出**：同上

6. **迭代4输出**：同上

7. **交互成本分析表**（作业PDF第6页表格）：

    

|The way of completing the assignment|The LLM used|Number of Human Interactions \(turns\)|Token Consumption \(K tokens\)|
|---|---|---|---|
|Direct LLM interaction|gemini\-3\.1\-pro\-preview|4|（根据API返回的usage累加）|



8. **Individual Reflection**（每人一段，中文或英文均可）：

    - 成员A：遇到的问题（如模型输出格式不遵循步骤）及解决方案（如强化prompt中的“必须”）

    - 成员B：如何确保迭代间的依赖（如手动复制前次输出的元素名）

    - 成员C：报告整合中如何保证一致性

9. **贡献表**（作业PDF第7页）：

    

|Name \(Chinese\)|Contributions|
|---|---|
|张三|编写调用脚本，准备先验知识，执行迭代1，生成Mermaid图|
|李四|执行迭代2和迭代3，处理质量属性，收集日志|
|王五|执行迭代4，整合报告，完成成本分析和反思|



### 8\.2 Mermaid图注意事项

- 每个视图必须使用````mermaid`代码块。

- 迭代1：模块分解图（例如：前端模块、后端服务模块、数据库模块、外部CMS模块）

- 迭代2：C\&C图（展示Price Change Controller, Query API, Channel Management System适配器等）

- 迭代3：部署图（云节点、负载均衡器、应用实例主备、数据库主从）

- 迭代4：开发视图（CI/CD流水线、模块与团队映射）

    

## 九、时间安排（课堂3小时内完成）



|时间段|成员A|成员B|成员C|
|---|---|---|---|
|0:00\-0:15|获取API key，配置环境，准备先验知识文本|同左|同左，同时准备报告模板|
|0:15\-0:45|编写Python脚本，测试调用|熟悉脚本，阅读先验知识|搭建报告框架（标题、表格）|
|0:45\-1:15|**执行迭代1**，保存日志，输出Mermaid|等待迭代1结果，准备迭代2提示词|继续填充报告框架|
|1:15\-1:45|协助C检查迭代1输出|**执行迭代2**，保存日志|将迭代1结果填入报告|
|1:45\-2:15|休息/协助|**执行迭代3**，保存日志|将迭代2结果填入报告|
|2:15\-2:45|准备个人反思|准备个人反思|**执行迭代4**，保存日志，合并所有日志，填入报告|
|2:45\-3:00|三人一起复核：检查Mermaid图、日志时间戳、报告格式，提交至Moodle|同左|同左|



## 十、重要提醒（对照作业要求）



1. **禁止外部知识**：不能在提示词中说“你应该使用微服务因为Netflix这么做”，必须引用HPS中的QA或CON。

2. **禁止few\-shot**：不能给模型提供例子输出。

3. **禁止任务重解释**：不能改变迭代目标（例如把“建立整体结构”改成“设计数据库”）。

4. **决策必须显式引用**：例如“根据QA\-1的性能要求（\<100ms），我选择事件驱动架构”。

5. **日志必须有时间戳**：每条请求的时间精确到分钟即可，但必须存在。

6. **源代码提交**：只需提交`.py`或`.ipynb`文件，不需要包含模型输出。

7. **报告为英文**：但允许少量语法错误，清晰即可。

    

## 十一、常见问题与解决方案（预判）



|可能问题|解决方案|
|---|---|
|模型输出不遵循Step 2→7顺序|在系统指令中强调“你必须先输出Step 2标题，再输出Step 3标题…”，并加入“如果跳过任何步骤，输出将无效”。|
|Mermaid代码无法渲染|提示词中要求“输出完整的Mermaid代码块，以\`\`\`mermaid开头和结尾”。|
|模型使用了外部知识（如推荐Redis）|在系统指令中加入“禁止提及任何非先验知识中的技术名，除非从约束CON\-2或CRN\-2中推导”。|
|迭代间依赖丢失（B不知道A输出了什么元素）|A在完成迭代1后，将Step 5中的元素表格复制给B；B在迭代2的user prompt中明确写上“基于你之前定义的X、Y、Z元素”。|
|时间不足|严格按照时间表执行，若某次迭代输出过长，可只保留关键部分（但必须包含Step 2\~7）。|



