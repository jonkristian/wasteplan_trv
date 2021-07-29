"""Platform for sensor integration."""
from datetime import datetime as date, timedelta
import logging

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.util.dt as dt_util
import requests
import voluptuous as vol

from .const import ATTRIBUTION, CONF_PICKUP_DAY, CONF_PICKUP_ID, URL, WASTE_TYPES

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_PICKUP_ID): cv.string, vol.Optional(CONF_PICKUP_DAY): cv.string}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the TRV sensor."""
    id = config.get(CONF_PICKUP_ID)

    pickup_day = 0
    if config.get(CONF_PICKUP_DAY):
        pickup_day = int(config.get(CONF_PICKUP_DAY))
    data = TRVData(id)
    data.update()

    sensors = []
    for wastetype in WASTE_TYPES:
        sensors.append(TRVSensor(wastetype, data, pickup_day))

    add_entities(sensors, True)


class TRVData:
    """Get the latest data for all authorities."""

    def __init__(self, id):
        """Initialize the object."""
        self.data = None
        self.id = id

    # Update only once in scan interval.
    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from TRV."""
        response = requests.get(URL + self.id, timeout=10)
        if response.status_code != 200:
            _LOGGER.warning("Invalid response from TRV API")
        else:
            self.data = response.json()


class TRVSensor(Entity):
    """Single authority wasteplan sensor."""

    def __init__(self, name, data, pickup_day):
        """Initialize the sensor."""
        self._data = data
        self._name = name
        self._icon = WASTE_TYPES[self._name][0]
        self._state = "Ikke bestemt"
        self._year = None
        self._pickup_this_week = False
        self._next_pickup_week = None
        self._date_week_start = None
        self._date_week_end = None
        self._description = None
        self._pickup_day = pickup_day
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
        self.attrs["pickup_this_week"] = self._pickup_this_week
        self.attrs["description"] = self._description
        self.attrs["date_week_start"] = self._date_week_start
        self.attrs["date_week_end"] = self._date_week_end

        return self.attrs

    def update(self):
        """Update the sensor."""
        self._data.update()

        containers = []
        today = dt_util.now().weekday()
        this_week = dt_util.now().isocalendar()[1]

        # Iterate and stop on match.
        for entry in self._data.data["calendar"]:

            # Containers? Make a list.
            if "," in entry["wastetype"]:
                containers = map(str.strip, entry["wastetype"].split(","))

            # Do we have a match?
            if self._name == entry["wastetype"] or self._name in containers:
                self._year = entry["year"]
                self._next_pickup_week = entry["week"]
                self._date_week_start = entry["date_week_start"]
                self._date_week_end = entry["date_week_end"]

                self._state, self._icon = self.pickup_state()

                if entry["week"] == this_week:
                    self._pickup_this_week = True
                    if today <= self._pickup_day:
                        break

                elif entry["week"] > this_week:
                    break

    def pickup_state(self):
        state = None
        icon = None

        year = dt_util.now().year
        today = dt_util.now().weekday()
        tomorrow = (dt_util.now() + timedelta(1)).weekday()
        weeks_until = 0
        this_week = dt_util.now().isocalendar()[1]

        weeks_until = self._next_pickup_week - this_week

        if 0 == weeks_until:

            if self._name.startswith("Tømmefri"):
                state = "Denne uken"
                icon = WASTE_TYPES[self._name][3]
            elif today == self._pickup_day:
                state = "I dag"
                icon = WASTE_TYPES[self._name][1]
            elif tomorrow == self._pickup_day:
                state = "I morgen"
                icon = WASTE_TYPES[self._name][2]
            elif today < self._pickup_day or self._pickup_this_week:
                state = "Denne uken"
                icon = WASTE_TYPES[self._name][3]
            else:
                state = "Tømt"
                icon = WASTE_TYPES[self._name][4]

        elif 1 == weeks_until:

            state = "Neste uke"
            icon = WASTE_TYPES[self._name][4]

        elif year < self._year:
            state = "Uke " + str(self._next_pickup_week) + " (" + str(self._year) + ")"
            icon = WASTE_TYPES[self._name][5]

        else:
            state = "Uke " + str(self._next_pickup_week)
            icon = WASTE_TYPES[self._name][5]

        return state, icon
