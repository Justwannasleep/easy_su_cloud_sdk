from .base_model import ApiInterface, BaseRequestData


class RequestHeartbeatData(BaseRequestData):
    pass


class ApiHeartbeat(ApiInterface):
    path: str = "/v1/card/heartbeat"
    method: str = "POST"
    event_name: str = "heartbeat"
