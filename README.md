# MCP CheatEngine Toolkit

MCP CheatEngine Toolkit is a Python-based toolset for communicating with CheatEngine through the MCP (Model Control Protocol) interface, providing memory reading/writing, assembly code analysis and other functions.

## Features

- **CheatEngine Connection Management**: Automatically connect to CheatEngine instances and maintain connection status
- **Memory Operations**: Provide memory reading and writing functions
- **Assembly Code Analysis**: Support getting and analyzing assembly code corresponding to memory addresses
- **Plugin Architecture**: Support dynamic loading of tool modules for easy extension of functionality

## Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Service

```bash
python main.py
```

## Tool Usage Instructions

### 1. Connection Tool (ce_connect)

Used to connect to CheatEngine and check connection status.

```python
# Example: Connect to CheatEngine
ce_connect()
```

### 2. Memory Reading (memory_read)

Read data from a specified memory address.

```python
# Example: Read memory address
memory_read("0x7065F60", "int32")

# Reading with options
memory_read("0x7065F60", "int32", {
    "assembly": True,
    "assemblySize": 10,
    "rawBytes": True
})
```

### 3. Test Tool (test_echo)

A testing tool that receives any type of input and outputs it as is.

```python
# Example
test_echo("Test string")
test_echo({"name": "Test", "value": 100})
```

## Development Guide

### Adding New Tools

1. Create a new tool directory in the `tools/` directory
2. Create a `tool.py` file and implement the `register_tool` function
3. Register the tool function using the MCP instance in the `register_tool` function

## Documentation

For Chinese documentation, please see [Readme_zh.md](./docs/Readme_zh.md)