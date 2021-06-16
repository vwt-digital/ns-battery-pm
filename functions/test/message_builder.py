import base64
import json
import time
from datetime import datetime


class MessageBuilder:
    def __init__(self):
        self.valid = [99, 90, 85, 80, 70, 60, 49, 55, 65, 75, 85, 95, 98, 99, 100]
        self.invalid = [99, 34, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    def __build_valid_battery(self, collected, index):
        return {
            "timestamp": collected,
            "hostName": "check_test_valid",
            "performanceData": [
                {
                    "var_name": "battery_capacity",
                    "actual": self.valid[index],
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
                    "actual": self.invalid[index],
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
        for i in range(15):
            time.sleep(7)

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
