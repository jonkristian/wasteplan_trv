ATTRIBUTION = "Data provided by https://trv.no"

CONF_PICKUP_ID = "id"
CONF_PICKUP_DAY = "pickup_day"

URL = "https://trv.no/wp-json/wasteplan/v1/calendar/"

WASTE_TYPES = {
    "Restavfall": [
        "mdi:recycle",  # Default
        "mdi:delete-alert",  # Today
        "mdi:delete-alert-outline",  # Tomorrow
        "mdi:delete-clock-outline",  # This week
        "mdi:delete-empty-outline",  # Emptied
        "mdi:delete-restore",  # Next week
    ],
    "Papir": [
        "mdi:file",  # Default
        "mdi:delete-alert",  # Today
        "mdi:delete-alert-outline",  # Tomorrow
        "mdi:delete-clock-outline",  # This week
        "mdi:delete-empty-outline",  # Emptied
        "mdi:delete-restore",  # Next week
    ],
    "Plastemballasje": [
        "mdi:bottle-soda",  # Default
        "mdi:delete-alert",  # Today
        "mdi:delete-alert-outline",  # Tomorrow
        "mdi:delete-clock-outline",  # This week
        "mdi:delete-empty-outline",  # Emptied
        "mdi:delete-restore",  # Next week
    ],
    "Hageavfall": [
        "mdi:apple",  # Default
        "mdi:delete-alert",  # Today
        "mdi:delete-alert-outline",  # Tomorrow
        "mdi:delete-clock-outline",  # This week
        "mdi:delete-empty-outline",  # Emptied
        "mdi:delete-restore",  # Next week
    ],
    "Tømmefri uke": [
        "mdi:delete-forever-outline",  # Default
        "mdi:delete-forever-outline",  # Today
        "mdi:delete-forever-outline",  # Tomorrow
        "mdi:delete-forever-outline",  # This week
        "mdi:delete-forever-outline",  # Emptied
        "mdi:delete-forever-outline",  # Next week
    ],
    "Farlig avfall": [
        "mdi:skull-crossbones",  # Default
        "mdi:skull-scan",  # Today
        "mdi:skull-scan-outline",  # Tomorrow
        "mdi:skull-scan-outline",  # This week
        "mdi:skull-outline",  # Emptied
        "mdi:skull-crossbones-outline",  # Next week
    ],
}
