# Version 2023.1.8 (2023-01-XX)
- Remove VALVE_STATE from HmIPW-FALMOT-C12
- Remove support for python 3.9
- Replace old-style union syntax
- Remove to int converter for HmIP-SCTH230 CONCENTRATION
- Remove set_value, put_paramset from central
- Remove put_paramset from custom_entity
- Cleanup code base with ruff 

# Version 2023.1.7 (2023-01-24)
- Aggregate calls to backend
- Fix HmIP-MOD-TM: inverted direction

# Version 2023.1.6 (2023-01-22)
- Add a new custom entity type for windows drive
- Return True if sending service calls succeed

# Version 2023.1.5 (2023-01-20)
- Remove LOWBAT from HM-LC-Sw1-DR
- Sort lists in parameter_visibility.py
- Replace custom entity config data structure by CustomConfig
- Allow multiple CustomConfigs for a hm device
- Add ExtendedConfig to custom entities
- Cleanup test imports
- Increase the line length to 99
- Add ExtendedConfig and use for additional_entities
- Remove obsolete ED_ADDITIONAL_ENTITIES_BY_DEVICE_TYPE from entity_definition
- Add LED_STATUS to HM-OU-LED16

# Version 2023.1.4 (2023-01-16)
- Remove obsolete parse_ccu_sys_var
- Add helper, central tests
- Add more tests and test based refactorings
- Reduce backend calls and logging during lost connection
- Update color_conversion threshold by @guillempages

# Version 2023.1.3 (2023-01-13)
- Unifiy event parameters
- Refactor entity.py for better event support
- Fix wrong warning after set_system_variable
- Add validation to event_data

# Version 2023.1.2 (2023-01-10)
- Remove OPERATING_VOLTAGE from HmIP-BROLL, HmIP-FROLL
- Remove loop from test signature
- Cleanup ignore/unignore handling and add tests

# Version 2023.1.1 (2023-01-09)
- No longer create ClientSession in json_rpc_client for tests
- Add backend tests
- Use mocked local client to check  method_calls
- Remove sleep after connection_checker stops
- Remove LOWBAT from HM-LC-Sw1-Pl, HM-LC-Sw2-FM
- Simplify entity de-/registration
- Refactor add/delete device and add tests
- Add un_ignore_list to test config
- Allow unignore for DEVICE_ERROR_EVENTS

# Version 2023.1.0 (2023-01-01)
- API Cleanup
- Allow to disable cache
- Allow to disable un_ignore load
- Add local client
- Use local client in tests
- Move event() code to central_unit
- Move listDevices() code to central_unit

# Version 2022.12.12 (2022-12-30)
- Add un_ignore list to central config
- Fix entity_definition schema
- Rename cache_dict to persistent_cache
- Reduce access to internal complex objects for custom_component

# Version 2022.12.11 (2022-12-28)
- Rename climate presets from 'Profile *' to 'week_program_*'
- Add support for python 3.11

# Version 2022.12.10 (2022-12-27)
- Make constant assignment final
- Fix native device units

# Version 2022.12.9 (2022-12-25)
- Remove empty unit for numeric sysvars
- Add enable_default to entity
- Remove some warn level parameters from ignore list

# Version 2022.12.8 (2022-12-22)
- Reformat code / check with flake8
- Refactor entity inheritance

# Version 2022.12.7 (2022-12-21)
- Send ERROR_* parameters as homematic.device_error event

# Version 2022.12.6 (2022-12-20)
- Add additional checks for custom entities
- Code Cleanup

# Version 2022.12.5 (2022-12-17)
- Code Cleanup
 - Remove sub_type from model to simplify code
 - Remove obsolete methods
 - Refactor binary_sensor check
 - Convert value_list to tuple
 - Use tuple for immutable lists

# Version 2022.12.4 (2022-12-13)
- Fix disable away_mode in climate. Now goes back to the origin control_mode.

# Version 2022.12.3 (2022-12-12)
- Disable temperature validation for setting to off for HM heating group HM-CC-VG-1

# Version 2022.12.2 (2022-12-09)
- Add HM-LC-AO-SM as light
- Remove hub from HmPlatform
- Hub is no longer an entity

# Version 2022.12.1 (2022-12-01)
- Improve naming of modules
- Add new platform for text sysvars

# Version 2022.12.0 (2022-12-01)
- Add transition to light turn_off
- Remove min brightness of 10 for lights

