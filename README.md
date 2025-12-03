# MCP
Global Hotel Supply Chain Management System

# Global Hotel Booking MCP Client

This is a hotel booking service client based on the FastMCP framework, providing hotel search, detail inquiry, and price query functions.

## 📋 Table of Contents

- [Features](#features)
- [Environment Requirements](#environment-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Methods](#api-methods)
- [Detailed Examples](#detailed-examples)
- [Error Handling](#error-handling)
- [Frequently Asked Questions](#frequently-asked-questions)

## 🚀 Features

- ✅ Search hotels by address (latitude/longitude)
- ✅ Search hotels by hotel name
- ✅ Query detailed hotel information
- ✅ Query real-time hotel prices and available room types
- ✅ Multi-language support (Chinese/English)
- ✅ Asynchronous programming for high performance
- ✅ Comprehensive logging

## 📦 Environment Requirements

- Python 3.8+
- Valid API Key and Secret Key

## 🔧 Installation

# 1. Install Dependencies

```bash
pip install -r requirements.txt
```

# 2. Obtain API Credentials

You can obtain API credentials through two ways: **platform contact** or **self-service registration**. Details are as follows:

### 2.1 Core Credentials

- `x_api_key`: Unique API access key (for identity verification)

- `x_secret_key`: Secret key (for request signature, keep it confidential)

### 2.2 Self-Service Registration (Recommended)

1. **Access Official Website**: [https://mcp.fusionconnectgroup.com](https://mcp.fusionconnectgroup.com)

2. **Register**: Complete registration via email on the official website.

3. **Email Verification**: Receive a verification email after successful registration and click the verification link.

4. **Get Credentials**: The system will send `x_api_key` and `x_secret_key` to your registered email.

### 2.3 Account  Types & Request Quotas

|Account  Type|Request Quota|
|---|---|
|Personal Account |100 requests|
|Enterprise Account |1000 requests|
### 2.4 Request for Additional Quotas

If you need more request quotas, contact us via:

- Email: 1941783199@qq.com


# 3. 🎯 Quick Start

### Basic Example

```python
import asyncio
from client import DhubMCPClient

async def main():
    # Initialize client
    client = DhubMCPClient()
    
    # Connect to server
    async with client.connect():
        # Search hotels
        result = await client.search_hotels_by_hotel_name(
            x_api_key="your_api_key",
            x_secret_key="your_secret_key",
            keyword="Tokyo",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN",
            page_size=10
        )
        print(result)

# Run
asyncio.run(main())
```

# 4. 📖 API Methods

### 1. Search Hotels by Address `search_hotels_by_address`

Search for nearby hotels using latitude and longitude coordinates.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| x_api_key | str | Yes | API Key |
| x_secret_key | str | Yes | Secret Key |
| lng_google | float | Yes | Google longitude (6 decimal places) |
| lat_google | float | Yes | Google latitude (6 decimal places) |
| check_in_date | str | Yes | Check-in date (Format: yyyy-MM-dd) |
| check_out_date | str | Yes | Check-out date (Format: yyyy-MM-dd) |
| language | str | No | Language type, default: en-US, optional: zh-CN |
| price_min | float | No | Minimum price |
| price_max | float | No | Maximum price |
| star_ratings | List[str] | No | Star rating list, e.g., ["3", "4", "5"] |
| distance | int | No | Distance range in km, default: 5 |
| page_size | int | No | Number of results per page, default: 20, max: 50 |

**Example:**

```python
result = await client.search_hotels_by_address(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    lng_google=139.691706,  # Tokyo Station
    lat_google=35.689487,
    check_in_date="2025-12-01",
    check_out_date="2025-12-03",
    language="zh-CN",
    distance=5,
    page_size=20
)
```

### 2. Search Hotels by Name `search_hotels_by_hotel_name`

Search for hotels using keywords in the hotel name.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| x_api_key | str | Yes | API Key |
| x_secret_key | str | Yes | Secret Key |
| keyword | str | Yes | Hotel name keyword |
| check_in_date | str | Yes | Check-in date (Format: yyyy-MM-dd) |
| check_out_date | str | Yes | Check-out date (Format: yyyy-MM-dd) |
| language | str | No | Language type, default: en-US, optional: zh-CN |
| price_min | float | No | Minimum price |
| price_max | float | No | Maximum price |
| star_ratings | List[str] | No | Star rating list |
| distance | int | No | Distance range in km, default: 5 |
| page_size | int | No | Number of results per page, default: 20, max: 50 |

**Example:**

```python
result = await client.search_hotels_by_hotel_name(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    keyword="Hilton",
    check_in_date="2025-12-01",
    check_out_date="2025-12-03",
    language="zh-CN",
    price_min=500.0,
    price_max=2000.0,
    star_ratings=["4", "5"],
    page_size=10
)
```

### 3. Query Hotel Details `get_hotel_details`

Get detailed information about a hotel using its ID.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| x_api_key | str | Yes | API Key |
| x_secret_key | str | Yes | Secret Key |
| hotel_id | int | Yes | Hotel ID |
| language | str | No | Language type, default: en-US, optional: zh-CN |
| need_facility | bool | No | Whether to include facility information, default: True |

**Example:**

```python
result = await client.get_hotel_details(
    x_api_key="your_api_key",
    x_secret_key="your_secret_key",
    hotel_id=1364848,
    language="zh-CN",
    need_facility=True
)
```

### 4. Check Hotel Price `check_hotel_price`

Query real-time prices and available room types for a specific hotel.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| x_api_key | str | Yes | API Key |
| x_secret_key | str | Yes | Secret Key |
| hotel_id | int | Yes | Hotel ID |
| check_in_date | str | Yes | Check-in date (Format: yyyy-MM-dd) |
| check_out_date | str | Yes | Check-out date (Format: yyyy-MM-dd) |
| num_of_adults | int | No | Number of adults, default: 2 |
| num_of_children | int | No | Number of children, default: 0 |
| nationality | str | No | Nationality code (ISO 2-digit), default: CN |
| language | str | No | Language type, default: en-US, optional: zh-CN |

**Example:**

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

# 5. 💡 Detailed Examples

### Complete Workflow

```python
import asyncio
from client import DhubMCPClient
from loguru import logger
import os

async def hotel_search_workflow():
    """Complete hotel search workflow"""
    
    # Get credentials from environment variables (recommended)
    api_key = os.getenv("DHUB_API_KEY")
    secret_key = os.getenv("DHUB_SECRET_KEY")
    
    # Or use credentials directly (not recommended for production)
    # x_api_key = "your_api_key"
    # x_secret_key = "your_secret_key"
    
    # Initialize client
    client = DhubMCPClient()
    
    async with client.connect():
        # Step 1: Search for hotels
        logger.info("Step 1: Search for hotels in Tokyo")
        search_result = await client.search_hotels_by_hotel_name(
            x_api_key=api_key,
            x_secret_key=secret_key,
            keyword="Tokyo",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN",
            page_size=5
        )
        print(f"Search Results: {search_result}\n")
        
        # Step 2: Assume hotel ID is obtained from search results
        hotel_id = 1364848  # Extract from search results in actual use
        
        # Step 3: Query hotel details
        logger.info(f"Step 2: Query details for hotel {hotel_id}")
        details = await client.get_hotel_details(
            x_api_key=api_key,
            x_secret_key=secret_key,
            hotel_id=hotel_id,
            language="zh-CN",
            need_facility=True
        )
        print(f"Hotel Details: {details}\n")
        
        # Step 4: Query price
        logger.info(f"Step 3: Check price for hotel {hotel_id}")
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
        print(f"Price Information: {price}\n")

if __name__ == "__main__":
    asyncio.run(hotel_search_workflow())
```

### Manage Credentials with Environment Variables

Create a `.env` file:

```env
X_API_KEY=your_api_key_here
X_SECRET_KEY=your_secret_key_here
```

Use in code:

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("X_API_KEY")
secret_key = os.getenv("X_SECRET_KEY")
```


# 6. 🖥️ Cursor IDE Configuration

To use this MCP service in Cursor IDE, add the following configuration to your `mcp.json` file:

**Configuration file location:**
- Windows: `C:\Users\<username>\.cursor\mcp.json`
- macOS: `~/.cursor/mcp.json`
- Linux: `~/.cursor/mcp.json`

**Configuration content:**

```json
{
  "mcpServers": {
    "global_hotel_mcp": {
      "name": "Global Hotel MCP",
      "type": "http",
      "url": "https://mcp.fusionconnectgroup.com/mcp",
      "env": {
        "x_api_key": "your_api_key_here",
        "x_secret_key": "your_secret_key_here"
      }
    }
  }
}
```

**Configuration Parameters:**

| Parameter | Description |
|-----------|-------------|
| `name` | Display name in Cursor |
| `type` | Connection type, use `http` |
| `url` | MCP service endpoint URL |
| `env.x_api_key` | Your API Key |
| `env.x_secret_key` | Your Secret Key |

**Steps:**

1. Open or create the `mcp.json` file at the location above
2. Copy the configuration content and replace with your actual API credentials
3. Save the file
4. Restart Cursor IDE
5. The MCP tools will be available in Cursor's AI assistant

**Verification:**

After configuration, you can verify by asking Cursor's AI assistant:
- "Search for hotels in Tokyo"
- "Find hotel details for hotel ID 1364848"
  
# 7. 🛡️ Error Handling

It is recommended to use try-except blocks to handle potential errors:

```python
async with client.connect():
    try:
        result = await client.search_hotels_by_hotel_name(
            x_api_key=api_key,
            x_secret_key=secret_key,
            keyword="Tokyo",
            check_in_date="2025-12-01",
            check_out_date="2025-12-03",
            language="zh-CN"
        )
        print(result)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        # Handle error
```

Common Error Types:
- **Authentication Failed**: Check if API Key and Secret Key are correct
- **Connection Timeout**: Check network connection
- **Invalid Parameters**: Verify date format, hotel ID, and other parameters

# 8. ❓ Frequently Asked Questions

### Q1: How to obtain API credentials?

Contact the platform to apply for API Key and Secret Key.

### Q2: Which languages are supported?

Currently supported:
- `en-US`: English
- `zh-CN`: Chinese

### Q3: What is the date format?

- Check-in/check-out date format: `yyyy-MM-dd` (e.g., `2025-12-01`)
- Must be a future date
- Check-out date must be later than check-in date

### Q4: How to change the server address?

To connect to a different server:

```python
client = DhubMCPClient(base_url="https://your-custom-url.com/mcp")
```

### Q5: How to fix garbled characters in Windows Command Prompt?

This is an encoding issue and does not affect functionality. You can:
1. Use PowerShell instead of CMD
2. Set environment variables:
   ```bash
   set PYTHONIOENCODING=utf-8
   chcp 65001
   ```

### Q6: How to test if the connection is working?

Run the client file:

```bash
python client.py
```

This will execute the built-in test example.


# 9. 🔗 Related Links

- **Server Address**: `https://mcp.fusionconnectgroup.com/mcp`
- **Official Website**: https://mcp.fusionconnectgroup.com

## 📄 License

Use in accordance with the project license.

## 🤝 Technical Support

For any questions, please contact the technical support team.

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-28
