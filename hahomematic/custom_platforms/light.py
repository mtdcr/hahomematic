"""
Module for entities implemented using the light platform.

See https://www.home-assistant.io/integrations/light/.
"""
from __future__ import annotations

from abc import abstractmethod
from typing import Any, cast

from hahomematic.const import HM_ARG_ON_TIME, HmPlatform
from hahomematic.custom_platforms.entity_definition import (
    FIELD_CHANNEL_COLOR,
    FIELD_CHANNEL_LEVEL,
    FIELD_COLOR,
    FIELD_COLOR_LEVEL,
    FIELD_LEVEL,
    FIELD_ON_TIME_UNIT,
    FIELD_ON_TIME_VALUE,
    FIELD_PROGRAM,
    FIELD_RAMP_TIME_UNIT,
    FIELD_RAMP_TIME_VALUE,
    CustomConfig,
    EntityDefinition,
    ExtendedConfig,
    make_custom_entity,
)
from hahomematic.decorators import bind_collector, value_property
import hahomematic.device as hmd
import hahomematic.entity as hme
from hahomematic.entity import CallParameterCollector, CustomEntity
from hahomematic.generic_platforms.action import HmAction
from hahomematic.generic_platforms.number import HmFloat, HmInteger
from hahomematic.generic_platforms.select import HmSelect
from hahomematic.generic_platforms.sensor import HmSensor

# HM constants
HM_ARG_BRIGHTNESS = "brightness"
HM_ARG_COLOR_NAME = "color_name"
HM_ARG_COLOR_TEMP = "color_temp"
HM_ARG_CHANNEL_COLOR = "channel_color"
HM_ARG_CHANNEL_LEVEL = "channel_level"
HM_ARG_EFFECT = "effect"
HM_ARG_HS_COLOR = "hs_color"
HM_ARG_RAMP_TIME = "ramp_time"

HM_EFFECT_OFF = "Off"

HM_MAX_MIREDS: int = 500
HM_MIN_MIREDS: int = 153

HM_DIMMER_OFF: float = 0.0

TIME_UNIT_SECONDS = 0
TIME_UNIT_MINUTES = 1
TIME_UNIT_HOURS = 2


class BaseHmLight(CustomEntity):
    """Base class for HomeMatic light entities."""

    _attr_platform = HmPlatform.LIGHT

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_level: HmFloat = self._get_entity(field_name=FIELD_LEVEL, entity_type=HmFloat)
        self._e_on_time_value: HmAction = self._get_entity(
            field_name=FIELD_ON_TIME_VALUE, entity_type=HmAction
        )
        self._e_ramp_time_value: HmAction = self._get_entity(
            field_name=FIELD_RAMP_TIME_VALUE, entity_type=HmAction
        )

    @value_property
    @abstractmethod
    def is_on(self) -> bool | None:
        """Return true if light is on."""

    @value_property
    @abstractmethod
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""

    @value_property
    def color_temp(self) -> int | None:
        """Return the color temperature in mireds of this light between 153..500."""
        return None

    @value_property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float]."""
        return None

    @value_property
    def supports_brightness(self) -> bool:
        """Flag if light supports brightness."""
        return isinstance(self._e_level, HmFloat)

    @value_property
    def supports_color_temperature(self) -> bool:
        """Flag if light supports color temperature."""
        return False

    @value_property
    def supports_effects(self) -> bool:
        """Flag if light supports effects."""
        return False

    @value_property
    def supports_hs_color(self) -> bool:
        """Flag if light supports color."""
        return False

    @value_property
    def supports_transition(self) -> bool:
        """Flag if light supports transition."""
        return isinstance(self._e_ramp_time_value, HmAction)

    @value_property
    def effect(self) -> str | None:
        """Return the current effect."""
        return None

    @value_property
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects."""
        return None

    @bind_collector
    async def turn_on(
        self,
        collector: CallParameterCollector | None = None,
        **kwargs: dict[str, Any] | None,
    ) -> None:
        """Turn the light on."""
        if HM_ARG_RAMP_TIME in kwargs:
            ramp_time = float(cast(float, kwargs[HM_ARG_RAMP_TIME]))
            await self.set_ramp_time_value(ramp_time=ramp_time, collector=collector)
        if HM_ARG_ON_TIME in kwargs:
            on_time = float(cast(float, kwargs[HM_ARG_ON_TIME]))
            await self.set_on_time_value(on_time=on_time, collector=collector)
        if (
            (brightness := cast(int, (kwargs.get(HM_ARG_BRIGHTNESS, self.brightness)) or 255))
            and brightness != self.brightness
            or kwargs
        ):
            level = brightness / 255.0
            await self._e_level.send_value(value=level, collector=collector)

    @bind_collector
    async def turn_off(
        self, collector: CallParameterCollector | None = None, **kwargs: dict[str, Any] | None
    ) -> None:
        """Turn the light off."""
        if HM_ARG_RAMP_TIME in kwargs:
            ramp_time = float(cast(float, kwargs[HM_ARG_RAMP_TIME]))
            await self.set_ramp_time_value(ramp_time=ramp_time, collector=collector)

        await self._e_level.send_value(value=HM_DIMMER_OFF, collector=collector)

    async def set_on_time_value(
        self, on_time: float, collector: CallParameterCollector | None = None
    ) -> None:
        """Set the on time value in seconds."""
        await self._e_on_time_value.send_value(value=on_time, collector=collector)

    async def set_ramp_time_value(
        self, ramp_time: float, collector: CallParameterCollector | None = None
    ) -> None:
        """Set the ramp time value in seconds."""
        await self._e_ramp_time_value.send_value(value=ramp_time, collector=collector)