# Version 2022.11.2 (2022-11-13)
- Generalize some collection helpers

# Version 2022.11.1 (2022-11-03)
- Rename protected attributes to _attr*
- Code cleanup
- Add option to wrap entities to a different platform
  - Wrap LEVEL of HmIP-TRV*, HmIP-HEATING to sensor

# Version 2022.11.0 (2022-11-02)
- Rename ATTR_HM_* to HM*
- Use generic property implementation

# Version 2022.10.10 (2022-10-25)
- Use min_temp if target_temp < min_temp
- Remove event_loop from signatures
- Refactor central_config, create xml_rpc server in central_unit

# Version 2022.10.9 (2022-10-23)
- Fix don't hide unignored parameters
- Refactor refesh_entity_data. Allow restriction to paramset and cache age.

# Version 2022.10.8 (2022-10-21)
- Add semaphore to fetch sysvar and programs from backend

# Version 2022.10.7 (2022-10-20)
- Accept some existing prefix for sysvars and programs to avoid additional prefixing with Sv_ / P_
  - accepted sysvar prefixes: V_, Sv_
  - accepted program prefixes: P_, Prg_
- Read min/max temperature for climate devices
- Min set temperature for thermostats is now 5.0 degree. 4.5. degree is only off

# Version 2022.10.6 (2022-10-15)
- Replace data_* by HmDataOperationResult
- Use HmHvacMode HEAT instead of AUTO for simple thermostats
- Add HUMIDITY and ACTUAL_TEMPERATURE to heating groups

# Version 2022.10.5 (2022-10-11)
- Set Hm Thermostat to manual mode before switching off

# Version 2022.10.4 (2022-10-10)
- Allow entity creation for some internal paramters

# Version 2022.10.3 (2022-10-10)
- Fix HM Blind/Cover custom entity types

# Version 2022.10.2 (2022-10-08)
- Make connection checker more resilent:
 - Reduce connection checker interval to 15s
 - Connection is not connected, if three consecutive checks fail.

# Version 2022.10.1 (2022-10-05)
- Ignore OPERATING_VOLTAGE for HmIP-PMFS
- Add ALPHA-IP-RBG

# Version 2022.10.0 (2022-10-01)
- Rename hub event
- Remove "Servicemeldungen" from sysvars. It's alread included in the hub_entity (sensor.{instance_name})

# Version 2022.9.1 (2022-09-20)
- Improve XmlServer shutdown
- Add name to threads and executors
- Improve ThreadPoolExecutor shutdown

# Version 2022.9.0 (2022-09-02)
- Exclude value from event_data if None

# Version 2022.8.15 (2022-08-27)
- Fix select entity detection

# Version 2022.8.14 (2022-08-23)
- Exclude STRING sysvar from extended check

# Version 2022.8.13 (2022-08-23)
- Allow three states for a forced availability of a device

# Version 2022.8.12 (2022-08-23)
- Add device_type to device availability event
- Code deduplication and small fixes

# Version 2022.8.11 (2022-08-18)
- Adjust logging (level and message)
- Delete sysvar if type changes

# Version 2022.8.10 (2022-08-16)
- Improve readability of XmlRpc server
- Remove module data

# Version 2022.8.9 (2022-08-16)
- Fix check if thread is started

# Version 2022.8.8 (2022-08-16)
- Remove unused local_ip from XmlRPCServer
- Create all XmlRpc server by requested port(s)

# Version 2022.8.7 (2022-08-12)
- Fix hs_color for CeColorDimmer(HM-LC-RGBW-WM)

# Version 2022.8.6 (2022-08-12)
- Reduce api calls for light

# Version 2022.8.5 (2022-08-11)
- Add cache for rega script files

# Version 2022.8.4 (2022-08-08)
- Add platform as field and remove obsolete constructors
- Reduce member

# Version 2022.8.3 (2022-08-07)
- Remove CHANNEL_OPERATION_MODE from cover ce
- Refactor get_value/set_value
- Remove domain from model
- Rename unique_id to unique_identifier
- Remove should_poll from model

# Version 2022.8.2 (2022-08-02)
- Remove obsolete methods
- Remove obsolete device_address parameter
- Rename sysvar to hub entity
- Add program buttons

