"""Support for Wasteplan TRV calendar."""
from __future__ import annotations
import logging
from datetime import date, datetime, timedelta
from homeassistant.util import dt

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import TRVEntity
from .const import DOMAIN, CALENDAR_NAME, LOCATION_ID

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
  hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
  """Set up Wasteplan calendars based on a config entry."""
  coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
  async_add_entities([TRVCalendar(coordinator, entry)])


class TRVCalendar(TRVEntity, CalendarEntity):
  """Define a Wasteplan calendar."""
  def __init__(
    self,
    coordinator: DataUpdateCoordinator,
    entry: ConfigEntry,
  ) -> None:
    """Initialize the Wasteplan entity."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = str(entry.data[LOCATION_ID])
    self._attr_name = str(entry.data[CALENDAR_NAME])
    self._event: CalendarEvent | None = None

  @property
  def event(self) -> CalendarEvent | None:
    """Return the next upcoming event."""
    return self._event

  async def async_get_events(
    self,
    hass: HomeAssistant,
    start_date: datetime,
    end_date: datetime,
  ) -> list[CalendarEvent]:
    """Return calendar events within a datetime range."""
    events: list[CalendarEvent] = []
    for waste in self.coordinator.data["calendar"]:
      waste_date = datetime.strptime(waste["dato"], "%Y-%m-%dT%H:%M:%S")
      waste_start = dt.start_of_local_day(waste_date)

      event = CalendarEvent(
        summary=str(waste["fraksjon"]),
        start=waste_start,
        end=waste_start + timedelta(days=1),
      )

      if start_date <= waste_start <= end_date and event is not None:
        events.append(event)

    return events

  async def get_calendar_item(self, calendar_item) -> object | None:
    """Return formatted calendar entry."""