class CeDimmer(BaseHmLight):
    """Class for HomeMatic dimmer entities."""

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_channel_level: HmSensor = self._get_entity(
            field_name=FIELD_CHANNEL_LEVEL, entity_type=HmSensor
        )

    @value_property
    def is_on(self) -> bool | None:
        """Return true if dimmer is on."""
        return self._e_level.value is not None and self._e_level.value > HM_DIMMER_OFF

    @value_property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        return int((self._e_level.value or 0.0) * 255)

    @value_property
    def channel_brightness(self) -> int | None:
        """Return the channel_brightness of this light between 0..255."""
        if self._e_channel_level.value is not None:
            return int(self._e_channel_level.value * 255)
        return None


class CeColorDimmer(CeDimmer):
    """Class for HomeMatic dimmer with color entities."""

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_color: HmInteger = self._get_entity(field_name=FIELD_COLOR, entity_type=HmInteger)

    @value_property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float]."""
        if self._e_color.value is not None:
            color = self._e_color.value
            if color >= 200:
                # 200 is a special case (white), so we have a saturation of 0.
                # Larger values are undefined.
                # For the sake of robustness we return "white" anyway.
                return 0.0, 0.0

            # For all other colors we assume saturation of 1
            return color / 200 * 360, 100
        return 0.0, 0.0

    @value_property
    def supports_hs_color(self) -> bool:
        """Flag if light supports color temperature."""
        return True

    @value_property
    def supports_effects(self) -> bool:
        """Flag if light supports effects."""
        return False

    @bind_collector
    async def turn_on(
        self, collector: CallParameterCollector | None = None, **kwargs: Any
    ) -> None:
        """Turn the light on."""
        if HM_ARG_HS_COLOR in kwargs:
            khue, ksaturation = kwargs[HM_ARG_HS_COLOR]
            hue = khue / 360
            saturation = ksaturation / 100
            if saturation < 0.1:  # Special case (white)
                color = 200
            else:
                color = int(round(max(min(hue, 1), 0) * 199))

            await self._e_color.send_value(value=color, collector=collector)
        await super().turn_on(collector=collector, **kwargs)


class CeColorDimmerEffect(CeColorDimmer):
    """Class for HomeMatic dimmer with color entities."""

    _effect_list: list[str] = [
        HM_EFFECT_OFF,
        "Slow color change",
        "Medium color change",
        "Fast color change",
        "Campfire",
        "Waterfall",
        "TV simulation",
    ]

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_effect: HmInteger = self._get_entity(
            field_name=FIELD_PROGRAM, entity_type=HmInteger
        )

    @value_property
    def supports_effects(self) -> bool:
        """Flag if light supports effects."""
        return True

    @value_property
    def effect(self) -> str | None:
        """Return the current effect."""
        if self._e_effect.value is not None:
            return self._effect_list[int(self._e_effect.value)]
        return None

    @value_property
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects."""
        return self._effect_list

    @bind_collector
    async def turn_on(
        self, collector: CallParameterCollector | None = None, **kwargs: Any
    ) -> None:
        """Turn the light on."""
        if HM_ARG_HS_COLOR in kwargs and self.supports_effects and self.effect != HM_EFFECT_OFF:
            await self._e_effect.send_value(value=0, collector=collector)

        if self.supports_effects and HM_ARG_EFFECT in kwargs:
            effect = str(kwargs[HM_ARG_EFFECT])
            effect_idx = self._effect_list.index(effect)
            if effect_idx is not None:
                await self._e_effect.send_value(value=effect_idx, collector=collector)

        await super().turn_on(collector=collector, **kwargs)


