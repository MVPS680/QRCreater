#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR码生成器包
"""

from .qrcode_generator import QRCodeGenerator
from .qrcode_decoder import QRCodeDecoder
from .gui import QRCodeGUI, create_gui

__version__ = "1.0.0"
__author__ = "QR Code Generator"
__all__ = ["QRCodeGenerator", "QRCodeDecoder", "QRCodeGUI", "create_gui"]
