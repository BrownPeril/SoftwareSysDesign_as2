# 成员 C 全流程指南

## 一、角色与职责概述

| 角色 | 负责迭代 | 具体任务 | 预估时间 |
|------|----------|----------|----------|
| **C** | 迭代 4 | ① 执行迭代 4（依赖迭代 3 输出）② 收集 A、B 的日志，合并为完整对话日志 ③ 按附录模板撰写报告（含 ADD 步骤输出、Mermaid 图、成本表、反思、贡献表）④ 最终提交 | 90 min |

---

## 二、时间安排

| 时间段 | 成员 C 行动 |
|--------|-------------|
| 0:00 - 0:15 | ✅ **已完成**：获取 API key，配置环境，准备报告模板框架 |
| 0:15 - 0:45 | ✅ **已完成**：搭建报告框架（标题、表格、章节结构）→ `report_template.md` |
| 0:45 - 1:15 | ✅ **已完成**：编写 Python 调用脚本 → `hps_add_script.py`、日志合并脚本 → `merge_logs.py` |
| 1:15 - 1:45 | 将迭代 1 结果填入报告（等待 A 交付 `log_iter1.txt`） |
| 1:45 - 2:15 | 将迭代 2 结果填入报告（等待 B 交付 `log_iter2.txt`） |
| 2:15 - 2:45 | **执行迭代 4**（运行 `hps_add_script.py 4`）→ 合并所有日志（运行 `merge_logs.py`）→ 填入报告全部内容 |
| 2:45 - 3:00 | 三人一起复核：Mermaid 图、日志时间戳、报告格式，提交至 Moodle |

---

## 三、迭代 4 执行指南

### 3.1 前提条件

- [✅] **Python 调用脚本已就绪**：`hps_add_script.py`（含完整先验知识、system prompt、全部 4 次迭代，API key 已配置）
- [✅] **日志合并脚本已就绪**：`merge_logs.py`
- [✅] **报告模板框架已就绪**：`report_template.md`
- [ ] 从成员 B 处获取迭代 3 的输出文件 `log_iter3.txt`
- [ ] 确认已安装 Python 依赖：`pip install openai`
- [✅] **API key 已配置**：已填入 `hps_add_script.py`（优先读取环境变量 `API_KEY`，默认使用已配置的 key）

### 3.2 Python 调用脚本

✅ **已完成**：完整脚本已保存在 `hps_add_script.py`（详见下方路径）。

该脚本已包含：
- 完整的先验知识（ADD 3.0 七步骤 + HPS 全部用例/质量属性/关注点/约束）
- Role Prompt（7 条约束规则）
- 全部 4 次迭代的 User Prompt
- 自动时间戳日志记录 + Token usage 记录
- 支持单次运行 `python hps_add_script.py 4` 或全跑 `python hps_add_script.py all`

> 如果成员 A 提供了不同的脚本，可用 A 的版本替换。当前脚本作为独立备用方案已就绪。

### 3.3 迭代 4 的 User Prompt

```text
Based on all previous iterations (especially the elements defined in iterations 1-3 for the Hotel Price System), now address development and operations.

Iteration Goal: Addressing Development and Operations.

Drivers: CRN-2 (Java/Angular/Kafka knowledge), CRN-3 (team work allocation), CRN-5 (continuous deployment infrastructure). Also CON-4 (6 months delivery, MVP in 2 months) and CON-3 (Git platform).

Step 2: State the iteration goal and select the above drivers. Explain why these drivers are selected for this iteration.

Step 3: Choose specific elements from the previous iterations' architecture that need refinement to support development and operations. Name them explicitly (e.g., build/deployment pipeline, module organization for team allocation).

Step 4: Select design concepts: Git branching strategy, CI/CD pipeline (e.g., Jenkins/GitHub Actions), containerization (Docker), environment promotion. Compare at least two alternatives for CI/CD and branching strategy based on team familiarity (CRN-2) and time constraints (CON-4). Select one and justify with explicit references.

Step 5: Instantiate development-related elements. Use a table with columns: Element Name, Responsibility, Properties. Define:
  - Version control repository structure (branches, tags)
  - CI jobs (build, test, lint, deploy stages)
  - Deployment environments (dev, staging, prod)
  - Module-to-team assignments

Step 6: Draw a development view or work assignment view using Mermaid code block. Show:
  - CI/CD pipeline stages
  - Modules assigned to teams (Frontend team, Backend team, DevOps team)
  - Environment promotion flow (dev → staging → prod)

Step 7: Analyze whether the design supports MVP in 2 months and full release in 6 months (CON-4). Discuss how the design avoids technical debt and enables team parallelism.
```

