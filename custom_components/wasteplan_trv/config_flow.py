"""config flow for the Wasteplan TRV integration."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    TRVApiClient,
    TRVApiClientCommunicationError,
    TRVApiClientError,
)
from .const import DOMAIN, CALENDAR_NAME, LOCATION_NAME, LOCATION_ID, LOGGER


class TRVConfigFLow(config_entries.ConfigFlow, domain=DOMAIN):
  """Handle config flow for Wasteplan TRV."""

  VERSION = 1
  CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

  def __init__(self) -> None:
    """Initialize the config flow."""
    self._errors: dict[str, str] = {}
    self._locations: list | None = None
    self._location_id: str | None = None

  async def async_step_user(
    self,
    user_input: dict | None = None,
  ) -> FlowResult:
    """Handle a flow initialized by the user."""
    self._errors = {}
    self._locations = None

    if user_input is not None:
      address = user_input[LOCATION_NAME]
      self._locations = await self._id_from_address(
        address=address,
      )

      if self._locations is not None:
        return await self.async_step_location()

    return self.async_show_form(
        step_id="user",
        data_schema=vol.Schema({vol.Required(LOCATION_NAME): str}),
        errors=self._errors,
    )

  async def async_step_location(
    self,
    user_input: dict | None = None,
  ) -> FlowResult:
    """Handle location select"""
    self._errors = {}

    assert self._locations is not None

    if user_input is not None:
      address = user_input[LOCATION_NAME]
      locations = [
        location
        for location in self._locations
        if location["adresse"] == address
      ]
      location = locations[0]
      location_id = location["id"]
      calendar_name = user_input.get(CALENDAR_NAME)

      return self.async_create_entry(
        title=address,
        data={
          CALENDAR_NAME: calendar_name,
          LOCATION_ID: location_id,
        },
      )

    return self.async_show_form(
      step_id="location",
      data_schema=vol.Schema(
        {
          vol.Required(CALENDAR_NAME): str,
          vol.Required(LOCATION_NAME): vol.In(
            [address["adresse"] for address in self._locations]
          ),
        }
      ),
      errors=self._errors,
    )

  async def _id_from_address(self, address: str) -> None:
    """Validate location."""
    client = TRVApiClient(
      address=address,
      location_id="",
      session=async_create_clientsession(self.hass),
    )

    try:
      locations = await client.async_lookup_address()
      if len(locations) == 0:
        self._errors["base"] = "no_location"
        return None
      return locations
    except TRVApiClientCommunicationError as exception:
      LOGGER.error(exception)
      self._errors["base"] = "connection"
    except TRVApiClientError as exception:
      LOGGER.exception(exception)
      self._errors["base"] = "unknown"
