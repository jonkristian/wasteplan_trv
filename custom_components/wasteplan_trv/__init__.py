"""Wasteplan TRV integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.update_coordinator import (
  CoordinatorEntity,
  DataUpdateCoordinator,
  UpdateFailed,
)

from .api import (
  TRVApiClient,
  TRVApiClientError,
)
from .const import DOMAIN, LOCATION_ID, LOGGER

PLATFORMS: list[Platform] = [
  Platform.CALENDAR,
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Set up this integration using UI."""
  hass.data.setdefault(DOMAIN, {})

  hass.data[DOMAIN][entry.entry_id] = coordinator = TRVDataUpdateCoordinator(
    hass=hass,
    client=TRVApiClient(
      location_id=entry.data[LOCATION_ID],
      address="",
      session=async_get_clientsession(hass),
    ),
  )

  await coordinator.async_config_entry_first_refresh()

  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  entry.async_on_unload(entry.add_update_listener(async_reload_entry))

  return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Handle removal of an entry."""
  if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
    hass.data[DOMAIN].pop(entry.entry_id)
  return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
  """Reload config entry."""
  await async_unload_entry(hass, entry)
  await async_setup_entry(hass, entry)


class TRVDataUpdateCoordinator(DataUpdateCoordinator):
  """Class to manage fetching data from the API."""

  def __init__(
    self,
    hass: HomeAssistant,
    client: TRVApiClient,
  ) -> None:
    """Initialize."""
    self.client = client
    super().__init__(
      hass=hass,
      logger=LOGGER,
      name=DOMAIN,
      update_interval=timedelta(hours=5),
    )
    self.entities: list[TRVEntity] = []

  async def _async_update_data(self):
    """Update data via library."""
    try:
      return await self.client.async_get_pickups()
    except TRVApiClientError as exception:
      raise UpdateFailed(exception) from exception


class TRVEntity(CoordinatorEntity):
  """Representation of a Wasteplan entity."""
  def __init__(
    self,
    coordinator: TRVDataUpdateCoordinator,
    entry: ConfigEntry,
  ) -> None:
    """Initialize Wasteplan entity."""
    super().__init__(coordinator=coordinator)
    self._attr_device_info = DeviceInfo(
      identifiers={(DOMAIN, str(entry.data[LOCATION_ID]))},
      entry_type=DeviceEntryType.SERVICE,
      configuration_url="https://github.com/jonkristian/wasteplan_trv",
      manufacturer="Trondheim Renholdsverk",
      name="Trondheim Renholdsverk",
    )
