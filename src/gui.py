#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI界面模块
使用tkinter构建QR码生成器的用户界面
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from typing import Optional

from .qrcode_generator import QRCodeGenerator
from .utils import validate_file_path, get_default_file_name, handle_error


class QRCodeGUI:
    """
    QR码生成器GUI类
    使用tkinter构建用户界面
    """
    
    def __init__(self, root: tk.Tk):
        """
        初始化GUI
        
        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.generator = QRCodeGenerator()
        self.current_image = None
        
        # 配置窗口
        self._setup_window()
        
        # 创建组件
        self._create_widgets()
        
        # 布局组件
        self._layout_widgets()
        
        # 绑定事件
        self._bind_events()
    
    def _setup_window(self) -> None:
        """配置窗口属性"""
        self.root.title("QR码生成器 MVP&TraeSOLO")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
        
        # 设置图标（如果有）
        # self._set_icon()
    
    def _set_icon(self) -> None:
        """设置窗口图标"""
        try:
            # 尝试加载图标
            pass
        except Exception as e:
            handle_error(e, "设置窗口图标")
    
    def _create_widgets(self) -> None:
        """创建界面组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # 左侧控制面板
        self.control_panel = ttk.LabelFrame(self.main_frame, text="控制面板", padding="10")
        
        # 内容类型选择
        self.content_type_frame = ttk.Frame(self.control_panel)
        ttk.Label(self.content_type_frame, text="内容类型:").pack(side=tk.LEFT, padx=(0, 10))
        self.content_type_var = tk.StringVar(value="text")
        self.content_type_combobox = ttk.Combobox(
            self.content_type_frame,
            textvariable=self.content_type_var,
            values=["text", "url", "contact"],
            state="readonly"
        )
        self.content_type_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 内容输入
        self.content_frame = ttk.Frame(self.control_panel)
        ttk.Label(self.content_frame, text="内容:").pack(anchor=tk.W)
        self.content_text = tk.Text(self.content_frame, height=5, width=40)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # 选项设置
        self.options_frame = ttk.LabelFrame(self.control_panel, text="选项设置", padding="10")
        
        # 尺寸设置
        self.size_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.size_frame, text="尺寸(1-40):").pack(side=tk.LEFT, padx=(0, 10))
        self.size_var = tk.IntVar(value=10)
        self.size_spinbox = ttk.Spinbox(
            self.size_frame,
            from_=1, to=40,
            textvariable=self.size_var,
            width=5
        )
        self.size_spinbox.pack(side=tk.LEFT)
        
        # 纠错级别
        self.ec_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.ec_frame, text="纠错级别:").pack(side=tk.LEFT, padx=(0, 10))
        self.ec_var = tk.StringVar(value="M")
        self.ec_combobox = ttk.Combobox(
            self.ec_frame,
            textvariable=self.ec_var,
            values=["L", "M", "Q", "H"],
            state="readonly",
            width=5
        )
        self.ec_combobox.pack(side=tk.LEFT)
        
        # 边框大小
        self.border_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.border_frame, text="边框大小:").pack(side=tk.LEFT, padx=(0, 10))
        self.border_var = tk.IntVar(value=4)
        self.border_spinbox = ttk.Spinbox(
            self.border_frame,
            from_=1, to=10,
            textvariable=self.border_var,
            width=5
        )
        self.border_spinbox.pack(side=tk.LEFT)
        
        # 格子大小
        self.box_size_frame = ttk.Frame(self.options_frame)
        ttk.Label(self.box_size_frame, text="格子大小:").pack(side=tk.LEFT, padx=(0, 10))
        self.box_size_var = tk.IntVar(value=10)
        self.box_size_spinbox = ttk.Spinbox(
            self.box_size_frame,
            from_=1, to=20,
            textvariable=self.box_size_var,
            width=5
        )
        self.box_size_spinbox.pack(side=tk.LEFT)
        
        # 生成按钮
        self.generate_button = ttk.Button(
            self.control_panel,
            text="生成QR码",
            command=self.generate_qr_code
        )
        
        # 右侧预览面板
        self.preview_panel = ttk.LabelFrame(self.main_frame, text="预览", padding="10")
        
        # 预览画布
        self.preview_canvas = tk.Canvas(self.preview_panel, width=300, height=300, bg="white")
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 保存按钮
        self.save_button = ttk.Button(
            self.preview_panel,
            text="保存QR码",
            command=self.save_qr_code
        )
        self.save_button.pack(pady=(10, 0))
    
    def _layout_widgets(self) -> None:
        """布局界面组件"""
        # 主框架布局
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧控制面板布局
        self.control_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 内容类型布局
        self.content_type_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 内容输入布局
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 选项设置布局
        self.options_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.size_frame.pack(fill=tk.X, pady=(0, 5))
        self.ec_frame.pack(fill=tk.X, pady=(0, 5))
        self.border_frame.pack(fill=tk.X, pady=(0, 5))
        self.box_size_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 生成按钮布局
        self.generate_button.pack(fill=tk.X)
        
        # 右侧预览面板布局
        self.preview_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def _bind_events(self) -> None:
        """绑定事件"""
        # 内容变化时自动生成
        self.content_text.bind("<KeyRelease>", self._on_content_change)
        
        # 选项变化时自动生成
        self.content_type_var.trace_add("write", self._on_option_change)
        self.size_var.trace_add("write", self._on_option_change)
        self.ec_var.trace_add("write", self._on_option_change)
        self.border_var.trace_add("write", self._on_option_change)
        self.box_size_var.trace_add("write", self._on_option_change)
        
        # 回车键生成
        self.content_text.bind("<Control-Return>", lambda e: self.generate_qr_code())
    
    def _on_content_change(self, event: tk.Event) -> None:
        """内容变化事件处理"""
        self.generate_qr_code()
    
    def _on_option_change(self, *args) -> None:
        """选项变化事件处理"""
        self.generate_qr_code()
    
    def generate_qr_code(self) -> None:
        """生成QR码并显示预览"""
        try:
            # 获取内容
            content = self.content_text.get("1.0", tk.END).strip()
            if not content:
                self._clear_preview()
                return
            
            # 获取选项
            content_type = self.content_type_var.get()
            size = self.size_var.get()
            error_correction = self.ec_var.get()
            border = self.border_var.get()
            box_size = self.box_size_var.get()
            
            # 生成QR码
            self.current_image = self.generator.generate_qr_code(
                content=content,
                content_type=content_type,
                size=size,
                error_correction=error_correction,
                border=border,
                box_size=box_size
            )
            
            # 显示预览
            self._update_preview()
            
        except Exception as e:
            handle_error(e, "生成QR码")
            messagebox.showerror("错误", f"生成QR码失败: {e}")
            self._clear_preview()
    
    def _update_preview(self) -> None:
        """更新预览显示"""
        if not self.current_image:
            return
        
        # 获取画布尺寸
        canvas_width = self.preview_canvas.winfo_width()
        canvas_height = self.preview_canvas.winfo_height()
        
        # 调整图像大小以适应画布
        img = self.current_image.copy()
        img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        # 转换为PhotoImage
        self.photo = ImageTk.PhotoImage(img)
        
        # 清除画布并显示图像
        self.preview_canvas.delete("all")
        
        # 计算居中位置
        x = (canvas_width - self.photo.width()) // 2
        y = (canvas_height - self.photo.height()) // 2
        
        # 显示图像
        self.preview_canvas.create_image(x, y, anchor=tk.NW, image=self.photo)
    
    def _clear_preview(self) -> None:
        """清除预览"""
        self.preview_canvas.delete("all")
        self.current_image = None
    
    def save_qr_code(self) -> None:
        """保存QR码到文件"""
        if not self.current_image:
            messagebox.showwarning("警告", "请先生成QR码")
            return
        
        try:
            # 获取内容
            content = self.content_text.get("1.0", tk.END).strip()
            content_type = self.content_type_var.get()
            
            # 生成默认文件名
            default_name = get_default_file_name(content, content_type)
            
            # 打开文件对话框
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=default_name,
                filetypes=[
                    ("PNG文件", "*.png"),
                    ("JPG文件", "*.jpg;*.jpeg"),
                    ("BMP文件", "*.bmp"),
                    ("GIF文件", "*.gif"),
                    ("所有文件", "*.*")
                ],
                title="保存QR码"
            )
            
            if file_path:
                # 验证文件路径
                validate_file_path(file_path)
                
                # 保存文件
                self.generator.save_qr_code(self.current_image, file_path)
                
                messagebox.showinfo("成功", f"QR码已保存到: {file_path}")
                
        except Exception as e:
            handle_error(e, "保存QR码")
            messagebox.showerror("错误", f"保存QR码失败: {e}")
    
    def run(self) -> None:
        """运行GUI程序"""
        self.root.mainloop()


def create_gui() -> None:
    """创建并运行GUI"""
    root = tk.Tk()
    app = QRCodeGUI(root)
    app.run()