### 3.4 执行命令

在终端中运行：

```bash
cd e:\SE3-2\SE-Arch\assignment\2
python hps_add_script.py 4
```

> `hps_add_script.py` 已存储在此目录下，可直接使用。

### 3.5 执行后检查清单

- [ ] `log_iter4.txt` 已生成
- [ ] 日志包含时间戳
- [ ] 日志包含完整的 System Prompt
- [ ] 日志包含完整的 User Prompt
- [ ] 日志包含完整的 Assistant Response
- [ ] Assistant Response 包含 Step 2 → Step 7
- [ ] Step 6 包含有效的 Mermaid 代码块
- [ ] 如果有 token usage 信息，已记录

---

## 四、日志收集与合并

### 4.1 收集文件清单

从各成员处收集以下文件：

| 文件 | 来源 | 状态确认 |
|------|------|----------|
| `log_iter1.txt` | 成员 A | □ 已获取 |
| `log_iter2.txt` | 成员 B | □ 已获取 |
| `log_iter3.txt` | 成员 B | □ 已获取 |
| `log_iter4.txt` | 自己生成 | □ 已生成 |

### 4.2 合并为完整对话日志

✅ **合并脚本已就绪**：`merge_logs.py` 已保存在此目录下。

直接运行：

```bash
python merge_logs.py
```

> 该脚本会自动按顺序合并 `log_iter1.txt` ~ `log_iter4.txt`，输出 `conversation_log.txt`，包含文件头、时间戳、迭代分隔线。

### 4.3 时间戳验证

确认每个日志文件的第一行时间戳格式正确，且顺序为：

```
log_iter1.txt  →  log_iter2.txt  →  log_iter3.txt  →  log_iter4.txt
```

---

## 五、报告撰写指南

### 5.1 报告结构（按附录模板，不超过 30 页）

✅ **报告模板已就绪**：`report_template.md` 已保存在此目录下，包含以下完整结构，只需填入内容即可。

#### 封面
- 课程名：Software Architecture
- 作业名：Assignment 2 - Attribute Driven Design
- 小组成员：A、B、C 的姓名
- 日期：提交日期
- 所选方式：Direct LLM interaction + gemini-3.1-pro-preview

#### ADD Step 1（全局输入回顾）
用列表形式展示所有输入：
- 6 个用例（HPS-1 ~ HPS-6）
- 9 个质量属性（QA-1 ~ QA-9）
- 5 个架构关注点（CRN-1 ~ CRN-5）
- 6 个约束（CON-1 ~ CON-6）
- 说明：成熟领域的绿地系统

#### 迭代 1 输出
从 `log_iter1.txt` 中提取 Assistant Response 的 Step 2 ~ Step 7：
- 复制每个步骤的文本内容
- 确保 Mermaid 代码块正确渲染（在 Markdown 预览中检查）
- 可以重新排版，但内容必须一致

#### 迭代 2 输出
从 `log_iter2.txt` 中提取，同上。

#### 迭代 3 输出
从 `log_iter3.txt` 中提取，同上。

#### 迭代 4 输出
从 `log_iter4.txt` 中提取，同上。

#### 交互成本分析表

| The way of completing the assignment | The LLM used | Number of Human Interactions (turns) | Token Consumption (K tokens) |
|--------------------------------------|--------------|-------------------------------------|------------------------------|
| Direct LLM interaction | gemini-3.1-pro-preview | 4 | 从各日志的 token usage 累加 |

> 如果日志中没有 token usage 信息，填写 "N/A" 并注明原因。

#### Individual Reflection（每人一段）

**成员 A 的反思方向**：
- 编写 Python 调用脚本时遇到的问题
- 准备先验知识文本的要点
- 模型输出不遵循步骤时如何通过强化 prompt 解决
- 迭代 1 中确保 Mermaid 图正确生成的经验

**成员 B 的反思方向**：
- 如何确保迭代 2 和迭代 3 之间的依赖关系
- 手动复制前次迭代输出的元素名的方法
- 处理质量属性（QA-2, QA-3）时的挑战
- 如何验证模型的决策是否合理引用先验知识

**成员 C 的反思方向**：
- 报告整合中如何保证 4 次迭代的一致性
- 日志合并时如何处理格式差异
- 执行迭代 4 时如何确保与前面迭代的输出衔接
- 最终复核时发现的常见问题

#### 贡献表

