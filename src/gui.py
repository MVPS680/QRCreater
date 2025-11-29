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
from .qrcode_decoder import QRCodeDecoder
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
        self.decoder = QRCodeDecoder()
        self.current_image = None
        self.decoded_results = []
        
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
        
        # 创建标签页控件
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # ------------------------ 生成标签页 ------------------------
        self.generate_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.generate_tab, text="生成")
        
        # 生成标签页的左侧控制面板
        self.control_panel = ttk.LabelFrame(self.generate_tab, text="控制面板", padding="10")
        
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
        
        # 生成标签页的右侧预览面板
        self.preview_panel = ttk.LabelFrame(self.generate_tab, text="预览", padding="10")
        
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
        
        # ------------------------ 解码标签页 ------------------------
        self.decode_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.decode_tab, text="解码")
        
        # 解码标签页的左侧控制面板
        self.decode_control_panel = ttk.LabelFrame(self.decode_tab, text="解码选项", padding="10")
        
        # 解码方式选择
        self.decode_method_frame = ttk.Frame(self.decode_control_panel)
        ttk.Label(self.decode_method_frame, text="解码方式:").pack(side=tk.LEFT, padx=(0, 10))
        self.decode_method_var = tk.StringVar(value="file")
        self.decode_method_combobox = ttk.Combobox(
            self.decode_method_frame,
            textvariable=self.decode_method_var,
            values=["file", "url"],
            state="readonly"
        )
        self.decode_method_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 文件选择区域
        self.file_select_frame = ttk.Frame(self.decode_control_panel)
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_select_frame, textvariable=self.file_path_var, state="readonly")
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.browse_button = ttk.Button(self.file_select_frame, text="浏览", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT)
        
        # URL输入区域
        self.url_frame = ttk.Frame(self.decode_control_panel)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(self.url_frame, textvariable=self.url_var)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.url_entry.pack_forget()  # 初始隐藏
        
        # 解码按钮
        self.decode_button = ttk.Button(
            self.decode_control_panel,
            text="解码QR码",
            command=self.decode_qr_code
        )
        
        # 解码标签页的右侧结果面板
        self.decode_result_panel = ttk.LabelFrame(self.decode_tab, text="结果", padding="10")
        
        # 解码预览画布
        self.decode_preview_canvas = tk.Canvas(self.decode_result_panel, width=300, height=300, bg="white")
        self.decode_preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 解码结果文本框
        self.result_text = tk.Text(self.decode_result_panel, height=10, width=40, state="disabled")
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
    
    def _layout_widgets(self) -> None:
        """布局界面组件"""
        # 主框架布局
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标签页布局
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # ------------------------ 生成标签页布局 ------------------------
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
        
        # ------------------------ 解码标签页布局 ------------------------
        # 左侧解码控制面板布局
        self.decode_control_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 解码方式布局
        self.decode_method_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 文件选择布局
        self.file_select_frame.pack(fill=tk.X, pady=(0, 10))
        
        # URL输入布局
        self.url_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 解码按钮布局
        self.decode_button.pack(fill=tk.X)
        
        # 右侧结果面板布局
        self.decode_result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def _bind_events(self) -> None:
        """绑定事件"""
        # 生成标签页事件绑定
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
        
        # 解码标签页事件绑定
        # 解码方式变化时切换界面
        self.decode_method_var.trace_add("write", self._on_decode_method_change)
    
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
    
    def _on_decode_method_change(self, *args) -> None:
        """
        解码方式变化事件处理
        """
        method = self.decode_method_var.get()
        if method == "file":
            # 显示文件选择区域，隐藏URL输入区域
            self.file_select_frame.pack(fill=tk.X, pady=(0, 10))
            self.url_frame.pack_forget()
        else:
            # 显示URL输入区域，隐藏文件选择区域
            self.url_frame.pack(fill=tk.X, pady=(0, 10))
            self.file_select_frame.pack_forget()
    
    def browse_file(self) -> None:
        """
        浏览文件并选择要解码的图片
        """
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                ("所有文件", "*.*")
            ],
            title="选择要解码的QR码图片"
        )
        if file_path:
            self.file_path_var.set(file_path)
    
    def decode_qr_code(self) -> None:
        """
        解码QR码并显示结果
        """
        try:
            method = self.decode_method_var.get()
            img = None
            
            # 根据解码方式获取图片
            if method == "file":
                file_path = self.file_path_var.get()
                if not file_path:
                    messagebox.showwarning("警告", "请先选择要解码的图片文件")
                    return
                
                # 解码本地文件
                results = self.decoder.decode_from_file(file_path)
                img = Image.open(file_path)
            else:
                url = self.url_var.get().strip()
                if not url:
                    messagebox.showwarning("警告", "请先输入图片URL")
                    return
                
                # 解码网络图片
                results = self.decoder.decode_from_url(url)
                
                # 获取图片用于预览
                import requests
                from io import BytesIO
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content))
            
            # 显示预览
            self._update_decode_preview(img)
            
            # 显示解码结果
            self._display_decode_results(results)
            
        except Exception as e:
            handle_error(e, "解码QR码")
            messagebox.showerror("错误", f"解码失败: {e}")
            self._clear_decode_preview()
            self._display_decode_results([])
    
    def _update_decode_preview(self, img: Image.Image) -> None:
        """
        更新解码预览显示
        
        Args:
            img: 要显示的图片
        """
        # 保存当前图片
        self.current_image = img
        
        # 获取画布尺寸
        canvas_width = self.decode_preview_canvas.winfo_width()
        canvas_height = self.decode_preview_canvas.winfo_height()
        
        # 调整图像大小以适应画布
        img_copy = img.copy()
        img_copy.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        
        # 转换为PhotoImage
        self.decode_photo = ImageTk.PhotoImage(img_copy)
        
        # 清除画布并显示图像
        self.decode_preview_canvas.delete("all")
        
        # 计算居中位置
        x = (canvas_width - self.decode_photo.width()) // 2
        y = (canvas_height - self.decode_photo.height()) // 2
        
        # 显示图像
        self.decode_preview_canvas.create_image(x, y, anchor=tk.NW, image=self.decode_photo)
    
    def _clear_decode_preview(self) -> None:
        """
        清除解码预览
        """
        self.decode_preview_canvas.delete("all")
        self.current_image = None
    
    def _display_decode_results(self, results: list) -> None:
        """
        显示解码结果
        
        Args:
            results: 解码结果列表
        """
        # 清空结果文本框
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        
        if not results:
            self.result_text.insert(tk.END, "未检测到QR码")
        else:
            self.result_text.insert(tk.END, f"检测到 {len(results)} 个QR码:\n\n")
            
            for i, result in enumerate(results, 1):
                self.result_text.insert(tk.END, f"=== 结果 {i} ===\n")
                self.result_text.insert(tk.END, f"类型: {result['type']}\n")
                self.result_text.insert(tk.END, f"数据: {result['data']}\n")
                self.result_text.insert(tk.END, "\n")
        
        self.result_text.config(state="disabled")
    
    def run(self) -> None:
        """运行GUI程序"""
        self.root.mainloop()


def create_gui() -> None:
    """创建并运行GUI"""
    root = tk.Tk()
    app = QRCodeGUI(root)
    app.run()
