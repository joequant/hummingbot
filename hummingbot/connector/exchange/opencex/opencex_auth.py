import hashlib
import hmac
from typing import Any, Dict

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSJSONRequest


class OpencexAuth(AuthBase):
    def __init__(self, api_key: str, secret_key: str, time_provider: TimeSynchronizer):
        self.api_key: str = api_key
        self.secret_key: str = secret_key
        self.time_provider = time_provider

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        headers = {}
        if request.headers is not None:
            headers.update(request.headers)
        auth_params = self.generate_auth_params_for_REST(request=request)
        headers.update(auth_params)
        request.headers = headers
        return request

    async def ws_authenticate(self, request: WSJSONRequest) -> WSJSONRequest:
        auth_params = self.generate_auth_params_for_REST(request=request)
        request.payload = {**(request.payload), **auth_params}
        return request

    def generate_auth_params_for_REST(self, request: RESTRequest) -> Dict[str, Any]:
        nonce = str(int(round(self.time_provider.time() * 1000)))
        params = request.params or {}
        signature = self.generate_signature(
            self.api_key,
            self.secret_key,
            nonce
        )
        params.update({
            'APIKEY': self.api_key,
            'SIGNATURE': signature,
            'NONCE': nonce
        })
        return params

    def generate_auth_params_for_WS(self, request: WSJSONRequest) -> Dict[str, Any]:
        print("generating signature")
        nonce = str(int(round(self.time_provider.time() * 1000)))
        signature = self.generate_signature(
            self.api_key,
            self.secret_key,
            nonce
        )
        return {
            'api_key': self.api_key,
            'signature': signature,
            'nonce': nonce
        }

    def generate_signature(self,
                           api_key: str,
                           secret_key: str,
                           nonce: str
                           ) -> str:
        message = api_key + nonce
        return hmac.new(self.secret_key.encode("utf8"), message.encode("utf8"), hashlib.sha256).hexdigest().upper()
