#!/usr/bin/env python3
"""
Hermes Agent Core - 独立 Agent 框架
每个 Agent 有独立的工作空间、配置和日志
"""

import json
import os
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

AGENTS_ROOT = Path("/opt/data/agents")
SHARED_DIR = AGENTS_ROOT / "shared"
LOGS_DIR = AGENTS_ROOT / "logs"

class Agent:
    """独立 Agent 实例"""
    
    def __init__(self, name: str, workspace: str = None):
        self.name = name
        self.id = str(uuid.uuid4())[:8]
        self.workspace = Path(workspace) if workspace else AGENTS_ROOT / f"{name}_{self.id}"
        self.config_file = self.workspace / "config.json"
        self.log_file = LOGS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        # 创建工作空间
        self._init_workspace()
    
    def _init_workspace(self):
        """初始化 Agent 工作空间"""
        dirs = [
            self.workspace,
            self.workspace / "tasks",
            self.workspace / "output",
            self.workspace / "cache",
            self.workspace / "scripts",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
        
        # 默认配置
        default_config = {
            "name": self.name,
            "id": self.id,
            "created_at": datetime.now().isoformat(),
            "workspace": str(self.workspace),
            "capabilities": ["terminal", "file", "web"],
            "max_turns": 50,
            "log_level": "info",
        }
        
        if not self.config_file.exists():
            self.config_file.write_text(json.dumps(default_config, indent=2))
    
    def log(self, message: str, level: str = "info"):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level.upper()}] [{self.name}] {message}\n"
        
        # 写入 Agent 专属日志
        agent_log = self.workspace / "agent.log"
        with open(agent_log, "a") as f:
            f.write(log_entry)
        
        # 同时写入全局日志
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        
        print(log_entry, end="")
    
    def execute(self, command: str, timeout: int = 180) -> dict:
        """在 Agent 工作空间执行命令"""
        self.log(f"Executing: {command}")
        
        env = os.environ.copy()
        env["AGENT_NAME"] = self.name
        env["AGENT_WORKSPACE"] = str(self.workspace)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )
            
            output = {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command,
                "timestamp": datetime.now().isoformat(),
            }
            
            self.log(f"Command finished with code {result.returncode}")
            return output
            
        except subprocess.TimeoutExpired:
            self.log(f"Command timed out after {timeout}s", "error")
            return {"success": False, "error": "timeout", "command": command}
        except Exception as e:
            self.log(f"Command failed: {str(e)}", "error")
            return {"success": False, "error": str(e), "command": command}
    
    def write_file(self, path: str, content: str) -> bool:
        """在工作空间写入文件"""
        try:
            file_path = self.workspace / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            self.log(f"Written: {path}")
            return True
        except Exception as e:
            self.log(f"Failed to write {path}: {e}", "error")
            return False
    
    def read_file(self, path: str) -> str:
        """读取工作空间文件"""
        try:
            file_path = self.workspace / path
            return file_path.read_text()
        except Exception as e:
            self.log(f"Failed to read {path}: {e}", "error")
            return ""
    
    def status(self) -> dict:
        """获取 Agent 状态"""
        return {
            "name": self.name,
            "id": self.id,
            "workspace": str(self.workspace),
            "tasks_count": len(list((self.workspace / "tasks").glob("*"))),
            "output_count": len(list((self.workspace / "output").glob("*"))),
            "log_exists": (self.workspace / "agent.log").exists(),
        }

def create_agent(name: str, workspace: str = None) -> Agent:
    """创建新 Agent"""
    return Agent(name, workspace)

def list_agents() -> list:
    """列出所有 Agent"""
    agents = []
    for d in AGENTS_ROOT.iterdir():
        if d.is_dir() and d.name not in ["shared", "logs"]:
            config_file = d / "config.json"
            if config_file.exists():
                config = json.loads(config_file.read_text())
                agents.append(config)
    return agents

if __name__ == "__main__":
    # 测试
    agent = create_agent("test_agent")
    print(f"Created agent: {agent.name}")
    print(f"Workspace: {agent.workspace}")
    print(f"Status: {agent.status()}")
