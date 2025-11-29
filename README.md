# QR码生成器

一个功能强大、完全离线的QR码生成小程序，支持多种内容类型和自定义选项。

## 功能特点

- 📱 **多种内容类型支持**：文本、URL、联系人信息等
- 🎨 **丰富的自定义选项**：
  - 尺寸调整（1-40）
  - 纠错级别选择（L、M、Q、H）
  - 边框大小设置
  - 格子大小调整
- 📊 **实时预览**：内容或选项变化时自动更新预览
- 💾 **多种格式保存**：支持PNG、JPG、BMP、GIF等
- 🖥️ **跨平台兼容**：支持Windows、macOS和Linux
- 🌐 **完全离线**：不依赖任何外部网络服务
- 🎯 **简洁直观的界面**：易于使用，操作流畅

## 技术栈

- **Python 3**：核心编程语言
- **tkinter**：GUI框架（Python标准库）
- **qrcode**：QR码生成库
- **PIL/Pillow**：图像处理库

## 安装步骤

### 1. 克隆或下载项目

```bash
git clone https://github.com/yourusername/qrcode-generator.git
cd qrcode-generator
```

### 2. 安装依赖

使用pip安装所需依赖：

```bash
pip install -r requirements.txt
```

### 3. 运行程序

直接运行主程序：

```bash
python main.py
```

## 使用方法

### 基本使用

1. **选择内容类型**：在下拉菜单中选择要生成的QR码内容类型（文本、URL、联系人）
2. **输入内容**：在文本框中输入要编码的内容
3. **调整选项**：根据需要调整QR码的尺寸、纠错级别、边框大小和格子大小
4. **查看预览**：右侧预览区域会实时显示生成的QR码
5. **保存QR码**：点击"保存QR码"按钮，选择保存路径和格式

### 快捷键

- `Ctrl + Enter`：快速生成QR码
- 内容或选项变化时自动生成预览

## 项目结构

```
qrcode-generator/
├── src/                      # 源代码目录
│   ├── __init__.py           # 包初始化文件
│   ├── qrcode_generator.py   # 核心QR码生成功能
│   ├── gui.py                # tkinter GUI界面
│   └── utils.py              # 工具函数
├── main.py                   # 程序入口
├── requirements.txt          # 依赖声明
└── README.md                 # 项目说明文档
```

## 功能说明

### 内容类型

1. **文本**：直接编码文本内容
2. **URL**：自动添加http://前缀（如果没有）
3. **联系人**：格式化为vCard格式，支持导入到通讯录

### 纠错级别

- **L**：7%的纠错能力
- **M**：15%的纠错能力（默认）
- **Q**：25%的纠错能力
- **H**：30%的纠错能力

### 尺寸

- 范围：1-40
- 数值越大，QR码包含的信息容量越大
- 建议根据实际需要选择合适的尺寸

## 示例

### 生成文本QR码

1. 选择内容类型为"文本"
2. 输入文本内容："Hello, QR Code!"
3. 调整选项（可选）
4. 查看预览并保存

### 生成URL QR码

1. 选择内容类型为"URL"
2. 输入URL："www.example.com"
3. 系统会自动添加http://前缀
4. 查看预览并保存

### 生成联系人QR码

1. 选择内容类型为"contact"
2. 输入联系人姓名："张三"
3. 生成后可直接导入到手机通讯录

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues：https://github.com/yourusername/qrcode-generator/issues

---

**享受使用QR码生成器！** 🚀
