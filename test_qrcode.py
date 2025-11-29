#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码生成器测试脚本
测试核心功能是否正常工作
"""

import os
import sys
from src.qrcode_generator import QRCodeGenerator


def test_qrcode_generation():
    """测试QR码生成功能"""
    print("=== 测试QR码生成功能 ===")
    
    generator = QRCodeGenerator()
    
    # 测试文本内容
    print("1. 测试文本内容...")
    try:
        img = generator.generate_qr_code("Hello, QR Code!")
        print("   ✓ 文本QR码生成成功")
    except Exception as e:
        print(f"   ✗ 文本QR码生成失败: {e}")
        return False
    
    # 测试URL内容
    print("2. 测试URL内容...")
    try:
        img = generator.generate_qr_code("www.example.com", content_type="url")
        print("   ✓ URL QR码生成成功")
    except Exception as e:
        print(f"   ✗ URL QR码生成失败: {e}")
        return False
    
    # 测试联系人内容
    print("3. 测试联系人内容...")
    try:
        img = generator.generate_qr_code("张三", content_type="contact")
        print("   ✓ 联系人QR码生成成功")
    except Exception as e:
        print(f"   ✗ 联系人QR码生成失败: {e}")
        return False
    
    # 测试不同纠错级别
    print("4. 测试不同纠错级别...")
    for ec in ["L", "M", "Q", "H"]:
        try:
            img = generator.generate_qr_code("Test", error_correction=ec)
            print(f"   ✓ 纠错级别 {ec} 测试成功")
        except Exception as e:
            print(f"   ✗ 纠错级别 {ec} 测试失败: {e}")
            return False
    
    # 测试不同尺寸
    print("5. 测试不同尺寸...")
    for size in [1, 10, 20, 40]:
        try:
            img = generator.generate_qr_code("Test", size=size)
            print(f"   ✓ 尺寸 {size} 测试成功")
        except Exception as e:
            print(f"   ✗ 尺寸 {size} 测试失败: {e}")
            return False
    
    return True


def test_qrcode_saving():
    """测试QR码保存功能"""
    print("\n=== 测试QR码保存功能 ===")
    
    generator = QRCodeGenerator()
    img = generator.generate_qr_code("Test Save")
    
    # 创建测试目录
    test_dir = "test_output"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # 测试不同格式保存
    formats = ["PNG", "JPG", "BMP", "GIF"]
    for fmt in formats:
        print(f"1. 测试保存为{fmt}格式...")
        try:
            file_path = os.path.join(test_dir, f"test.{fmt.lower()}")
            generator.save_qr_code(img, file_path)
            if os.path.exists(file_path):
                print(f"   ✓ {fmt}格式保存成功")
                # 清理测试文件
                os.remove(file_path)
            else:
                print(f"   ✗ {fmt}格式保存失败: 文件未创建")
                return False
        except Exception as e:
            print(f"   ✗ {fmt}格式保存失败: {e}")
            return False
    
    # 清理测试目录
    os.rmdir(test_dir)
    
    return True


def main():
    """主测试函数"""
    print("开始测试QR码生成器...\n")
    
    # 运行测试
    test1_passed = test_qrcode_generation()
    test2_passed = test_qrcode_saving()
    
    print("\n=== 测试结果 ===")
    if test1_passed and test2_passed:
        print("✓ 所有测试通过！QR码生成器功能正常。")
        return 0
    else:
        print("✗ 部分测试失败，请检查代码。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
