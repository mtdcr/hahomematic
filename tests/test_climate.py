"""Tests for climate entities of hahomematic."""
from __future__ import annotations

from datetime import datetime
from typing import cast
from unittest.mock import call

import const
import helper
import pytest

from hahomematic.const import HmEntityUsage
from hahomematic.custom_platforms.climate import (
    HMIP_MODE_AUTO,
    HMIP_MODE_AWAY,
    HMIP_MODE_MANU,
    CeIpThermostat,
    CeRfThermostat,
    CeSimpleRfThermostat,
    HmHvacAction,
    HmHvacMode,
    HmPresetMode,
)

TEST_DEVICES: dict[str, str] = {
    "VCU1769958": "HmIP-BWTH.json",
    "VCU3609622": "HmIP-eTRV-2.json",
    "INT0000001": "HM-CC-VG-1.json",
    "VCU5778428": "HmIP-HEATING.json",
    "VCU0000054": "HM-CC-TC.json",
    "VCU0000050": "HM-CC-RT-DN.json",
}


@pytest.mark.asyncio
async def test_cesimplerfthermostat(
    central_local_factory: helper.CentralUnitLocalFactory,
) -> None:
    """Test CeSimpleRfThermostat."""
    central, mock_client = await central_local_factory.get_default_central(TEST_DEVICES)
    climate: CeSimpleRfThermostat = cast(
        CeSimpleRfThermostat, await helper.get_custom_entity(central, "VCU0000054", 1)
    )
    assert climate.usage == HmEntityUsage.CE_PRIMARY

    assert climate.is_valid is False
    assert climate.state_uncertain is True
    assert climate.temperature_unit == "°C"
    assert climate.min_temp == 6.0
    assert climate.max_temp == 30.0
    assert climate.supports_preset is False
    assert climate.target_temperature_step == 0.5

    assert climate.current_humidity is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000054:1", "HUMIDITY", 75)
    assert climate.current_humidity == 75

    assert climate.target_temperature is None
    await climate.set_temperature(12.0)
    last_call = call.set_value(
        channel_address="VCU0000054:2",
        paramset_key="VALUES",
        parameter="SETPOINT",
        value=12.0,
    )
    assert mock_client.method_calls[-1] == last_call
    assert climate.target_temperature == 12.0

    assert climate.current_temperature is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000054:1", "TEMPERATURE", 11.0)
    assert climate.current_temperature == 11.0

    assert climate.hvac_mode == HmHvacMode.HEAT
    assert climate.hvac_modes == [HmHvacMode.HEAT]
    assert climate.preset_mode == HmPresetMode.NONE
    assert climate.preset_modes == [HmPresetMode.NONE]
    assert climate.hvac_action is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000054:1", "TEMPERATURE", 11.0)

    # No new method call, because called methods has no implementation
    await climate.set_hvac_mode(HmHvacMode.HEAT)
    assert mock_client.method_calls[-1] == last_call
    await climate.set_preset_mode(HmPresetMode.NONE)
    assert mock_client.method_calls[-1] == last_call
    await climate.enable_away_mode_by_duration(hours=100, away_temperature=17.0)
    assert mock_client.method_calls[-1] == last_call
    await climate.enable_away_mode_by_calendar(
        start=datetime.now(), end=datetime.now(), away_temperature=17.0
    )
    assert mock_client.method_calls[-1] == last_call
    await climate.disable_away_mode()
    assert mock_client.method_calls[-1] == last_call