# Version 2022.8.0 (2022-08-01)
- Fix pylint, mypy issues due to newer versions
- Remove properties of final members
- Add types to Final
- Init entity fields in init method
- Remove device_info from model
- Remove attributes from model

# Version 2022.7.14 (2022-07-28)
- Add HmIP-BS2 to custom entities
- Remove force and add call_source for getValue

# Version 2022.7.13 (2022-07-22)
- Cleanup API
- Limit init cache time usage
- Avoid repetitive calls to CCU within max_age_seconds

# Version 2022.7.12 (2022-07-21)
- Add ELV-SH-BS2 to custom entities
- Code Cleanup
- Rearrange validity check
- Cleanup entity code

# Version 2022.7.11 (2022-07-19)
- Raise interval for alive checks

# Version 2022.7.10 (2022-07-19)
- Use entities instead of values inside custom entities
- Fix _check_connection for Homegear/CCU

# Version 2022.7.9 (2022-07-17)
- Remove state_uncertain from default attributes

# Version 2022.7.8 (2022-07-13)
- Fix entity update

# Version 2022.7.7 (2022-07-12)
- Fix naming of custom entity

# Version 2022.7.6 (2022-07-12)
- Fix last_state handling for custom entities

# Version 2022.7.5 (2022-07-11)
- Rename value_uncertain to state_uncertain
- Add state_uncertain to custom entity

# Version 2022.7.4 (2022-07-11)
- Set value_uncertain to True if no data could be loaded from CCU

# Version 2022.7.3 (2022-07-10)
- Set default value for hub entity to None

# Version 2022.7.2 (2022-07-10)
- Align enity naming to HA entity name
- Ensure entity value refresh after reconnect
- Ignore further parameters by device

# Version 2022.7.1 (2022-07-07)
- Better distinguish between NO_CACHE_ENTRY and None

# Version 2022.7.0 (2022-07-07)
- Switch to calendar versioning for hahomematic

# Version 1.9.4 (2022-07-03)
- Load MASTER data on initial load

# Version 1.9.3 (2022-07-02)
- Fix export of device definitions

# Version 1.9.2 (2022-07-01)
- Use CHANNEL_OPERATION_MODE for devices with MULTI_MODE_INPUT_TRANSMITTER, KEY_TRANSCEIVER channels
- Readd HmIPW-FIO6 to custom device handling

# Version 1.9.1 (2022-06-29)
- Remove HmIPW-FIO6 from custom device handling

# Version 1.9.0 (2022-06-09)
- Refactor entity name creation
- Cleanup entity selection
- Add button to virtual remote

# Version 1.8.6 (2022-06-07)
 - Code cleanup

# Version 1.8.5 (2022-06-06)
 - Remove sysvars if deleted from CCU
 - Add check for sysvar type in sensor
 - Remove unused sysvar attributes
 - Refactor EntityDefinition

# Version 1.8.4 (2022-06-04)
- Refactor all sysvar script
- Use ext_marker script in combination with SysVar.getAll

# Version 1.8.3 (2022-06-04)
- Refactor sysvar creation eventing

# Version 1.8.2 (2022-06-03)
- Fix build

# Version 1.8.1 (2022-06-03)
- Use marker in sysvar description for extended sysvars

# Version 1.8.0 (2022-06-02)
- Enable additional sysvar entity types

# Version 1.7.3 (2022-06-01)
- Add more debug logging

# Version 1.7.2 (2022-06-01)
- Better differentiate between float and int for sysvars
- Switch from # as unit placeholder for sysvars to ' '
- Move sysvar length check to sensor

# Version 1.7.1 (2022-05-31)
- Rename parameter channel_address to address for put/get_paramset

# Version 1.7.0 (2022-05-31)
- Refactor system variables
- Add more types for sysvar entities

# Version 1.6.2 (2022-05-30)
- Add more options for boolean conversions

# Version 1.6.1 (2022-05-29)
- Fix entity definition for HMIP-HEATING

# Version 1.6.0 (2022-05-29)
- Add impulse event
- Add LEVEL and STATE to HmIP-Heating group to display hvac_action
- Add device_type as model to attributes

# Version 1.5.4 (2022-05-24)
- Add function attribute only if set

# Version 1.5.3 (2022-05-24)
- Rename subsection to function

# Version 1.5.2 (2022-05-24)
- Add subsection to attributes
- Use parser for internal sysvars

