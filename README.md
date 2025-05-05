# MCP CheatEngine Cto

[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)
[![简体中文](https://img.shields.io/badge/中文文档-点击查看-orange)](docs/README-zh.md)


MCP CheatEngine `unofficial` is a Python-based toolkit that communicates with CheatEngine through the MCP interface, providing features such as reading memory and assembly code analysis.

Python and CE use the socket protocol for communication. Currently, the Python MCP only has a built-in read module, and the write module has not been implemented in the MCP client. Lua has also implemented writing and pointer scanning, but it's unstable.

If you're interested, please give it a star.

* The project is still in its early stages and there are issues and problems
# CE Plugin Link

* Must Download
* Otherwise, MCP SERVER cannot function as expected
* [CE Plugin Download](https://github.com/Lyoneos/mcp-cheatengine-Cto_CEPlugins)

## Features

* Automatically connect to CheatEngine and analyze application memory and assembly
* Provide AI interactive memory reading functionality
* Support getting and analyzing assembly code corresponding to memory addresses


## Getting Started

* It is recommended to use the cursor in conjunction with this project to complete the usage

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run MCPService

```bash
python main.py
```

## Tool Usage Instructions

#### For detailed information, please refer to the API documentation

### 1. Connection Tool (ce_connect)

Used to connect to CheatEngine and check the connection status.

```python
ce_connect()
```

### 2. Memory Reading (memory_read)

Read data from a specified memory address.

```python
memory_read("0x7065F60", "int32")

memory_read("0x7065F60", "int32", {
    "assembly": True,
    "assemblySize": 10,
    "rawBytes": True
})
```

### 3. Testing Tool (test_echo)

A testing tool that receives input of any type and outputs it unchanged.

```python
# Example
test_echo("Test String")
test_echo({"name": "Test", "value": 100})
```

# UpDate
* I recently discovered that Python is able to read memory directly, and this project may be deprecated and discontinued at any time due to the complexity of the code. Subsequent code will probably be done directly by Python.