@pytest.mark.asyncio
async def test_cerfthermostat(
    central_local_factory: helper.CentralUnitLocalFactory,
) -> None:
    """Test CeRfThermostat."""
    central, mock_client = await central_local_factory.get_default_central(TEST_DEVICES)
    climate: CeRfThermostat = cast(
        CeRfThermostat, await helper.get_custom_entity(central, "VCU0000050", 4)
    )
    assert climate.usage == HmEntityUsage.CE_PRIMARY
    assert climate.min_temp == 5.0
    assert climate.max_temp == 30.5
    assert climate.supports_preset is True
    assert climate.target_temperature_step == 0.5
    assert climate.preset_mode == HmPresetMode.NONE
    assert climate.hvac_action is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "VALVE_STATE", 10)
    assert climate.hvac_action == HmHvacAction.HEAT
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "VALVE_STATE", 0)
    assert climate.hvac_action == HmHvacAction.IDLE
    assert climate.current_humidity is None
    assert climate.target_temperature is None
    await climate.set_temperature(12.0)
    assert mock_client.method_calls[-1] == call.set_value(
        channel_address="VCU0000050:4",
        paramset_key="VALUES",
        parameter="SET_TEMPERATURE",
        value=12.0,
    )
    assert climate.target_temperature == 12.0

    assert climate.current_temperature is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "ACTUAL_TEMPERATURE", 11.0)
    assert climate.current_temperature == 11.0

    assert climate.hvac_mode == HmHvacMode.AUTO
    assert climate.hvac_modes == [HmHvacMode.AUTO, HmHvacMode.HEAT, HmHvacMode.OFF]
    await climate.set_hvac_mode(HmHvacMode.HEAT)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU0000050:4", paramset_key="VALUES", value={"MANU_MODE": 12.0}
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "CONTROL_MODE", HMIP_MODE_MANU)
    assert climate.hvac_mode == HmHvacMode.HEAT

    await climate.set_hvac_mode(HmHvacMode.OFF)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU0000050:4",
        paramset_key="VALUES",
        value={"MANU_MODE": 12.0, "SET_TEMPERATURE": 4.5},
    )

    assert climate.hvac_mode == HmHvacMode.OFF
    assert climate.hvac_action == HmHvacAction.OFF

    await climate.set_hvac_mode(HmHvacMode.AUTO)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU0000050:4", paramset_key="VALUES", value={"AUTO_MODE": True}
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "CONTROL_MODE", 0)
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "SET_TEMPERATURE", 24.0)
    assert climate.hvac_mode == HmHvacMode.AUTO

    assert climate.preset_mode == HmPresetMode.NONE
    assert climate.preset_modes == [
        HmPresetMode.BOOST,
        HmPresetMode.COMFORT,
        HmPresetMode.ECO,
        HmPresetMode.NONE,
    ]
    await climate.set_preset_mode(HmPresetMode.BOOST)
    assert mock_client.method_calls[-1] == call.set_value(
        channel_address="VCU0000050:4",
        paramset_key="VALUES",
        parameter="BOOST_MODE",
        value=True,
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "CONTROL_MODE", 3)
    assert climate.preset_mode == HmPresetMode.BOOST
    central.event(const.LOCAL_INTERFACE_ID, "VCU0000050:4", "CONTROL_MODE", 2)
    assert climate.preset_mode == HmPresetMode.AWAY
    await climate.set_preset_mode(HmPresetMode.COMFORT)
    assert mock_client.method_calls[-1] == call.set_value(
        channel_address="VCU0000050:4",
        paramset_key="VALUES",
        parameter="COMFORT_MODE",
        value=True,
    )
    await climate.set_preset_mode(HmPresetMode.ECO)
    assert mock_client.method_calls[-1] == call.set_value(
        channel_address="VCU0000050:4",
        paramset_key="VALUES",
        parameter="LOWERING_MODE",
        value=True,
    )


