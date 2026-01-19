#!/usr/bin/env python3
"""验证 WorldGym 环境安装是否正确"""

import sys

def check_import(module_name, display_name=None):
    """检查模块是否可以导入"""
    if display_name is None:
        display_name = module_name

    try:
        module = __import__(module_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"✅ {display_name}: {version}")
        return True
    except ImportError as e:
        print(f"❌ {display_name}: Not found ({e})")
        return False

def main():
    print("=" * 60)
    print("WorldGym Environment Verification")
    print("=" * 60)
    print()

    # 检查 Python 版本
    print(f"Python version: {sys.version}")
    print()

    # 核心包
    print("Core Packages:")
    print("-" * 60)
    all_good = True

    all_good &= check_import('world_model_eval', 'world-model-eval')
    all_good &= check_import('torch', 'PyTorch')
    all_good &= check_import('torchvision')
    all_good &= check_import('diffusers')
    all_good &= check_import('accelerate')
    print()

    # OpenVLA & SpatialVLA
    print("OpenVLA & SpatialVLA Packages:")
    print("-" * 60)
    all_good &= check_import('transformers')
    all_good &= check_import('timm')
    all_good &= check_import('scipy')
    print()

    # Octo
    print("Octo Packages:")
    print("-" * 60)
    all_good &= check_import('jax')
    all_good &= check_import('jaxlib')
    all_good &= check_import('flax')
    all_good &= check_import('tensorflow')
    all_good &= check_import('optax')
    all_good &= check_import('chex')
    all_good &= check_import('gym')

    try:
        import octo
        print(f"✅ octo: installed")
    except ImportError:
        print(f"❌ octo: Not found")
        all_good = False
    print()

    # CUDA 检查
    print("CUDA Support:")
    print("-" * 60)
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.version.cuda}")
            print(f"   GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            print("⚠️  CUDA not available")
            all_good = False
    except Exception as e:
        print(f"❌ Error checking CUDA: {e}")
        all_good = False
    print()

    # JAX CUDA 检查
    print("JAX CUDA Support:")
    print("-" * 60)
    try:
        import jax
        devices = jax.devices()
        print(f"✅ JAX devices: {devices}")
        if any('gpu' in str(d).lower() or 'cuda' in str(d).lower() for d in devices):
            print("   CUDA support: ✅")
        else:
            print("   CUDA support: ⚠️  No GPU devices found")
    except Exception as e:
        print(f"❌ Error checking JAX devices: {e}")
    print()

    # 总结
    print("=" * 60)
    if all_good:
        print("✅ All checks passed! Environment is ready.")
    else:
        print("⚠️  Some checks failed. Please review the output above.")
    print("=" * 60)

    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
