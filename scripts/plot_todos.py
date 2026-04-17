import re
import matplotlib.pyplot as plt
from datetime import datetime

def parse_todo(filepath):
    """从 Markdown 中提取 TODO 项的优先级和难易度"""
    coord = dict()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # 匹配行首的 - [ ] 或 * [ ] 开头的任务行
            match = re.match(r'-\s\[\]\s(.*)', line)
            if not match:
                continue
            content = match.group(1)
            # 提取 priority 和 difficulty（支持多种写法）
            pri_match = re.search(r'priority=(\d+)', content, re.IGNORECASE)
            dif_match = re.search(r'difficulty=(\d+)', content, re.IGNORECASE)
            if pri_match and dif_match:
                pri = int(pri_match.group(1))
                dif = int(dif_match.group(1))
                if 0 <= pri <= 100 and 0 <= dif <= 100:
                    coord[(pri, dif)] = (coord[(pri, dif)] if (pri, dif) in coord.keys() else 0) + 1
    
    return list(coord.items())

def generate_scatter_plot(todos, output_path='./todos_scatter.png'):
    """生成散点图并保存"""
    plt.figure(figsize=(8, 8))
    x = [t[0][0] for t in todos]
    y = [t[0][1] for t in todos]
    labels = [f"count: {t[1]}" for t in todos]

    plt.scatter(x, y, c='blue', alpha=0.6)
    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]), fontsize=10)

    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xlabel('Priority (higher = more urgent)')
    plt.ylabel('Difficulty (higher = harder)')
    plt.title(f'TODO Scatter Plot - {datetime.now().strftime("%Y-%m-%d")}')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    todos = parse_todo('./TODO.md')
    if todos:
        generate_scatter_plot(todos)
        print(f"✅ 生成散点图，包含 {len(todos)} 个 TODO 项")
    else:
        print("⚠️ 未找到带有 priority 和 difficulty 的 TODO 项")
