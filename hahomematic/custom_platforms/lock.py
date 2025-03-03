"""
Module for entities implemented using the lock platform.

See https://www.home-assistant.io/integrations/lock/.
"""
from __future__ import annotations

from abc import abstractmethod

from hahomematic.const import HmPlatform
from hahomematic.custom_platforms.entity_definition import (
    FIELD_DIRECTION,
    FIELD_ERROR,
    FIELD_LOCK_STATE,
    FIELD_LOCK_TARGET_LEVEL,
    FIELD_OPEN,
    FIELD_STATE,
    CustomConfig,
    EntityDefinition,
    ExtendedConfig,
    make_custom_entity,
)
from hahomematic.decorators import value_property
import hahomematic.device as hmd
import hahomematic.entity as hme
from hahomematic.entity import CustomEntity
from hahomematic.generic_platforms.action import HmAction
from hahomematic.generic_platforms.sensor import HmSensor
from hahomematic.generic_platforms.switch import HmSwitch

# HM constants
LOCK_STATE_UNKNOWN = "UNKNOWN"
LOCK_STATE_LOCKED = "LOCKED"
LOCK_STATE_UNLOCKED = "UNLOCKED"

LOCK_TARGET_LEVEL_LOCKED = "LOCKED"
LOCK_TARGET_LEVEL_UNLOCKED = "UNLOCKED"
LOCK_TARGET_LEVEL_OPEN = "OPEN"

HM_UNLOCKING = "UP"
HM_LOCKING = "DOWN"


class BaseLock(CustomEntity):
    """Class for HomematicIP lock entities."""

    _attr_platform = HmPlatform.LOCK

    @value_property
    @abstractmethod
    def is_locked(self) -> bool:
        """Return true if lock is on."""

    @value_property
    @abstractmethod
    def is_jammed(self) -> bool:
        """Return true if lock is jammed."""

    @value_property
    @abstractmethod
    def is_locking(self) -> bool | None:
        """Return true if the lock is locking."""

    @value_property
    @abstractmethod
    def is_unlocking(self) -> bool | None:
        """Return true if the lock is unlocking."""

    @abstractmethod
    async def lock(self) -> None:
        """Lock the lock."""

    @abstractmethod
    async def unlock(self) -> None:
        """Unlock the lock."""

    @abstractmethod
    async def open(self) -> None:
        """Open the lock."""


class CeIpLock(BaseLock):
    """Class for HomematicIP lock entities."""

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_lock_state: HmSensor = self._get_entity(
            field_name=FIELD_LOCK_STATE, entity_type=HmSensor
        )
        self._e_lock_target_level: HmAction = self._get_entity(
            field_name=FIELD_LOCK_TARGET_LEVEL, entity_type=HmAction
        )
        self._e_direction: HmSensor = self._get_entity(
            field_name=FIELD_DIRECTION, entity_type=HmSensor
        )

    @value_property
    def is_locked(self) -> bool:
        """Return true if lock is on."""
        return self._e_lock_state.value == LOCK_STATE_LOCKED

    @value_property
    def is_locking(self) -> bool | None:
        """Return true if the lock is locking."""
        if self._e_direction.value is not None:
            return str(self._e_direction.value) == HM_LOCKING
        return None

    @value_property
    def is_unlocking(self) -> bool | None:
        """Return true if the lock is unlocking."""
        if self._e_direction.value is not None:
            return str(self._e_direction.value) == HM_UNLOCKING
        return None

    @value_property
    def is_jammed(self) -> bool:
        """Return true if lock is jammed."""
        return False

    async def lock(self) -> None:
        """Lock the lock."""
        await self._e_lock_target_level.send_value(value=LOCK_TARGET_LEVEL_LOCKED)

    async def unlock(self) -> None:
        """Unlock the lock."""
        await self._e_lock_target_level.send_value(value=LOCK_TARGET_LEVEL_UNLOCKED)

    async def open(self) -> None:
        """Open the lock."""
        await self._e_lock_target_level.send_value(value=LOCK_TARGET_LEVEL_OPEN)


class CeRfLock(BaseLock):
    """Class for classic HomeMatic lock entities."""

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_state: HmSwitch = self._get_entity(field_name=FIELD_STATE, entity_type=HmSwitch)
        self._e_open: HmAction = self._get_entity(field_name=FIELD_OPEN, entity_type=HmAction)
        self._e_direction: HmSensor = self._get_entity(
            field_name=FIELD_DIRECTION, entity_type=HmSensor
        )
        self._e_error: HmSensor = self._get_entity(field_name=FIELD_ERROR, entity_type=HmSensor)

    @value_property
    def is_locked(self) -> bool:
        """Return true if lock is on."""
        return self._e_state.value is not True

    @value_property
    def is_locking(self) -> bool | None:
        """Return true if the lock is locking."""
        if self._e_direction.value is not None:
            return str(self._e_direction.value) == HM_LOCKING
        return None

    @value_property
    def is_unlocking(self) -> bool | None:
        """Return true if the lock is unlocking."""
        if self._e_direction.value is not None:
            return str(self._e_direction.value) == HM_UNLOCKING
        return None

    @value_property
    def is_jammed(self) -> bool:
        """Return true if lock is jammed."""
        return self._e_error.value is not None and self._e_error.value != "NO_ERROR"

    async def lock(self) -> None:
        """Lock the lock."""
        await self._e_state.send_value(value=False)

    async def unlock(self) -> None:
        """Unlock the lock."""
        await self._e_state.send_value(value=True)

    async def open(self) -> None:
        """Open the lock."""
        await self._e_open.send_value(value=True)


def make_ip_lock(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomematicIP lock entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeIpLock,
        device_enum=EntityDefinition.IP_LOCK,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_lock(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic rf lock entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeRfLock,
        device_enum=EntityDefinition.RF_LOCK,
        group_base_channels=group_base_channels,
        extended=extended,
    )


# Case for device model is not relevant
DEVICES: dict[str, CustomConfig | tuple[CustomConfig, ...]] = {
    "HM-Sec-Key": CustomConfig(
        func=make_rf_lock,
        channels=(1,),
        extended=ExtendedConfig(
            additional_entities={
                1: (
                    "DIRECTION",
                    "ERROR",
                ),
            }
        ),
    ),
    "HmIP-DLD": CustomConfig(
        func=make_ip_lock,
        channels=(0,),
        extended=ExtendedConfig(
            additional_entities={
                0: ("ERROR_JAMMED",),
            }
        ),
    ),
}

BLACKLISTED_DEVICES: tuple[str, ...] = ()
