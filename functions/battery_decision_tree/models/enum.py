from enum import Enum


class Advice(Enum):
    SAFE = "The battery has been predicted as safe for use for at least {weeks} weeks"
    UNSAFE = "The battery has been predicted as unsafe for use and needs changing within {weeks} weeks"
    UNDETERMINED = "The battery could not receive a prediction by a lack of (valid) data or invalid configuration"
