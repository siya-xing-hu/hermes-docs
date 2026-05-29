# Hermes Agent 系统

> 轻量级独立 Agent 框架，每个 Agent 拥有独立的工作空间、配置和日志。

---

## 🏗️ 架构

```
/opt/data/agents/
├── agent_core.py          # Agent 核心类
├── agent_cli.py           # 命令行工具
├── README.md              # 本文档
├── shared/                # 共享资源
├── logs/                  # 全局日志
├── coder_xxxx/            # Agent: coder
│   ├── config.json        # Agent 配置
│   ├── agent.log          # Agent 专属日志
│   ├── tasks/             # 任务目录
│   ├── output/            # 输出目录
│   ├── cache/             # 缓存目录
│   └── scripts/           # 脚本目录
└── researcher_xxxx/       # Agent: researcher
    └── ...
```

---

## 🚀 快速开始

### 1. 创建 Agent

```bash
agent create <name> [--workspace /custom/path]
```

示例：
```bash
agent create coder
agent create researcher --workspace /mnt/data/research
```

### 2. 列出所有 Agent

```bash
agent list
```

### 3. 查看 Agent 状态

```bash
agent status <name>
```

### 4. 在 Agent 工作空间执行命令

```bash
agent run <name> -- <command>
```

示例：
```bash
agent run coder -- "python3 script.py"
agent run researcher -- "curl -s https://api.example.com/data > output/data.json"
```

### 5. 查看日志

```bash
agent logs <name> [--tail 20]
```

---

## 📋 Agent 特性

| 特性 | 说明 |
|------|------|
| **独立工作空间** | 每个 Agent 有自己的目录，互不干扰 |
| **环境隔离** | 执行命令时设置 `AGENT_NAME` 和 `AGENT_WORKSPACE` 环境变量 |
| **自动日志** | 所有操作自动记录到 `agent.log` 和全局日志 |
| **配置持久化** | 每个 Agent 有独立的 `config.json` |
| **命令超时** | 默认 180 秒，可自定义 |

---

## 🔧 高级用法

### 在 Python 中使用

```python
from agent_core import create_agent, list_agents

# 创建 Agent
agent = create_agent("my_agent")

# 执行命令
result = agent.execute("ls -la", timeout=30)
print(result["stdout"])

# 读写文件
agent.write_file("notes.txt", "Hello World")
content = agent.read_file("notes.txt")

# 查看状态
print(agent.status())
```

### 自定义配置

编辑 Agent 的 `config.json`：

```json
{
  "name": "coder",
  "id": "246d3431",
  "capabilities": ["terminal", "file", "web"],
  "max_turns": 50,
  "log_level": "debug"
}
```

---

## 📝 与 hermes-docs 集成

Agent 的工作记录可以同步到 `hermes-docs` 仓库：

```bash
# 将 Agent 输出复制到 hermes-docs
agent run coder -- "cp output/report.md /opt/data/hermes-docs/logs/"
```

---

*创建时间：2026-05-29*
