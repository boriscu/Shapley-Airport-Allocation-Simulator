from enum import Enum

class AlgorithmType(str, Enum):
    """
    Enumeration for the supported Shapley value calculation algorithms.
    """
    EXACT = "exact"
    APPROXIMATE = "approximate"
    CONFIGURATION_VALUE = "configuration_value"
