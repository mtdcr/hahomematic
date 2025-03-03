"""
Module for entities implemented using the switch platform.

See https://www.home-assistant.io/integrations/switch/.
"""
from __future__ import annotations

from typing import Any, cast

from hahomematic.const import HM_ARG_ON_TIME, TYPE_ACTION, HmPlatform
from hahomematic.decorators import value_property
from hahomematic.entity import (
    CallParameterCollector,
    GenericEntity,
    GenericSystemVariable,
)

PARAM_ON_TIME = "ON_TIME"


class HmSwitch(GenericEntity[bool]):
    """
    Implementation of a switch.

    This is a default platform that gets automatically generated.
    """

    _attr_platform = HmPlatform.SWITCH

    @value_property
    def value(self) -> bool | None:  # type: ignore[override]
        """Get the value of the entity."""
        if self._attr_type == TYPE_ACTION:
            return False
        return self._attr_value

    async def turn_on(
        self, collector: CallParameterCollector | None = None, **kwargs: dict[str, Any] | None
    ) -> None:
        """Turn the switch on."""
        if HM_ARG_ON_TIME in kwargs:
            on_time = float(cast(float, kwargs[HM_ARG_ON_TIME]))
            await self.set_on_time_value(on_time=on_time)
        await self.send_value(value=True, collector=collector)

    async def turn_off(self, collector: CallParameterCollector | None = None) -> None:
        """Turn the switch off."""
        await self.send_value(value=False, collector=collector)

    async def set_on_time_value(self, on_time: float) -> None:
        """Set the on time value in seconds."""
        await self._client.set_value(
            channel_address=self._attr_channel_address,
            paramset_key=self._attr_paramset_key,
            parameter=PARAM_ON_TIME,
            value=float(on_time),
        )


class HmSysvarSwitch(GenericSystemVariable):
    """Implementation of a sysvar switch entity."""

    _attr_platform = HmPlatform.HUB_SWITCH
    _attr_is_extended = True
