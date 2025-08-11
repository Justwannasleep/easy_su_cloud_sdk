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


