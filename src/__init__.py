#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码生成器包
"""

from .qrcode_generator import QRCodeGenerator
from .gui import QRCodeGUI, create_gui

__version__ = "1.0.0"
__author__ = "QR Code Generator"
__all__ = ["QRCodeGenerator", "QRCodeGUI", "create_gui"]

# 延迟导入QRCodeDecoder，避免启动时加载pyzbar依赖
def __getattr__(name):
    if name == "QRCodeDecoder":
        from .qrcode_decoder import QRCodeDecoder
        return QRCodeDecoder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
