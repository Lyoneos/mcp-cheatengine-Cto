# MCP CheatEngine工具集

[![English](https://img.shields.io/badge/English-Click-yellow)](docs/README.md)
[![简体中文](https://img.shields.io/badge/中文文档-点击查看-orange)](docs/README-zh.md)


MCP CheatEngine `非官方`是一个基于Python的工具包，通过MCP接口与CheatEngine进行通信，提供读取内存、汇编代码分析等功能。

Py和CE通讯用的是socket协议，目前Python MCP 只内置了读模块，写模块未在MCP客户端实现。lua里也实现了写和指针扫描，不稳定。

感兴趣的可以点个星

* 项目还在初期，有问题issues

# CE 插件链接

* 必下
* [CE插件下载](https://github.com/Lyoneos/mcp-cheatengine-Cto_CEPlugins)
* 详细的Lua文档可看docx下的API_zh.md

## 特性

* 自动连接到CheatEngine并分析应用内存和汇编
* 提供Ai交互读内存功能
* 支持获取并分析内存地址对应的汇编代码

## 开始使用

* 推荐使用 cursor 配合本项目完成使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python main.py
```

## 工具使用说明

#### 详细可看Api文档

### 1. 连接工具 (ce_connect)

用于连接到CheatEngine并检查连接状态。

```python
ce_connect()
```

### 2. 内存读取 (memory_read)

从指定内存地址读取数据。

```python
memory_read("0x7065F60", "int32")

memory_read("0x7065F60", "int32", {
    "assembly": True,
    "assemblySize": 10,
    "rawBytes": True
})
```

### 3. 测试工具 (test_echo)

接收任意类型的输入并原样输出的测试工具。

```python
# 示例
test_echo("测试字符串")
test_echo({"name": "测试", "value": 100})
```


### 联系方式

*    ✉️ [ieeLyon@163.com](mailto:ieeLyon@163.com)
*    注明来意
*    本人还有 *渗透* 和 *前端加密解密* AiMCP方案，感兴趣联系我的邮箱
