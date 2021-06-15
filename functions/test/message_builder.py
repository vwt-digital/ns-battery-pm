import base64
import json
import time
from datetime import datetime


class MessageBuilder:
    def __init__(self):
        pass

    @staticmethod
    def expr(x, a, b, c):
        return (a * x ** 2) + (b * x) + c

    def __build_valid_battery(self, collected, index):
        return {
            "timestamp": collected,
            "hostName": "check_test_valid",
            "performanceData": [
                {
                    "var_name": "battery_capacity",
                    "actual": self.expr(x=index, a=0.8, b=0, c=20),
                }
            ],
        }

    def __build_invalid_battery(self, collected, index):
        return {
            "timestamp": collected,
            "hostName": "check_test_invalid",
            "performanceData": [
                {
                    "var_name": "battery_capacity",
                    "actual": self.expr(x=index, a=0.51, b=0, c=49),
                }
            ],
        }

    def __build_limited_battery(self, collected, index):
        return {
            "timestamp": collected,
            "hostName": "check_test_limited",
            "performanceData": [
                {"var_name": "battery_capacity", "actual": 99 if index == 0 else 100}
            ],
        }

    def build_message(self):
        for i in range(-10, 11):
            time.sleep(1)

            collected = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

            data = {
                "ns_tcc_performance": [
                    self.__build_invalid_battery(collected, i),
                    self.__build_valid_battery(collected, i),
                    self.__build_limited_battery(collected, i),
                ]
            }
            message = {
                "message": {
                    "data": base64.b64encode(json.dumps(data).encode()).decode("utf-8")
                }
            }
            yield json.dumps(message)
