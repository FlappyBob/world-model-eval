#!/usr/bin/env python3
"""
任务数据准备工具

此脚本帮助创建符合 world-model-eval 要求的任务数据目录结构。
"""

import json
import shutil
from pathlib import Path
from PIL import Image
import numpy as np


def create_example_tasks(output_dir="./example_tasks"):
    """
    创建示例任务数据结构

    Args:
        output_dir: 输出目录路径
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    print(f"创建示例任务数据到: {output_path.absolute()}")
    print("=" * 60)

    # 定义示例任务
    tasks = [
        {
            "name": "pick_and_place",
            "trials": [
                {
                    "instruction": "place the red block on the blue plate",
                    "partial_credit_criteria": "Pick up the red block"
                },
                {
                    "instruction": "place the carrot on plate",
                    "partial_credit_criteria": "Pick up the carrot"
                },
                {
                    "instruction": "put the apple in the bowl",
                    "partial_credit_criteria": "Grasp the apple"
                }
            ]
        },
        {
            "name": "drawer_opening",
            "trials": [
                {
                    "instruction": "open the top drawer",
                    "partial_credit_criteria": "Grasp the drawer handle"
                },
                {
                    "instruction": "open the cabinet door",
                    "partial_credit_criteria": "Touch the cabinet handle"
                }
            ]
        },
        {
            "name": "stacking_blocks",
            "trials": [
                {
                    "instruction": "stack the blue block on top of the red block",
                    "partial_credit_criteria": "Pick up the blue block"
                },
                {
                    "instruction": "create a tower with three blocks",
                    "partial_credit_criteria": "Stack two blocks"
                }
            ]
        }
    ]

    total_trials = 0

    for task in tasks:
        task_dir = output_path / task["name"]
        task_dir.mkdir(exist_ok=True)

        print(f"\n任务: {task['name']}")
        print("-" * 60)

        for i, trial in enumerate(task["trials"]):
            trial_num = i + 1

            # 创建示例图片（256x256 的随机噪声图，模拟机器人场景）
            img_name = f"trial_{trial_num:03d}.png"
            json_name = f"trial_{trial_num:03d}.json"

            img_path = task_dir / img_name
            json_path = task_dir / json_name

            # 生成示例图片（实际使用时应该是真实的机器人场景图片）
            create_placeholder_image(img_path)

            # 创建 JSON 元数据
            metadata = {
                "instruction": trial["instruction"],
                "partial_credit_criteria": trial.get("partial_credit_criteria")
            }

            with open(json_path, "w") as f:
                json.dump(metadata, f, indent=2)

            print(f"  ✅ {img_name} + {json_name}")
            print(f"     指令: {trial['instruction']}")
            total_trials += 1

    print("\n" + "=" * 60)
    print(f"✅ 完成！共创建 {total_trials} 个试验，分布在 {len(tasks)} 个任务中")
    print(f"📂 输出目录: {output_path.absolute()}")
    print(f"\n使用方法:")
    print(f"  /venv/worldgym/bin/world-model-eval-openvla \\")
    print(f"    --root-dir {output_path.absolute()} \\")
    print(f"    --checkpoint-path /path/to/checkpoint.pt \\")
    print(f"    --model-name openvla-7b")

    return output_path


def create_placeholder_image(img_path, size=(256, 256)):
    """
    创建占位符图片

    实际使用时，应该用真实的机器人场景初始帧替换这些图片。
    """
    # 创建一个渐变图片作为示例
    img_array = np.zeros((size[1], size[0], 3), dtype=np.uint8)

    # 添加一些渐变色
    for y in range(size[1]):
        for x in range(size[0]):
            img_array[y, x] = [
                int(x / size[0] * 255),  # R
                int(y / size[1] * 255),  # G
                128                       # B
            ]

    img = Image.fromarray(img_array)
    img.save(img_path)


def validate_task_directory(root_dir):
    """
    验证任务目录是否符合格式要求

    Args:
        root_dir: 任务根目录

    Returns:
        bool: 是否通过验证
    """
    root_path = Path(root_dir)

    if not root_path.exists():
        print(f"❌ 目录不存在: {root_path}")
        return False

    print(f"验证任务目录: {root_path.absolute()}")
    print("=" * 60)

    png_files = list(root_path.rglob("*.png"))

    if not png_files:
        print("❌ 未找到任何 PNG 文件")
        return False

    print(f"找到 {len(png_files)} 个 PNG 文件")

    valid_trials = 0
    issues = []

    for png in png_files:
        task_dir = png.parent
        base = png.stem
        json_path = task_dir / f"{base}.json"

        # 检查 JSON 文件是否存在
        if not json_path.exists():
            issues.append(f"❌ 缺少 JSON: {png.relative_to(root_path)}")
            continue

        # 检查 JSON 内容
        try:
            with open(json_path, 'r') as f:
                metadata = json.load(f)

            if "instruction" not in metadata or not metadata["instruction"]:
                issues.append(f"❌ 缺少 instruction: {json_path.relative_to(root_path)}")
                continue

            valid_trials += 1
            print(f"✅ {png.relative_to(root_path)}")
            print(f"   指令: {metadata['instruction']}")
            if "partial_credit_criteria" in metadata:
                print(f"   部分成功: {metadata['partial_credit_criteria']}")

        except json.JSONDecodeError as e:
            issues.append(f"❌ 无效的 JSON: {json_path.relative_to(root_path)} - {e}")
            continue
        except Exception as e:
            issues.append(f"❌ 错误: {json_path.relative_to(root_path)} - {e}")
            continue

    print("\n" + "=" * 60)

    if issues:
        print("\n⚠️  发现以下问题:")
        for issue in issues:
            print(f"  {issue}")

    print(f"\n总结: {valid_trials}/{len(png_files)} 个有效试验")

    return valid_trials > 0 and len(issues) == 0


def create_task_from_images(image_dir, output_dir, task_name, default_instruction):
    """
    从现有图片目录创建任务数据

    Args:
        image_dir: 包含 PNG 图片的目录
        output_dir: 输出目录
        task_name: 任务名称
        default_instruction: 默认指令（如果未提供会使用此值）
    """
    image_path = Path(image_dir)
    output_path = Path(output_dir)
    task_dir = output_path / task_name
    task_dir.mkdir(exist_ok=True, parents=True)

    png_files = sorted(image_path.glob("*.png"))

    if not png_files:
        print(f"❌ 在 {image_dir} 中未找到 PNG 文件")
        return

    print(f"从 {len(png_files)} 张图片创建任务数据...")

    for i, png in enumerate(png_files):
        new_name = f"trial_{i+1:03d}"
        new_png = task_dir / f"{new_name}.png"
        new_json = task_dir / f"{new_name}.json"

        # 复制图片
        shutil.copy(png, new_png)

        # 创建 JSON
        metadata = {
            "instruction": default_instruction,
            "partial_credit_criteria": None  # 可以手动编辑添加
        }

        with open(new_json, 'w') as f:
            json.dump(metadata, f, indent=2)

        print(f"  ✅ {new_name}.png + {new_name}.json")

    print(f"\n✅ 完成！任务保存到: {task_dir.absolute()}")
    print(f"💡 提示: 请手动编辑 JSON 文件以自定义每个试验的指令")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "create":
            # 创建示例数据
            output_dir = sys.argv[2] if len(sys.argv) > 2 else "./example_tasks"
            create_example_tasks(output_dir)

        elif command == "validate":
            # 验证现有目录
            if len(sys.argv) < 3:
                print("用法: python prepare_tasks.py validate <task_directory>")
                sys.exit(1)
            validate_task_directory(sys.argv[2])

        elif command == "from-images":
            # 从图片创建任务
            if len(sys.argv) < 5:
                print("用法: python prepare_tasks.py from-images <image_dir> <output_dir> <task_name> [instruction]")
                sys.exit(1)
            image_dir = sys.argv[2]
            output_dir = sys.argv[3]
            task_name = sys.argv[4]
            instruction = sys.argv[5] if len(sys.argv) > 5 else "complete the task"
            create_task_from_images(image_dir, output_dir, task_name, instruction)

        else:
            print(f"未知命令: {command}")
            print("可用命令: create, validate, from-images")

    else:
        # 默认：创建示例数据
        print("WorldGym 任务数据准备工具")
        print("=" * 60)
        print("\n用法:")
        print("  1. 创建示例数据:")
        print("     python prepare_tasks.py create [output_dir]")
        print("\n  2. 验证任务目录:")
        print("     python prepare_tasks.py validate <task_directory>")
        print("\n  3. 从现有图片创建任务:")
        print("     python prepare_tasks.py from-images <image_dir> <output_dir> <task_name> [instruction]")
        print("\n默认执行: 创建示例数据到 ./example_tasks")
        print("=" * 60)
        print()

        create_example_tasks()
