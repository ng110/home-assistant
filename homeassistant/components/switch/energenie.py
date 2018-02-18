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
#    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_API_KEY): cv.string,
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_cb, discovery_info=None):
    """Set up the demo switches."""
    import pymihome as pymi
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    key = config.get(CONF_API_KEY)
    try:
        mihome = pymi.Connection(username, key, _LOGGER)
    except:
        mihome = pymi.Connection(username, password, _LOGGER)

    # Verify that passed in configuration works
    _LOGGER.error("ng testing1.")
    if not mihome.is_valid_login:
        _LOGGER.error("Could not connect to MiHome Gateway.")
        return False

    # Add devices
    icon = 'mdi:power-socket-uk'
    add_devices_cb(EnergenieSwitch(pymi.EnergenieSwitch(mihome, dev), icon)
                         for dev in mihome.subdevices
                         if dev['is_switch'])


class EnergenieSwitch(SwitchDevice):
    """Representation of an energenie switch."""

    # def __init__(self, name, state, icon, assumed):
    def __init__(self, device, icon):
        """Initialize the Energenie switch."""
        self._device = device
        self._name = self._device.name or DEVICE_DEFAULT_NAME
        self._icon = icon
        self._state = False
        if self._device.is_sensor:
            self._assumed = False
        else:
            self._assumed = True

    @property
    def should_poll(self):
        """Poll only for monitor switch."""
        if self._device.is_sensor:
            return True
        return False

    @property
    def unique_id(self):
        """Return the unique ID of the device."""
        return self._device.id

    @property
    def name(self):
        """Return the name of the device if any."""
        return self._device.name

    @property
    def icon(self):
        """Return the icon to use for device if any."""
        return self._icon

    @property
    def assumed_state(self):
        """Return if the state is based on assumptions."""
        if self._device.is_sensor:
            return False
        return True

    def update(self):
        """Get the latest state and update the state."""
        return self._device.getinfo()

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        return self._device.lastpower

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return self._device.todays_usage / 1000

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._device.state
        # try:
        #     return self._device.state
        # except:
        #     return self._state

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._device.turn_on()
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._device.turn_off()
        self._state = False
        self.schedule_update_ha_state()






    # @property
    # def device_state_attributes(self):
    #     """Return device specific state attributes.
    #     Implemented by platform classes.
    #     """
    #     return None

    # @property
    # def available(self) -> bool:
    #     """Return True if entity is available."""
    #     return True

    # @property
    # def force_update(self) -> bool:
    #     """Return True if state updates should be forced.
    #     If True, a state change will be triggered anytime the state property is
    #     updated, not just when the value changes.
    #     """
    #     return False


