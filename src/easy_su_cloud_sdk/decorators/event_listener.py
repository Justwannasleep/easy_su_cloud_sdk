class EventListener:
    def __init__(self):
        self._before_listeners = {}
        self._after_listeners = {}

    # def register_before_event(self, event_name, callback):
    #     if event_name not in self._before_listeners:
    #         self._before_listeners[event_name] = []
    #     self._before_listeners[event_name].append(callback)

    def register_event(self, event_name, callback):
        """只提供请求后的事件监听

        Args:
            event_name (_type_): _description_
            callback (function): _description_
        """
        if event_name not in self._after_listeners:
            self._after_listeners[event_name] = []
        self._after_listeners[event_name].append(callback)

    def event_listener(self, event_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                # 触发前置事件
                # if event_name in self._before_listeners:
                #     for callback in self._before_listeners[event_name]:
                #         callback(*args, **kwargs)

                # 执行原函数
                result = func(*args, **kwargs)

                # 触发后置事件
                if event_name in self._after_listeners:
                    for callback in self._after_listeners[event_name]:
                        callback(result, *args, **kwargs)

                return result

            return wrapper

        return decorator


# 创建全局事件监听器实例
event_listener = EventListener()
