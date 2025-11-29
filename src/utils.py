#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
包含文件操作、内容格式化和错误处理等功能
"""

import os
import logging
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qrcode_generator.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def validate_file_path(file_path: str) -> str:
    """
    验证文件路径，确保目录存在
    
    Args:
        file_path: 完整文件路径
        
    Returns:
        str: 验证后的文件路径
        
    Raises:
        OSError: 当目录创建失败时
    """
    # 获取目录路径
    dir_path = os.path.dirname(file_path)
    
    # 如果目录不存在则创建
    if dir_path and not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"创建目录: {dir_path}")
        except OSError as e:
            logger.error(f"创建目录失败: {e}")
            raise
    
    return file_path


def get_default_file_name(content: str, content_type: str) -> str:
    """
    生成默认文件名
    
    Args:
        content: 内容
        content_type: 内容类型
        
    Returns:
        str: 默认文件名
    """
    # 截取内容前20个字符作为文件名
    if len(content) > 20:
        base_name = content[:20] + '...'
    else:
        base_name = content
    
    # 替换特殊字符
    base_name = base_name.replace(' ', '_').replace('/', '_').replace('\\', '_')
    
    return f"qrcode_{content_type}_{base_name}.png"


def format_contact_info(name: str, phone: Optional[str] = None, 
                        email: Optional[str] = None) -> str:
    """
    格式化联系人信息为vCard格式
    
    Args:
        name: 联系人姓名
        phone: 电话号码
        email: 电子邮件
        
    Returns:
        str: 格式化后的vCard字符串
    """
    vcard = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{name}"
    ]
    
    if phone:
        vcard.append(f"TEL:{phone}")
    
    if email:
        vcard.append(f"EMAIL:{email}")
    
    vcard.append("END:VCARD")
    
    return '\n'.join(vcard)


def handle_error(error: Exception, context: str) -> None:
    """
    统一错误处理函数
    
    Args:
        error: 异常对象
        context: 错误上下文
    """
    logger.error(f"{context} 错误: {error}", exc_info=True)


def get_file_extension(file_path: str) -> str:
    """
    获取文件扩展名
    
    Args:
        file_path: 文件路径
        
    Returns:
        str: 文件扩展名（小写）
    """
    return os.path.splitext(file_path)[1].lower().lstrip('.')


def is_supported_image_format(file_path: str, supported_formats: list) -> bool:
    """
    检查文件格式是否支持
    
    Args:
        file_path: 文件路径
        supported_formats: 支持的格式列表
        
    Returns:
        bool: 是否支持
    """
    ext = get_file_extension(file_path).upper()
    return ext in supported_formats
