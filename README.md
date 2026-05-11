# 智能PDF转Word

一款基于 PySide6 的桌面端 PDF 转 Word 工具，支持原生文本提取、OCR 识别和自适应混合处理三种模式。

## 功能特性

- **智能分类**: 自动识别 PDF 类型（原生/扫描件/混合），选择最优处理策略
- **三种处理模式**
  - 模式A — 原生提取通道：直接提取 PDF 中的文本和图片，速度快、格式保真度高
  - 模式B — OCR 识别通道：基于 PaddleOCR 对扫描件进行文字识别
  - 模式C — 自适应混合通道：逐页判断类型，自动切换原生提取与 OCR 识别
- **拖拽操作**: 支持拖拽 PDF 文件到窗口直接打开
- **输出为 .docx**: 使用 python-docx 生成标准的 Word 文档，保留字号、段落间距等格式
- **权限自动回退**: 当目标输出目录无写入权限时，自动回退到系统临时目录保存
- **可配置项**: 支持自定义 OCR DPI、文本检测阈值、默认输出目录

## 环境要求

- Windows 10/11
- Python 3.8 或更高版本

## 安装与运行

### 1. 克隆项目

```bash
git clone <仓库地址>
cd PDF2word
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

> **注意**: `paddlepaddle` 和 `paddleocr` 在首次运行时会自动下载模型文件，请确保网络畅通。如需 GPU 加速，可将 `requirements.txt` 中的 `paddlepaddle` 替换为 `paddlepaddle-gpu`。

### 4. 运行程序

```bash
python main.py
```

## 使用说明

1. 启动程序后，将 PDF 文件拖入窗口，或点击"选择文件"按钮
2. 程序会自动分析 PDF 类型并显示文件信息（页数、分类等）
3. 点击"开始转换"，选择输出 .docx 文件的保存位置
4. 等待转换完成，程序会询问是否立即打开生成的 Word 文档

### 设置选项

点击菜单栏 **文件 → 设置** 可调整以下参数：

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| 默认输出目录 | 转换结果默认保存位置 | 用户主目录 |
| OCR 转换 DPI | OCR 识别时的渲染分辨率，越高越清晰但越慢 | 300 |
| 文本检测阈值 | 判断页面是否为原生 PDF 的字符数阈值 | 50 |

## 项目结构

```
PDF2word/
├── main.py                     # 程序入口
├── config.py                   # 全局配置
├── requirements.txt            # Python 依赖清单
├── controllers/                # 控制器层
│   ├── app_controller.py       # 主控制器，协调 UI 与业务逻辑
│   └── settings_controller.py  # 设置控制器
├── models/                     # 业务模型层
│   ├── pdf_model.py            # PDF 文档模型（分类、读取）
│   ├── extract_engine.py       # 原生文本提取引擎
│   ├── ocr_engine.py           # OCR 识别引擎
│   ├── hybrid_engine.py        # 混合处理引擎（调度器）
│   ├── word_builder.py         # Word 文档构建器
│   └── task_runner.py          # 后台任务线程
├── views/                      # 视图层
│   ├── main_window.py          # 主窗口
│   ├── drop_area.py            # 拖拽区域组件
│   ├── progress_panel.py       # 进度展示组件
│   ├── preview_panel.py        # 文件信息预览组件
│   └── settings_dialog.py      # 设置对话框
└── utils/                      # 工具函数
    ├── file_utils.py           # 文件路径处理与验证
    └── font_utils.py           # 中文字体设置
```

## 打包为 EXE

使用 PyInstaller 将程序打包为独立的 Windows 可执行文件。

### 安装 PyInstaller

```bash
pip install pyinstaller
```

### 打包命令

```bash
pyinstaller --name "智能PDF转Word" ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "requirements.txt;." ^
    --hidden-import paddle ^
    --hidden-import paddleocr ^
    --collect-all paddleocr ^
    --collect-all paddle ^
    main.py
```

### 参数说明

| 参数 | 说明 |
| --- | --- |
| `--name` | 生成的 EXE 文件名 |
| `--windowed` | 不显示命令行窗口（GUI 程序） |
| `--icon` | 程序图标（.ico 文件，可选） |
| `--add-data` | 打包额外的数据文件 |
| `--hidden-import` | 显式声明隐式导入的模块 |
| `--collect-all` | 收集指定包的所有数据文件（PaddleOCR 模型文件较大） |

### 注意事项

1. PaddleOCR 的模型文件较大，打包后体积可能超过 1GB，首次打包耗时较长
2. 如果遇到打包后运行报缺失 DLL 的错误，可尝试添加 `--collect-binaries paddle` 参数
3. 建议在干净的虚拟环境中执行打包，避免引入不必要的依赖

## 依赖清单

| 依赖 | 用途 |
| --- | --- |
| PySide6 | GUI 框架 |
| PyMuPDF (fitz) | PDF 文档读取与解析 |
| paddlepaddle + paddleocr | OCR 文字识别 |
| python-docx | Word 文档生成 |
| Pillow | 图像处理 |
| opencv-python | 图像预处理（OCR 引擎使用） |

## License

仅供学习与个人使用。
