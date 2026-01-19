#!/usr/bin/env python3
"""
从 Bridge V2 数据准备评估任务

此脚本从 put_carrot_on_plate.json 下载图片并创建符合评估格式的任务数据。
"""

import json
import urllib.request
from pathlib import Path
from PIL import Image
from io import BytesIO
from tqdm import tqdm
import sys


def download_bridge_data(json_path, output_dir, max_trials=None):
    """
    从 Bridge V2 JSON 文件下载数据并创建评估任务

    Args:
        json_path: put_carrot_on_plate.json 文件路径
        output_dir: 输出目录
        max_trials: 最多下载的试验数量（None 表示全部）
    """
    print(f"读取 Bridge V2 数据: {json_path}")

    # 读取 JSON 数据
    with open(json_path, 'r') as f:
        trials_data = json.load(f)

    total_trials = len(trials_data)
    if max_trials:
        trials_data = trials_data[:max_trials]
        print(f"限制为前 {max_trials} 个试验（共 {total_trials} 个）")
    else:
        print(f"共 {total_trials} 个试验")

    # 创建输出目录
    output_path = Path(output_dir)
    task_dir = output_path / "put_carrot_on_plate"
    task_dir.mkdir(exist_ok=True, parents=True)

    print(f"\n下载图片到: {task_dir.absolute()}")
    print("=" * 60)

    successful = 0
    failed = []

    for i, trial in enumerate(tqdm(trials_data, desc="下载试验数据")):
        trial_num = i + 1
        img_url = trial["im_0_path"]
        instruction = trial["instruction"]
        subtasks = trial.get("subtasks", [])

        # 文件名
        png_name = f"trial_{trial_num:03d}.png"
        json_name = f"trial_{trial_num:03d}.json"
        png_path = task_dir / png_name
        json_path = task_dir / json_name

        # 跳过已存在的文件
        if png_path.exists() and json_path.exists():
            successful += 1
            continue

        try:
            with urllib.request.urlopen(img_url, timeout=30) as response:
                img_data = response.read()

            img = Image.open(BytesIO(img_data))

            if img.mode != 'RGB':
                img = img.convert('RGB')

            img.save(png_path)
            partial_criteria = subtasks[0] if subtasks else None

            metadata = {
                "instruction": instruction,
                "partial_credit_criteria": partial_criteria,
                "source": "bridge_v2",
                "original_url": img_url
            }

            with open(json_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            successful += 1

        except Exception as e:
            failed.append({
                "trial": trial_num,
                "url": img_url,
                "error": str(e)
            })
            tqdm.write(f"❌ 试验 {trial_num} 失败: {e}")

    print("\n" + "=" * 60)
    print(f"✅ 成功: {successful}/{len(trials_data)}")

    if failed:
        print(f"❌ 失败: {len(failed)}")
        print("\n失败的试验:")
        for item in failed[:5]:  # 只显示前5个
            print(f"  - 试验 {item['trial']}: {item['error']}")
        if len(failed) > 5:
            print(f"  ... 还有 {len(failed) - 5} 个失败")

    print(f"\n📂 任务数据保存到: {task_dir.absolute()}")

    return task_dir


def download_with_retry(url, max_retries=3):
    """
    带重试的下载函数

    Args:
        url: 图片 URL
        max_retries: 最大重试次数

    Returns:
        PIL.Image: 下载的图片
    """
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                img_data = response.read()
            return Image.open(BytesIO(img_data))
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            continue


def validate_bridge_data(task_dir):
    """
    验证下载的 Bridge 数据

    Args:
        task_dir: 任务目录路径
    """
    from prepare_tasks import validate_task_directory

    print("\n验证下载的数据...")
    print("=" * 60)
    validate_task_directory(task_dir)


if __name__ == "__main__":
    # 默认参数
    json_file = "src/world_model_eval/put_carrot_on_plate.json"
    output_dir = "./bridge_tasks"
    max_trials = None  # 下载全部

    # 解析命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Bridge V2 数据准备工具")
            print("=" * 60)
            print("\n用法:")
            print("  python prepare_bridge_data.py [output_dir] [max_trials]")
            print("\n参数:")
            print("  output_dir   - 输出目录（默认: ./bridge_tasks）")
            print("  max_trials   - 最多下载的试验数量（默认: 全部）")
            print("\n示例:")
            print("  # 下载全部数据到默认目录")
            print("  python prepare_bridge_data.py")
            print("\n  # 下载到自定义目录")
            print("  python prepare_bridge_data.py /path/to/output")
            print("\n  # 只下载前10个试验（用于快速测试）")
            print("  python prepare_bridge_data.py ./bridge_tasks 10")
            sys.exit(0)

        output_dir = sys.argv[1]

    if len(sys.argv) > 2:
        max_trials = int(sys.argv[2])

    print("=" * 60)
    print("Bridge V2 数据准备工具")
    print("=" * 60)
    print(f"\n配置:")
    print(f"  输入文件: {json_file}")
    print(f"  输出目录: {output_dir}")
    print(f"  试验数量: {'全部' if max_trials is None else max_trials}")
    print()

    # 检查输入文件
    if not Path(json_file).exists():
        print(f"❌ 错误: 未找到文件 {json_file}")
        sys.exit(1)

    # 下载数据
    try:
        task_dir = download_bridge_data(json_file, output_dir, max_trials)

        # 验证数据
        validate_bridge_data(task_dir)

        print("\n" + "=" * 60)
        print("✅ 完成！")
        print("\n使用方法:")
        print(f"  /venv/worldgym/bin/world-model-eval-openvla \\")
        print(f"    --root-dir {Path(output_dir).absolute()} \\")
        print(f"    --checkpoint-path /path/to/checkpoint.pt \\")
        print(f"    --model-name openvla-7b \\")
        print(f"    --save-video --video-out-dir ./rollouts/openvla")

    except KeyboardInterrupt:
        print("\n\n⚠️  下载被中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
