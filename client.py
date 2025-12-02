"""
全球酒店预订 HTTP/SSE MCP 客户端
"""
import asyncio
import json
from typing import Optional, List, Any, Dict, Callable
from contextlib import asynccontextmanager
import httpx
from loguru import logger


class DhubHTTPMCPClient:
    """全球酒店预订 HTTP/SSE MCP客户端"""
    
    def __init__(self, base_url: str):
        """
        初始化HTTP MCP客户端
        
        Args:
            base_url: MCP服务的基础URL（不包含 /mcp 路径）
        """
        self.base_url = base_url.rstrip('/')
        self.mcp_base = f"{self.base_url}/mcp"
        self.http_client: Optional[httpx.AsyncClient] = None
        self.available_tools: List[Dict[str, Any]] = []
        self._sse_connection = None
        self._sse_listeners: List[Callable] = []
    
    @asynccontextmanager
    async def connect(self):
        """连接到MCP服务器"""
        logger.info(f"正在连接到 GLOBAL HOTEL MCP 服务器: {self.base_url}")
        
        # 创建HTTP客户端
        self.http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        try:
            # 测试连接 - 健康检查
            try:
                health_response = await self.http_client.get(f"{self.base_url}/health")
                health_response.raise_for_status()
                health_data = health_response.json()
                logger.info(f"[OK] 服务器健康状态: {health_data.get('status')}")
            except Exception as e:
                logger.warning(f"健康检查失败，但继续尝试: {e}")
            
            # 获取服务信息
            try:
                info_response = await self.http_client.get(f"{self.base_url}/info")
                info_response.raise_for_status()
                info_data = info_response.json()
                logger.info(f"[OK] 已连接到: {info_data.get('name')}")
                logger.info(f"     协议: {info_data.get('protocol')}")
                logger.info(f"     传输方式: {', '.join(info_data.get('transport', []))}")
            except Exception as e:
                logger.warning(f"获取服务信息失败: {e}")
            
            # 列出可用工具
            await self._load_tools()
            
            yield self
            
        finally:
            # 清理资源
            if self._sse_connection:
                await self._close_sse()
            
            if self.http_client:
                await self.http_client.aclose()
                logger.info("HTTP 客户端已关闭")
    
    async def _load_tools(self):
        """加载可用工具列表"""
        try:
            response = await self.http_client.get(f"{self.mcp_base}/tools/list")
            response.raise_for_status()
            data = response.json()
            
            self.available_tools = data.get("tools", [])
            logger.info(f"可用工具数量: {data.get('count', 0)}")
            
            for tool in self.available_tools:
                if tool.get("type") == "function":
                    func_info = tool.get("function", {})
                    tool_name = func_info.get("name", "unknown")
                    tool_desc = func_info.get("description", "")
                    logger.info(f"  - {tool_name}: {tool_desc}")
                    
        except Exception as e:
            logger.error(f"获取工具列表失败: {e}")
            self.available_tools = []
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        调用MCP工具（HTTP POST方式）
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            工具执行结果
        """
        logger.info(f"调用工具: {tool_name}")
        logger.debug(f"参数: {arguments}")
        
        try:
            response = await self.http_client.post(
                f"{self.mcp_base}/call_tool",
                json={
                    "name": tool_name,
                    "arguments": arguments
                },
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            result_data = response.json()
            
            # 提取文本内容
            content = result_data.get("content", [])
            if content and len(content) > 0:
                first_content = content[0]
                if isinstance(first_content, dict) and "text" in first_content:
                    return first_content["text"]
                elif isinstance(first_content, str):
                    return first_content
            
            return json.dumps(result_data, indent=2, ensure_ascii=False)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP错误: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"调用工具时发生错误: {e}")
            raise
    
    async def connect_sse(self, on_message: Optional[Callable[[Dict], None]] = None):
        """
        建立SSE连接
        
        Args:
            on_message: 接收到消息时的回调函数
        """
        logger.info("正在建立SSE连接...")
        
        if on_message:
            self._sse_listeners.append(on_message)
        
        try:
            async with self.http_client.stream(
                "GET",
                f"{self.mcp_base}/sse",
                headers={"Accept": "text/event-stream"}
            ) as response:
                response.raise_for_status()
                logger.info("[OK] SSE连接已建立")
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]  # 移除 "data: " 前缀
                        
                        try:
                            data = json.loads(data_str)
                            logger.debug(f"收到SSE消息: {data.get('type', 'unknown')}")
                            
                            # 触发所有监听器
                            for listener in self._sse_listeners:
                                try:
                                    if asyncio.iscoroutinefunction(listener):
                                        await listener(data)
                                    else:
                                        listener(data)
                                except Exception as e:
                                    logger.error(f"SSE监听器错误: {e}")
                        
                        except json.JSONDecodeError:
                            logger.warning(f"无法解析SSE数据: {data_str}")
                    
                    elif line.startswith(": "):
                        # 心跳消息
                        logger.debug("收到SSE心跳")
                        
        except Exception as e:
            logger.error(f"SSE连接错误: {e}")
            raise
    
    async def _close_sse(self):
        """关闭SSE连接"""
        if self._sse_connection:
            logger.info("正在关闭SSE连接...")
            self._sse_connection = None
            self._sse_listeners.clear()
    
    def add_sse_listener(self, listener: Callable[[Dict], None]):
        """
        添加SSE消息监听器
        
        Args:
            listener: 消息监听器函数
        """
        self._sse_listeners.append(listener)
    
    async def get_connections(self) -> Dict[str, Any]:
        """
        获取活跃的SSE连接列表
        
        Returns:
            连接信息
        """
        try:
            response = await self.http_client.get(f"{self.mcp_base}/connections")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"获取连接列表失败: {e}")
            return {"active_connections": [], "count": 0}
    
    # ==================== 酒店预订工具方法 ====================
    
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
    """测试HTTP客户端"""

    # API密钥（请替换为实际密钥）
    api_key = "dhub_TLYC_FeVJg***********0wu_CNaK-rM"
    secret_key = "vYMbUrYmfviHrK******************EQr7L-EuVQnYJtaqv73"

    if not api_key or not secret_key:
        logger.error("❌ 请设置 API 密钥")
        return

    # 创建客户端
    client = DhubHTTPMCPClient(base_url="https://mcp.fusionconnectgroup.com/sse")

    async with client.connect():
        logger.info("\n" + "=" * 60)
        logger.info("开始测试 GLOBAL HOTEL SSE MCP 客户端")
        logger.info("=" * 60 + "\n")

        # 示例1: 通过酒店名称搜索
        logger.info("📍 示例1: 搜索长春的酒店")
        logger.info("-" * 60)

        try:
            result = await client.search_hotels_by_hotel_name(
                x_api_key=api_key,
                x_secret_key=secret_key,
                keyword="长春",
                check_in_date="2025-12-01",
                check_out_date="2025-12-03",
                language="zh-CN",
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
                lng_google=125.276516,
                lat_google=43.88597,
                check_in_date="2025-12-10",
                check_out_date="2025-12-12",
                language="zh-CN",
                distance=5,
                page_size=5
            )
            logger.info(f"\n搜索结果:\n{result}\n")
        except Exception as e:
            logger.error(f"搜索失败: {e}")

        # 示例3: 获取酒店详情
        logger.info("\n📍 示例3: 查询酒店详情")
        logger.info("-" * 60)

        try:
            hotel_id = 1364848
            result = await client.get_hotel_details(
                x_api_key=api_key,
                x_secret_key=secret_key,
                hotel_id=hotel_id,
                language="zh-CN",
                need_facility=True
            )
            logger.info(f"\n酒店详情:\n{result}\n")
        except Exception as e:
            logger.error(f"查询详情失败: {e}")

        # 示例4: 查询酒店价格
        logger.info("\n📍 示例4: 查询酒店价格")
        logger.info("-" * 60)

        try:
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
                language="zh-CN"
            )
            logger.info(f"\n价格信息:\n{result}\n")
        except Exception as e:
            logger.error(f"查询价格失败: {e}")

        logger.info("\n" + "=" * 60)
        logger.info("HTTP客户端测试完成")
        logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

