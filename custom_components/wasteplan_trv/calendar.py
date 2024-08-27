"""Support for Wasteplan TRV calendar."""
from __future__ import annotations
import logging
from datetime import date, datetime, timedelta
from homeassistant.util import dt

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TRVEntity
from .const import DOMAIN, LOCATION_NAME, CALENDAR_NAME, LOCATION_ID

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
  hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
  """Set up Wasteplan calendars based on a config entry."""
  coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
  async_add_entities([TRVCalendar(coordinator, entry)])


class TRVCalendar(TRVEntity, CalendarEntity):
    _attr_icon = "mdi:delete-empty"

    def __init__(self, coordinator: DataUpdateCoordinator, entry: ConfigEntry) -> None:
        """Initialize the Wasteplan entity."""
        super().__init__(coordinator, entry)
        self._attr_unique_id = entry.data[LOCATION_ID]
        self._attr_name = entry.data[CALENDAR_NAME]
        self._attr_location = entry.data[LOCATION_NAME]
        self._events: list[CalendarEvent] = []

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        if self._events:
            return self._events[0]  # Return the first event in the list
        return None  # Return None if no events are available

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        return {"events": self._events}  # Expose all events

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._events.clear()  # Clear previous events
        for waste in self.coordinator.data["calendar"]:
            waste_date = datetime.strptime(waste["dato"], "%Y-%m-%dT%H:%M:%S").replace(hour=8)
            if waste_date.date() >= dt.now().date():
                waste_pickup = dt.as_local(waste_date)
                waste_summary = waste["fraksjon"]

                event = CalendarEvent(
                    summary=waste_summary,
                    start=waste_pickup,
                    end=waste_pickup + timedelta(hours=8),
                )

                self._events.append(event)  # Add the event to the list

        super()._handle_coordinator_update()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()
