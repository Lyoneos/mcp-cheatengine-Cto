# Cheat Engine SocketAPI 通信规则
# version: v1.6
## 通信协议概要

- **服务端地址**：127.0.0.1
- **通信端口**：8082
- **传输协议**：TCP
- **数据包格式**：
  ```
  +-------------+-------------+------------------+
  | 类型(2字节) | 长度(2字节) |   数据(变长)     |
  +-------------+-------------+------------------+
  ```

## 数据包类型

| 类型值 | 常量名称 | 说明 |
|--------|----------|------|
| 0x01   | ASSEMBLY | 汇编代码 |
| 0x02   | BYTECODE | 原始字节码 |
| 0x03   | TEXT     | 文本消息 |
| 0x04   | COMMAND  | 命令 |
| 0x05   | RESPONSE | 响应 |
| 0x10   | MEMORY_READ | 内存读取 |
| 0x11   | MEMORY_WRITE | 内存写入 |
| 0x12   | MEMORY_BATCH | 批量内存读取 |
| 0x13   | ASSEMBLY_WRITE | 汇编代码修改 |
| 0x20   | LUA_EXEC | Lua代码执行 |
| 0x30   | ENUM_MODULES | 枚举进程模块 |
| 0x31   | POINTER_SCAN | 指针扫描 |
| 0x32   | POINTER_READ | 模块偏移指针读取 |
| 0xFF   | ERROR    | 错误 |

## 内存操作API

### 1. 读取内存 (MEMORY_READ, 0x10)

**请求格式**:
```json
{
  "address": "0x12345678",  // 内存地址
  "dataType": "int32",      // 数据类型
  "options": {              // 可选参数
    "endian": "little",     // 字节序，默认little
    "assembly": true,       // 是否返回汇编代码
    "assemblySize": 10,     // 要反汇编的指令数量
    "comments": true,       // 是否返回该地址的注释
    "multiType": true,      // 是否返回多种数据类型解释
    "rawBytes": true,       // 是否返回原始字节
    "bytesSize": 16,        // 读取的原始字节数量
    "opcode": true,         // 是否返回操作码
    "opcodeSize": 10,       // 读取的操作码字节数量
    "instructionMultiType": true // 是否为每条汇编指令提供多类型解释
  }
}
```

**响应格式**:
```json
{
  "success": true,          // 操作是否成功
  "address": "0x12345678",  // 原请求地址
  "dataType": "int32",      // 数据类型
  "value": 12345,           // 读取的主要值
  "bytes": [0x12, 0x34, 0x56, 0x78], // 原始字节(如请求)
  "opcode": [0x89, 0xE5, 0x90, 0xC3], // 操作码(如请求)
  "comments": "注释内容",    // 地址注释(如请求)
  "multiType": {            // 多种类型解释(如请求)
    "int8": 18,
    "uint8": 18,
    "int16": 34464,
    "uint16": 34464,
    "int32": 100000,
    "uint32": 100000,
    "int64": 4294967396100000,
    "uint64": 4294967396100000,
    "float": 1.4012984643248e-40,
    "double": 2.1219957910147e-308,
    "string": "Hello World"
  },
  "assembly": [             // 汇编代码(如请求)
    {
      "address": "0x12345678", 
      "instruction": "12345678 - mov eax, [ebx]", 
      "comment": "这是一个重要的跳转点",
      "annotation": "[ebx]",
      "isFirstInstruction": true,
      "instructionCount": 1,  // 指令序号，表示这是第1条指令
      "multiType": {        // 该指令地址的多类型解释(如请求)
        "int32": 12345,
        "float": 1.2e-12,
        // 更多类型...
      }
    },
    // 中间的指令...
    {
      "address": "0x12345682",
      "instruction": "12345682 - ret",
      "comment": "",
      "instructionCount": 10,  // 指令序号，表示这是第10条指令
      "isLastInstruction": true
    }
  ],
  "instructionCount": 10,   // 指令总数
  "startInstruction": {     // 第一条指令的引用
    "address": "0x12345678",
    "instruction": "12345678 - mov eax, [ebx]",
    "instructionCount": 1
  },
  "endInstruction": {       // 最后一条指令的引用
    "address": "0x12345682",
    "instruction": "12345682 - ret",
    "instructionCount": 10
  },
  "error": null             // 错误信息
}
```

### 2. 写入内存 (MEMORY_WRITE, 0x11)

**请求格式**:
```json
{
  "address": "0x12345678",  // 内存地址
  "value": 12345,           // 要写入的值
  "dataType": "int32",      // 数据类型
  "options": {              // 可选参数
    "endian": "little",     // 字节序
    "conditional": {        // 条件写入
      "previousValue": 0    // 当前值必须等于此值才写入
    },
    "multiValues": {        // 多值写入（相对偏移）
      "4": {                // 相对主地址的偏移量
        "value": 99,        // 要写入的值
        "dataType": "int8"  // 数据类型
      },
      "8": {
        "value": 3.14,
        "dataType": "float"
      }
    }
  }
}
```

