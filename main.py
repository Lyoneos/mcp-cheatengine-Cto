#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MCP CheatEngine-CTO主程序

此文件作为MCP CheatEngine-CTO的主入口点，负责加载所有工具并启动MCP服务。
"""
from mcp.server.fastmcp import FastMCP
import importlib
import os
import glob
import logging
from util import logger, create_ce_client
import json
from typing import Dict, Any, Union

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建 MCP 实例
mcp = FastMCP("CheatEngine专家")

# 全局帮助信息
HELP_INFO = """
MCP CheatEngine工具集使用说明：

1. 连接工具 (ce_connect)
   - 用途：连接到CheatEngine并检查连接状态
   - 用法：直接调用，无需参数

2. 内存读取 (memory_read)
   - 用途：读取指定内存地址的数据
   - 参数：地址、数据类型、选项(可选)
   - 示例：memory_read("0x7065F60", "int32")

3. 测试工具 (test_echo)
   - 用途：接收任意类型的输入并原样输出
   - 参数：任意类型的输入数据
   - 示例：test_echo("测试字符串")、test_echo({"name": "测试", "value": 100})
"""


def show_help():
    """
    显示MCP Linux工具集使用帮助
    """
    return HELP_INFO


# 自动导入所有工具模块
def load_all_tools():
    """
    自动加载tools目录下的所有工具模块
    """
    # 注册帮助工具
    mcp.tool(description="显示MCP CheatEngine工具集使用帮助信息，包括所有工具的简要说明和使用流程")(show_help)
    logger.info("注册了帮助工具: show_help")

    # 注册内存读取工具(直接处理JSON请求)
    memory_read_desc = """
    读取指定内存地址的数据(直接处理JSON请求)
    
    参数:
    - request_json: 完整的JSON格式请求对象或字符串，格式如下:
    {
      "address": 整数或十六进制字符串,
      "dataType": "int32|float|double|string等",
      "options": {
        "assembly": true/false,         // 是否返回汇编代码
        "assemblySize": 整数,           // 汇编指令数量
        "rawBytes": true/false,         // 是否返回原始字节
        "bytesSize": 整数,              // 原始字节数量
        "opcode": true/false,           // 是否返回操作码
        "comments": true/false,         // 是否返回注释
        "multiType": true/false,        // 是否返回多种类型解释
        "instructionMultiType": true/false  // 是否为指令提供多种解释
      }
    }
    
    示例:

    返回:
    - 读取的内存数据及元信息
    """
    # 使用特殊参数指定接受任意类型


    # 获取tools目录下所有工具目录
    tools_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tools')
    if not os.path.exists(tools_dir):
        os.makedirs(tools_dir)
        logger.warning(f"工具目录{tools_dir}不存在，已创建空目录")
        return

    # 遍历所有工具目录
    tool_count = 0

    # 使用os.listdir获取目录列表，比glob更可控
    for item in os.listdir(tools_dir):
        tool_dir = os.path.join(tools_dir, item)

        # 只处理目录
        if not os.path.isdir(tool_dir):
            continue

        # 排除__pycache__目录和以点开头的隐藏目录
        if item == '__pycache__' or item.startswith('.'):
            logger.debug(f"跳过目录: {item}")
            continue

        # 检查是否存在tool.py文件
        tool_file = os.path.join(tool_dir, 'tool.py')
        if not os.path.isfile(tool_file):
            logger.warning(f"工具目录 {item} 中没有找到tool.py文件，跳过")
            continue

        module_path = f"tools.{item}.tool"

        try:
            # 导入工具模块
            module = importlib.import_module(module_path)

            # 调用模块的register_tool函数注册工具
            if hasattr(module, 'register_tool'):
                module.register_tool(mcp)
                tool_count += 1
                logger.info(f"成功加载工具: {item}")
            else:
                logger.warning(f"工具模块{item}没有register_tool函数")
        except Exception as e:
            logger.error(f"加载工具{item}失败: {str(e)}")

    logger.info(f"总共加载了{tool_count}个工具")


# 运行服务器
if __name__ == "__main__":
    try:
        logger.info("MCP CheatEngine工具开始运行")
        # 加载所有工具
        load_all_tools()
        # 启动MCP服务
        mcp.run()
    except KeyboardInterrupt:
        logger.info("用户中断，程序正在结束")
    except Exception as e:
        logger.error(f"程序遇到错误: {str(e)}")
    finally:
        # 确保关闭所有SSH连接
        logger.info("清理资源并关闭连接")