# Version 1.5.0 (2022-05-23)
- Add option to replace too technical parameter name by friendly parameter name
- Ignore more parameters by device
- Use dataclass for sysvars
- Limit sysvar length to 255 chars due to HA limitations

# Version 1.4.0 (2022-05-16)
- Block parameters by device_type that should not create entities in HA
- Fix remove instance on shutdown

# Version 1.3.1 (2022-05-13)
- Increase connection timeout(30s->60s) and reconnect interval(90s->120s) to better support slower hardware

# Version 1.3.0 (2022-05-06)
- Use unit for vars, if available
- Remove special handling for pydevccu
- Remove set boost mode to false, when preset is none for bidcos climate entities

# Version 1.2.2 (2022-05-02)
- Fix light channel for multi dimmer

# Version 1.2.1 (2022-04-27)
- Fix callback alive check
- Reconnect clients based on outstanding xml callback events

# Version 1.2.0 (2022-04-26)
- Cleanup build

# Version 1.1.5 (2022-04-25)
- Reorg light attributes
- Add on_time to light and switch

# Version 1.1.4 (2022-04-21)
- Use min as default if default is unset for parameter_data

# Version 1.1.3 (2022-04-20)
- Add CeColorDimmer
- Fix interface_event

# Version 1.1.2 (2022-04-12)
- Add extra_params to _post_script
- Add set_system_variable with string value
- Disallow html tags in string system variable

# Version 1.1.1 (2022-04-11)
- Read # Version and serial in get_client

# Version 1.1.0 (2022-04-09)
- Add BATTERY_STATE to DEFAULT_ENTITIES
- Migrate device_info to dataclass
- Add rega script (provided by @baxxy13) to get serial from CCU
- Add method to clean up cache dirs

# Version 1.0.6 (2022-04-06)
- Revert to XmlRPC getValue and getParamset for CCU

# Version 1.0.5 (2022-04-05)
- Limit hub_state to ccu only

# Version 1.0.4 (2022-03-30)
- Use max # Version of interfaces for backend version
- Remove device as parameter from parameter_availability
- Add XmlRPC.listDevice to Client
- Add start_direct for starts without waiting for events (only for temporary usage)

# Version 1.0.3 (2022-03-30)
- Revert to XmlRPC get# Version for CCU

# Version 1.0.2 (2022-03-29)
- Revert to XmlRPC getParamsetDescription for CCU

# Version 1.0.1 (2022-03-29)
- Add central_id for uniqueness of heating groups, sysvars and hub

# Version 1.0.0 (2022-03-28)
- Simplify json usage
- Move json methods to json client
- Make json client independent from central config
- Add get_serial to validate
- Use serial for sysvar unique_ids
- Rename domain for test and example from hahm to homematicip_local

# Version 0.38.5 (2022-03-22)
- Use interface_id for interface events
- Add support for color temp dimmer

# Version 0.38.4 (2022-03-21)
- Fix interface name for BidCos-Wired

# Version 0.38.3 (2022-03-20)
- Add check for available API method to identify BidCos Wired
- Cleanup backend identification

# Version 0.38.2 (2022-03-20)
- Catch SysVar parsing exceptions

# Version 0.38.1 (2022-03-20)
- Fix lock/unlock for HM-Sec-Key

# Version 0.38.0 (2022-03-20)
- Add central validation
- Add jso_rpc.post_script

# Version 0.37.7 (2022-03-18)
- Add additional system_listMethods to avoid errors on CCU

# Version 0.37.6 (2022-03-18)
- Add JsonRPC.Session.logout before central stop to avoid warn logs at CCU.

# Version 0.37.5 (2022-03-18)
- Add api for available interfaces
- Send event if interface is not available
- Don't block available interfaces

# Version 0.37.4 (2022-03-17)
- Fix reload paramset
- Fix value converter

# Version 0.37.3 (2022-03-17)
- Cleanup caching code

# Version 0.37.2 (2022-03-17)
- Use homematic script to fetch initial data for CCU/HM

# Version 0.37.1 (2022-03-16)
- Add semaphore(1) to improve cache usage (less api calls)

# Version 0.37.0 (2022-03-15)
- Avoid unnecessary prefetches
- Fix JsonRPC Session handling
- Rename NamesCache to DeviceDetailsCache
- Move RoomCache to DeviceDetailsCache
- Move hm value converter to helpers
- Use JSON RPC for get_value, get_paramset, get_paramset_description
- Use default for binary_sensor