**响应格式**:
```json
{
  "success": true,          // 操作是否成功
  "address": "0x12345678",  // 原请求地址
  "dataType": "int32",      // 数据类型
  "value": 12345,           // 写入的值
  "multiValuesResult": {    // 多值写入结果（如请求）
    "4": {
      "success": true,
      "error": null
    },
    "8": {
      "success": true,
      "error": null
    }
  },
  "error": null             // 错误信息
}
```

### 3. 批量读取内存 (MEMORY_BATCH, 0x12)

**请求格式**:
```json
{
  "addresses": ["0x12345678", "0x87654321"],  // 内存地址数组
  "dataType": "int32",      // 所有地址统一的数据类型
  "options": {              // 可选参数，同读取内存
    "assembly": true
  }
}
```

**响应格式**:
```json
{
  "success": true,          // 批量操作整体是否成功
  "dataType": "int32",      // 数据类型
  "results": [              // 结果数组
    {
      "address": "0x12345678",
      "value": 12345,
      "assembly": [...],    // 如请求
      "success": true,
      "error": null
    },
    // 其他地址的结果...
  ]
}
```

## 汇编代码修改API (ASSEMBLY_WRITE, 0x13)

该API允许直接在指定内存地址写入汇编代码，CE会自动将汇编代码转换为机器码并写入内存。

**请求格式**:
```json
{
  "address": "0x12345678",   // 写入地址
  "assembly": "mov eax, 100; push ebx; call 0x12345690", // 汇编代码，可以用分号或换行分隔
  "options": {
    "fillNOP": true,         // 是否用NOP填充多余字节
    "preserveRegisters": true // 是否自动添加保存/恢复寄存器代码
  }
}
```

**响应格式**:
```json
{
  "success": true,           // 操作是否成功
  "address": "0x12345678",   // 写入地址
  "bytesWritten": 12,        // 写入的字节数
  "instructions": [          // 写入的指令列表
    {
      "address": "0x12345678",
      "instruction": "mov eax, 100",
      "bytes": [0xB8, 0x64, 0x00, 0x00, 0x00], 
      "byteSize": 5
    },
    {
      "address": "0x1234567D",
      "instruction": "push ebx",
      "bytes": [0x53],
      "byteSize": 1
    },
    {
      "address": "0x1234567E",
      "instruction": "call 0x12345690",
      "bytes": [0xE8, 0x0D, 0x00, 0x00, 0x00],
      "byteSize": 5
    },
    {
      "address": "0x12345683", 
      "instruction": "nop",  // 自动填充的NOP（如请求）
      "bytes": [0x90],
      "byteSize": 1
    }
  ],
  "error": null              // 错误信息
}
```

## LUA代码执行API (LUA_EXEC, 0x20)

通过Socket API执行CheatEngine的Lua脚本，扩展功能。

**请求格式**:
```json
{
  "script": "return 'Hello ' .. 'World'",  // Lua脚本
  "timeout": 5000,                         // 超时时间(毫秒)
  "params": {                              // 可选参数，通过_G传递给脚本
    "pid": 1234,
    "baseAddr": "0x400000"
  }
}
```

**响应格式**:
```json
{
  "success": true,           // 操作是否成功
  "result": "Hello World",   // Lua脚本返回值
  "output": "Debug output",  // 脚本print输出内容
  "executionTime": 15,       // 执行时间(毫秒)
  "error": null              // 错误信息
}
```

### Lua脚本示例

1. **读取模块信息**
```lua
local modules = getModuleList()
local result = {}
for i=1, #modules do
  result[i] = {
    name = modules[i].Name,
    base = string.format("%X", modules[i].Address),
    size = modules[i].Size
  }
end
return result
```

2. **指针扫描示例**
```lua
local addr = 0x12345678
local offsets = {0x10, 0x20, 0x30}
local baseAddr = getAddress("kernel32.dll")

-- 执行指针解析
local result = resolvePointer(baseAddr, offsets)
return {
  baseAddr = string.format("%X", baseAddr),
  result = result and string.format("%X", result) or "Failed",
  offsets = offsets
}
```

## 模块枚举API (ENUM_MODULES, 0x30)

获取当前进程所有已加载模块的信息。

**请求格式**:
```json
{
  "options": {              // 可选参数
    "nameFilter": "kernel", // 模块名称过滤
    "detailed": true        // 是否返回详细信息
  }
}
```

**响应格式**:
```json
{
  "success": true,
  "modules": [
    {
      "name": "kernel32.dll",
      "baseAddress": "0x77320000",
      "size": 1228800,
      "entryPoint": "0x77343210",
      "path": "C:\\Windows\\System32\\kernel32.dll",
      "sections": [          // 如果detailed=true
        {
          "name": ".text",
          "address": "0x77320400",
          "size": 983040,
          "flags": "rx"      // 权限：r=读, w=写, x=执行
        },
        // 更多区段...
      ],
      "exports": [           // 如果detailed=true
        {
          "name": "CreateFileW",
          "address": "0x77351234",
          "ordinal": 123
        },
        // 更多导出函数...
      ]
    },
    // 更多模块...
  ],
  "error": null
}
```

