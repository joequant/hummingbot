from decimal import Decimal

from pydantic import Field, SecretStr

from hummingbot.client.config.config_data_types import BaseConnectorConfigMap, ClientFieldData
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

CENTRALIZED = True
EXAMPLE_PAIR = "ETH-USDT"


DEFAULT_FEES = TradeFeeSchema(
    buy_percent_fee_deducted_from_returns=True,
    maker_percent_fee_decimal=Decimal("0.002"),
    taker_percent_fee_decimal=Decimal("0.002"),
)


class OpencexConfigMap(BaseConnectorConfigMap):
    connector: str = Field(default="opencex", client_data=None)
    opencex_host: str = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Opencex host",
            is_secure=False,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    opencex_api_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Opencex API key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )
    opencex_secret_key: SecretStr = Field(
        default=...,
        client_data=ClientFieldData(
            prompt=lambda cm: "Enter your Opencex secret key",
            is_secure=True,
            is_connect_key=True,
            prompt_on_new=True,
        )
    )

    class Config:
        title = "opencex"


KEYS = OpencexConfigMap.construct()