# Version 0.36.3 (2022-03-09)
- Add hub property
- Add check if callback is already registered
- Use callback when hub is created

# Version 0.36.2 (2022-03-06)
- Fix cover device mapping

# Version 0.36.1 (2022-03-06)
- Small climate fix
- Make more devices custom_entities

# Version 0.36.0 (2022-02-24)
- Remove HA constants
- Use enums own constants

# Version 0.35.3 (2022-02-23)
- Move xmlrpc credentials to header

# Version 0.35.2 (2022-02-22)
- Remove password from Exceptions

# Version 0.35.1 (2022-02-21)
- Fix IpBlind
- Fix parameter visibility

# Version 0.35.0 (2022-02-19)
- Fix usage of async_add_executor_job
- Improve local_ip identification

# Version 0.34.2 (2022-02-16)
- Add is_locking/is_unlocking to lock

# Version 0.34.1 (2022-02-16)
- Fix siren definition

# Version 0.34.0 (2022-02-15)
- Use backported StrEnum
- Sort constants to identify HA constants
- Add new platform siren

# Version 0.33.0 (2022-02-14)
- Make parameter availability more robust
- Add hvac_action to IP Thermostats
- Add hvac_action to some HM Thermostats

# Version 0.32.4 (2022-02-12)
- add opening/closing to IPGarage

# Version 0.32.3 (2022-02-12)
- Add state to HmIP-MOD-HO
- Use enum value for actions

# Version 0.32.2 (2022-02-11)
- Fix HmIP-MOD-HO

# Version 0.32.1 (2022-02-11)
- Update to pydevccu 0.1.3
- Priotize detection of devices for custom entities (e.g. HmIP-PCBS2)
- Add HmIPW-FIO6 as CE

# Version 0.32.0 (2022-02-10)
- Move create_devices to central
- Move parameter visibility relevant data to own module

# Version 0.31.2 (2022-02-08)
- Add HmIP-HDM2 to cover
- Fix unignore filename

# Version 0.31.1 (2022-02-07)
- Improve naming
- Add multiplier to entity
- Substitute device_type of HB devices for usage in custom_entities

# Version 0.31.0 (2022-02-06)
- Add missing return statement
- Add last_update to every value_cache_entry
- Rename init_entity_value to load_entity_value
- move (un)ignore methods to device
- Add support for unignore file
- Make PROCESS a binary_sensor
- Add DIRECTION & ACTIVITY_STATE to cover (is_opening, is_closing)

# Version 0.30.1 (2022-02-04)
- Start hub earlier

# Version 0.30.0 (2022-02-03)
- Add paramset to entity
- Add CHANNEL_OPERATION_MODE for HmIP(W)-DRBL4
- Fix DLD lock_state
- Add is_jammed to locks

# Version 0.29.2 (2022-02-02)
- Add support for blacklisting a custom entity
- Add HmIP-STH to climate custom entities

# Version 0.29.1 (2022-02-02)
- Check if interface callback is alive
- Add class for HomeamaticIP Blinds

# Version 0.29.0 (2022-02-01)
- Make device availability dependent on the client
- Fire event about interface availability

# Version 0.28.7 (2022-01-30)
- Add additional check to reconnect

# Version 0.28.6 (2022-01-30)
- Optimize get_value caching

# Version 0.28.5 (2022-01-30)
- Extend device cache to use get_value

# Version 0.28.4 (2022-01-30)
- Limit read proxy workers to 1

# Version 0.28.3 (2022-01-29)
- Rename RawDevicesCache to DeviceDescriptionCache

# Version 0.28.2 (2022-01-29)
- Make names cache non persistent
- Bump pydevccu to 0.1.2

# Version 0.28.1 (2022-01-28)
- Update hub.py to match GenericEntity
- Cleanup central API
- Use dedicated proxy for mass read operations, to avoid blocking of connection checker

# Version 0.28.0 (2022-01-27)
- Try create client after init failure
- Reduce CCU calls

# Version 0.27.2 (2022-01-25)
- Optimize data_load

# Version 0.27.1 (2022-01-25)
- Fix naming paramset -> paramset_description pt2
- Optimize data_load by using get_paramset

# Version 0.27.0 (2022-01-25)
- Fix naming paramset -> paramset_description
- Add get_value and get_paramset to central
- Add hmcli.py as command line script

