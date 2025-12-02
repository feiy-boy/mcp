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

### 1. Install Dependencies

```bash
pip install fastmcp loguru python-dotenv
```

Or use the provided requirements file:

```bash
pip install -r requirements.txt
```

### 2. Obtain API Credentials

Contact the platform to get your:
- `x_api_key`: API Key
- `x_secret_key`: Secret Key
- Official Website: https://mcp.fusionconnectgroup.com

## 🎯 Quick Start

### Basic Example

```python
import asyncio
from client import DhubMCPClient

async def main():
    # Initialize client
    client = DhubMCPClient("url endpoint")
    
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

## 📖 API Methods

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

## 💡 Detailed Examples

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
    # api_key = "your_api_key"
    # secret_key = "your_secret_key"
    
    # Initialize client
    client = DhubMCPClient("url endpoint")
    
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
DHUB_API_KEY=your_api_key_here
DHUB_SECRET_KEY=your_secret_key_here
```

Use in code:

```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("DHUB_API_KEY")
secret_key = os.getenv("DHUB_SECRET_KEY")
```

## 🛡️ Error Handling

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

## ❓ Frequently Asked Questions

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

## 📝 Logging

The client automatically logs to the `logs/` directory:
- File name format: `mcp_client_{timestamp}.log`
- Logs are retained for 7 days
- Daily log rotation

View logs:

```bash
tail -f logs/mcp_client_*.log
```

## 🔗 Related Links

- **Server Address**: `https://mcp.fusionconnectgroup.com/sse`
- **Official Website**: https://mcp.fusionconnectgroup.com

## 📄 License

Use in accordance with the project license.

## 🤝 Technical Support

For any questions, please contact the technical support team.

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-28