| Name (Chinese) | Contributions |
|----------------|---------------|
| 成员A姓名 | 编写调用脚本，准备先验知识，执行迭代1，生成Mermaid图 |
| 成员B姓名 | 执行迭代2和迭代3，处理质量属性，收集日志 |
| 成员C姓名 | 执行迭代4，整合报告，完成成本分析和反思 |

### 5.2 Mermaid 图检查要点

| 迭代 | 视图类型 | 检查要点 |
|------|----------|----------|
| 迭代 1 | 模块分解图 | 包含前端、后端、数据库、外部 CMS 等模块，连线正确 |
| 迭代 2 | C&C 图 | 展示 Price Change Controller、Query API、CMS 适配器等组件间的交互 |
| 迭代 3 | 部署图 | 展示云节点、负载均衡器、应用实例主备、数据库主从 |
| 迭代 4 | 开发视图 | 展示 CI/CD 流水线阶段、模块与团队映射、环境晋升流程 |

在每个 Mermaid 代码块前后检查：
- [ ] 以 ` ```mermaid ` 开头
- [ ] 以 ` ``` ` 结尾
- [ ] 在 Markdown 预览中能正确渲染
- [ ] 节点关系清晰，文本不重叠

### 5.3 报告格式规范

- 使用英文撰写（允许少量语法错误）
- PDF 输出，不超过 30 页
- 使用清晰的章节编号
- Mermaid 图建议截图嵌入（如果直接渲染有问题）
- 字体建议：11-12pt，行距 1.15-1.5

---

## 六、最终提交检查清单

### 6.1 源代码提交

- [✅] ~~提交完整的 `.py` 文件（或 `.ipynb`）~~ → `hps_add_script.py` **已就绪**
- [✅] ~~文件包含 4 次迭代的调用代码~~ → **已包含**
- [✅] ~~API key 可配置（建议从环境变量读取）~~ → `os.environ.get("API_KEY")` **已实现**
- [✅] ~~代码包含自动时间戳日志功能~~ → `call_llm()` 函数 **已实现**

### 6.2 日志文件

- [✅] ~~日志合并脚本~~ → `merge_logs.py` **已就绪**
- [ ] `log_iter1.txt` — 等待 A 交付
- [ ] `log_iter2.txt` — 等待 B 交付
- [ ] `log_iter3.txt` — 等待 B 交付
- [ ] `log_iter4.txt` — 运行 `python hps_add_script.py 4` 生成
- [ ] `conversation_log.txt` — 运行 `python merge_logs.py` 生成

### 6.3 报告（PDF）

- [✅] ~~报告模板框架~~ → `report_template.md` **已就绪**（含封面、Step 1、迭代 1~4 占位、成本表、反思、贡献表）
- [ ] 封面信息完整（成员姓名已填入模板）
- [ ] ADD Step 1 全局输入回顾（模板中已列出全部内容）
- [ ] 迭代 1 ~ 4 的输出（Step 2 ~ 7）
- [ ] 每个迭代的 Mermaid 图正确渲染
- [ ] 交互成本分析表（待 API 返回 token usage 后填入）
- [ ] 三人 Individual Reflection
- [ ] 贡献表（成员姓名已填入模板）
- [ ] 不超过 30 页

### 6.4 合规检查

- [ ] 没有外部领域知识（没有 Redis、Netflix 等非先验知识中的内容）
- [ ] 没有 few-shot 示例
- [ ] 没有任务重解释
- [ ] 决策都有显式引用（"根据 QA-X"、"根据 CON-X"）
- [ ] 所有视图使用 Mermaid
- [ ] 日志包含时间戳

---

## 七、常见问题与解决方案

| 可能问题 | 解决方案 |
|----------|----------|
| 模型输出不遵循 Step 2 → 7 顺序 | 在 system prompt 中强调"必须严格按照顺序输出"，并在 user prompt 中再次强调 |
| Mermaid 代码无法渲染 | 检查是否有非法字符；在 https://mermaid.live/ 中测试代码 |
| 模型使用了外部知识 | 在后续 prompt 中指出"请不要使用先验知识中未包含的技术" |
| 迭代 3 的输出中元素名称与迭代 2 不一致 | 手动修正名称以保持一致，或在迭代 4 的 prompt 中明确指定元素名 |
| 各成员的日志格式略有差异 | 在合并时统一格式（如统一时间戳格式、分隔符等） |
| API 调用失败 | 检查 API key、base URL 是否正确，网络是否通畅 |
| 时间不足 | 优先保证日志和报告核心内容，Mermaid 图可以在报告中使用截图替代 |