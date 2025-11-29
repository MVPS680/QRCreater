#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码生成器主程序入口
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui import create_gui
from src.utils import handle_error


def main() -> None:
    """
    主程序入口
    """
    try:
        # 启动GUI应用
        create_gui()
    except KeyboardInterrupt:
        print("\n程序已中断")
        sys.exit(0)
    except Exception as e:
        handle_error(e, "启动程序")
        print(f"程序启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
