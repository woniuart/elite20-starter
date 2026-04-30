# 脚本目录

存放用于生成艺术教学内容的自动化脚本。

## 使用方法

### 环境准备
```bash
pip install anthropic
export ANTHROPIC_API_KEY="your-api-key"
```

### 单个作品生成
```bash
python scripts/generate-knowledge-card.py "蒙娜丽莎"
```

### 批量生成
```bash
# 创建作品列表文件 artworks.json
# ["蒙娜丽莎", "星空", "最后的晚餐"]
python scripts/generate-knowledge-card.py --batch artworks.json
```

### 参数说明
- `artwork`: 艺术作品名称
- `--batch`: 批量模式，输入JSON文件
- `--output`: 输出目录（默认 outputs/）
