# 说明
该项目是一个基于python的easy su云平台的sdk, easy su 的地址：http://doc.easysu.cn/

项目旨在提供一个简单的sdk, 方便开发者快速集成easy su云平台的功能，方便开发者不用考虑HTTP的细节，只需要关注业务逻辑即可。


# 集成接口
目前继承了以下能力：
1. 卡密登录
2. 登出
3. 心跳
4. 获取最新版本

# 事件监听和注册
1. 监听事件的方法可以使用 SDK 中暴露的 `register_event_listener` 方法。

2. 监听的事件根据 common.models.model_api_interface 中API 模型的 event_name 定义。

3. 事件的回调函数需要符合以下签名：

```python
def callback(data:dict, *args, **kwargs) -> 
None:
    """
    事件回调函数
    :param data: 事件数据, 来自服务端的响应数据
    :param args: 额外参数
    :param kwargs: 额外参数
    :return: None
    """

    pass
```


# 调用示例
1. 初始化sdk
```python
from easy_su_cloud_sdk import EasySuCloudHelper
easy_sdk = EasySuCloudHelper(
    protocol="https",
    host_addr="api.easysu.com",
    port=443,
    app_key="",
    app_secret="",
    cd_key=cdkey,
    heartbeat_interval=60,
)
```

2. 定义和注册事件回调
```python
def hook(data, *args, **kwargs):
    logger.info(f"login success: {data}")
    assert data["code"] == 10304

easy_sdk.register_event_listener(
            ApiLastVersion.event_name, hook
        )
```



3. CDK登录
```python
easy_sdk.login()
```

4. 开始心跳
```python
easy_sdk.keep_heartbeat()
```

# 手动停止
1. 手动停止心跳
    1. 调用 `stop_heartbeat` 方法停止心跳，该方法会返回一个 `bool` 值的数据，
        表示是否成功停止心跳。通常会在最后1次心跳调用后返回。
        ```python
        while TestBaseFeature.easy_sdk.stop_heartbeat():
            time.sleep(1)
        ```

2. 手动登出
    1. 调用 `logout` 方法手动登出。
    2. 等待 `ApiLogout` 事件触发，确认登出成功。



