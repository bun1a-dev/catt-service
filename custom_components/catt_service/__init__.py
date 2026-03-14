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

    hass.data[DOMAIN] = True

    async def scan(call):
        output = await hass.async_add_executor_job(run_cmd, SCAN_CMD)
        _LOGGER.info("[%s] scan -> %s", DOMAIN, output)
        return {"output": output}

    hass.services.async_register(
        DOMAIN,
        "scan",
        scan,
        supports_response=SupportsResponse.ONLY,
    )

    async def help_cmd(call):
        output = await hass.async_add_executor_job(run_cmd, HELP_CMD)
        return {"help": output}

    hass.services.async_register(
        DOMAIN,
        "help",
        help_cmd,
        supports_response=SupportsResponse.ONLY,
    )

    async def stop(call):
        device = call.data["friendly_name"]
        await hass.async_add_executor_job(
            run_cmd,
            CMD_BASE + [device] + STOP_ARGS
        )

    hass.services.async_register(DOMAIN, "stop", stop)

    async def command(call):
        device = call.data["friendly_name"]
        cmd = call.data["command"]
        param = call.data.get("param")

        command = CMD_BASE + [device, cmd]

        if param:
            command.append(param)

        await hass.async_add_executor_job(run_cmd, command)

    hass.services.async_register(DOMAIN, "command", command)

    return True
