"""
内存读取工具

提供读取指定内存地址数据的功能
"""
from util import (
    logger, create_ce_client
)
from typing import Dict, Union, Any, Optional
import time
import json

TOOL_DESCRIPTION = """
    读取指定内存地址的数据
    
    参数:
    - address: 内存地址(十六进制字符串或整数，例如：0x7065F60 或 117879888)
    - data_type: 数据类型(int32, int64, float, double, string, bytes等)
    - options: 可选参数，支持以下选项：
      - assembly: 是否返回汇编代码(true/false)
      - assemblySize: 要反汇编的指令数量(整数，默认10)
      - rawBytes: 是否返回原始字节(true/false)
      - bytesSize: 读取的原始字节数量(整数，默认16)
      - opcode: 是否返回操作码(true/false)
      - opcodeSize: 操作码字节数(整数，默认16)
      - comments: 是否返回地址注释(true/false)
      - multiType: 是否返回多种数据类型解释(true/false)
      - instructionMultiType: 是否为指令提供多种解释(true/false)
    
    用法示例:
    memory_read("0x7065F60", "int32", {"assembly": True, "bytesSize": 16})
    memory_read(117879888, "int32", {"rawBytes": True, "assembly": True})
    memory_read("0x401000", "float", {"multiType": True, "comments": True})
    
    高级用法:
    # 显示所有详细信息
    memory_read("0x7065F60", "int32", {
        "rawBytes": True, 
        "assembly": True, 
        "opcode": True,
        "comments": True,
        "multiType": True,
        "instructionMultiType": True,
        "bytesSize": 32,
        "assemblySize": 10,
        "opcodeSize": 16
    })
    
    返回:
    - 读取的内存数据及元信息的字典
    - 如果成功，result["success"]=True且result["value"]包含读取的值
    - 如果失败，result["success"]=False且result["error"]包含错误信息
"""

def format_address(address: Union[str, int]) -> tuple:
    """
    格式化内存地址，返回格式化后的地址字符串和整数值

    Args:
        address: 内存地址(十六进制字符串或整数)

    Returns:
        tuple: (格式化后的地址字符串, 地址整数值)
    """
    if isinstance(address, str):
        # 如果地址是字符串格式，确保正确的0x前缀
        if address.startswith('0x') or address.startswith('$'):
            # 已经有前缀，保持原样
            formatted_addr = address
            if address.startswith('$'):
                formatted_addr = '0x' + address[1:]
        else:
            # 添加0x前缀
            formatted_addr = f"0x{address}"

        # 尝试转换为整数
        try:
            if formatted_addr.startswith('0x'):
                addr_int = int(formatted_addr[2:], 16)
            elif formatted_addr.startswith('$'):
                addr_int = int(formatted_addr[1:], 16)
            else:
                addr_int = int(formatted_addr, 16)
        except ValueError:
            raise ValueError(f"无效的内存地址格式: {address}")
    else:
        # 如果是整数，则直接使用
        addr_int = address
        formatted_addr = f"0x{addr_int:X}"

    return formatted_addr, addr_int

