# MCP CheatEngine工具集开发指南

本文档面向希望扩展或修改MCP CheatEngine工具集的开发者，详细介绍项目架构和扩展方法。

## 项目架构

MCP CheatEngine工具集采用模块化设计，主要组件包括：

1. **主程序(main.py)**：负责加载工具模块和启动MCP服务
2. **辅助函数模块(util.py)**：提供各工具共享的辅助函数
3. **工具模块(tools/)**：包含各个功能工具的实现

### 目录结构

```
mcp-cheatengine-Cto/
├── main.py             # 主程序入口
├── util.py             # 通用辅助函数
├── requirements.txt    # 依赖项
├── README.md           # 项目说明
├── docs/               # 文档目录
│   ├── usage.md        # 使用说明
│   ├── api.md          # API参考
│   └── development.md  # 开发指南
└── tools/              # 工具模块目录
    ├── __init__.py     # 工具包初始化
    ├── ce_connect/     # 连接工具
    ├── memory_tools/   # 内存操作工具
    └── test_tool/      # 测试工具
```

## 添加新工具

要添加新工具，请按照以下步骤操作：

1. 在`tools/`目录下创建新的工具目录，例如`tools/my_new_tool/`
2. 在工具目录中创建`__init__.py`和`tool.py`文件
3. 在`tool.py`中实现工具功能并提供`register_tool`函数

### 工具模板

以下是新工具的基本模板：

```python
"""
新工具模块

工具功能描述
"""
from util import logger  # 导入必要的模块

# 工具描述，将显示在MCP界面中
TOOL_DESCRIPTION = """
    工具的描述信息
    
    参数:
    - param1: 参数1的说明
    - param2: 参数2的说明
    
    返回:
    - 返回值说明
"""

def my_tool_function(param1, param2=None):
    """
    工具函数的实现
    
    Args:
        param1: 参数1
        param2: 参数2(可选)
        
    Returns:
        处理结果
    """
    # 记录日志
    logger.info(f"工具函数被调用: param1={param1}, param2={param2}")
    
    # 功能实现
    result = {
        "success": True,
        "param1": param1,
        "param2": param2,
        "result": "处理结果"
    }
    
    return result

# 为MCP创建适配器函数(如果需要)
def tool_adapter(param1=None, param2=None):
    """
    适配MCP接口的包装函数
    
    Args:
        param1: 参数1
        param2: 参数2
        
    Returns:
        工具函数的返回结果
    """
    try:
        return my_tool_function(param1, param2)
    except Exception as e:
        logger.error(f"工具执行错误: {str(e)}")
        return {
            "success": False,
            "error": f"处理错误: {str(e)}"
        }

def register_tool(mcp):
    """
    向MCP注册工具
    
    Args:
        mcp: MCP实例
    """
    # 注册工具函数
    mcp.tool(description=TOOL_DESCRIPTION)(tool_adapter)
```

## CheatEngine通信

如果您的工具需要与CheatEngine通信，可以使用`util.py`中提供的`create_ce_client`函数创建客户端实例：

```python
from util import create_ce_client

# 创建CE客户端
client = create_ce_client(auto_connect=True)

# 发送请求
# ... 实现通信逻辑 ...
```

## 数据包结构

与CheatEngine通信的数据包遵循以下格式：

- 2字节类型标识
- 2字节数据长度
- 变长数据内容

工具开发时可使用`CESocketClient`类的`_pack_data`和`_unpack_data`方法处理数据包。

## 错误处理

工具函数应当捕获所有可能的异常，并返回统一格式的错误信息：

```python
try:
    # 功能实现
    result = process_data(input_data)
    return {"success": True, "data": result}
except Exception as e:
    logger.error(f"处理错误: {str(e)}")
    return {"success": False, "error": f"处理错误: {str(e)}"}
```

## 测试

开发新工具时，建议创建单元测试并使用模拟数据进行验证。测试文件可以放在工具目录中，例如`tools/my_new_tool/test.py`。

## 文档

为新工具添加文档，包括：

1. 在`tool.py`中使用详细的函数文档字符串
2. 更新`docs/api.md`，添加新工具的API说明
3. 在`docs/usage.md`中添加使用示例

## 贡献流程

1. Fork项目仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

请确保遵循项目的代码风格和命名约定。