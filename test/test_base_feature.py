from loguru import logger
from easy_su_cloud_sdk.easy_su_cloud_sdk import EasySuCloudHelper
from easy_su_cloud_sdk.common.models import ApiHeartbeat
from easy_su_cloud_sdk.helper.logger import init_sdk_logger
import time


class TestBaseFeature:
    easy_sdk = EasySuCloudHelper(
        protocol="https",
        host_addr="api.easysu.cn",
        port=443,
        app_key="lJyA57I57jxBR741ShDE",
        app_secret="cc3552b75dfb4e77a360f6f86f014679",
        cd_key="j78rUoMLyfMLMNhuP3fX",
        heartbeat_interval=6,
    )

    @staticmethod
    def test_login_card():
        TestBaseFeature.easy_sdk.req_card_login()
        assert TestBaseFeature.easy_sdk._token != ""

    @staticmethod
    def test_heartbeat():
        TestBaseFeature.easy_sdk.req_card_login()
        TestBaseFeature.easy_sdk.req_heartbeat()

    @staticmethod
    def test_listen_heartbeat():
        def login_success(data, *args, **kwargs):
            assert data["msg"] == "调用成功"

        TestBaseFeature.easy_sdk.register_event_listener("card_login", login_success)
        TestBaseFeature.easy_sdk.req_card_login()

    @staticmethod
    def test_run_back_heartbeat():
        init_sdk_logger("INFO")

        def login_success(data, *args, **kwargs):
            assert data["msg"] == "调用成功"
            logger.info(f"login success: {data}")

        TestBaseFeature.easy_sdk.register_event_listener(
            ApiHeartbeat.event_name, login_success
        )

        TestBaseFeature.easy_sdk.req_card_login()
        TestBaseFeature.easy_sdk.keep_heartbeat()
        time.sleep(10)
        while TestBaseFeature.easy_sdk.stop_heartbeat():
            time.sleep(1)

        assert 1 == 1
        return

    @staticmethod
    def test_ver_is_low():
        from easy_su_cloud_sdk.common.models import ApiLastVersion

        TestBaseFeature.easy_sdk = EasySuCloudHelper(
            protocol="https",
            host_addr="api.easysu.cn",
            port=443,
            app_key="lJyA57I57jxBR741ShDE",
            app_secret="cc3552b75dfb4e77a360f6f86f014679",
            cd_key="j78rUoMLyfMLMNhuP3fX",
            heartbeat_interval=6,
        )
        init_sdk_logger("DEBUG")
        ver = "1.0.0"

        def hook(data, *args, **kwargs):
            logger.info(f"login success: {data}")
            assert data["code"] == 0

        TestBaseFeature.easy_sdk.register_event_listener(
            ApiLastVersion.event_name, hook
        )
        TestBaseFeature.easy_sdk.req_card_login()

        TestBaseFeature.easy_sdk.get_last_ver(ver)

    @staticmethod
    def test_ver_is_new():
        TestBaseFeature.easy_sdk = EasySuCloudHelper(
            protocol="https",
            host_addr="api.easysu.cn",
            port=443,
            app_key="lJyA57I57jxBR741ShDE",
            app_secret="cc3552b75dfb4e77a360f6f86f014679",
            cd_key="j78rUoMLyfMLMNhuP3fX",
            heartbeat_interval=6,
        )

        from easy_su_cloud_sdk.common.models import ApiLastVersion

        ver = "0.7.1"

        def hook(data, *args, **kwargs):
            logger.info(f"login success: {data}")
            assert data["code"] == 10304

        TestBaseFeature.easy_sdk.register_event_listener(
            ApiLastVersion.event_name, hook
        )
        TestBaseFeature.easy_sdk.req_card_login()

        TestBaseFeature.easy_sdk.get_last_ver(ver)