class CeColorTempDimmer(CeDimmer):
    """Class for HomeMatic dimmer with color temperature entities."""

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_color_level: HmFloat = self._get_entity(
            field_name=FIELD_COLOR_LEVEL, entity_type=HmFloat
        )

    @value_property
    def color_temp(self) -> int | None:
        """Return the color temperature in mireds of this light between 153..500."""
        return int(
            HM_MAX_MIREDS - (HM_MAX_MIREDS - HM_MIN_MIREDS) * (self._e_color_level.value or 0.0)
        )

    @value_property
    def supports_color_temperature(self) -> bool:
        """Flag if light supports color temperature."""
        return True

    @bind_collector
    async def turn_on(
        self, collector: CallParameterCollector | None = None, **kwargs: Any
    ) -> None:
        """Turn the light on."""
        if HM_ARG_COLOR_TEMP in kwargs:
            color_level = (HM_MAX_MIREDS - kwargs[HM_ARG_COLOR_TEMP]) / (
                HM_MAX_MIREDS - HM_MIN_MIREDS
            )
            await self._e_color_level.send_value(value=color_level, collector=collector)

        await super().turn_on(collector=collector, **kwargs)


class CeIpFixedColorLight(BaseHmLight):
    """Class for HomematicIP HmIP-BSL, HmIPW-WRC6 light entities."""

    _color_switcher: dict[str, tuple[float, float]] = {
        "WHITE": (0.0, 0.0),
        "RED": (0.0, 100.0),
        "YELLOW": (60.0, 100.0),
        "GREEN": (120.0, 100.0),
        "TURQUOISE": (180.0, 100.0),
        "BLUE": (240.0, 100.0),
        "PURPLE": (300.0, 100.0),
    }

    @value_property
    def color_name(self) -> str | None:
        """Return the name of the color."""
        return self._e_color.value

    @property
    def channel_color_name(self) -> str | None:
        """Return the name of the channel color."""
        return self._e_channel_color.value

    def _init_entity_fields(self) -> None:
        """Init the entity fields."""
        super()._init_entity_fields()
        self._e_color: HmSelect = self._get_entity(field_name=FIELD_COLOR, entity_type=HmSelect)
        self._e_channel_color: HmSensor = self._get_entity(
            field_name=FIELD_CHANNEL_COLOR, entity_type=HmSensor
        )
        self._e_level: HmFloat = self._get_entity(field_name=FIELD_LEVEL, entity_type=HmFloat)
        self._e_channel_level: HmSensor = self._get_entity(
            field_name=FIELD_CHANNEL_LEVEL, entity_type=HmSensor
        )
        self._e_on_time_unit: HmAction = self._get_entity(
            field_name=FIELD_ON_TIME_UNIT, entity_type=HmAction
        )
        self._e_ramp_time_unit: HmAction = self._get_entity(
            field_name=FIELD_RAMP_TIME_UNIT, entity_type=HmAction
        )

    @value_property
    def is_on(self) -> bool | None:
        """Return true if dimmer is on."""
        return self._e_level.value is not None and self._e_level.value > 0.0

    @value_property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        return int((self._e_level.value or 0.0) * 255)

    @property
    def channel_brightness(self) -> int | None:
        """Return the channel brightness of this light between 0..255."""
        if self._e_channel_level.value is not None:
            return int(self._e_channel_level.value * 255)
        return None

    @value_property
    def hs_color(self) -> tuple[float, float] | None:
        """Return the hue and saturation color value [float, float]."""
        if self._e_color.value is not None:
            return self._color_switcher.get(self._e_color.value, (0.0, 0.0))
        return 0.0, 0.0

    @property
    def channel_hs_color(self) -> tuple[float, float] | None:
        """Return the channel hue and saturation color value [float, float]."""
        if self._e_channel_color.value is not None:
            return self._color_switcher.get(self._e_channel_color.value, (0.0, 0.0))
        return None

    @value_property
    def supports_hs_color(self) -> bool:
        """Flag if light supports color."""
        return True

    @bind_collector
    async def turn_on(
        self, collector: CallParameterCollector | None = None, **kwargs: Any
    ) -> None:
        """Turn the light on."""
        if HM_ARG_HS_COLOR in kwargs:
            hs_color = kwargs[HM_ARG_HS_COLOR]
            simple_rgb_color = _convert_color(hs_color)
            await self._e_color.send_value(value=simple_rgb_color, collector=collector)

        await super().turn_on(collector=collector, **kwargs)

    @bind_collector
    async def set_on_time_value(
        self, on_time: float, collector: CallParameterCollector | None = None
    ) -> None:
        """Set the on time value in seconds."""
        on_time_unit = TIME_UNIT_SECONDS
        if on_time > 16343:
            on_time /= 60
            on_time_unit = TIME_UNIT_MINUTES
        if on_time > 16343:
            on_time /= 60
            on_time_unit = TIME_UNIT_HOURS

        await self._e_on_time_unit.send_value(value=on_time_unit, collector=collector)
        await self._e_on_time_value.send_value(value=float(on_time), collector=collector)

    @bind_collector
    async def set_ramp_time_value(
        self, ramp_time: float, collector: CallParameterCollector | None = None
    ) -> None:
        """Set the ramp time value in seconds."""
        ramp_time_unit = TIME_UNIT_SECONDS
        if ramp_time > 16343:
            ramp_time /= 60
            ramp_time_unit = TIME_UNIT_MINUTES
        if ramp_time > 16343:
            ramp_time /= 60
            ramp_time_unit = TIME_UNIT_HOURS

        await self._e_ramp_time_unit.send_value(value=ramp_time_unit, collector=collector)
        await self._e_ramp_time_value.send_value(value=float(ramp_time), collector=collector)