def memory_read(address: Union[str, int], data_type: str, options: Optional[Union[Dict, str]] = None) -> Dict[str, Any]:
    """
    读取指定内存地址的数据
    
    支持多种数据类型和高级选项，能够处理包含特殊字符的响应数据

    Args:
        address: 内存地址(十六进制字符串或整数)，可以是字符串形式的JSON
        data_type: 数据类型(int32, float, double, string, bytes等)
        options: 可选参数，包括assembly、multiType等，可以是字符串(将尝试解析为JSON)或字典

    Returns:
        Dict: 读取的内存数据及元信息
    """
    # 处理address参数
    if isinstance(address, str):
        try:
            # 尝试解析为JSON，看是否是字符串形式的数字或对象
            addr_data = json.loads(address)
            if isinstance(addr_data, (int, str)):
                # 如果是数字或字符串，直接使用
                address = addr_data
                logger.info(f"将JSON字符串address解析为: {address}")
        except json.JSONDecodeError:
            # 不是JSON字符串，保持原样
            pass
    
    # 处理data_type参数
    if isinstance(data_type, str):
        try:
            # 尝试解析为JSON，看是否是字符串形式的值
            dt_value = json.loads(data_type)
            if isinstance(dt_value, str):
                data_type = dt_value
                logger.info(f"将JSON字符串data_type解析为: {data_type}")
        except json.JSONDecodeError:
            # 不是JSON字符串，保持原样
            pass
            
    # 处理options参数
    if isinstance(options, str):
        try:
            options = json.loads(options)
            logger.info(f"将字符串options解析为: {options}")
        except json.JSONDecodeError:
            logger.warning(f"无法解析options字符串，将设为None: {options}")
            options = None
    
    # 初始化选项
    options = options or {}

    print(address, data_type, options)

    # 默认响应结构
    result = {
        "success": False,
        "address": None,
        "dataType": data_type,
        "value": None,
        "error": None
    }

    try:
        # 格式化地址
        formatted_addr, addr_int = format_address(address)
        result["address"] = formatted_addr

        # 获取CE客户端(优先使用长连接)
        client = create_ce_client(auto_connect=True)

        # 构建请求结构
        request = {
            "address": addr_int,
            "dataType": data_type
        }

        # 添加选项
        if options:
            request["options"] = options

            # 记录高级选项
            advanced_opts = []
            if options.get("rawBytes"):
                advanced_opts.append("原始字节")
                if options.get("bytesSize"):
                    advanced_opts[-1] += f"({options.get('bytesSize')}字节)"
            if options.get("assembly"):
                advanced_opts.append("汇编代码")
                if options.get("assemblySize"):
                    advanced_opts[-1] += f"({options.get('assemblySize')}条)"
            if options.get("opcode"):
                advanced_opts.append("操作码")
                if options.get("opcodeSize"):
                    advanced_opts[-1] += f"({options.get('opcodeSize')}字节)"
            if options.get("comments"):
                advanced_opts.append("注释")
            if options.get("multiType"):
                advanced_opts.append("多类型解释")
            if options.get("instructionMultiType"):
                advanced_opts.append("指令多类型解释")

            # 记录日志
            if advanced_opts:
                logger.info(f"内存读取高级选项: {', '.join(advanced_opts)}")

        # 发送读取请求
        if not client.connected:
            result["error"] = "未连接到CheatEngine服务器"
            return result

        # 将请求转换为JSON并发送
        json_data = json.dumps(request)
        packet = client._pack_data(json_data, client.PACKET_TYPE["MEMORY_READ"])

        try:
            client.socket.sendall(packet)
            logger.info(f"已发送内存读取请求: {formatted_addr}, 类型: {data_type}")

            # 接收响应
            data_type, content = client.receive_response(retry_count=2)

            if data_type is None or content is None:
                result["error"] = "未收到服务器响应"
                return result

            # 解析响应JSON - 改进的解析方式，处理特殊字符
            try:
                # 首先尝试标准解析
                try:
                    response = json.loads(content.decode('utf-8'))
                    # 将响应内容合并到结果中
                    result.update(response)
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    # 处理特殊字符和控制字符
                    logger.info(f"标准解析失败，尝试处理特殊字符: {str(e)}")
                    
                    content_str = content.decode('utf-8', errors='replace')
                    
                    # 2. 在解析时忽略特殊字符
                    response = json.loads(content_str, strict=False)
                    # 将响应内容合并到结果中
                    result.update(response)

                # 日志记录
                if result.get("success"):
                    logger.info(f"内存读取成功: {formatted_addr}, 值: {result.get('value')}")

                    # 记录高级信息
                    advanced_info = []
                    if result.get("bytes"):
                        advanced_info.append(f"原始字节({len(result.get('bytes'))}字节)")
                    if result.get("assembly"):
                        advanced_info.append(f"汇编代码({len(result.get('assembly'))}条)")
                    if result.get("opcode"):
                        advanced_info.append(f"操作码({len(result.get('opcode'))}字节)")
                    if result.get("multiType"):
                        advanced_info.append(f"多类型解释({len(result.get('multiType'))}种)")

                    if advanced_info:
                        logger.info(f"返回高级信息: {', '.join(advanced_info)}")
                else:
                    logger.warning(f"内存读取失败: {result.get('error')}")
            except Exception as parse_error:
                logger.error(f"解析响应数据失败: {str(parse_error)}")
                result["error"] = f"解析响应数据失败: {str(parse_error)}"
                result["raw_content"] = content.decode('utf-8', errors='replace')
                
        except Exception as comm_error:
            logger.error(f"与CheatEngine服务器通信时发生错误: {str(comm_error)}")
            result["error"] = f"通信错误: {str(comm_error)}"
        finally:
            # 不关闭连接，保持长连接
            pass
    except Exception as e:
        logger.error(f"内存读取处理失败: {str(e)}")
        result["error"] = f"处理错误: {str(e)}"
        
    return result


# 为MCP创建适配器函数
def memory_read_adapter(address=None, data_type=None, options=None):
    """
    为MCP适配的memory_read包装器
    
    用于适配MCP的参数格式，将多个独立的参数传递给memory_read函数
    
    Args:
        address: 内存地址(十六进制字符串或整数)
        data_type: 数据类型
        options: 可选参数
        
    Returns:
        Dict: memory_read的返回结果
    """
    try:
        logger.info(f"内存读取适配器接收到参数: address={address}, data_type={data_type}, options={options}")
        return memory_read(address, data_type, options)
    except Exception as e:
        logger.error(f"内存读取适配器错误: {str(e)}")
        return {
            "success": False,
            "error": f"参数处理错误: {str(e)}",
            "address": str(address) if address else None,
            "dataType": data_type
        }


def register_tool(mcp):
    """
    向MCP注册工具
    
    Args:
        mcp: MCP实例
    """
    # 注册memory_read工具
    mcp.tool(description=TOOL_DESCRIPTION)(memory_read_adapter)