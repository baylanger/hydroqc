"""Tests for the optional, caller-owned aiohttp session."""

import aiohttp
import pytest

from hydroqc.hydro_api.client import HydroClient
from hydroqc.webuser import WebUser


@pytest.mark.asyncio(loop_scope="module")
async def test_external_session_is_not_closed() -> None:
    """A session injected by the caller must survive close_session()."""
    jar = aiohttp.CookieJar(quote_cookie=False, unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        client = HydroClient("user", "pass", session=session)
        await client.close_session()
        assert not session.closed
        assert client._session is session


@pytest.mark.asyncio(loop_scope="module")
async def test_external_session_cookie_jar_is_adopted() -> None:
    """The client uses the injected session's jar, not a separate one."""
    jar = aiohttp.CookieJar(quote_cookie=False, unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        client = HydroClient("user", "pass", session=session)
        await client._get_httpsession()
        assert client._cookie_jar is jar


@pytest.mark.asyncio(loop_scope="module")
async def test_explicit_cookie_jar_wins() -> None:
    """An explicit cookie_jar takes precedence over the session's jar."""
    explicit = aiohttp.CookieJar(quote_cookie=False, unsafe=True)
    async with aiohttp.ClientSession() as session:
        client = HydroClient("user", "pass", session=session, cookie_jar=explicit)
        assert client._cookie_jar is explicit


@pytest.mark.asyncio(loop_scope="module")
async def test_internal_session_is_closed() -> None:
    """Without an injected session the client owns and closes its own."""
    client = HydroClient("user", "pass")
    await client._get_httpsession()
    session = client._session
    assert session is not None
    await client.close_session()
    assert session.closed


@pytest.mark.asyncio(loop_scope="module")
async def test_webuser_passes_session_through() -> None:
    """WebUser forwards the session to HydroClient."""
    async with aiohttp.ClientSession() as session:
        user = WebUser("user", "pass", verify_ssl=True, session=session)
        assert user._hydro_client._session is session
