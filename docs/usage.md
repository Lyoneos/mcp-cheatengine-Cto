# MCP CheatEngine工具集使用指南

本文档介绍如何使用MCP CheatEngine工具集与CheatEngine进行交互，以实现内存读写、汇编代码分析等功能。

## 准备工作

在使用本工具集前，请确保：

1. 已安装Python 3.6+
2. 已安装CheatEngine并启动
3. CheatEngine开启了网络接口

## 安装

```bash
# 克隆仓库
git clone https://github.com/Lyoneos/mcp-cheatengine-Cto.git
cd mcp-cheatengine-Cto

# 安装依赖
pip install -r requirements.txt
```

## 基本用法

### 启动服务

```bash
python main.py
```

服务启动后，将通过指定端口提供MCP接口，可以通过兼容MCP协议的客户端进行交互。

## 工具详细使用说明

### 1. 连接工具 (ce_connect)

用于连接到CheatEngine并检查连接状态。

```python
# 示例调用
ce_connect()

# 返回示例
"已成功连接到CheatEngine服务器 127.0.0.1:8082，连接正常"
```

### 2. 内存读取 (memory_read)

从指定内存地址读取数据。

```python
# 基本用法
memory_read("0x7065F60", "int32")

# 带选项的读取
memory_read("0x7065F60", "int32", {
    "assembly": True,  # 返回汇编代码
    "assemblySize": 10,  # 返回10条汇编指令
    "rawBytes": True  # 返回原始字节
})

# 返回示例
{
    "success": true,
    "address": "0x7065F60",
    "dataType": "int32",
    "value": 12345,
    "bytes": ["FF", "23", "45", "67"],
    "assembly": [
        {"address": "0x7065F60", "instruction": "mov eax, [ebp+8]"},
        {"address": "0x7065F63", "instruction": "cmp eax, 0"}
        // ...更多指令
    ]
}
```

### 3. 测试工具 (test_echo)

接收任意类型的输入并原样输出的测试工具。

```python
# 字符串
test_echo("测试字符串")

# 对象
test_echo({"name": "测试", "value": 100})

# 返回示例
{
    "success": true,
    "input": {"name": "测试", "value": 100},
    "original_input": {"name": "测试", "value": 100},
    "type": "dict",
    "meta": {
        "timestamp": 1680524400.123456,
        "is_primitive": false,
        "length": 2,
        "keys": ["name", "value"]
    }
}
```

## 高级选项

### 内存读取高级选项

```python
memory_read("0x7065F60", "int32", {
    "rawBytes": True,        # 返回原始字节
    "bytesSize": 32,         # 返回32字节的原始数据
    "assembly": True,        # 返回汇编代码
    "assemblySize": 10,      # 返回10条汇编指令
    "opcode": True,          # 返回操作码
    "opcodeSize": 16,        # 返回16字节的操作码
    "comments": True,        # 返回注释
    "multiType": True,       # 以多种类型解释数据
    "instructionMultiType": True  # 以多种方式解释指令
})
```

## 故障排除

如果连接到CheatEngine失败，请检查：

1. CheatEngine是否已启动
2. 网络接口是否已开启
3. 端口是否被占用（默认8082）
4. 防火墙设置是否阻止了连接

## API参考

更多详细的API文档，请参阅[API参考文档](Api_zh.md)。