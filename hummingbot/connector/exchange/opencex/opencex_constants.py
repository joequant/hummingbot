# A single source of truth for constant variables related to the exchange

from hummingbot.core.api_throttler.data_types import RateLimit

EXCHANGE_NAME = "opencex"
BROKER_ID = "AAc484720a"
MAX_CLIENT_ORDER_ID_LENGTH = 64


WS_PUBLIC_URL = "/wsapi/v1/live_notifications"
WS_PRIVATE_URL = "/wsapi/v1/live_notifications"

WS_HEARTBEAT_TIME_INTERVAL = 5  # seconds

# Websocket event types
TRADE_CHANNEL_SUFFIX = "trade.detail"
ORDERBOOK_CHANNEL_SUFFIX = "depth.step0"

TRADE_INFO_URL = "/api/public/v1/summary"
MOST_RECENT_TRADE_URL = "/api/public/v1/trades/{}"
DEPTH_URL = "/market/depth"
LAST_TRADE_URL = "/market/trade"

SERVER_TIME_URL = "/api/public/v1/common/timestamp"
ACCOUNT_ID_URL = "/api/public/v1/account/accounts"
ACCOUNT_BALANCE_URL = "/api/public/v1/balance"
OPEN_ORDERS_URL = "/api/public/v1/order/openOrders"
ORDER_DETAIL_URL = "/api/public/v1/order/orders/{}"
ORDER_MATCHES_URL = "/api/public/v1/order/orders/{}"
PLACE_ORDER_URL = "/api/public/v1/order/{}"
CANCEL_ORDER_URL = "/api/public/v1/order/{}"

OPENCEX_STACK_TOPIC = "add_stack"
OPENCEX_TRADE_TOPIC = "add_trade"
OPENCEX_BALANCE_TOPIC = "add_balance"
OPENCEX_OPENED_ORDERS_TOPIC = "add_opened_orders"
OPENCEX_CLOSED_ORDERS_TOPIC = "add_closed_orders"
OPENCEX_EXECUTED_ORDERS = "add_executed_orders"

OPENCEX_SUBSCRIBE_TOPICS = {OPENCEX_STACK_TOPIC, OPENCEX_BALANCE_TOPIC, OPENCEX_TRADE_TOPIC}

WS_CONNECTION_LIMIT_ID = "WSConnection"
WS_REQUEST_LIMIT_ID = "WSRequest"
CANCEL_URL_LIMIT_ID = "cancelRequest"
ORDER_DETAIL_LIMIT_ID = "orderDetail"
ORDER_MATCHES_LIMIT_ID = "orderMatch"

RATE_LIMITS = [
    RateLimit(WS_CONNECTION_LIMIT_ID, limit=50, time_interval=1),
    RateLimit(WS_REQUEST_LIMIT_ID, limit=10, time_interval=1),
    RateLimit(limit_id=TRADE_INFO_URL, limit=10, time_interval=1),
    RateLimit(limit_id=MOST_RECENT_TRADE_URL, limit=10, time_interval=1),
    RateLimit(limit_id=DEPTH_URL, limit=10, time_interval=1),
    RateLimit(limit_id=LAST_TRADE_URL, limit=10, time_interval=1),
    RateLimit(limit_id=SERVER_TIME_URL, limit=10, time_interval=1),
    RateLimit(limit_id=ACCOUNT_ID_URL, limit=100, time_interval=2),
    RateLimit(limit_id=ACCOUNT_BALANCE_URL, limit=100, time_interval=2),
    RateLimit(limit_id=ORDER_DETAIL_LIMIT_ID, limit=50, time_interval=2),
    RateLimit(limit_id=ORDER_MATCHES_LIMIT_ID, limit=50, time_interval=2),
    RateLimit(limit_id=PLACE_ORDER_URL, limit=100, time_interval=2),
    RateLimit(limit_id=CANCEL_URL_LIMIT_ID, limit=100, time_interval=2)
]