@pytest.mark.asyncio
async def test_ceipthermostat(
    central_local_factory: helper.CentralUnitLocalFactory,
) -> None:
    """Test CeIpThermostat."""
    central, mock_client = await central_local_factory.get_default_central(TEST_DEVICES)
    climate: CeIpThermostat = cast(
        CeIpThermostat, await helper.get_custom_entity(central, "VCU1769958", 1)
    )
    assert climate.usage == HmEntityUsage.CE_PRIMARY
    assert climate.min_temp == 5.0
    assert climate.max_temp == 30.5
    assert climate.supports_preset is True
    assert climate.target_temperature_step == 0.5
    assert climate.hvac_action == HmHvacAction.IDLE
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:9", "STATE", 1)
    assert climate.hvac_action == HmHvacAction.HEAT
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:9", "STATE", 0)
    assert climate.hvac_action == HmHvacAction.IDLE

    assert climate.current_humidity is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "HUMIDITY", 75)
    assert climate.current_humidity == 75

    assert climate.target_temperature is None
    await climate.set_temperature(12.0)
    assert mock_client.method_calls[-1] == call.set_value(
        channel_address="VCU1769958:1",
        paramset_key="VALUES",
        parameter="SET_POINT_TEMPERATURE",
        value=12.0,
    )
    assert climate.target_temperature == 12.0

    assert climate.current_temperature is None
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "ACTUAL_TEMPERATURE", 11.0)
    assert climate.current_temperature == 11.0

    assert climate.hvac_mode == HmHvacMode.AUTO
    assert climate.hvac_modes == [HmHvacMode.AUTO, HmHvacMode.HEAT, HmHvacMode.OFF]
    assert climate.preset_mode == HmPresetMode.NONE

    await climate.set_hvac_mode(HmHvacMode.OFF)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={"CONTROL_MODE": 1, "SET_POINT_TEMPERATURE": 4.5},
    )
    assert climate.hvac_mode == HmHvacMode.OFF
    assert climate.hvac_action == HmHvacAction.OFF

    await climate.set_hvac_mode(HmHvacMode.HEAT)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={"CONTROL_MODE": 1, "SET_POINT_TEMPERATURE": 5.0},
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "SET_POINT_MODE", HMIP_MODE_MANU)
    assert climate.hvac_mode == HmHvacMode.HEAT

    assert climate.preset_mode == HmPresetMode.NONE
    assert climate.preset_modes == [
        HmPresetMode.BOOST,
        HmPresetMode.NONE,
    ]
    await climate.set_preset_mode(HmPresetMode.BOOST)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1", paramset_key="VALUES", value={"BOOST_MODE": True}
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "BOOST_MODE", 1)
    assert climate.preset_mode == HmPresetMode.BOOST

    await climate.set_hvac_mode(HmHvacMode.AUTO)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={"BOOST_MODE": False, "CONTROL_MODE": 0},
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "SET_POINT_MODE", HMIP_MODE_AUTO)
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "BOOST_MODE", 1)
    assert climate.hvac_mode == HmHvacMode.AUTO
    assert climate.preset_modes == [
        HmPresetMode.BOOST,
        HmPresetMode.NONE,
        "week_program_1",
        "week_program_2",
        "week_program_3",
        "week_program_4",
        "week_program_5",
        "week_program_6",
    ]
    await climate.set_preset_mode(HmPresetMode.NONE)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1", paramset_key="VALUES", value={"BOOST_MODE": False}
    )
    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "SET_POINT_MODE", HMIP_MODE_AWAY)
    assert climate.preset_mode == HmPresetMode.AWAY

    central.event(const.LOCAL_INTERFACE_ID, "VCU1769958:1", "SET_POINT_MODE", HMIP_MODE_AUTO)
    await climate.set_preset_mode(HmPresetMode.WEEK_PROGRAM_1)
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1", paramset_key="VALUES", value={"ACTIVE_PROFILE": 1}
    )
    assert climate.preset_mode == HmPresetMode.WEEK_PROGRAM_1

    await climate.enable_away_mode_by_duration(hours=100, away_temperature=17.0)
    # assert mock_client.method_calls[-2] == call.put_paramset(
    #     address="VCU1769958:1",
    #     paramset_key="VALUES",
    #     value={
    #         "CONTROL_MODE": 2,
    #         "PARTY_TIME_END": "2023_01_28 18:47",
    #         "PARTY_TIME_START": "2023_01_24 14:37",
    #     },
    # )
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={"SET_POINT_TEMPERATURE": 17.0},
    )
    await climate.enable_away_mode_by_calendar(
        start=datetime(2000, 12, 1), end=datetime(2024, 12, 1), away_temperature=17.0
    )
    assert mock_client.method_calls[-2] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={
            "CONTROL_MODE": 2,
            "PARTY_TIME_END": "2024_12_01 00:00",
            "PARTY_TIME_START": "2000_12_01 00:00",
        },
    )
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={"SET_POINT_TEMPERATURE": 17.0},
    )
    await climate.disable_away_mode()
    assert mock_client.method_calls[-1] == call.put_paramset(
        address="VCU1769958:1",
        paramset_key="VALUES",
        value={
            "CONTROL_MODE": 2,
            "PARTY_TIME_START": "2000_01_01 00:00",
            "PARTY_TIME_END": "2000_01_01 00:00",
        },
    )
