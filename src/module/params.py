from os import getenv

PARAMS = {
    "INTERVAL_UNIT": getenv("INTERVAL_UNIT", "s"),
    "INTERVAL_PERIOD": float(getenv("INTERVAL_PERIOD", "10")),
    "FUNCTION": getenv("FUNCTION", "sum"),
    "INPUT_LABEL": getenv("INPUT_LABEL", "temperature"),
    "OUTPUT_LABEL": getenv("OUTPUT_LABEL", "sumTemperature"),
}
