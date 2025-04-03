# MCP CheatEngine Toolset

MCP CheatEngine toolset is a Python-based toolkit for communicating with CheatEngine through the MCP interface, providing memory read and write, assembly code analysis, and other functions.

Here, CE plugins and MCP interfaces have been developed.

Python and CE use the socket protocol for communication. Currently, Python MCP only has built-in read and write modules, and Lua has also implemented writing and pointers, but stability is general.

Those interested can give it a star.

## Features

* Automatically connect to CheatEngine and analyze application memory and assembly
* Provide AI interactive memory reading function
* Support obtaining and analyzing assembly code corresponding to memory addresses

## Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Service

```bash
python main.py
```

## Tool Usage Instructions

#### Detailed documentation can be found in the API documentation

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

### 3. Test Tool (test_echo)

A test tool that receives input of any type and outputs it unchanged.

```python
# Example
test_echo("Test string")
test_echo({"name": "Test", "value": 100})
```

## Documentation

For Chinese documentation, please see [docs/README_zh.md](docs/README_zh.md).
For API reference, please see [docs/Api_zh.md](docs/Api_zh.md).