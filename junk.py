def get_high_voltage(devices, first_n_devices=10):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        high_voltage_device (DataFrame): return the n devices with the highest voltage
    """
    # Get all the voltage
    voltage = get_voltage(devices)

    # Sort out the voltage
    voltage['maximum_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].max(axis=1)
    voltage = voltage.sort_values('maximum_voltage_ABC', ascending=False)
    voltage = voltage.drop(['maximum_voltage_ABC'], axis=1)

    return voltage[0:first_n_devices]


def get_low_voltage(devices, first_n_devices=10):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        low_voltage_device (DataFrame): return the n devices with the lowest voltage 
    """
    # Get all the voltage
    voltage = get_voltage(devices)

    # Sort out the voltage
    voltage['minimum_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].min(axis=1)
    voltage = voltage.sort_values('minimum_voltage_ABC', ascending=True)
    voltage = voltage.drop(['minimum_voltage_ABC'], axis=1)

    return voltage[0:first_n_devices]


# Sort out the overload
overload['maximum_overload_ABC'] = overload[['overload_A', 'overload_B', 'overload_C']].max(axis=1)
overload = overload.sort_values('maximum_overload_ABC', ascending=False)
overload = overload.drop(['maximum_overload_ABC'], axis=1)