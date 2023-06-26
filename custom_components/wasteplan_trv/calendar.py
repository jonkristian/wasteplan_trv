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
  """Define a Wasteplan calendar."""
  _attr_icon = "mdi:delete-empty"
  def __init__(
    self,
    coordinator: DataUpdateCoordinator,
    entry: ConfigEntry,
  ) -> None:
    """Initialize the Wasteplan entity."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = entry.data[LOCATION_ID]
    self._attr_name = entry.data[CALENDAR_NAME]
    self._attr_location = entry.data[LOCATION_NAME]
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
      waste_date = datetime.strptime(waste["dato"], "%Y-%m-%dT%H:%M:%S").replace(hour=8, minute=00)

      event = CalendarEvent(
        summary=str(waste["fraksjon"]),
        start=waste_date,
        end=waste_date + timedelta(hours=8),
        location=self._attr_location
      )

      if start_date.date() <= waste_date.date() <= end_date.date() and event is not None:
        events.append(event)

    return events

  @callback
  def _handle_coordinator_update(self) -> None:
    """Handle updated data from the coordinator."""
    next_waste_pickup_type = None
    next_waste_pickup_date = None
    for waste in self.coordinator.data["calendar"]:
      waste_date = datetime.strptime(waste["dato"], "%Y-%m-%dT%H:%M:%S").replace(hour=8, minute=00)
      if (waste_date and (next_waste_pickup_date is None)
        and waste_date.date() >= dt.now().date()
      ):
        next_waste_pickup_date = waste_date
        next_waste_pickup_type = waste["fraksjon"]

      self._event = None
      if next_waste_pickup_date is not None and next_waste_pickup_type is not None:
        self._event = CalendarEvent(
          summary=next_waste_pickup_type,
          start=next_waste_pickup_date,
          end=next_waste_pickup_date + timedelta(days=1),
        )

      super()._handle_coordinator_update()

  async def async_added_to_hass(self) -> None:
    """When entity is added to hass."""
    await super().async_added_to_hass()
    self._handle_coordinator_update()
