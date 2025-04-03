# MCP CheatEngine工具集

MCP CheatEngine工具集是一个基于Python的工具包，用于通过MCP接口与CheatEngine进行通信，提供内存读写、汇编代码分析等功能。


Py和CE通讯用的是socket协议，目前Python MCP 只内置了读模块，写的模块，lua里也实现了了写和指针，不过稳定性一般。

感兴趣的可以点个星

## 特性

* 自动连接到CheatEngine并分析应用内存和汇编
* 提供Ai交互读内存功能
* 支持获取并分析内存地址对应的汇编代码

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
