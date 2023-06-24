"""TRV API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class TRVApiClientError(Exception):
  """Exception to indicate a general API error."""


class TRVApiClientCommunicationError(TRVApiClientError):
  """Exception to indicate a communication error."""


class TRVApiClient:
  """TRV API Client."""
  def __init__(
    self,
    address: str,
    location_id: str,
    session: aiohttp.ClientSession,
    ) -> None:
      self._location_id = location_id
      self._address = address
      self._session = session

  async def async_lookup_address(self) -> any:
    """Get address locations from TRV."""
    return await self._api_wrapper(
        method="get",
        url="https://trv.no/wp-json/wasteplan/v2/adress?s=" + self._address,
    )

  async def async_get_pickups(self) -> any:
    """Get pickup base data from TRV."""
    return await self._api_wrapper(
        method="get",
        url="https://trv.no/wp-json/wasteplan/v2/calendar/" + self._location_id,
    )

  async def _api_wrapper(
    self,
    method: str,
    url: str,
    data: dict | None = None,
    headers: dict | None = None,
    ) -> any:
      """Fetch the information from the API."""
      try:
        async with async_timeout.timeout(10):
          response = await self._session.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
          )
          response.raise_for_status()
          return await response.json()

      except asyncio.TimeoutError as exception:
        raise TRVApiClientCommunicationError("Timeout error fetching information") from exception
      except (aiohttp.ClientError, socket.gaierror) as exception:
        raise TRVApiClientCommunicationError("Error fetching information") from exception
      except Exception as exception:  # pylint: disable=broad-except
        raise TRVApiClientError("Something really wrong happened!") from exception
