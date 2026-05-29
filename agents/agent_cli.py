#!/usr/bin/env python3
"""
Agent CLI - 管理独立 Agent 的命令行工具
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, "/opt/data/agents")
from agent_core import Agent, create_agent, list_agents, AGENTS_ROOT

def cmd_create(args):
    """创建新 Agent"""
    workspace = args.workspace or None
    agent = create_agent(args.name, workspace)
    print(f"✅ Agent '{agent.name}' 创建成功")
    print(f"   ID: {agent.id}")
    print(f"   工作空间: {agent.workspace}")
    print(f"   配置: {agent.config_file}")

def cmd_list(args):
    """列出所有 Agent"""
    agents = list_agents()
    if not agents:
        print("暂无 Agent")
        return
    
    print(f"{'名称':<20} {'ID':<10} {'创建时间':<25} {'工作空间'}")
    print("-" * 80)
    for a in agents:
        print(f"{a['name']:<20} {a['id']:<10} {a['created_at']:<25} {a['workspace']}")

def cmd_status(args):
    """查看 Agent 状态"""
    agents = list_agents()
    target = next((a for a in agents if a["name"] == args.name), None)
    
    if not target:
        print(f"❌ Agent '{args.name}' 不存在")
        return
    
    agent = Agent(args.name, target["workspace"])
    status = agent.status()
    
    print(f"📊 Agent: {status['name']}")
    print(f"   ID: {status['id']}")
    print(f"   工作空间: {status['workspace']}")
    print(f"   任务数: {status['tasks_count']}")
    print(f"   输出数: {status['output_count']}")
    print(f"   日志: {'✅' if status['log_exists'] else '❌'}")

def cmd_run(args):
    """在 Agent 工作空间执行命令"""
    agents = list_agents()
    target = next((a for a in agents if a["name"] == args.name), None)
    
    if not target:
        print(f"❌ Agent '{args.name}' 不存在")
        return
    
    agent = Agent(args.name, target["workspace"])
    # 将命令列表拼接成完整字符串
    command_parts = getattr(args, 'cmd', [])
    if isinstance(command_parts, list):
        command = " ".join(command_parts)
    else:
        command = str(command_parts)
    result = agent.execute(command, timeout=args.timeout)
    
    print(f"\n{'='*60}")
    print(f"命令: {result['command']}")
    print(f"返回码: {result['returncode']}")
    print(f"{'='*60}")
    
    if result.get('stdout'):
        print("\n📤 STDOUT:")
        print(result['stdout'])
    
    if result.get('stderr'):
        print("\n📥 STDERR:")
        print(result['stderr'])
    
    if result.get('error'):
        print(f"\n❌ 错误: {result['error']}")

def cmd_logs(args):
    """查看 Agent 日志"""
    agents = list_agents()
    target = next((a for a in agents if a["name"] == args.name), None)
    
    if not target:
        print(f"❌ Agent '{args.name}' 不存在")
        return
    
    agent = Agent(args.name, target["workspace"])
    log_file = agent.workspace / "agent.log"
    
    if not log_file.exists():
        print("暂无日志")
        return
    
    lines = log_file.read_text().strip().split('\n')
    
    if args.tail:
        lines = lines[-args.tail:]
    
    for line in lines:
        print(line)

def main():
    parser = argparse.ArgumentParser(description="Agent 管理工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # create
    create_parser = subparsers.add_parser("create", help="创建新 Agent")
    create_parser.add_argument("name", help="Agent 名称")
    create_parser.add_argument("--workspace", help="自定义工作空间路径")
    
    # list
    subparsers.add_parser("list", help="列出所有 Agent")
    
    # status
    status_parser = subparsers.add_parser("status", help="查看 Agent 状态")
    status_parser.add_argument("name", help="Agent 名称")
    
    # run
    run_parser = subparsers.add_parser("run", help="在 Agent 工作空间执行命令")
    run_parser.add_argument("name", help="Agent 名称")
    run_parser.add_argument("--timeout", type=int, default=180, help="超时时间(秒)")
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="要执行的命令（放在最后，如: agent run coder -- echo hello）")
    
    # logs
    logs_parser = subparsers.add_parser("logs", help="查看 Agent 日志")
    logs_parser.add_argument("name", help="Agent 名称")
    logs_parser.add_argument("--tail", type=int, help="显示最后 N 行")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 确保根目录存在
    AGENTS_ROOT.mkdir(parents=True, exist_ok=True)
    
    # 路由命令
    commands = {
        "create": cmd_create,
        "list": cmd_list,
        "status": cmd_status,
        "run": cmd_run,
        "logs": cmd_logs,
    }
    
    commands[args.command](args)

if __name__ == "__main__":
    main()
