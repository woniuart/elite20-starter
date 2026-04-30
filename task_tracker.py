#!/usr/bin/env python3
"""
AI+X 学习任务助手
帮助管理AI+X学习和GitHub提交任务
"""
import json
from datetime import datetime

class TaskTracker:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title, description, status="pending"):
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "status": status,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        return task
    
    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                return task
        return None
    
    def list_tasks(self, status=None):
        if status:
            return [t for t in self.tasks if t["status"] == status]
        return self.tasks
    
    def to_json(self):
        return json.dumps(self.tasks, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    tracker = TaskTracker()
    
    # 添加示例任务
    tracker.add_task("完成GitHub仓库fork", "fork elite20启动仓库", "completed")
    tracker.add_task("阅读技能文档", "学习GitHub PR工作流", "completed")
    tracker.add_task("创建学习总结", "整理K-STAR闭环学习成果", "in_progress")
    
    print("=== AI+X 学习任务追踪 ===")
    for task in tracker.list_tasks():
        status_icon = "✅" if task["status"] == "completed" else "🔄" if task["status"] == "in_progress" else "📋"
        print(f"{status_icon} [{task['id']}] {task['title']} - {task['status']}")
    
    print("\nJSON输出:")
    print(tracker.to_json())
