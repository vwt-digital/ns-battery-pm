class Battery(object):
    def __init__(self, actual: float, battery_hg_name: str = None, placed=None):
        self.actual = actual
        self.battery_hg_name = battery_hg_name
        self.placed = placed

    @staticmethod
    def from_dict(source):
        return Battery(
            source["actual"],
            source.get("hostName", "hostless"),
            source.get("timestamp", "0000-00-00T00:00:00.000Z"),
        )

    def add_timestamp(self, timestamp):
        self.placed = timestamp
        return self

    def add_host(self, host):
        self.battery_hg_name = host
        return self

    def to_dict(self):
        return {
            "actual": self.actual,
            "battery_hg_name": self.battery_hg_name,
            "collected": self.placed,
        }

    def __repr__(self):
        return f"Battery(\
                actual={self.actual}, \
                battery_hg_name={self.battery_hg_name}, \
                placed={self.placed} \
            )"
