# MCP CheatEngine工具集文档

欢迎使用MCP CheatEngine工具集文档！本文档将帮助您了解如何使用该工具集与CheatEngine进行交互。

## 文档索引

- [使用指南](usage.md)：详细介绍工具集的基本用法和高级选项
- [API参考](api.md)：完整的API文档，包括函数接口、参数说明和返回值格式
- [开发指南](development.md)：如何为工具集添加新功能或扩展现有功能

## 快速入门

### 安装

```bash
git clone https://github.com/Lyoneos/mcp-cheatengine-Cto.git
cd mcp-cheatengine-Cto
pip install -r requirements.txt
```

### 运行

```bash
python main.py
```

### 基本用法

1. 连接到CheatEngine：`ce_connect()`
2. 读取内存：`memory_read("0x7065F60", "int32")`
3. 带选项读取内存：`memory_read("0x7065F60", "int32", {"assembly": True})`

## 系统要求

- Python 3.6+
- CheatEngine 7.0+
- 依赖项：参见requirements.txt

## 更多资源

- [项目主页](https://github.com/Lyoneos/mcp-cheatengine-Cto)
- [问题反馈](https://github.com/Lyoneos/mcp-cheatengine-Cto/issues)
- [贡献指南](CONTRIBUTING.md)

## 许可证

本项目基于MIT许可证开源。