from urllib.parse import urljoin
from requests.sessions import (
    RequestsCookieJar,
)
from typing import Any, TypeAlias
import requests
from hashlib import md5
from ..utils.device import get_device_code
from ..decorators.event_listener import event_listener


Incomplete: TypeAlias = Any


class EasySuCloudClient(requests.Session):
    _heartbeat_interval = 60
    _interface_prefix = ""
    _host = ""
    _app_key: str = ""
    _app_secret: str = ""
    _token: str = ""
    _card: str = ""
    _device_id = ""

    def __init__(
        self, protocol, host_addr, port, app_key, app_secret, cd_key, heartbeat_interval
    ) -> None:
        self._set_interface_prefix(protocol=protocol, host_addr=host_addr, port=port)
        self._set_app_info(
            app_key=app_key, app_secret=app_secret, cd_key=cd_key, heartbeat_interval=60
        )
        super().__init__()

    def _set_interface_prefix(self, protocol, host_addr, port):
        self._host = host_addr
        self._interface_prefix = f"{protocol}://{host_addr}:{port}"
        return self

    def _set_app_info(self, app_key, app_secret, cd_key, heartbeat_interval):
        self._app_key = app_key
        self._card = cd_key
        self._app_secret = app_secret
        self._device_id = get_device_code()
        self._heartbeat_interval = heartbeat_interval
        return self

    def compute_sign(self, method, path, data: dict):
        data_array = [f"{k}={data[k]}" for k in sorted(data.keys())]
        params = "&".join(data_array)
        host = self._host
        return md5(
            (method + host + path + params + self._app_secret).encode("utf8")
        ).hexdigest()

    def register_event_listener(
        self, event_name, before_callback=None, after_callback=None
    ):
        if after_callback:
            event_listener.register_event(event_name, after_callback)

    def compute_response_sign(self, response_dict):
        result = ""
        if not response_dict.get("result"):
            return ""

        for k in response_dict["result"]:
            result = result + k + "=" + str(response_dict["result"][k]) + "&"

        result = result[0:-1]
        data = (
            str(response_dict["code"])
            + response_dict["msg"]
            + result
            + response_dict["nonce"]
            + self._app_secret
        )
        return md5(data.encode("utf8")).hexdigest()

    def _http_client(
        self,
        method: str | bytes,
        url: str | bytes,
        params: dict | None = None,
        data: dict | None = None,
        headers: Incomplete | None = None,
        cookies: None | RequestsCookieJar | Incomplete = None,
        files: Incomplete | None = None,
        auth: Incomplete | None = None,
        timeout: int | float | None = None,
        allow_redirects: bool = True,
        proxies: Incomplete | None = None,
        hooks: Incomplete | None = None,
        stream: bool | None = None,
        verify: bool | str | None = None,
        cert: str | None = None,
        json: Incomplete | None | dict = None,
    ) -> dict[str, Any]:
        if method == "POST" and json:
            sign = self.compute_sign(method, url, json)
            json["sign"] = sign
        elif method == "POST" and data:
            sign = self.compute_sign(method, url, data)
            data["sign"] = sign
        if method == "GET" and params:
            sign = self.compute_sign(method, url, params)
            params["sign"] = sign
        # 显示转换，方便通过类型检查
        if isinstance(url, str):
            url = urljoin(self._interface_prefix, url)
        else:
            url = urljoin(self._interface_prefix, str(url))
        response: requests.Response = self.request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
        if response.status_code != 200:
            raise RuntimeError(f"request failed, status_code: {response.status_code}")
        resp_data = response.json()
        if resp_data.get("sign") and (
            self.compute_response_sign(resp_data) != resp_data["sign"]
        ):
            raise RuntimeError(f"response sign error, resp_data: {resp_data}")

        return resp_data
