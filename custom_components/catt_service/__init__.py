import logging
import subprocess

from homeassistant.core import SupportsResponse
from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CMD_BASE = ["catt", "-d"]
SCAN_CMD = ["catt", "scan"]
HELP_CMD = ["catt", "-h"]
STOP_ARGS = ["stop"]


def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        _LOGGER.error("[%s] Command failed: %s", DOMAIN, cmd)

    return result.stdout


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, config_entry):
    """Set up the integration."""

    if hass.data.get(DOMAIN):
        return False

    async def scan(service):
        output = run_cmd(SCAN_CMD)
        _LOGGER.info("[%s] scan -> %s", DOMAIN, output)
        return {"output": output}

    hass.services.async_register(
        DOMAIN,
        "scan",
        scan,
        supports_response=SupportsResponse.ONLY,
    )

    async def help_cmd(service):
        output = run_cmd(HELP_CMD)
        return {"help": output}

    hass.services.async_register(
        DOMAIN,
        "help",
        help_cmd,
        supports_response=SupportsResponse.ONLY,
    )

    async def stop(service):
        device = service.data["friendly_name"]
        run_cmd(CMD_BASE + [device] + STOP_ARGS)

    hass.services.async_register(DOMAIN, "stop", stop)

    async def command(service):
        device = service.data["friendly_name"]
        cmd = service.data["command"]
        param = service.data["param"]

        run_cmd(CMD_BASE + [device, cmd, param])

    hass.services.async_register(DOMAIN, "command", command)

    return True
