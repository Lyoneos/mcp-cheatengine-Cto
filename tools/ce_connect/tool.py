"""
CheatEngine连接测试工具

用于测试CheatEngine连接是否正常工作
"""
from util import logger, create_ce_client, cheatEngine_config


TOOL_DESCRIPTION = """
    连接到CheatEngine并检查连接状态
    """


def ce_connect() -> str:
    """
    连接到CheatEngine服务器并返回连接状态
    
    Returns:
        str: 连接状态信息
    """
    try:
        # 创建CE客户端
        client = create_ce_client(
            host=cheatEngine_config["host"], 
            port=cheatEngine_config["port"],
            auto_connect=True
        )
        
        # 检查服务器状态
        if client.connected:
            # 进一步测试连接是否响应
            if client.check_server(timeout=3):
                return f"已成功连接到CheatEngine服务器 {client.host}:{client.port}，连接正常"
            else:
                return f"已连接到CheatEngine服务器 {client.host}:{client.port}，但服务器无响应"
        else:
            return f"无法连接到CheatEngine服务器 {cheatEngine_config['host']}:{cheatEngine_config['port']}"
    except Exception as e:
        logger.error(f"连接CheatEngine服务器时发生错误: {str(e)}")
        return f"连接CheatEngine服务器时发生错误: {str(e)}"
    finally:
        # 确保断开连接
        if 'client' in locals() and client.connected:
            client.disconnect()


def register_tool(mcp):
    """
    向MCP注册工具
    
    Args:
        mcp: MCP实例
    """
    mcp.tool(description=TOOL_DESCRIPTION)(ce_connect) 