## 指针扫描API (POINTER_SCAN, 0x31)

执行指针扫描，查找可能的指针路径。

**请求格式**:
```json
{
  "targetAddress": "0x12345678",  // 目标地址
  "options": {
    "maxLevel": 3,                // 最大指针层级
    "maxResults": 10,             // 最大结果数量
    "baseModules": ["kernel32.dll", "user32.dll"], // 基址模块过滤
    "offsetFilter": {             // 偏移过滤
      "min": 0,                   // 最小偏移
      "max": 0x1000,              // 最大偏移
      "alignAs": 4                // 偏移对齐字节
    }
  }
}
```

**响应格式**:
```json
{
  "success": true,
  "targetAddress": "0x12345678",
  "results": [
    {
      "baseModule": "kernel32.dll",
      "baseAddress": "0x77320000",
      "offsets": [0x1234, 0x8, 0x10],
      "resultAddress": "0x12345678", // 解析结果，应当等于目标地址
      "offsetsText": "kernel32.dll+1234,8,10", // 文本表示
      "score": 95                    // 匹配评分
    },
    // 更多结果...
  ],
  "error": null
}
```

## 模块偏移指针读取API (POINTER_READ, 0x32)

解析并读取基于模块偏移的指针链。

**请求格式**:
```json
{
  "baseModule": "kernel32.dll",   // 基址模块名称
  "offsets": [0x1234, 0x8, 0x10], // 偏移链
  "dataType": "int32",            // 读取的数据类型
  "options": {                    // 同memory_read的options
    "assembly": true,
    "assemblySize": 10
  }
}
```

**响应格式**:
```json
{
  "success": true,
  "baseModule": "kernel32.dll",
  "baseAddress": "0x77320000",
  "offsets": [0x1234, 0x8, 0x10],
  "offsetsText": "kernel32.dll+1234,8,10",
  "addressChain": [                // 解析链中的每一步
    {
      "step": 0,
      "offset": null,              // 初始步骤无偏移
      "address": "0x77320000",
      "description": "Base: kernel32.dll"
    },
    {
      "step": 1,
      "offset": 0x1234,
      "address": "0x77321234",
      "description": "kernel32.dll+1234"
    },
    {
      "step": 2,
      "offset": 0x8,
      "address": "0x12340008",     // 在上一步读取的地址上加偏移
      "description": "[kernel32.dll+1234]+8"
    },
    {
      "step": 3,
      "offset": 0x10,
      "address": "0x12345678",     // 最终地址
      "description": "[[kernel32.dll+1234]+8]+10"
    }
  ],
  "finalAddress": "0x12345678",    // 最终解析的内存地址
  "dataType": "int32",
  "value": 12345,                  // 读取的值
  "assembly": [                    // 如请求，同memory_read
    // 汇编指令...
  ],
  "error": null
}
```

## 错误处理

当操作失败时，响应中的`success`字段将为`false`，`error`字段将包含错误信息：

```json
{
  "success": false,
  "error": {
    "code": 3,                    // 错误代码
    "message": "Invalid address", // 错误消息
    "details": "Address 0x12345678 is not accessible" // 详细说明
  }
}
```

### 常见错误代码

| 错误代码 | 说明 |
|--------|------|
| 1 | 一般错误 |
| 2 | 连接错误 |
| 3 | 地址无效或无法访问 |
| 4 | 数据类型无效 |
| 5 | 解析失败 |
| 6 | 无效参数 |
| 7 | 超时 |
| 8 | 权限不足 |
| 9 | 内存保护错误 |
| 10 | 进程操作失败 |
| 11 | 汇编失败 |
| 12 | Lua执行错误 |
| 13 | 模块未找到 |
| 14 | 指针解析失败 |

## 数据类型参考

支持的数据类型列表：

| 数据类型 | 大小(字节) | 说明 |
|---------|---------|------|
| byte    | 1       | 有符号8位整数 |
| ubyte   | 1       | 无符号8位整数 |
| int16   | 2       | 有符号16位整数 |
| uint16  | 2       | 无符号16位整数 |
| int32   | 4       | 有符号32位整数 |
| uint32  | 4       | 无符号32位整数 |
| int64   | 8       | 有符号64位整数 |
| uint64  | 8       | 无符号64位整数 |
| float   | 4       | 单精度浮点数 |
| double  | 8       | 双精度浮点数 |
| string  | 可变     | ANSI字符串(到0结束) |
| wstring | 可变     | UTF-16字符串(到0结束) |
| bytes   | 可变     | 原始字节数组 |
| aob     | 可变     | 字节数组模式(支持通配符) |
| short   | 2       | int16的别名 |
| ushort  | 2       | uint16的别名 |
| long    | 4       | int32的别名 |
| ulong   | 4       | uint32的别名 |
| pointer | 4/8     | 根据进程架构的指针(x86=4字节, x64=8字节) |