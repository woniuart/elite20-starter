# C2S 产出物追踪器

> 用 Notion 追踪 C2S Challenge 四件产物进度的模板

## 文件结构

```
c2s-tracker/
├── notion-template/          # Notion 数据库结构定义
│   ├── 01-understanding.json
│   ├── 02-kstar.json
│   ├── 03-personal-grounding.json
│   └── 04-aar.json           # v0.2 新增执行轨迹字段
├── prompts/                  # AI 检查清单生成 prompt
│   └── checklist-generator.md
├── deploy_to_notion.py       # Notion API 部署脚本（需配置）
├── NOTION-DEPLOY-GUIDE.md    # 手动部署指南
└── README.md
```

## 四件产物

| 产物 | 名称 | 最低标准 |
|------|------|---------|
| ① | 论文理解 | 看过产物的人能区分哪里是论文讲的、哪里是你讲的 |
| ② | KSTAR 行动方案 | 评审教师读完后能说"下学期可以试着跑一下" |
| ③ | 个人联结 | 必须有具体的"你"——专业、名字、真实生活事实 |
| ④ | AAR 复盘 | AI 不知道你这 4 天具体发生了什么 |

## 使用方法

### 1. 创建 Notion 数据库

根据 `notion-template/` 中的 JSON 定义，在 Notion 中创建对应的数据库。

### 2. 生成检查清单

使用 `prompts/checklist-generator.md` 中的 prompt，让 AI 生成质量检查清单。

### 3. 追踪进度

在 Notion 中更新每个产物的状态，完成后 commit 到本仓库。

---

*创建于：2026年4月30日*
*版本：v0.2 执行轨迹版*

## 更新日志

### v0.2 执行轨迹版（2026年4月30日）
- ✅ AAR 数据库新增 6 个协作轨迹字段
  - AI模型：记录使用的 AI 模型
  - 对话轮次：记录对话往返次数
  - 关键提示词：记录最重要的 1-2 条提示词
  - AI输出摘要：记录 AI 输出的核心结论
  - 协作质量：评估 AI 协作的帮助程度
  - 对话时间：记录协作时间戳
- ✅ 检查清单新增 3 项协作轨迹相关检查项
- ✅ 新增 `NOTION-DEPLOY-GUIDE.md` 手动部署指南
- ✅ 新增 `deploy_to_notion.py` API 部署脚本
