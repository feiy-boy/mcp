Here’s the full code with all comments and log messages translated to English (code logic remains unchanged):

```python
"""
Global Hotel Booking MCP Client
Used to call MCP tools provided by server.py
"""
import asyncio
from typing import Optional, List, Any, Dict
from contextlib import asynccontextmanager

from fastmcp import Client
from loguru import logger


class DhubMCPClient:
    """Global Hotel Booking MCP Client"""
    
    def __init__(self, base_url: str = "https://mcp.fusionconnectgroup.com/mcp"):
        """
        Initialize MCP Client
        
        Args:
            base_url: Base URL of the MCP service
        """
        self.base_url = base_url
        self.client = Client(base_url)
        self.available_tools: List[Any] = []
    
    @asynccontextmanager
    async def connect(self):
        """Connect to MCP Server"""
        logger.info(f"Connecting to MCP Server: {self.base_url}")
        
        async with self.client:
            # Test connection
            try:
                await self.client.ping()
                logger.info("[OK] Connected to Global Hotel MCP Server")
            except Exception as e:
                logger.warning(f"Ping failed, but continuing to try: {e}")
            
            # List available tools
            try:
                tools_result = await self.client.list_tools()
                
                # Process return result
                if hasattr(tools_result, 'tools'):
                    self.available_tools = tools_result.tools
                elif isinstance(tools_result, list):
                    self.available_tools = tools_result
                else:
                    self.available_tools = []
                
                logger.info(f"Number of available tools: {len(self.available_tools)}")
                for tool in self.available_tools:
                    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                    tool_desc = tool.description if hasattr(tool, 'description') else ''
                    logger.info(f"  - {tool_name}: {tool_desc}")
            except Exception as e:
                logger.error(f"Failed to get tool list: {e}")
            
            yield self
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call MCP Tool"""
        logger.info(f"Calling tool: {tool_name}")
        logger.debug(f"Arguments: {arguments}")
        
        try:
            result = await self.client.call_tool(tool_name, arguments)
            
            # Extract text content
            if hasattr(result, 'content') and result.content:
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        return content_item.text
                    elif hasattr(content_item, 'type') and content_item.type == 'text':
                        return str(content_item)
            
            return str(result)
            
        except Exception as e:
            logger.error(f"Error occurred while calling tool: {e}")
            raise
    
    async def search_hotels_by_address(
        self,
        x_api_key: str,
        x_secret_key: str,
        lng_google: float,
        lat_google: float,
        check_in_date: str,
        check_out_date: str,
        language: str = "en-US",
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        star_ratings: Optional[List[str]] = None,
        distance: int = 5,
        page_size: int = 20
    ) -> str:
        """
        Search Hotels by Address
        
        Args:
            x_api_key: User's API key
            x_secret_key: User's Secret key
            lng_google: Google longitude (keep 6 decimal places)
            lat_google: Google latitude (keep 6 decimal places)
            check_in_date: Check-in date (format: yyyy-MM-dd)
            check_out_date: Check-out date (format: yyyy-MM-dd)
            language: Language type, default en-US, optional zh-CN
            price_min: Minimum price
            price_max: Maximum price
            star_ratings: List of star ratings
            distance: Distance range, unit: km, default 5
            page_size: Number of items per page, default 20, max 50
        
        Returns:
            Hotel list information
        """
        arguments = {
            "x_api_key": x_api_key,
            "x_secret_key": x_secret_key,
            "lng_google": lng_google,
            "lat_google": lat_google,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "language": language,
            "distance": distance,
            "page_size": page_size
        }
        
        if price_min is not None:
            arguments["price_min"] = price_min
        if price_max is not None:
            arguments["price_max"] = price_max
        if star_ratings is not None:
            arguments["star_ratings"] = star_ratings
        
        return await self.call_tool("search_hotels_by_address", arguments)
    
    async def search_hotels_by_hotel_name(
        self,
        x_api_key: str,
        x_secret_key: str,
        keyword: str,
        check_in_date: str,
        check_out_date: str,
        language: str = "en-US",
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        star_ratings: Optional[List[str]] = None,
        distance: int = 5,
        page_size: int = 20
    ) -> str:
        """
        Search Hotels by Hotel Name
        
        Args:
            x_api_key: User's API key
            x_secret_key: User's Secret key
            keyword: Hotel name
            check_in_date: Check-in date (format: yyyy-MM-dd)
            check_out_date: Check-out date (format: yyyy-MM-dd)
            language: Language type, default en-US, optional zh-CN
            price_min: Minimum price
            price_max: Maximum price
            star_ratings: List of star ratings
            distance: Distance range, unit: km, default 5
            page_size: Number of items per page, default 20, max 50
        
        Returns:
            Hotel list information
        """
        arguments = {
            "x_api_key": x_api_key,
            "x_secret_key": x_secret_key,
            "keyword": keyword,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "language": language,
            "distance": distance,
            "page_size": page_size
        }
        
        if price_min is not None:
            arguments["price_min"] = price_min
        if price_max is not None:
            arguments["price_max"] = price_max
        if star_ratings is not None:
            arguments["star_ratings"] = star_ratings
        
        return await self.call_tool("search_hotels_by_hotel_name", arguments)
    
    async def get_hotel_details(
        self,
        x_api_key: str,
        x_secret_key: str,
        hotel_id: int,
        language: str = "en-US",
        need_facility: bool = True
    ) -> str:
        """
        Get Hotel Detailed Information
        
        Args:
            x_api_key: User's API key
            x_secret_key: User's Secret key
            hotel_id: Hotel ID
            language: Language type, default en-US, optional zh-CN
            need_facility: Whether to include facility information, default True
        
        Returns:
            Detailed hotel information
        """
        arguments = {
            "x_api_key": x_api_key,
            "x_secret_key": x_secret_key,
            "hotel_id": hotel_id,
            "language": language,
            "need_facility": need_facility
        }
        
        return await self.call_tool("get_hotel_details", arguments)
    
    async def check_hotel_price(
        self,
        x_api_key: str,
        x_secret_key: str,
        hotel_id: int,
        check_in_date: str,
        check_out_date: str,
        num_of_adults: int = 2,
        num_of_children: int = 0,
        nationality: str = "CN",
        language: str = "en-US"
    ) -> str:
        """
        Check Hotel Real-time Price and Available Room Types
        
        Args:
            x_api_key: User's API key
            x_secret_key: User's Secret key
            hotel_id: Hotel ID
            check_in_date: Check-in date (format: YYYY-MM-DD)
            check_out_date: Check-out date (format: YYYY-MM-DD)
            num_of_adults: Number of adults, default 2
            num_of_children: Number of children, default 0
            nationality: Nationality code (ISO 2-digit code), default CN
            language: Language type, default en-US, optional zh-CN
        
        Returns:
            Detailed price information
        """
        arguments = {
            "x_api_key": x_api_key,
            "x_secret_key": x_secret_key,
            "hotel_id": hotel_id,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "num_of_adults": num_of_adults,
            "num_of_children": num_of_children,
            "nationality": nationality,
            "language": language
        }
        
        return await self.call_tool("check_hotel_price", arguments)


async def main():
    """Example: Use MCP Client"""
    
    # Read API keys from environment variables
    api_key = "dhub_TLY************wu_CNaK-rM"
    secret_key = "vYMbUrYmfviHrKGCm***************uVQnYJtaqv73"
    
    if not api_key or not secret_key:
        logger.error("❌ Please set environment variables X_API_KEY and X_SECRET_KEY")
        return
    
    client = DhubMCPClient()
    
    async with client.connect():
        logger.info("\n" + "="*60)
        logger.info("Start testing Global Hotel MCP Client")
        logger.info("="*60 + "\n")
        
        # Example 1: Search by hotel name
        logger.info("📍 Example 1: Search hotels in Tokyo")
        logger.info("-" * 60)
        
        try:
            result = await client.search_hotels_by_hotel_name(
                x_api_key=api_key,
                x_secret_key=secret_key,
                keyword="Changchun",
                check_in_date="2025-12-01",
                check_out_date="2025-12-03",
                language="en-US",
                page_size=5
            )
            logger.info(f"\nSearch results:\n{result}\n")
        except Exception as e:
            logger.error(f"Search failed: {e}")
        
        # Example 2: Search by address (longitude/latitude)
        logger.info("\n📍 Example 2: Search hotels by longitude and latitude")
        logger.info("-" * 60)
        
        try:
            result = await client.search_hotels_by_address(
                x_api_key=api_key,
                x_secret_key=secret_key,
                lng_google=125.276516,  # Tokyo
                lat_google=43.88597,
                check_in_date="2025-11-21",
                check_out_date="2025-11-23",
                language="zh-CN",
                distance=5,
                page_size=5
            )
            logger.info(f"\nSearch results:\n{result}\n")
        except Exception as e:
            logger.error(f"Search failed: {e}")
        
        # Example 3: Get hotel details (use a sample hotel ID)
        logger.info("\n📍 Example 3: Query hotel details")
        logger.info("-" * 60)
        
        try:
            # Note: Please replace with the actual hotel ID
            hotel_id = 1364848
            result = await client.get_hotel_details(
                x_api_key=api_key,
                x_secret_key=secret_key,
                hotel_id=hotel_id,
                language="en-US",
                need_facility=True
            )
            logger.info(f"\nHotel details:\n{result}\n")
        except Exception as e:
            logger.error(f"Failed to query details: {e}")
        
        # Example 4: Check hotel price
        logger.info("\n📍 Example 4: Query hotel price")
        logger.info("-" * 60)
        
        try:
            # Note: Please replace with the actual hotel ID
            hotel_id = 1364848
            result = await client.check_hotel_price(
                x_api_key=api_key,
                x_secret_key=secret_key,
                hotel_id=hotel_id,
                check_in_date="2025-12-01",
                check_out_date="2025-12-03",
                num_of_adults=2,
                num_of_children=0,
                nationality="CN",
                language="en-US"
            )
            logger.info(f"\nPrice information:\n{result}\n")
        except Exception as e:
            logger.error(f"Failed to query price: {e}")
        
        logger.info("\n" + "="*60)
        logger.info("Test completed")
        logger.info("="*60)


if __name__ == "__main__":
    # Configure logger
    logger.add(
        "logs/mcp_client_{time}.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # Run the client
    asyncio.run(main())