def _convert_color(color: tuple[float, float] | None) -> str:
    """
    Convert the given color to the reduced color of the device.

    Device contains only 8 colors including white and black,
    so a conversion is required.
    """
    if color is None:
        return "WHITE"

    hue: int = int(color[0])
    saturation: int = int(color[1])
    if saturation < 5:
        return "WHITE"
    if 30 < hue <= 90:
        return "YELLOW"
    if 90 < hue <= 150:
        return "GREEN"
    if 150 < hue <= 210:
        return "TURQUOISE"
    if 210 < hue <= 270:
        return "BLUE"
    if 270 < hue <= 330:
        return "PURPLE"
    return "RED"


def make_ip_dimmer(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomematicIP dimmer entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeDimmer,
        device_enum=EntityDefinition.IP_DIMMER,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_dimmer(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic classic dimmer entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeDimmer,
        device_enum=EntityDefinition.RF_DIMMER,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_dimmer_color(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic classic dimmer with color entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeColorDimmer,
        device_enum=EntityDefinition.RF_DIMMER_COLOR,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_dimmer_color_effect(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic classic dimmer and effect with color entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeColorDimmerEffect,
        device_enum=EntityDefinition.RF_DIMMER_COLOR,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_dimmer_color_temp(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic classic dimmer with color temperature entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeColorTempDimmer,
        device_enum=EntityDefinition.RF_DIMMER_COLOR_TEMP,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_rf_dimmer_with_virt_channel(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create HomeMatic classic dimmer entities."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeDimmer,
        device_enum=EntityDefinition.RF_DIMMER_WITH_VIRT_CHANNEL,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_ip_fixed_color_light(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create fixed color light entities like HmIP-BSL."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeIpFixedColorLight,
        device_enum=EntityDefinition.IP_FIXED_COLOR_LIGHT,
        group_base_channels=group_base_channels,
        extended=extended,
    )


def make_ip_simple_fixed_color_light(
    device: hmd.HmDevice,
    group_base_channels: tuple[int, ...],
    extended: ExtendedConfig | None = None,
) -> tuple[hme.BaseEntity, ...]:
    """Create simple fixed color light entities like HmIPW-WRC6."""
    return make_custom_entity(
        device=device,
        custom_entity_class=CeIpFixedColorLight,
        device_enum=EntityDefinition.IP_SIMPLE_FIXED_COLOR_LIGHT,
        group_base_channels=group_base_channels,
        extended=extended,
    )


# Case for device model is not relevant
DEVICES: dict[str, CustomConfig | tuple[CustomConfig, ...]] = {
    "263 132": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "263 133": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "263 134": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "HBW-LC-RGBWW-IN6-DR": (
        CustomConfig(
            func=make_rf_dimmer,
            channels=(7, 8),
            extended=ExtendedConfig(
                additional_entities={
                    (1, 2, 3, 4, 5, 6,): (
                        "PRESS_LONG",
                        "PRESS_SHORT",
                        "SENSOR",
                    )
                },
            ),
        ),
        CustomConfig(
            func=make_rf_dimmer_color,
            channels=(9, 10, 11),
            extended=ExtendedConfig(fixed_channels={15: {FIELD_COLOR: "COLOR"}}),
        ),
        CustomConfig(
            func=make_rf_dimmer_color,
            channels=(12, 13, 14),
            extended=ExtendedConfig(fixed_channels={16: {FIELD_COLOR: "COLOR"}}),
        ),
    ),
    "HM-DW-WM": CustomConfig(func=make_rf_dimmer, channels=(1, 2, 3, 4)),
    "HM-LC-AO-SM": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-DW-WM": CustomConfig(func=make_rf_dimmer_color_temp, channels=(1, 3, 5)),
    "HM-LC-Dim1L-CV": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1L-CV-2": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1L-Pl": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1L-Pl-2": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "HM-LC-Dim1L-Pl-3": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1PWM-CV": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1PWM-CV-2": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-CV": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-CV-2": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-DR": CustomConfig(func=make_rf_dimmer, channels=(1, 2, 3)),
    "HM-LC-Dim1T-FM": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-FM-2": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-FM-LF": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "HM-LC-Dim1T-Pl": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1T-Pl-2": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "HM-LC-Dim1T-Pl-3": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1TPBU-FM": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim1TPBU-FM-2": CustomConfig(func=make_rf_dimmer_with_virt_channel, channels=(1,)),
    "HM-LC-Dim2L-CV": CustomConfig(func=make_rf_dimmer, channels=(1, 2)),
    "HM-LC-Dim2L-SM": CustomConfig(func=make_rf_dimmer, channels=(1, 2)),
    "HM-LC-Dim2L-SM-2": CustomConfig(func=make_rf_dimmer, channels=(1, 2, 3, 4, 5, 6)),
    "HM-LC-Dim2T-SM": CustomConfig(func=make_rf_dimmer, channels=(1, 2)),
    "HM-LC-Dim2T-SM-2": CustomConfig(func=make_rf_dimmer, channels=(1, 2, 3, 4, 5, 6)),
    "HM-LC-RGBW-WM": CustomConfig(func=make_rf_dimmer_color_effect, channels=(1,)),
    "HMW-LC-Dim1L-DR": CustomConfig(func=make_rf_dimmer, channels=(3,)),
    "HSS-DX": CustomConfig(func=make_rf_dimmer, channels=(1,)),
    "HmIP-BDT": CustomConfig(func=make_ip_dimmer, channels=(3,)),
    "HmIP-BSL": CustomConfig(func=make_ip_fixed_color_light, channels=(7, 11)),
    "HmIP-DRDI3": CustomConfig(
        func=make_ip_dimmer,
        channels=(4, 8, 12),
        extended=ExtendedConfig(
            additional_entities={
                0: ("ACTUAL_TEMPERATURE",),
            }
        ),
    ),
    "HmIP-FDT": CustomConfig(func=make_ip_dimmer, channels=(1,)),
    "HmIP-PDT": CustomConfig(func=make_ip_dimmer, channels=(2,)),
    "HmIP-SCTH230": CustomConfig(
        func=make_ip_dimmer,
        channels=(11,),
        extended=ExtendedConfig(
            additional_entities={
                1: ("CONCENTRATION",),
                4: (
                    "HUMIDITY",
                    "ACTUAL_TEMPERATURE",
                ),
            }
        ),
    ),
    "HmIPW-DRD3": CustomConfig(
        func=make_ip_dimmer,
        channels=(1, 5, 9),
        extended=ExtendedConfig(
            additional_entities={
                0: ("ACTUAL_TEMPERATURE",),
            }
        ),
    ),
    "HmIPW-WRC6": CustomConfig(
        func=make_ip_simple_fixed_color_light, channels=(7, 8, 9, 10, 11, 12)
    ),
    "OLIGO.smart.iq.HM": CustomConfig(func=make_rf_dimmer, channels=(1, 2, 3, 4, 5, 6)),
}

BLACKLISTED_DEVICES: tuple[str, ...] = ()
