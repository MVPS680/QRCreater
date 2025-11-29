#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码解码核心模块
支持从本地图片和网络图片解码
"""

from pyzbar.pyzbar import decode
from PIL import Image
from typing import List, Dict, Any, Optional
import requests
from io import BytesIO


class QRCodeDecoder:
    """
    QR码解码器类
    支持从本地图片和网络图片解码
    """
    
    def decode_from_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        从本地图片文件解码QR码
        
        Args:
            file_path: 本地图片文件路径
            
        Returns:
            List[Dict[str, Any]]: 解码结果列表，每个结果包含类型和数据
            
        Raises:
            FileNotFoundError: 当文件不存在时
            ValueError: 当文件不是有效的图片时
        """
        try:
            # 打开图片
            img = Image.open(file_path)
            
            # 解码QR码
            results = self._decode_image(img)
            
            return results
        except FileNotFoundError:
            raise
        except Exception as e:
            raise ValueError(f"无法解码图片: {e}")
    
    def decode_from_url(self, url: str) -> List[Dict[str, Any]]:
        """
        从网络图片URL解码QR码
        
        Args:
            url: 网络图片URL
            
        Returns:
            List[Dict[str, Any]]: 解码结果列表，每个结果包含类型和数据
            
        Raises:
            requests.exceptions.RequestException: 当网络请求失败时
            ValueError: 当URL不是有效的图片时
        """
        try:
            # 发送网络请求获取图片
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # 从响应中读取图片
            img = Image.open(BytesIO(response.content))
            
            # 解码QR码
            results = self._decode_image(img)
            
            return results
        except requests.exceptions.RequestException as e:
            raise
        except Exception as e:
            raise ValueError(f"无法解码网络图片: {e}")
    
    def decode_from_image(self, img: Image.Image) -> List[Dict[str, Any]]:
        """
        从PIL Image对象解码QR码
        
        Args:
            img: PIL Image对象
            
        Returns:
            List[Dict[str, Any]]: 解码结果列表，每个结果包含类型和数据
        """
        return self._decode_image(img)
    
    def _decode_image(self, img: Image.Image) -> List[Dict[str, Any]]:
        """
        内部方法：从Image对象解码QR码
        
        Args:
            img: PIL Image对象
            
        Returns:
            List[Dict[str, Any]]: 解码结果列表，每个结果包含类型和数据
        """
        # 确保图片是RGB模式
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 使用pyzbar解码
        decoded_objects = decode(img)
        
        # 格式化结果
        results = []
        for obj in decoded_objects:
            result = {
                'type': obj.type,
                'data': obj.data.decode('utf-8'),
                'rect': {
                    'left': obj.rect.left,
                    'top': obj.rect.top,
                    'width': obj.rect.width,
                    'height': obj.rect.height
                },
                'polygon': [{'x': point.x, 'y': point.y} for point in obj.polygon]
            }
            results.append(result)
        
        return results
