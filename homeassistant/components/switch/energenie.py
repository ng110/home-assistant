"""
Demo platform that has two fake switches.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/demo/
"""
from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import DEVICE_DEFAULT_NAME
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_API_KEY
import homeassistant.helpers.config_validation as cv
import logging
import voluptuous as vol

# REQUIREMENTS = ['awesome_lights==1.2.3']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_API_KEY): cv.string,
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up the demo switches."""
    from pymihome import Connection, EnergenieSwitch
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    key = config.get(CONF_API_KEY)
    try:
        mihome = pymihome.Connection(username, key, _LOGGER)
    except:
        mihome = pymihome.Connection(username, password, _LOGGER)

    # Verify that passed in configuration works
    if not mihome.is_valid_login():
        _LOGGER.error("Could not connect to MiHome Gateway")
        return False

    # Add devices
    add_devices(EnergenieSwitch(mihome, dev) for dev in mihome.devices())
    add_devices(EnergenieSensor(mihome, dev) for dev in mihome.devices())



    add_devices_callback([
        DemoSwitch('Decorative Lights', True, None, True),
        DemoSwitch('AC', False, 'mdi:air-conditioner', False)
    ])


class EnergenieSwitch(SwitchDevice):
    """Representation of an energenie switch."""

    def __init__(self, name, state, icon, assumed):
        """Initialize the Demo switch."""
        self._name = name or DEVICE_DEFAULT_NAME
        self._state = state
        self._icon = icon
        self._assumed = assumed

    @property
    def should_poll(self):
        """No polling needed for a demo switch."""
        return False

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use for device if any."""
        return self._icon

    @property
    def assumed_state(self):
        """Return if the state is based on assumptions."""
        return self._assumed

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        if self._state:
            return 100

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return 15

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._state = False
        self.schedule_update_ha_state()
