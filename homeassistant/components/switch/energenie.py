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
    if not mihome.is_valid_login():
        _LOGGER.error("Could not connect to MiHome Gateway.")
        return False

    # Add devices
    icon = 'mdi:power-socket-uk'
    add_devices_cb(EnergenieSwitch(pymi.EnergenieSwitch(mihome, dev), icon)
                         for dev in mihome.devices()
                         if dev['is_switch'])


class EnergenieSwitch(SwitchDevice):
    """Representation of an energenie switch."""

    # def __init__(self, name, state, icon, assumed):
    def __init__(self, device, icon):
        """Initialize the Energenie switch."""
        self._device = device
        self._name = self._device.name or DEVICE_DEFAULT_NAME
        self._icon = icon
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


class GenericSwitch(SwitchDevice):

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        return None

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return None

    @property
    def is_standby(self):
        """Return true if device is in standby."""
        return None

    @property
    def state(self) -> str:
        """Return the state."""
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        raise NotImplementedError()

    def turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        raise NotImplementedError()

    def turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        raise NotImplementedError()
    

    entity_id = None  # type: str
    # Process updates in parallel
    parallel_updates = None

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return True

    @property
    def unique_id(self) -> str:
        """Return an unique ID."""
        return None

    @property
    def name(self) -> Optional[str]:
        """Return the name of the entity."""
        return None

    @property
    def device_state_attributes(self):
        """Return device specific state attributes.
        Implemented by platform classes.
        """
        return None

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return None

    @property
    def entity_picture(self):
        """Return the entity picture to use in the frontend, if any."""
        return None

    @property
    def hidden(self) -> bool:
        """Return True if the entity should be hidden from UIs."""
        return False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        return False

    @property
    def force_update(self) -> bool:
        """Return True if state updates should be forced.
        If True, a state change will be triggered anytime the state property is
        updated, not just when the value changes.
        """
        return False

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return None

    def update(self):
        """Retrieve latest state.
        For asyncio use coroutine async_update.
        """
        pass












#### Base class methods to rewrite
class xSwitchDevice(ToggleEntity):
    """Representation of a switch."""

    # pylint: disable=no-self-use
    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        return None

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return None

    @property
    def is_standby(self):
        """Return true if device is in standby."""
        return None

    @property
    def state_attributes(self):
        """Return the optional state attributes."""
        data = {}

        for prop, attr in PROP_TO_ATTR.items():
            value = getattr(self, prop)
            if value:
                data[attr] = value

        return data


class xToggleEntity(Entity):
    """An abstract class for entities that can be turned on and off."""

    # pylint: disable=no-self-use
    @property
    def state(self) -> str:
        """Return the state."""
        return STATE_ON if self.is_on else STATE_OFF

    @property
    def is_on(self) -> bool:
        """Return True if entity is on."""
        raise NotImplementedError()

    def turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        raise NotImplementedError()

    def async_turn_on(self, **kwargs):
        """Turn the entity on.

        This method must be run in the event loop and returns a coroutine.
        """
        return self.hass.async_add_job(
            ft.partial(self.turn_on, **kwargs))

    def turn_off(self, **kwargs) -> None:
        """Turn the entity off."""
        raise NotImplementedError()

    def async_turn_off(self, **kwargs):
        """Turn the entity off.

        This method must be run in the event loop and returns a coroutine.
        """
        return self.hass.async_add_job(
            ft.partial(self.turn_off, **kwargs))

    def toggle(self, **kwargs) -> None:
        """Toggle the entity."""
        if self.is_on:
            self.turn_off(**kwargs)
        else:
            self.turn_on(**kwargs)

    def async_toggle(self, **kwargs):
        """Toggle the entity.

        This method must be run in the event loop and returns a coroutine.
        """
        if self.is_on:
            return self.async_turn_off(**kwargs)
        return self.async_turn_on(**kwargs)


class xEntity(object):
    """An abstract class for Home Assistant entities."""

    # pylint: disable=no-self-use
    # SAFE TO OVERWRITE
    # The properties and methods here are safe to overwrite when inheriting
    # this class. These may be used to customize the behavior of the entity.
    entity_id = None  # type: str

    # Owning hass instance. Will be set by EntityPlatform
    hass = None  # type: Optional[HomeAssistant]

    # Owning platform instance. Will be set by EntityPlatform
    platform = None

    # If we reported if this entity was slow
    _slow_reported = False

    # Protect for multiple updates
    _update_staged = False

    # Process updates in parallel
    parallel_updates = None

    # Name in the entity registry
    registry_name = None

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return True

    @property
    def unique_id(self) -> str:
        """Return an unique ID."""
        return None

    @property
    def name(self) -> Optional[str]:
        """Return the name of the entity."""
        return None

    @property
    def state(self) -> str:
        """Return the state of the entity."""
        return STATE_UNKNOWN

    @property
    def state_attributes(self):
        """Return the state attributes.

        Implemented by component base class.
        """
        return None

    @property
    def device_state_attributes(self):
        """Return device specific state attributes.

        Implemented by platform classes.
        """
        return None

    @property
    def device_class(self) -> str:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return None

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return None

    @property
    def entity_picture(self):
        """Return the entity picture to use in the frontend, if any."""
        return None

    @property
    def hidden(self) -> bool:
        """Return True if the entity should be hidden from UIs."""
        return False

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return True

    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        return False

    @property
    def force_update(self) -> bool:
        """Return True if state updates should be forced.

        If True, a state change will be triggered anytime the state property is
        updated, not just when the value changes.
        """
        return False

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return None

    def update(self):
        """Retrieve latest state.

        For asyncio use coroutine async_update.
        """
        pass



