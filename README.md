# mcp
Global Hotel Supply Chain Management System

# Dhub 酒店预订 MCP 客户端

这是一个基于 FastMCP 框架的酒店预订服务客户端，提供酒店搜索、详情查询和价格查询功能。

## 📋 目录

- [功能特性](#功能特性)
- [环境要求](#环境要求)
- [安装](#安装)
- [快速开始](#快速开始)
- [API 方法](#api-方法)
- [详细示例](#详细示例)
- [错误处理](#错误处理)
- [常见问题](#常见问题)

## 🚀 功能特性

- ✅ 通过地址（经纬度）搜索酒店
- ✅ 通过酒店名称搜索酒店
- ✅ 查询酒店详细信息
- ✅ 查询酒店实时价格和可用房型
- ✅ 支持多语言（中文/英文）
- ✅ 异步编程，高性能
- ✅ 完整的日志记录

## 📦 环境要求

- Python 3.8+
- 有效的 Dhub API 密钥和 Secret 密钥

## 🔧 安装

### 1. 安装依赖

```bash
pip install fastmcp loguru python-dotenv
```

或使用提供的依赖文件：

```bash
pip install -r requirements-client.txt
```

### 2. 获取 API 凭证

联系 Dhub 平台获取您的：
- `x_api_key`: API 密钥
- `x_secret_key`: Secret 密钥
- 官网获取：https://mcp.mongoso.vip
- 
## 🎯 快速开始

### 基础示例

```python
import asyncio
from client import DhubMCPClient

async def main():
    # 初始化客户端
    client = DhubMCPClient()
    
    # 连接到服务器
    async with client.connect():
        # 搜索酒店
        result = await client.search_hotels_by_hotel_name(
            x_api_key="your_api_key",
            x_secret_key="your_secret_key",
            keyword="东京",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN",
            page_size=10
        )
        print(result)

# 运行
asyncio.run(main())
```

## 📖 API 方法

### 1. 通过地址搜索酒店 `search_hotels_by_address`

通过经纬度坐标搜索附近的酒店。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_api_key | str | 是 | API 密钥 |
| x_secret_key | str | 是 | Secret 密钥 |
| lng_google | float | 是 | 谷歌经度（保留6位小数） |
| lat_google | float | 是 | 谷歌纬度（保留6位小数） |
| check_in_date | str | 是 | 入住日期（格式：yyyy-MM-dd） |
| check_out_date | str | 是 | 退房日期（格式：yyyy-MM-dd） |
| language | str | 否 | 语言类型，默认 en-US，可选 zh-CN |
| price_min | float | 否 | 最低价格 |
| price_max | float | 否 | 最高价格 |
| star_ratings | List[str] | 否 | 星级列表，如 ["3", "4", "5"] |
| distance | int | 否 | 距离范围，单位 km，默认 5 |
| page_size | int | 否 | 每页数量，默认 20，最大 50 |

**示例：**

```python
result = await client.search_hotels_by_address(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    lng_google=139.691706,  # 东京站
    lat_google=35.689487,
    check_in_date="2025-12-01",
    check_out_date="2025-12-03",
    language="zh-CN",
    distance=5,
    page_size=20
)
```

### 2. 通过酒店名称搜索 `search_hotels_by_hotel_name`

通过酒店名称关键词搜索酒店。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_api_key | str | 是 | API 密钥 |
| x_secret_key | str | 是 | Secret 密钥 |
| keyword | str | 是 | 酒店名称关键词 |
| check_in_date | str | 是 | 入住日期（格式：yyyy-MM-dd） |
| check_out_date | str | 是 | 退房日期（格式：yyyy-MM-dd） |
| language | str | 否 | 语言类型，默认 en-US，可选 zh-CN |
| price_min | float | 否 | 最低价格 |
| price_max | float | 否 | 最高价格 |
| star_ratings | List[str] | 否 | 星级列表 |
| distance | int | 否 | 距离范围，单位 km，默认 5 |
| page_size | int | 否 | 每页数量，默认 20，最大 50 |

**示例：**

```python
result = await client.search_hotels_by_hotel_name(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    keyword="希尔顿",
    check_in_date="2025-12-01",
    check_out_date="2025-12-03",
    language="zh-CN",
    price_min=500.0,
    price_max=2000.0,
    star_ratings=["4", "5"],
    page_size=10
)
```

### 3. 查询酒店详细信息 `get_hotel_details`

根据酒店 ID 获取酒店的详细信息。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_api_key | str | 是 | API 密钥 |
| x_secret_key | str | 是 | Secret 密钥 |
| hotel_id | int | 是 | 酒店 ID |
| language | str | 否 | 语言类型，默认 en-US，可选 zh-CN |
| need_facility | bool | 否 | 是否包含设施信息，默认 True |

**示例：**

```python
result = await client.get_hotel_details(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    hotel_id=1364848,
    language="zh-CN",
    need_facility=True
)
```

### 4. 查询酒店价格 `check_hotel_price`

查询指定酒店的实时价格和可用房型。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| x_api_key | str | 是 | API 密钥 |
| x_secret_key | str | 是 | Secret 密钥 |
| hotel_id | int | 是 | 酒店 ID |
| check_in_date | str | 是 | 入住日期（格式：YYYY-MM-DD） |
| check_out_date | str | 是 | 退房日期（格式：YYYY-MM-DD） |
| num_of_adults | int | 否 | 成人数量，默认 2 |
| num_of_children | int | 否 | 儿童数量，默认 0 |
| nationality | str | 否 | 国籍代码（ISO 2位代码），默认 CN |
| language | str | 否 | 语言类型，默认 en-US，可选 zh-CN |

**示例：**

```python
result = await client.check_hotel_price(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    hotel_id=1364848,
    check_in_date="2025-12-01",
    check_out_date="2025-12-03",
    num_of_adults=2,
    num_of_children=1,
    nationality="CN",
    language="zh-CN"
)
```

## 💡 详细示例

### 完整工作流程

```python
import asyncio
from client import DhubMCPClient
from loguru import logger
import os

async def hotel_search_workflow():
    """完整的酒店搜索工作流程"""
    
    # 从环境变量获取凭证（推荐）
    api_key = os.getenv("DHUB_API_KEY")
    secret_key = os.getenv("DHUB_SECRET_KEY")
    
    # 或直接使用凭证（不推荐在生产环境中）
    # api_key = "your_api_key"
    # secret_key = "your_secret_key"
    
    # 初始化客户端
    client = DhubMCPClient()
    
    async with client.connect():
        # 步骤1: 搜索酒店
        logger.info("步骤1: 搜索东京的酒店")
        search_result = await client.search_hotels_by_hotel_name(
            x_api_key=api_key,
            x_secret_key=secret_key,
            keyword="东京",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN",
            page_size=5
        )
        print(f"搜索结果: {search_result}\n")
        
        # 步骤2: 假设从搜索结果中得到了酒店ID
        hotel_id = 1364848  # 实际使用时从搜索结果中提取
        
        # 步骤3: 查询酒店详情
        logger.info(f"步骤2: 查询酒店 {hotel_id} 的详细信息")
        details = await client.get_hotel_details(
            x_api_key=api_key,
            x_secret_key=secret_key,
            hotel_id=hotel_id,
            language="zh-CN",
            need_facility=True
        )
        print(f"酒店详情: {details}\n")
        
        # 步骤4: 查询价格
        logger.info(f"步骤3: 查询酒店 {hotel_id} 的价格")
        price = await client.check_hotel_price(
            x_api_key=api_key,
            x_secret_key=secret_key,
            hotel_id=hotel_id,
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            num_of_adults=2,
            num_of_children=0,
            nationality="CN",
            language="zh-CN"
        )
        print(f"价格信息: {price}\n")

if __name__ == "__main__":
    asyncio.run(hotel_search_workflow())
```

### 使用环境变量管理凭证

创建 `.env` 文件：

```env
DHUB_API_KEY=your_api_key_here
DHUB_SECRET_KEY=your_secret_key_here
```

在代码中使用：

```python
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

api_key = os.getenv("DHUB_API_KEY")
secret_key = os.getenv("DHUB_SECRET_KEY")
```

## 🛡️ 错误处理

建议使用 try-except 块处理可能的错误：

```python
async with client.connect():
    try:
        result = await client.search_hotels_by_hotel_name(
            x_api_key=api_key,
            x_secret_key=secret_key,
            keyword="东京",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN"
        )
        print(result)
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        # 处理错误
```

常见错误类型：
- **认证失败**: 检查 API Key 和 Secret Key 是否正确
- **连接超时**: 检查网络连接
- **参数错误**: 检查日期格式、酒店ID等参数是否正确

## ❓ 常见问题

### Q1: 如何获取 API 凭证？

联系 Dhub 平台申请 API 密钥和 Secret 密钥。

### Q2: 支持哪些语言？

目前支持：
- `en-US`: 英文
- `zh-CN`: 中文

### Q3: 日期格式是什么？

- 入住/退房日期格式：`yyyy-MM-dd`（例如：`2025-12-01`）
- 必须是未来的日期
- 退房日期必须晚于入住日期

### Q4: 如何更改服务器地址？

如果需要连接到不同的服务器：

```python
client = DhubMCPClient(base_url="https://your-custom-url.com/mcp")
```

### Q5: Windows 控制台显示乱码怎么办？

这是编码问题，不影响功能。可以：
1. 使用 PowerShell 而不是 CMD
2. 设置环境变量：
   ```bash
   set PYTHONIOENCODING=utf-8
   chcp 65001
   ```

### Q6: 如何测试连接是否正常？

运行客户端文件：

```bash
python client.py
```

这将执行内置的测试示例。

## 📝 日志

客户端会自动记录日志到 `logs/` 目录：
- 文件名格式：`mcp_client_{时间}.log`
- 日志保留 7 天
- 每天轮换一次

查看日志：

```bash
tail -f logs/mcp_client_*.log
```

## 🔗 相关链接

- **服务器地址**: `https://mcp.mongoso.vip/dhub_mcp/mcp`
- **官网地址**:  https://mcp.mongoso.vip

## 📄 许可证

根据项目许可证使用。

## 🤝 技术支持

如有问题，请联系 Dhub 技术支持团队。

---

**版本**: 1.0.0  
**更新日期**: 2025-11-28

