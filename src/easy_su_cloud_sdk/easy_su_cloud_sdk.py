# coding=utf-8
import time
import uuid
import threading

from .client.easy_su_cloud_client import EasySuCloudClient

from .decorators.event_listener import event_listener


from .common.models import (
    RequestLoginData,
    RequestHeartbeatData,
    RequestLogoutData,
    RequestLastVersionData,
    ApiHeartbeat,
    ApiLogout,
    ApiLogin,
    ApiLastVersion,
)


class EasySuCloudHelper(EasySuCloudClient):
    def __init__(
        self, protocol, host_addr, port, app_key, app_secret, cd_key, heartbeat_interval
    ) -> None:
        super().__init__(
            protocol, host_addr, port, app_key, app_secret, cd_key, heartbeat_interval
        )
        self._heartbeat_stop_event = threading.Event()  # 添加退出事件标志
        self._heartbeat_thread = None  # 保存线程引用

    # def async_card_logout(self, card, token):
    #     return self.keep_heart(self.card_logout, card, token)

    # def async_card_login(self, card, device_id):
    #     return self.keep_heart(self.card_login, card, device_id)

    @event_listener.event_listener(ApiLogin.event_name)
    def req_card_login(self) -> dict:
        req_data: RequestLoginData = RequestLoginData(
            app_key=self._app_key,
            card=self._card,
            device_id=self._device_id,
        )
        method, path = ApiLogin.method, ApiLogin.path

        req = self._http_client(
            method=method, url=path, json=req_data.model_dump(), verify=False
        )
        if req["code"] == 0 and req.get("result"):
            self._token = req["result"].get("token")

        return req

    @event_listener.event_listener(ApiHeartbeat.event_name)
    def req_heartbeat(self) -> dict:
        req_data = RequestHeartbeatData(
            app_key=self._app_key,
            card=self._card,
            token=self._token,
        )
        method, path = (
            ApiHeartbeat.method,
            ApiHeartbeat.path,
        )
        return self._http_client(
            method=method, url=path, json=req_data.model_dump(), verify=False
        )

    @event_listener.event_listener(ApiLogout.event_name)
    def req_card_logout(self) -> dict:
        req_data = RequestLogoutData(
            app_key=self._app_key,
            card=self._card,
            nonce=str(uuid.uuid1()),
            timestamp=int(time.time()),
            token=self._token,
        )
        method, path = ApiLogout.method, ApiLogout.path
        return self._http_client(
            method=method, url=path, json=req_data.model_dump(), verify=False
        )

    @event_listener.event_listener(ApiLastVersion.event_name)
    def get_last_ver(self, app_ver) -> dict:
        params = RequestLastVersionData(
            app_key=self._app_key,
            version=app_ver,
        )
        method, path = ApiLastVersion.method, ApiLastVersion.path

        return self._http_client(
            method=method, url=path, params=params.model_dump(), verify=False
        )

    def _jump_heartbeat(self):
        # 将无限循环改为事件驱动的条件循环
        while not self._heartbeat_stop_event.is_set():
            self.req_heartbeat()
            # 使用事件等待代替time.sleep，可立即响应退出信号
            self._heartbeat_stop_event.wait(self._heartbeat_interval)

    def keep_heartbeat(self):
        # 确保先停止已有线程
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self.stop_heartbeat()
        self._heartbeat_stop_event.clear()  # 重置事件标志
        self._heartbeat_thread = threading.Thread(
            target=self._jump_heartbeat, daemon=True
        )
        self._heartbeat_thread.start()
        return self._heartbeat_thread

    def stop_heartbeat(self):
        """优雅停止心跳线程"""
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_stop_event.set()  # 设置退出标志
            self._heartbeat_thread.join()  # 等待线程结束
            self._heartbeat_thread = None
            return True
        return False
