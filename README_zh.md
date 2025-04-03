# MCP CheatEngine工具集

MCP CheatEngine工具集是一个基于Python的工具包，用于通过MCP（模型控制协议）接口与CheatEngine进行通信，提供内存读写、汇编代码分析等功能。

## 特性

* **CheatEngine连接管理**：自动连接到CheatEngine实例并维护连接状态
* **内存操作**：提供内存读写功能
* **汇编代码分析**：支持获取并分析内存地址对应的汇编代码
* **插件架构**：支持动态加载工具模块，便于扩展功能

## 开始使用

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python main.py
```

## 工具使用说明

### 1. 连接工具 (ce_connect)

用于连接到CheatEngine并检查连接状态。

```python
# 示例：连接到CheatEngine
ce_connect()
```

### 2. 内存读取 (memory_read)

从指定内存地址读取数据。

```python
# 示例：读取内存地址
memory_read("0x7065F60", "int32")

# 带选项的读取
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

## 开发指南

### 添加新工具

1. 在`tools/`目录下创建新的工具目录
2. 创建`tool.py`文件并实现`register_tool`函数
3. 在`register_tool`函数中使用MCP实例注册工具函数