# Version 0.26.0 (2022-01-22)
- Make whitelist for parameter depend on the device_type/sub_type
- Add additional params for HM-SEC-Win (DIRECTION, ERROR, WORKING, STATUS)
- Add additional params for HM-SEC-Key (DIRECTION, ERROR)
- Assign secondary channels for HM dimmers
- Remove explicit wildcard in entity_definition

# Version 0.25.0 (2022-01-19)
- Remove SpecialEvents
- Make UNREACH, STICKY_UNREACH, CONFIG_PENDING generic entities
- init UNREACH ... on init
- only poll sysvars when central is available

# Version 0.24.4 (2022-01-18)
- Improve logging
- Generic schema for entities is name(str):channel(int), everthing else is custom.

- Fix sysvar unique_id
- Slugify sysvar name
- Kill executor on shutdown
- Catch ValueError on conversion
- Add more data to logging

# Version 0.24.0-0.24.2 (2022-01-17)
- Improve exception handling

# Version 0.23.3 (2022-01-16)
- Update fix_rssi according to doc

# Version 0.23.1 (2022-01-16)
- Add more logging to reconnect
- Add doc link for RSSI fix

# Version 0.23.0 (2022-01-16)
- Make ["DRY", "RAIN"] sensor a binary_sensor
- Add converter to sensor value
    - HmIP-SCTH230 CONCENTRATION to int
    - Fix RSSI
- raise connection_checker interval to 60s
- Add sleep interval(120s) to wait with reconnect after successful connection check

# Version 0.22.2 (2022-01-15)
- Rename hub extra_state_attributes to attributes

# Version 0.22.1 (2022-01-15)
- Add VALVE_STATE for hm climate
- Add entity_type to attributes
- Accept LOWBAT only on channel 0

# Version 0.22.0 (2022-01-14)
- Move client management to central
- Add rooms
- Move calls to create_devices and start_connection_checker

# Version 0.21.2 (2022-01-13)
- Add ERROR_LOCK form HmIP-DLD
- Remove ALARM_EVENTS

# Version 0.21.1 (2022-01-13)
- Fix event identification and generation

# Version 0.21.0 (2022-01-13)
- Remove typecast for text, binary_sensor and number
- Don't exclude Servicemeldungen from sysvars
- Use Servicemeldungen sysvar for hub state
- Add test for HM-CC-VG-1 (HM-Heatinggroup)
- Remove additional typecasts for number

# Version 0.20.0 (2022-01-12)
- Add converter to BaseParameterEntity/GenericEntity
- Fix number entities returning None when 0

# Version 0.19.0 (2022-01-11)
- Mark secondary channels name with a V --> Vch

# Version 0.18.1 (2022-01-10)
- Reduce some log_level
- Fix callback to notify un_reach

# Version 0.18.0 (2022-01-09)
- Add config option to specify storage directory
- Move Exceptions to own module
- Add binary_sensor platform for SVs
- Add config check
- Add hub_entities_by_platform
- Remove option_enable_sensors_for_system_variables

# Version 0.17.1 (2022-01-09)
- Fix naming for multi channel custom entities

# Version 0.17.0 (2022-01-09)
- Refactor entity definition
    - improve naming
    - classify entities (primary, secondary, sensor, Generic, Event)
- remove option_enable_virtual_channels from central
- remove entity.create_in_ha. Replaced by HmEntityUsage

# Version 0.16.2 (2022-01-08)
- Fix enum str in entity definition

# Version 0.16.1 (2022-01-08)
- Use helper for device_name
- Add logging to show usage of unique_id in name
- Add HmIPW-WRC6 to custom entities
- Add HmIP-SCTH230 to custom entities
- Refactor entity definition
    - Remove unnecessary field names from additional entity definitions
    - Add additional entity definitions by device type

# Version 0.16.0 (2022-01-08)
- Return unique_id if name is not in cache
- Remove no longer needed press_virtual_remote_key

# Version 0.15.2 (2022-01-07)
- Add devices to CustomEntity
    - HmIP-WGC
    - HmIP-WHS
- Update to pydevccu 0.1.0

# Version 0.15.1 (2022-01-07)
- Identify virtual remote by device type
- Fix Device Exporter / format output

# Version 0.15.0 (2022-01-07)
- Use actions instead of buttons for virtual remotes

