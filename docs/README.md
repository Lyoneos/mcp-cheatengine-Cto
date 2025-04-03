# MCP CheatEngine Toolkit Documentation

Welcome to the MCP CheatEngine Toolkit documentation! This documentation will help you understand how to use this toolkit to interact with CheatEngine.

## Documentation Index

- [Chinese Documentation](README_zh.md): Detailed documentation in Chinese
- [API Reference (Chinese)](Api_zh.md): Complete API documentation in Chinese

## Quick Start

### Installation

```bash
git clone https://github.com/Lyoneos/mcp-cheatengine-Cto.git
cd mcp-cheatengine-Cto
pip install -r requirements.txt
```

### Running

```bash
python main.py
```

### Basic Usage

1. Connect to CheatEngine: `ce_connect()`
2. Read memory: `memory_read("0x7065F60", "int32")`
3. Read memory with options: `memory_read("0x7065F60", "int32", {"assembly": True})`

## System Requirements

- Python 3.6+
- CheatEngine 7.0+
- Dependencies: See requirements.txt

## More Resources

- [Project Home](https://github.com/Lyoneos/mcp-cheatengine-Cto)
- [Issue Reporting](https://github.com/Lyoneos/mcp-cheatengine-Cto/issues)

## License

This project is open source under the MIT license.