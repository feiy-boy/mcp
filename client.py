"""
Dhub酒店预订MCP客户端
用于调用server.py提供的MCP工具
"""
import asyncio
from typing import Optional, List, Any, Dict
from contextlib import asynccontextmanager

from fastmcp import Client
from loguru import logger


class DhubMCPClient:
    """Dhub酒店预订MCP客户端"""
    
    def __init__(self, base_url: str = "https://dhub-mcp.mongoso.vip/dhub_mcp/mcp"):
        """
        初始化MCP客户端
        
        Args:
            base_url: MCP服务的基础URL
        """
        self.base_url = base_url
        self.client = Client(base_url)
        self.available_tools: List[Any] = []
    
    @asynccontextmanager
    async def connect(self):
        """连接到MCP服务器"""
        logger.info(f"正在连接到MCP服务器: {self.base_url}")
        
        async with self.client:
            # 测试连接
            try:
                await self.client.ping()
                logger.info("[OK] 已连接到Dhub MCP服务器")
            except Exception as e:
                logger.warning(f"Ping失败，但继续尝试: {e}")
            
            # 列出可用工具
            try:
                tools_result = await self.client.list_tools()
                
                # 处理返回结果
                if hasattr(tools_result, 'tools'):
                    self.available_tools = tools_result.tools
                elif isinstance(tools_result, list):
                    self.available_tools = tools_result
                else:
                    self.available_tools = []
                
                logger.info(f"可用工具数量: {len(self.available_tools)}")
                for tool in self.available_tools:
                    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                    tool_desc = tool.description if hasattr(tool, 'description') else ''
                    logger.info(f"  - {tool_name}: {tool_desc}")
            except Exception as e:
                logger.error(f"获取工具列表失败: {e}")
            
            yield self
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """调用MCP工具"""
        logger.info(f"调用工具: {tool_name}")
        logger.debug(f"参数: {arguments}")
        
        try:
            result = await self.client.call_tool(tool_name, arguments)
            
            # 提取文本内容
            if hasattr(result, 'content') and result.content:
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        return content_item.text
                    elif hasattr(content_item, 'type') and content_item.type == 'text':
                        return str(content_item)
            
            return str(result)
            
        except Exception as e:
            logger.error(f"调用工具时发生错误: {e}")
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
        通过地址搜索酒店
        
        Args:
            x_api_key: 用户的API密钥
            x_secret_key: 用户的Secret密钥
            lng_google: 谷歌经度（保留6位小数）
            lat_google: 谷歌纬度（保留6位小数）
            check_in_date: 入住日期（格式yyyy-MM-dd）
            check_out_date: 退房日期（格式yyyy-MM-dd）
            language: 语言类型，默认en-US，可选zh-CN
            price_min: 最低价格
            price_max: 最高价格
            star_ratings: 星级列表
            distance: 距离范围，单位km，默认5
            page_size: 每页数量，默认20，最大50
        
        Returns:
            酒店列表信息
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
        通过酒店名称搜索酒店
        
        Args:
            x_api_key: 用户的API密钥
            x_secret_key: 用户的Secret密钥
            keyword: 酒店名称
            check_in_date: 入住日期（格式yyyy-MM-dd）
            check_out_date: 退房日期（格式yyyy-MM-dd）
            language: 语言类型，默认en-US，可选zh-CN
            price_min: 最低价格
            price_max: 最高价格
            star_ratings: 星级列表
            distance: 距离范围，单位km，默认5
            page_size: 每页数量，默认20，最大50
        
        Returns:
            酒店列表信息
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
        查询酒店详细信息
        
        Args:
            x_api_key: 用户的API密钥
            x_secret_key: 用户的Secret密钥
            hotel_id: 酒店ID
            language: 语言类型，默认en-US，可选zh-CN
            need_facility: 是否包含设施信息，默认True
        
        Returns:
            酒店详细信息
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
        查询酒店实时价格和可用房型
        
        Args:
            x_api_key: 用户的API密钥
            x_secret_key: 用户的Secret密钥
            hotel_id: 酒店ID
            check_in_date: 入住日期（格式YYYY-MM-DD）
            check_out_date: 退房日期（格式YYYY-MM-DD）
            num_of_adults: 成人数量，默认2
            num_of_children: 儿童数量，默认0
            nationality: 国籍代码（ISO 2位代码），默认CN
            language: 语言类型，默认en-US，可选zh-CN
        
        Returns:
            详细的价格信息
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
    """示例：使用MCP客户端"""
    
    # 从环境变量读取API密钥
    api_key = "dhub_j********1A-C84VT4o"
    secret_key = "0_jufgzOe*******JRhf7ahqHydov-VjWWK7zgU"
    
    if not api_key or not secret_key:
        logger.error("❌ 请设置环境变量 X_API_KEY 和 X_SECRET_KEY")
        return
    
    client = DhubMCPClient()
    
    async with client.connect():
        logger.info("\n" + "="*60)
        logger.info("开始测试 Dhub MCP 客户端")
        logger.info("="*60 + "\n")
        
        # 示例1: 通过酒店名称搜索
        logger.info("📍 示例1: 搜索东京的酒店")
        logger.info("-" * 60)
        
        try:
            result = await client.search_hotels_by_hotel_name(
                x_api_key=api_key,
                x_secret_key=secret_key,
                keyword="长春",
                check_in_date="2025-12-01",
                check_out_date="2025-12-03",
                language="en-US",
                page_size=5
            )
            logger.info(f"\n搜索结果:\n{result}\n")
        except Exception as e:
            logger.error(f"搜索失败: {e}")
        
        # 示例2: 通过地址搜索
        logger.info("\n📍 示例2: 通过经纬度搜索酒店")
        logger.info("-" * 60)
        
        try:
            result = await client.search_hotels_by_address(
                x_api_key=api_key,
                x_secret_key=secret_key,
                lng_google=125.276516,  # 东京
                lat_google=43.88597,
                check_in_date="2025-11-21",
                check_out_date="2025-11-23",
                language="zh-CN",
                distance=5,
                page_size=5
            )
            logger.info(f"\n搜索结果:\n{result}\n")
        except Exception as e:
            logger.error(f"搜索失败: {e}")
        
        # 示例3: 获取酒店详情（使用一个示例酒店ID）
        logger.info("\n📍 示例3: 查询酒店详情")
        logger.info("-" * 60)
        
        try:
            # 注意：请替换为实际的酒店ID
            hotel_id = 1364848
            result = await client.get_hotel_details(
                x_api_key=api_key,
                x_secret_key=secret_key,
                hotel_id=hotel_id,
                language="en-US",
                need_facility=True
            )
            logger.info(f"\n酒店详情:\n{result}\n")
        except Exception as e:
            logger.error(f"查询详情失败: {e}")
        
        # 示例4: 查询酒店价格
        logger.info("\n📍 示例4: 查询酒店价格")
        logger.info("-" * 60)
        
        try:
            # 注意：请替换为实际的酒店ID
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
            logger.info(f"\n价格信息:\n{result}\n")
        except Exception as e:
            logger.error(f"查询价格失败: {e}")
        
        logger.info("\n" + "="*60)
        logger.info("测试完成")
        logger.info("="*60)


if __name__ == "__main__":
    # 配置日志
    logger.add(
        "logs/mcp_client_{time}.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # 运行客户端
    asyncio.run(main())

