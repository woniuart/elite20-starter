"""
Notion 模板部署脚本
将 c2s-tracker JSON 模板导入到 Notion 工作区

使用方法:
1. 在 https://www.notion.so/my-integrations 创建集成
2. 获取 Internal Integration Token
3. 在 Notion 中创建一个父级页面（用于存放数据库）
4. 复制页面 URL，获取页面 ID
5. 设置环境变量或直接修改下方配置
6. 运行脚本: python deploy_to_notion.py

依赖安装: pip install notion-client python-dotenv
"""

import json
import os
from notion_client import NotionClient
from dotenv import load_dotenv

# ============ 配置区域 ============
# 方式1: 环境变量
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "your-integration-token-here")
PARENT_PAGE_ID = os.getenv("NOTION_PAGE_ID", "your-page-id-here")

# 模板文件路径
TEMPLATE_DIR = "notion-template"

# 字段类型映射 (JSON schema type -> Notion property type)
TYPE_MAPPING = {
    "title": "title",
    "text": "rich_text",
    "select": "select",
    "number": "number",
    "date": "date",
    "checkbox": "checkbox",
    "url": "url",
    "email": "email",
    "phone_number": "phone_number"
}
# ==================================


def load_template(filename):
    """加载 JSON 模板文件"""
    with open(os.path.join(TEMPLATE_DIR, filename), 'r', encoding='utf-8') as f:
        return json.load(f)


def build_properties(template):
    """将 JSON 模板转换为 Notion 数据库属性"""
    properties = {}
    
    for prop_name, prop_config in template["properties"].items():
        prop_type = prop_config["type"]
        notion_type = TYPE_MAPPING.get(prop_type, "rich_text")
        
        if notion_type == "select":
            properties[prop_name] = {
                "select": {
                    "options": [
                        {"name": opt} for opt in prop_config.get("options", [])
                    ]
                }
            }
        elif notion_type == "number":
            # 检查是否是百分比格式
            if prop_config.get("format") == "percent":
                properties[prop_name] = {
                    "number": {"format": "percent"}
                }
            else:
                properties[prop_name] = {
                    "number": {"format": "number"}
                }
        else:
            properties[prop_name] = {
                notion_type: {}
            }
    
    return properties


def create_database(client, parent_id, template):
    """创建 Notion 数据库"""
    database_body = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": [
            {
                "type": "text",
                "text": {"content": template["name"]}
            }
        ],
        "description": template.get("description", ""),
        "properties": build_properties(template),
        "is_inline": True
    }
    
    return client.databases.create(**database_body)


def main():
    print("🚀 开始部署 C2S 产出物追踪模板到 Notion...\n")
    
    # 验证配置
    if NOTION_TOKEN == "your-integration-token-here":
        print("❌ 错误: 请设置 NOTION_TOKEN 环境变量")
        print("   在 https://www.notion.so/my-integrations 创建集成并获取 Token")
        return
    
    if PARENT_PAGE_ID == "your-page-id-here":
        print("❌ 错误: 请设置 NOTION_PAGE_ID 环境变量")
        print("   创建一个 Notion 页面，复制页面 URL 中的 32 位 ID")
        return
    
    # 初始化 Notion 客户端
    client = NotionClient(auth=NOTION_TOKEN)
    
    # 模板文件列表
    templates = [
        "01-understanding.json",
        "02-kstar.json",
        "03-personal-grounding.json",
        "04-aar.json"
    ]
    
    created_databases = []
    
    for i, template_file in enumerate(templates, 1):
        try:
            print(f"📦 [{i}/4] 正在创建: {template_file.replace('.json', '')}...")
            
            template = load_template(template_file)
            database = create_database(client, PARENT_PAGE_ID, template)
            
            db_id = database["id"]
            created_databases.append({
                "name": template["name"],
                "id": db_id,
                "url": f"https://notion.so/{db_id.replace('-', '')}"
            })
            
            print(f"   ✅ 创建成功! Database ID: {db_id}\n")
            
        except Exception as e:
            print(f"   ❌ 创建失败: {str(e)}\n")
    
    # 输出汇总
    print("\n" + "="*50)
    print("📊 部署完成!")
    print("="*50)
    
    for db in created_databases:
        print(f"\n✅ {db['name']}")
        print(f"   ID: {db['id']}")
        print(f"   URL: {db['url']}")
    
    print("\n💡 下一步:")
    print("   1. 在 Notion 中打开上述链接")
    print("   2. 将数据库添加到您的工作区")
    print("   3. 分享数据库给您的集成")
    print("   4. 开始追踪您的 C2S Challenge 产出物!")


if __name__ == "__main__":
    main()
