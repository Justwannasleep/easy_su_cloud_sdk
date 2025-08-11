from .base_model import ApiInterface, BaseRequestData


class RequestLoginData(BaseRequestData):
    card: str
    device_id: str


class ApiLogin(ApiInterface):
    path: str = "/v1/card/login"
    method: str = "POST"
    event_name = "card_login"
