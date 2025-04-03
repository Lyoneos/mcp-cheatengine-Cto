"""
MCP CheatEngine工具辅助函数模块
包含各工具共享的辅助函数
"""
import re
import logging
import time
import os
import socket
import struct
import json
from collections import Counter, defaultdict
from typing import Dict, List, Any, Tuple, Set, Optional, Union

# 配置日志
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mcp_ssh.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)
logger = logging.getLogger('MCP_SSH')

# cheatEngine连接配置 - 默认值，可通过函数动态修改
cheatEngine_config = {
    "host": "127.0.0.1",
    "port": 8082,
    "timeout": 10,
    "retries": 3
}

class CESocketClient:
    """
    CheatEngine Socket客户端
    用于与CheatEngine通信的Socket客户端实现
    """
    
    # 数据包类型常量
    PACKET_TYPE = {
        "ASSEMBLY": 0x01,    # 汇编代码
        "BYTECODE": 0x02,    # 原始字节码
        "TEXT": 0x03,        # 文本消息
        "COMMAND": 0x04,     # 命令
        "RESPONSE": 0x05,    # 响应
        "MEMORY_READ": 0x10, # 内存读取
        "MEMORY_WRITE": 0x11,# 内存写入
        "MEMORY_BATCH": 0x12,# 批量内存读取
        "ASSEMBLY_WRITE": 0x13, # 汇编代码修改
        "LUA_EXEC": 0x20,    # Lua代码执行
        "ENUM_MODULES": 0x30, # 枚举进程模块
        "POINTER_SCAN": 0x31, # 指针扫描
        "POINTER_READ": 0x32, # 模块偏移指针读取
        "ERROR": 0xFF        # 错误
    }
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8082, timeout: int = 10, 
                 auto_connect: bool = True, max_retries: int = 3):
        """
        初始化客户端
        
        @param {str} host - 服务器地址
        @param {int} port - 服务器端口
        @param {int} timeout - 超时时间(秒)
        @param {bool} auto_connect - 是否开启自动连接
        @param {int} max_retries - 最大重试次数
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.connected = False
        self.auto_connect = auto_connect
        self.max_retries = max_retries
        self.logger = logger
    
    def connect(self) -> bool:
        """
        连接到服务器
        
        @return {bool} - 是否连接成功
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.logger.info(f"已连接到CheatEngine服务器 {self.host}:{self.port}")
            return True
        except socket.error as e:
            self.logger.error(f"连接CheatEngine服务器失败: {e}")
            self.connected = False
            return False
    
    def disconnect(self) -> None:
        """
        断开连接
        """
        if self.socket:
            self.socket.close()
            self.socket = None
            self.connected = False
            self.logger.info("已断开与CheatEngine服务器的连接")
    
    def ensure_connected(self) -> bool:
        """
        确保已连接到服务器，如果未连接则尝试连接
        
        @return {bool} - 是否已连接
        """
        if not self.connected and self.auto_connect:
            self.logger.info(f"自动连接到CheatEngine服务器 {self.host}:{self.port}")
            return self.connect()
        return self.connected
    
    def _pack_data(self, data: Union[bytes, str], data_type: int) -> bytes:
        """
        打包数据
        
        @param {bytes|str} data - 要发送的数据
        @param {int} data_type - 数据类型
        @return {bytes} - 打包后的数据
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # 打包头部: >HH 表示大端序的两个2字节无符号整数
        header = struct.pack(">HH", data_type, len(data))
        return header + data
    
    def _unpack_data(self, packet: bytes) -> Tuple[Optional[int], Optional[bytes]]:
        """
        解包数据
        
        @param {bytes} packet - 接收到的数据包
        @return {tuple} - (数据类型, 数据内容)
        """
        if not packet or len(packet) < 4:
            return None, None
        
        data_type, length = struct.unpack(">HH", packet[:4])
        
        if len(packet) < 4 + length:
            return None, None
        
        data = packet[4:4+length]
        return data_type, data
    
    def send_text(self, text: str) -> bool:
        """
        发送文本消息
        
        @param {str} text - 要发送的文本
        @return {bool} - 是否发送成功
        """
        if not self.ensure_connected():
            return False
        
        try:
            packet = self._pack_data(text, self.PACKET_TYPE["TEXT"])
            self.socket.sendall(packet)
            self.logger.info(f"已发送文本消息: {text}")
            return True
        except socket.error as e:
            self.logger.error(f"发送失败: {e}")
            self.connected = False
            return False
    
    def receive_response(self, buffer_size: int = 16384, 
                         retry_count: int = 2, 
                         retry_interval: float = 0.5) -> Tuple[Optional[int], Optional[bytes]]:
        """
        接收服务器响应
        
        @param {int} buffer_size - 缓冲区大小
        @param {int} retry_count - 接收超时时的重试次数
        @param {float} retry_interval - 重试间隔时间(秒)
        @return {tuple} - (数据类型, 数据内容)
        """
        if not self.connected:
            self.logger.error("未连接到CheatEngine服务器")
            return None, None
        
        # 重试逻辑
        for attempt in range(retry_count + 1):
            try:
                if attempt > 0:
                    self.logger.info(f"正在尝试接收响应... (第{attempt}/{retry_count}次)")
                
                # 接收头部(4字节)
                header_data = b''
                while len(header_data) < 4:
                    chunk = self.socket.recv(4 - len(header_data))
                    if not chunk:
                        self.logger.warning("服务器关闭了连接")
                        self.disconnect()
                        return None, None
                    header_data += chunk
                
                # 解析头部，获取类型和长度
                data_type, length = struct.unpack(">HH", header_data)
                
                # 接收完整数据
                content = b''
                remaining = length
                
                while remaining > 0:
                    # 每次读取剩余数据量或缓冲区大小中的较小值
                    read_size = min(buffer_size, remaining)
                    chunk = self.socket.recv(read_size)
                    
                    if not chunk:
                        self.logger.warning("接收数据过程中连接关闭")
                        self.disconnect()
                        return None, None
                    
                    content += chunk
                    remaining -= len(chunk)
                
                return data_type, content
                
            except socket.timeout:
                if attempt < retry_count:
                    self.logger.warning(f"接收超时，等待{retry_interval}秒后重试...")
                    time.sleep(retry_interval)
                else:
                    self.logger.warning("接收超时，已达到最大重试次数")
                    return None, None
            except socket.error as e:
                self.logger.error(f"接收失败: {e}")
                self.disconnect()
                return None, None
        
        return None, None
    
    def check_server(self, timeout: int = 2) -> bool:
        """
        检查服务器状态
        
        @param {int} timeout - 检测超时时间(秒)
        @return {bool} - 服务器是否正常响应
        """
        if not self.ensure_connected():
            return False
            
        self.logger.info("正在检测CheatEngine服务器状态...")
        
        # 备份当前超时设置
        original_timeout = self.socket.gettimeout()
        self.socket.settimeout(timeout)
        
        try:
            # 发送一个简单的文本消息检测连接状态
            ping_message = "PING"
            packet = self._pack_data(ping_message, self.PACKET_TYPE["TEXT"])
            self.socket.sendall(packet)
            
            # 尝试接收响应
            data_type, content = self.receive_response(retry_count=0)
            
            # 恢复原始超时设置
            self.socket.settimeout(original_timeout)
            
            if data_type is not None:
                self.logger.info("CheatEngine服务器状态正常")
                return True
            else:
                self.logger.warning("CheatEngine服务器无响应")
                return False
                
        except socket.error as e:
            self.logger.error(f"检测CheatEngine服务器状态时发生错误: {e}")
            self.connected = False
            return False
        finally:
            # 确保恢复原始超时设置
            try:
                self.socket.settimeout(original_timeout)
            except:
                pass


def create_ce_client(host: Optional[str] = None, 
                     port: Optional[int] = None, 
                     timeout: Optional[int] = None, 
                     auto_connect: bool = True) -> CESocketClient:
    """
    创建CheatEngine客户端实例
    
    参数:
    - host: 服务器主机名或IP地址，默认使用全局配置
    - port: 服务器端口，默认使用全局配置
    - timeout: 连接超时时间，默认使用全局配置
    - auto_connect: 是否自动连接，默认为True
    
    返回:
    - 创建的CESocketClient实例
    """
    # 使用参数或默认配置
    actual_host = host or cheatEngine_config["host"]
    actual_port = port or cheatEngine_config["port"]
    actual_timeout = timeout or cheatEngine_config["timeout"]
    
    # 创建客户端实例
    client = CESocketClient(
        host=actual_host,
        port=actual_port,
        timeout=actual_timeout,
        auto_connect=auto_connect,
        max_retries=cheatEngine_config["retries"]
    )
    
    # 如果设置了自动连接，则尝试连接
    if auto_connect:
        client.connect()
    
    return client


def update_ce_config(host: Optional[str] = None, 
                     port: Optional[int] = None, 
                     timeout: Optional[int] = None, 
                     retries: Optional[int] = None) -> None:
    """
    更新CheatEngine连接配置
    
    参数:
    - host: 服务器主机名或IP地址
    - port: 服务器端口
    - timeout: 连接超时时间(秒)
    - retries: 重试次数
    """
    global cheatEngine_config
    
    # 只更新提供的参数
    if host is not None:
        cheatEngine_config["host"] = host
    
    if port is not None:
        cheatEngine_config["port"] = port
    
    if timeout is not None:
        cheatEngine_config["timeout"] = timeout
    
    if retries is not None:
        cheatEngine_config["retries"] = retries
    
    logger.info(f"已更新CheatEngine连接配置: {cheatEngine_config}")
