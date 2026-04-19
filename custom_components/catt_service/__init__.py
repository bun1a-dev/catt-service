import logging
import subprocess

from homeassistant import config_entries
from homeassistant.core import SupportsResponse

from .const import DOMAIN
from homeassistant.helpers import config_validation as cv

CONFIG_SCHEMA = cv.config_entry_only_config_schema
_LOGGER = logging.getLogger(__name__)

CMD_BASE = ["catt", "-d"]
STOP_ARGS = ["stop"]
SCAN_CMD = ["catt", "scan"]
HELP_CMD = ["catt", "-h"]


def subp_run(cmd):
    output = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if output.returncode != 0:
        _LOGGER.error("[%s] The command '%s' failed.", DOMAIN, cmd)

    return output


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""

    if hass.data.get(DOMAIN) is not None:
        return False

    # scan service
    async def scan(service):
        output = subp_run(SCAN_CMD).stdout
        _LOGGER.info("[%s] scan -> %s", DOMAIN, output)
        return {"output": output}

    hass.services.async_register(
        DOMAIN,
        "scan",
        scan,
        supports_response=SupportsResponse.ONLY,
    )

    # help service
    async def help(service):
        output = subp_run(HELP_CMD).stdout
        return {"help": output}

    hass.services.async_register(
        DOMAIN,
        "help",
        help,
        supports_response=SupportsResponse.ONLY,
    )

    # stop service
    async def stop(service):
        dname = service.data["friendly_name"]
        subp_run(CMD_BASE + [dname] + STOP_ARGS)

    hass.services.async_register(DOMAIN, "stop", stop)

    # command service
    async def command(service):
        dname = service.data["friendly_name"]
        cmd = service.data["command"]
        param = service.data.get("param")

        cmdline = CMD_BASE + [dname, cmd]

        if param:
            cmdline.append(param)

        subp_run(cmdline)

    hass.services.async_register(DOMAIN, "command", command)

    return True