# Version 0.14.1 (2022-01-06)
- Remove SVs from EXCLUDED_FROM_SENSOR

# Version 0.14.0 (2022-01-06)
- Switch some HM-LC-Bl1 to cover
- Use decorators on central methods
- Make decorators async aware
- Don't exclude DutyCycle, needed for old rf-modules
- Don't exclude Watchdog from SV sensor
- Ignore mypy error

# Version 0.13.3 (2022-01-05)
- HM cover fix: check level for None
- Only device_address is required for HA callback
- Fix: max_temp issue for hm thermostats
- Fix: hm const are str instead of int

# Version 0.13.2 (2022-01-04)
- Fix cover state
- Move delete_devices from RPCFunctions to central
- Move new_devices from RPCFunctions to central
- Add method to delete a single device to central

# Version 0.13.1 (2022-01-04)
- Use generic climate profiles list

# Version 0.13.0 (2022-01-04)
- Remove dedicated json tls option
- Fix unique_id for heating_groups
- Use domain name as base folder name
- Remove domain const from hahomematic

# Version 0.12.0 (2022-01-03)
- Split number to integer and float

# Version 0.11.2 (2022-01-02)
- Precise entity definitions

# Version 0.11.1 (2022-01-02)
- Improve detection of multi channel devices

# Version 0.11.0 (2022-01-02)
- Add positional arguments
- Add missing channel no
- Set ED_PHY_CHANNEL min_length to 1
- Add platform zu hub entities
- Use entities in properties
- Add transition to dimmer
- Rename entity.state to entity.value
- Remove channel no, if channel is the only_primary_channel

# Version 0.10.0 (2021-12-31)
- Make reset_motion, reset_presence a button
- add check to device_name / Fixes

# Version 0.9.1 (2021-12-30)
- Load and clear caches async
- Extend naming strategy to use device name if channel name is not customized

# Version 0.9.0 (2021-12-30)
- Add new helper for event_name
- Add channel to click_event payload

# Version 0.8.0 (2021-12-29)
- Use base class for file cache
- Rename primary_client to client
- Add export for device definition

# Version 0.7.0 (2021-12-28)
- Remove deleted entities from device and central collections
- use datetime for last_events
- Climate IP: use calendar for duration away

# Version 0.6.1 (2021-12-27)
- Display profiles only when hvac_mode auto is enabled
- Fix binary sensor state update for hmip 2-state sensors

# Version 0.6.0 (2021-12-27)
- Add climate methods for away mode
- Fix HVAC_MODE_OFF for climate

# Version 0.5.1 (2021-12-26)
- Fix hm_light turn_off

# Version 0.5.0 (2021-12-25)
- Fix Select Entity
- Remove internal device temperature (ACTUAL_TEMPERATURE CH0)
- Support Cool Mode for IPThermostats
- Display if AWAY_MODE is set on thermostat
- Separate device_address and channel_address

# Version 0.4.0 (2021-12-24)
- Use datetime for last_updated (time_initialized)
- Fix example
- Add ACTUAL_TEMPERATURE as separate entity by @towo
- Add HEATING_COOLING to IPThermostat and Group
- Add (*)HUMIDITY and (*)TEMPERATURE as separate entities for Bidcos thermostats
- use ACTIVE_PROFILE in climate presets

# Version 0.3.1 (2021-12-23)
- Make HmIP-BSM a switch (only dimable devices should be lights)

# Version 0.3.0 (2021-12-23)
- Cleanup API, device/entity
- Add ACTIVE_PROFILE to IPThermostat

# Version 0.2.0  (2021-12-22)
- Cleanup API, reduce visibility
- Add setValue to client

# Version 0.1.2  (2021-12-21)
- Rotate device identifier

# Version 0.1.1  (2021-12-21)
- Remove unnecessary async
- Removed unused helper
- Add interface_id to identifiers in device_info

# Version 0.1.0  (2021-12-20)
- Bump # Version to 0.1.0
- Remove interface_id from get_entity_name and get_custom_entity_name
- Add initial test
- Add coverage config

# Version 0.0.22 (2021-12-16)
- Resolve names without interface
- Fix device.entities for virtual remotes
- Remove unused const
- Cache model and primary_client

# Version 0.0.21 (2021-12-15)
- Fix number set_state
- Update ignore list
- Fix select entity

# Version 0.0.20 (2021-12-14)
- Move caches to classes

