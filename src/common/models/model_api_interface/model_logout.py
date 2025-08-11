from .base_model import ApiInterface, BaseRequestData


class RequestLogoutData(BaseRequestData):
    pass


class ApiLogout(ApiInterface):
    path: str = "/v1/card/logout"
    method: str = "POST"
    event_name: str = "logout"
