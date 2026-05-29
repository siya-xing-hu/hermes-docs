# Hermes 工作流程规范

## 🎯 核心理念

Hermes 作为你的 AI 助手，通过 GitHub Issues 接收你的指令和建议。
我不会主动轮询，而是通过**定时任务**每天检查一次。

---

## 📅 定时任务

**执行时间**：每天下午 5:00（17:00）
**任务内容**：拉取最新代码 → 检查 open issues → 处理带 `auto` 标签的 issue

---

## 🏷️ Issue 标签约定

| 标签 | 含义 | 行为 |
|------|------|------|
| `auto` | 自动处理 | 定时任务会自动完成并关闭 issue |
| `manual` | 等待手动确认 | 我会读取但不主动执行，等你下次会话明确指示 |
| `discuss` | 讨论中 | 不会自动处理，等你和我对齐方向 |
| 无标签 | 默认 | 跳过，等下次手动处理 |

---

## 📝 Issue 类型与处理方式

### 1. 更新工作规范
**触发关键词**（title 包含）：`规范`、`guideline`、`规则`、`rule`、`更新 readme`、`文档`
**处理**：在 `guidelines/YYYY-MM-DD-update.md` 创建文件，记录新规范

### 2. 添加工作日志
**触发关键词**（title 包含）：`日志`、`log`、`记录`、`工作记录`
**处理**：追加到 `logs/YYYY-MM/YYYY-MM-DD.md`

### 3. 通用任务
**其他所有 issue**
**处理**：记录到 `tasks/issue-{number}.md`

---

## ✍️ 如何给我提 Issue（示例）

### 示例 1：建议改进工作方式
```
Title: 规范：每次推送代码前先运行测试
Labels: auto

Body:
以后每次自动提交代码前，需要先确保：
1. 代码语法无误
2. 关键功能可运行
```

### 示例 2：记录今天的工作
```
Title: 工作日志：研究了 GitHub Actions
Labels: auto

Body:
今天讨论了如何使用 GitHub Actions 替代 cron job...
```

### 示例 3：需要讨论的想法
```
Title: 想法：是否引入 issue 优先级机制
Labels: discuss

Body:
有些 issue 比较紧急，是否需要 P0/P1/P2 标签？
```

---

## 📁 仓库结构

```
hermes-docs/
├── README.md                       # 项目说明
├── guidelines/                     # 工作规范（由 issue 更新）
│   └── YYYY-MM-DD-update.md
├── logs/                           # 工作日志（按月归档）
│   └── YYYY-MM/
│       └── YYYY-MM-DD.md
├── tasks/                          # 任务记录
│   └── issue-{N}.md
└── workflow.md                     # 本文件
```

---

## 🔄 处理流程

```
1. 你创建 issue → 加 auto 标签
   ↓
2. 17:00 定时任务触发
   ↓
3. Hermes 拉取最新代码
   ↓
4. 评论 "🤖 开始处理..."
   ↓
5. 根据 issue 类型生成对应文件
   ↓
6. git commit + push
   ↓
7. 评论 "✅ 处理完成" 并关闭 issue
   ↓
8. Telegram 通知你结果
```

---

## 🛠️ 技术细节

- **脚本位置**：`/opt/data/home/scripts/hermes-issue-processor.py`
- **Cron Job ID**：`a86bf63dd39f`
- **认证方式**：
  - Git 操作：SSH Deploy Key（`~/.ssh/id_ed25519`）
  - API 调用：Personal Access Token（`~/.hermes-secrets/github_token`）
- **触发频率**：每天 17:00

---

## 🚨 失败处理

如果某个 issue 处理失败：
- Issue 不会被关闭
- 会在 issue 下评论错误信息
- Telegram 会收到通知，你可以手动指示我重试

---

*最后更新：2026-05-29*
