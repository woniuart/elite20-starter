# projects/art-education/scripts/generate-knowledge-card.py
import anthropic
import os
import json

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def generate_knowledge_card(artwork_name):
    """
    作为大学艺术通识课教师，为指定艺术作品生成知识点卡片
    """
    prompt = f"""
    作为大学艺术通识课资深教师，为"{artwork_name}"生成一份符合《美术鉴赏》课程标准的知识点卡片。
    
    严格按照以下格式输出（使用中文）：
    
    ## {artwork_name}
    - 作者：
    - 年代：
    - 流派：
    - 核心知识点：
      1. 
      2. 
      3. 
      4. 
      5. 
    - 美育思政切入点：
      1. 
    - 课堂讨论题：
      1. 
      2. 
    """
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1500,
        system="你是一位有10年教学经验的大学艺术通识课教师，擅长将复杂的艺术概念用通俗易懂的方式讲解给学生。",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text


def generate_batch(artworks):
    """批量生成知识点卡片"""
    results = []
    for artwork in artworks:
        print(f"正在生成: {artwork}...")
        try:
            card = generate_knowledge_card(artwork)
            results.append({"artwork": artwork, "card": card})
            print(f"✓ {artwork} 完成")
        except Exception as e:
            print(f"✗ {artwork} 失败: {e}")
            results.append({"artwork": artwork, "card": None, "error": str(e)})
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="美术鉴赏知识点卡片生成器")
    parser.add_argument("artwork", nargs="?", help="作品名称")
    parser.add_argument("--batch", "-b", help="批量模式，传入JSON文件路径")
    parser.add_argument("--output", "-o", default="outputs/", help="输出目录")
    
    args = parser.parse_args()
    
    if args.batch:
        # 批量模式
        with open(args.batch, "r", encoding="utf-8") as f:
            artworks = json.load(f)
        results = generate_batch(artworks)
        
        # 保存结果
        os.makedirs(args.output, exist_ok=True)
        for r in results:
            if r["card"]:
                filename = f"{args.output}{r['artwork'].replace(' ', '_')}_知识点卡片.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(r["card"])
        print(f"\n批量生成完成！共 {len([r for r in results if r['card']])}/{len(results)} 个")
    
    elif args.artwork:
        # 单个作品模式
        card = generate_knowledge_card(args.artwork)
        print(card)
        
        # 保存到文件
        os.makedirs(args.output, exist_ok=True)
        filename = f"{args.output}{args.artwork.replace(' ', '_')}_知识点卡片.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(card)
        print(f"\n已保存到: {filename}")
    
    else:
        # 交互模式
        artwork = input("请输入作品名称：")
        card = generate_knowledge_card(artwork)
        print(card)
        
        # 保存到文件
        os.makedirs(args.output, exist_ok=True)
        filename = f"{args.output}{artwork.replace(' ', '_')}_知识点卡片.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(card)
        print(f"\n已保存到: {filename}")
