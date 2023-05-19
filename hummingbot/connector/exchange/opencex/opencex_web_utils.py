from typing import Optional

import hummingbot.connector.exchange.opencex.opencex_constants as CONSTANTS
from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.api_throttler.async_throttler import AsyncThrottler
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTMethod, RESTRequest
from hummingbot.core.web_assistant.rest_pre_processors import RESTPreProcessorBase
from hummingbot.core.web_assistant.web_assistants_factory import WebAssistantsFactory


def public_rest_url(path_url: str, domain: str = None) -> str:
    return domain + path_url


def private_rest_url(path_url: str, domain: str = None) -> str:
    return public_rest_url(path_url=path_url, domain=domain)


class OpencexRESTPreProcessor(RESTPreProcessorBase):

    async def pre_process(self, request: RESTRequest) -> RESTRequest:
        if request.headers is None:
            request.headers = {}
        request.headers["Content-Type"] = (
            "application/json" if request.method == RESTMethod.POST else "application/x-www-form-urlencoded"
        )
        return request


def build_api_factory(throttler: Optional[AsyncThrottler] = None,
                      time_synchronizer: Optional[TimeSynchronizer] = None,
                      auth: Optional[AuthBase] = None, ) -> WebAssistantsFactory:
    throttler = throttler or AsyncThrottler(CONSTANTS.RATE_LIMITS)
    time_synchronizer = time_synchronizer or TimeSynchronizer()
    api_factory = WebAssistantsFactory(
        throttler=throttler,
        auth=auth,
        rest_pre_processors=[
            OpencexRESTPreProcessor(),
        ])
    return api_factory
