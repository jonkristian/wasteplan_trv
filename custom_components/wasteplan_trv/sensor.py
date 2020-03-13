"""Platform for sensor integration."""
from datetime import timedelta
import logging

import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.util.dt import now

_LOGGER = logging.getLogger(__name__)

ATTRIBUTION = "Data provided by https://trv.no"

SCAN_INTERVAL = timedelta(days=30)

CONF_BIN_NUMBER = "bin_number"
CONF_BIN_TYPE = "bin_type"

URL = "https://trv.no/wp-json/wasteplan/v1/calendar/"

SENSOR_TYPES = {
    "Restavfall": ["mdi:trash-can", "mdi:trash-can-outline"],
    "Papir": ["mdi:trash-can", "mdi:trash-can-outline"],
    "Plastemballasje": ["mdi:trash-can", "mdi:trash-can-outline"],
    "Hageavfall": ["mdi:trash-can", "mdi:trash-can-outline"],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_BIN_NUMBER): cv.string,
        vol.Optional(CONF_BIN_TYPE): vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)])
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the TRV sensor."""
    bin_number = config.get(CONF_BIN_NUMBER)
    data = TRVData(bin_number)
    data.update()

    sensors = []
    for bintype in SENSOR_TYPES:
        sensors.append(TRVSensor(bintype, data))

    add_entities(sensors, True)


class TRVData:
    """Get the latest data for all authorities."""

    def __init__(self, bin_number):
        """Initialize the AirData object."""
        self.data = None
        self.bin_number = bin_number

    # Update only once in scan interval.
    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from TRV."""
        response = requests.get(URL + self.bin_number, timeout=10)
        if response.status_code != 200:
            _LOGGER.warning("Invalid response from API")
        else:
            self.data = response.json()


class TRVSensor(Entity):
    """Single authority wasteplan sensor."""

    def __init__(self, name, data):
        """Initialize the sensor."""
        self._data = data
        self._name = name
        self._icon = SENSOR_TYPES[self._name][0]
        self._next_pickup_week = None
        self._state = None
        self.attrs = {ATTR_ATTRIBUTION: ATTRIBUTION}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        self.attrs["next_pickup_week"] = self._next_pickup_week

        return self.attrs

    def update(self):
        """Update the sensor."""
        self._data.update()
        self._state = 0

        weeks_until = 0
        this_week = now().isocalendar()[1]

        for entry in self._data.data['calendar']:
            if self._name == entry['wastetype']:
                weeks_until = entry['week'] - this_week

                if 0 == weeks_until:
                    self._state = 'Denne uken'
                    self._icon = SENSOR_TYPES[self._name][1]
                elif 1 == weeks_until:
                    self._state = 'Neste uke'
                else:
                    self._state = 'Om '+str(weeks_until)+' uker'

                self._next_pickup_week = entry['week']
                break