"""
测试工具

提供接收任意类型输入并原样输出的功能
"""
from util import logger
from typing import Any, Dict, List, Union, Optional
import json

TOOL_DESCRIPTION = """
    测试工具：接收任意类型的输入并原样输出
    
    参数:
    - input_data: 任意类型的输入数据(字符串、数字、列表、字典等任意类型)
    
    返回:
    - 原样返回输入的数据及其类型信息
"""


def test_echo(input_data: Any) -> Dict[str, Any]:
    """
    接收任意类型的输入并原样输出
    
    Args:
        input_data: 任意类型的输入数据，如果是字符串会尝试解析为JSON
    
    Returns:
        Dict: 包含输入数据、类型信息和元数据的字典
    """
    # 记录日志
    logger.info(f"测试工具接收到输入: {input_data}")
    
    # 如果是字符串，尝试解析为JSON
    original_input = input_data
    if isinstance(input_data, str):
        try:
            input_data = json.loads(input_data)
            logger.info(f"将字符串输入解析为: {input_data}")
        except json.JSONDecodeError:
            # 如果不是有效的JSON，保持为字符串
            logger.info("输入不是有效的JSON，保持为字符串")
    
    # 获取输入数据的类型
    data_type = type(input_data).__name__
    
    # 构建结果字典
    result = {
        "success": True,
        "input": input_data,
        "original_input": original_input,
        "type": data_type,
        "meta": {
            "timestamp": __import__('time').time(),
            "is_primitive": isinstance(input_data, (str, int, float, bool, type(None))),
            "length": len(input_data) if hasattr(input_data, "__len__") else None
        }
    }
    
    # 根据不同类型添加额外信息
    if isinstance(input_data, dict):
        result["meta"]["keys"] = list(input_data.keys())
    elif isinstance(input_data, (list, tuple)):
        result["meta"]["element_count"] = len(input_data)
        if len(input_data) > 0:
            result["meta"]["first_element_type"] = type(input_data[0]).__name__
    elif isinstance(input_data, str):
        result["meta"]["character_count"] = len(input_data)
        result["meta"]["word_count"] = len(input_data.split())
    elif isinstance(input_data, (int, float)):
        result["meta"]["is_negative"] = input_data < 0
        
    logger.info(f"测试工具返回结果: {result}")
    return result

 # 创建一个包装函数，接收字符串参数然后转发给test_echo
def test_echo_adapter(input_data=None):
    """
    为AI工具接口适配的包装器，直接接收input_data参数
    
    Args:
        input_data: 任意类型的输入数据
        
    Returns:
        Dict: test_echo的返回结果
    """
    try:
        logger.info(f"适配器接收到: {input_data}，类型: {type(input_data)}")
        
        # 传递给原始的test_echo函数
        return test_echo(input_data)
    except Exception as e:
        logger.error(f"适配器处理错误: {str(e)}")
        return {
            "success": False,
            "error": f"参数处理错误: {str(e)}",
            "input": str(input_data)
        }

def register_tool(mcp):
    """
    向MCP注册工具
    
    Args:
        mcp: MCP实例
    """
   
    
    # 注册适配器函数
    mcp.tool(description=TOOL_DESCRIPTION)(test_echo_adapter) 