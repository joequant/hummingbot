import asyncio
from typing import TYPE_CHECKING, List, Optional

import hummingbot.connector.exchange.opencex.opencex_constants as CONSTANTS
from hummingbot.connector.exchange.opencex.opencex_auth import OpencexAuth
from hummingbot.core.data_type.user_stream_tracker_data_source import UserStreamTrackerDataSource
from hummingbot.core.web_assistant.connections.data_types import WSJSONRequest
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory
from hummingbot.core.web_assistant.ws_assistant import WSAssistant
from hummingbot.logger import HummingbotLogger

if TYPE_CHECKING:
    from hummingbot.connector.exchange.opencex.opencex_exchange import OpencexExchange


class OpencexAPIUserStreamDataSource(UserStreamTrackerDataSource):

    _logger: Optional[HummingbotLogger] = None

    def __init__(self, opencex_auth: OpencexAuth,
                 trading_pairs: List[str],
                 connector: 'OpencexExchange',
                 api_factory: Optional[WebAssistantsFactory]):
        self._auth: OpencexAuth = opencex_auth
        self._connector = connector
        self._api_factory = api_factory
        self._trading_pairs = trading_pairs
        super().__init__()

    async def _connected_websocket_assistant(self) -> WSAssistant:
        ws: WSAssistant = await self._api_factory.get_ws_assistant(
            ws_url=f'wss://{self._connector.domain}{CONSTANTS.WS_PUBLIC_URL}',
            ping_timeout=CONSTANTS.WS_HEARTBEAT_TIME_INTERVAL
        )
        return ws

    async def _subscribe_topic(self, topic: str, websocket_assistant: WSAssistant):
        """
        Specifies which event channel to subscribe to

        :param topic: the event type to subscribe to

        :param websocket_assistant: the websocket assistant used to connect to the exchange
        """
        try:
            subscribe_request: WSJSONRequest = WSJSONRequest({"command": topic, "params": {}})
            await websocket_assistant.send(subscribe_request)
            self.logger().info(f"Subscribed to {topic}")
        except asyncio.CancelledError:
            raise
        except Exception:
            self.logger().error(f"Cannot subscribe to user stream topic: {topic}")
            raise

    async def _subscribe_channels(self, websocket_assistant: WSAssistant):
        """
        Subscribes to order events, balance events and account events

        :param websocket_assistant: the websocket assistant used to connect to the exchange
        """
        try:
            await self._authenticate_client(websocket_assistant)
            await self._subscribe_topic(CONSTANTS.OPENCEX_BALANCE_TOPIC, websocket_assistant)
            for trading_pair in self._trading_pairs:
                await self._subscribe_topic(CONSTANTS.OPENCEX_ADD_OPENED_ORDERS_TOPIC,
                                            websocket_assistant)
                await self._subscribe_topic(CONSTANTS.OPENCEX_ADD_CLOSED_ORDERS_TOPIC,
                                            websocket_assistant)
                await self._subscribe_topic(CONSTANTS.OPENCEX_ADD_EXECUTED_ORDERS_TOPIC,
                                            websocket_assistant)
        except asyncio.CancelledError:
            raise
        except Exception:
            self.logger().error("Unexpected error occurred subscribing to private user streams...", exc_info=True)
            raise

    async def _process_websocket_messages(self, websocket_assistant: WSAssistant, queue: asyncio.Queue):
        async for ws_response in websocket_assistant.iter_messages():
            data = ws_response.data
            if data["action"] == "ping":
                pong_request = WSJSONRequest(payload={"action": "pong", "data": data["data"]})
                await websocket_assistant.send(request=pong_request)
            elif data["action"] == "sub":
                if data.get("code") != 200:
                    raise ValueError(f"Error subscribing to topic: {data.get('ch')} ({data})")
            else:
                queue.put_nowait(data)