# Version 0.0.19 (2021-12-12)
- Add helper for address
- Fixes for Hub init

# Version 0.0.18 (2021-12-11)
- Add type hints based on HA coding guidelines
- Rename device_description to entity_definition
- Send alarm event on value change
- Rename impulse to special events
- reduce event_callbacks

# Version 0.0.17 (2021-12-05)
- Remove variables that are covered by other sensors (CCU only)
- Remove dummy from service message (HmIP-RF always sends 0001D3C98DD4B6:3 unreach)
- Rename Bidcos thermostats to SimpleRfThermostat and RfThermostat
- Use more Enums (like HA does): HmPlatform, HmEventType
- Use assignment expressions
- Add more type hints (fix most mypy errors)

# Version 0.0.16 (2021-12-02)
- Don't use default entities for climate groups (already included in device)

# Version 0.0.15 (2021-12-01)
- Fix: remove wildcard for HmIP-STHD
- Add unit to hub entities

# Version 0.0.14 (2021-11-30)
- Add KeyMatic
- Add HmIP-MOD-OC8
- Add HmIP-PCBS, HmIP-PCBS2, HmIP-PCBS-BAT, HmIP-USBSM
- Remove xmlrpc calls related to ccu system variables (not supported by api)
- Update hub sensor excludes

# Version 0.0.13 (2021-11-29)
- Add HmIP-MOD-HO, HmIP-MOD-TM
- Add sub_type to device/entity
- Add PRESET_NONE to climate
- Add level und state as additional entities for climate

# Version 0.0.12 (2021-11-27)
- Add more type converter
- Move get_tls_context to helper
- Update requirements
- Cleanup constants
- Use flags from parameter_data
- Add wildcard start to exclude parameters that start with word
- Fix channel assignment for dimmers
- Fix entity name: add channel only if a parameter name exists is in multiple channels of the device.

# Version 0.0.11 (2021-11-26)
- Fix: cover open/close default values to float
- Fix: add missing async/await
- make get_primary_client public

# Version 0.0.10 (2021-11-26)
- Fix TLS handling

# Version 0.0.9 (2021-11-25)
- Don't start connection checker for pydevccu
- Use a dummy hub for pydevccu
- Convert min, max, default values (fix for cover)

# Version 0.0.8 (2021-11-25)
- Add button platform. This allows to use the virtual remotes of a ccu in automations.
- Cleanup entity inheritance.

# Version 0.0.7 (2021-11-23)
- Switch to a non-permanent session for jsonrpc calls
  The json capabilities of a ccu are limited (3 parallel session!?!).
  So we no longer us a persisted session. (like pyhomematic)
- Enable write-only params as HMAction(solves a problem with climate writing CONTROL_MODE)

# Version 0.0.6 (2021-11-22)
- Rename server to central_unit (after the extraction of the XMLRPC-Server server has not been a server anymore).
- Rename json_rpc to json_rpc_client
- Move json_rpc from client to central_unit to remove number of active sessions
- Add hub with option to enable own system variables as sensors

# Version 0.0.5 (2021-11-20)
- Add method for virtual remote
- Update entity availability based on connection status
- Fix action_event for ha device trigger

# Version 0.0.4 (2021-11-18)
- Use one XMLRPC-Server for all backends

# Version 0.0.3 (2021-11-16)
- Reduce back to parameters with events
- Rewrite climate-entity creation
- Refactor to Async
- Remove entity_id and replace by unique_id
- Reorg Client/Server/Caches
- Use One Server per backend (CCU/Homegear) with multiple clients/interfaces
- Define device_description for custom_entities
- Create custom_entities for climate, cover, light, lock and switch
- Maintain ignored parameters
- Add collection with wildcard parameters to ignore
- Enable click, impulse and alarm events
- Add connection checker

# Version 0.0.2 (2021-04-20)
- Use input_select for ENUM actors (Issue #8)
- Added `DEVICE_IN_BOOTLOADER` and `INSTALL_TEST` to ignored parameters
- Create `switch` for type `ACTION` for parameters with only write-flag
- Create `number` for type `FLOAT` for parameters with only write-flag
- Add exceptions to abort startup under certain conditions
- Refactoring, introduce `Device` class
- Allow to fetch single paramset on demand
- Renew JSON-RPC sessions instead of logging in and out all the time

# Version 0.0.1 (2021-04-08)
- Initial testing release