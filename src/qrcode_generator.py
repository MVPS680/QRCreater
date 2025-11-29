#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码生成核心模块
支持多种内容类型和自定义选项
"""

import qrcode
from PIL import Image
from typing import Optional, Dict, Any


class QRCodeGenerator:
    """
    QR码生成器类
    支持多种内容类型和自定义选项
    """
    
    # 纠错级别映射
    ERROR_CORRECTION = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # 7%
        'M': qrcode.constants.ERROR_CORRECT_M,  # 15%
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # 25%
        'H': qrcode.constants.ERROR_CORRECT_H   # 30%
    }
    
    # 图片格式支持
    SUPPORTED_FORMATS = ['PNG', 'JPG', 'JPEG', 'BMP', 'GIF']
    
    def __init__(self):
        """初始化QR码生成器"""
        pass
    
    def generate_qr_code(self, content: str, content_type: str = 'text', 
                        size: int = 10, error_correction: str = 'M', 
                        box_size: int = 10, border: int = 4) -> Image.Image:
        """
        生成QR码图像
        
        Args:
            content: 要编码的内容
            content_type: 内容类型，支持'text', 'url', 'contact'
            size: QR码版本(1-40)，决定二维码大小
            error_correction: 纠错级别，支持'L', 'M', 'Q', 'H'
            box_size: 每个格子的像素大小
            border: 边框格子数
            
        Returns:
            PIL.Image.Image: 生成的QR码图像
            
        Raises:
            ValueError: 当参数无效时
        """
        # 验证参数
        if error_correction not in self.ERROR_CORRECTION:
            raise ValueError(f"无效的纠错级别: {error_correction}，支持{L, M, Q, H}")
        
        if size < 1 or size > 40:
            raise ValueError(f"无效的尺寸: {size}，支持1-40")
        
        # 格式化内容
        formatted_content = self._format_content(content, content_type)
        
        # 创建QR码对象
        qr = qrcode.QRCode(
            version=size,
            error_correction=self.ERROR_CORRECTION[error_correction],
            box_size=box_size,
            border=border,
        )
        
        # 添加内容
        qr.add_data(formatted_content)
        qr.make(fit=True)
        
        # 生成图像
        img = qr.make_image(fill_color="black", back_color="white")
        
        return img
    
    def save_qr_code(self, img: Image.Image, file_path: str, 
                    image_format: Optional[str] = None, 
                    quality: int = 90) -> None:
        """
        保存QR码图像到文件
        
        Args:
            img: 要保存的QR码图像
            file_path: 保存路径
            image_format: 图像格式，如'PNG', 'JPG'等
            quality: 图像质量(0-100)，仅对JPG等有损格式有效
            
        Raises:
            ValueError: 当图像格式不支持时
        """
        # 确定图像格式
        if not image_format:
            # 从文件扩展名推断格式
            image_format = file_path.split('.')[-1].upper()
        
        # 验证格式
        if image_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的图像格式: {image_format}，支持{self.SUPPORTED_FORMATS}")
        
        # 保存图像
        save_format = image_format
        if image_format == 'JPG':
            save_format = 'JPEG'
            
        if save_format in ['JPEG']:
            # 转换为RGB模式以支持JPG/JPEG
            img = img.convert('RGB')
            img.save(file_path, format=save_format, quality=quality)
        else:
            img.save(file_path, format=save_format)
    
    def _format_content(self, content: str, content_type: str) -> str:
        """
        根据内容类型格式化内容
        
        Args:
            content: 原始内容
            content_type: 内容类型
            
        Returns:
            str: 格式化后的内容
        """
        if content_type == 'url':
            # 确保URL格式正确
            if not content.startswith(('http://', 'https://')):
                content = f'http://{content}'
        elif content_type == 'contact':
            # 格式化为vCard格式
            content = f"BEGIN:VCARD\nVERSION:3.0\nFN:{content}\nEND:VCARD"
        
        return content
    
    def get_supported_formats(self) -> list:
        """
        获取支持的图像格式列表
        
        Returns:
            list: 支持的图像格式列表
        """
        return self.SUPPORTED_FORMATS.copy()
    
    def get_error_correction_levels(self) -> list:
        """
        获取支持的纠错级别列表
        
        Returns:
            list: 支持的纠错级别列表
        """
        return list(self.ERROR_CORRECTION.keys())
