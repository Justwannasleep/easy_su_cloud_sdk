from .base_model import ApiInterface, BaseRequestData


class RequestLastVersionData(BaseRequestData):
    card: str | None = None
    version: str


class ApiLastVersion(ApiInterface):
    path: str = "/v1/software/latest_ver"
    method: str = "GET"
    event_name: str = "last_version"
