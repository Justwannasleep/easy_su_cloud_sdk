from typing import Any, Callable, Literal, Mapping, TypeAlias, Union
import uuid
from pydantic import BaseModel, Field
import time
from dataclasses import dataclass, field


IncEx: TypeAlias = Union[
    set[int],
    set[str],
    Mapping[int, Union["IncEx", bool]],
    Mapping[str, Union["IncEx", bool]],
]


class BaseRequestData(BaseModel):
    card: str
    app_key: str
    nonce: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="随机数, 一般用uuid"
    )
    timestamp: int = Field(default_factory=lambda: int(time.time()))
    sign: str | None = Field(default=None, description="签名")
    token: str | None = Field(default=None, description="token")

    # 重写model_dump方法，默认exclude_none为True
    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "python",
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
    ) -> dict[str, Any]:
        return super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )


@dataclass
class ApiInterface:
    path: str = field(metadata={"description": "接口路径"})
    method: str = field(metadata={"description": "请求方法"})
    event_name: str = field(metadata={"description": "事件名称"})
