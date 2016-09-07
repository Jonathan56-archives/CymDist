# -*- coding: utf-8 -*-
from __future__ import division
import cympy
import cympy.rm
import pandas
import lookup


def list_devices(device_type=False, verbose=True):
    """List all devices and return a break down of their type

    Args:
        device_type (Device): if passed then list of device with the same type
        verbose (Boolean): if True print result (default True)

    Return:
        DataFrame <device, device_type, device_number, device_type_id>
    """

    # Get the list of devices
    if device_type:
        devices = cympy.study.ListDevices(device_type)
    else:
        # Get all devices
        devices = cympy.study.ListDevices()

    # Create a dataframe
    devices = pandas.DataFrame(devices, columns=['device'])
    devices['device_type_id'] = devices['device'].apply(lambda x: x.DeviceType)
    devices['device_number'] = devices['device'].apply(lambda x: x.DeviceNumber)
    devices['device_type'] = devices['device_type_id'].apply(lambda x: lookup.type_table[x])

    # Get the break down of each type
    if verbose:
        unique_type = devices['device_type'].unique().tolist()
        for device_type in unique_type:
            print('There are ' + str(devices[devices.device_type == device_type].count()[0]) +
                  ' ' + device_type)

    return devices


def _describe_object(device):
        for value in cympy.dm.Describe(device.GetObjType()):
            print(value.Name)


def get_device(id, device_type, verbose=False):
    """Return a device

    Args:
        id (String): unique identifier
        device_type (DeviceType): type of device
        verbose (Boolean): describe an object

    Return:
        Device (Device)
    """
    # Get object
    device = cympy.study.GetDevice(id, device_type)

    # Describe attributes
    if verbose:
        _describe_object(device)

    return device


def load_allocation(values):
    """Run a load allocation

    Args:
        values (dictionnary): value1 (KVA) and value2 (PF) for A, B and C
    """

    # Create Load Allocation object
    la = cympy.sim.LoadAllocation()

    # Create the Demand object
    demand = cympy.sim.Meter()

    # Fill in the demand values
    demand.IsTotalDemand = False
    demand.DemandA = cympy.sim.LoadValue()
    demand.DemandA.Value1 = values['P_A']
    demand.DemandA.Value2 = values['Q_A']
    demand.DemandB = cympy.sim.LoadValue()
    demand.DemandB.Value1 = values['P_B']
    demand.DemandB.Value2 = values['Q_B']
    demand.DemandC = cympy.sim.LoadValue()
    demand.DemandC.Value1 = values['P_C']
    demand.DemandC.Value2 = values['Q_C']
    demand.LoadValueType = cympy.enums.LoadValueType.KW_KVAR

    # Get a list of networks
    networks = cympy.study.ListNetworks()

    # Set the first feeders demand
    la.SetDemand(networks[0], demand)

    # Run the load allocation
    la.Run([networks[0]])


def get_voltage(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding voltage for
            each phase
    """
    # Create a new frame to hold the results 
    voltage = devices.copy()

    # Reset or create new columns to hold the result
    voltage['voltage_A'] = [0] * len(voltage)
    voltage['voltage_B'] = [0] * len(voltage)
    voltage['voltage_C'] = [0] * len(voltage)

    for device in devices.itertuples():
        # Get the according voltage per phase in a pandas dataframe
        voltage.loc[device.Index, 'voltage_A'] = cympy.study.QueryInfoDevice(
            "VpuA", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_B'] = cympy.study.QueryInfoDevice(
            "VpuB", device.device_number, int(device.device_type_id))
        voltage.loc[device.Index, 'voltage_C'] = cympy.study.QueryInfoDevice(
            "VpuC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['voltage_A', 'voltage_B', 'voltage_C']:
        voltage[column] = voltage[column].apply(lambda x: None if x is '' else float(x))

    return voltage


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


def get_overload(devices, first_n_devices=10):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load 
    """
    # Create a new frame to hold the results 
    overload = devices.copy()

    # Reset or create new columns to hold the result
    overload['overload_A'] = [0] * len(overload)
    overload['overload_B'] = [0] * len(overload)
    overload['overload_C'] = [0] * len(overload)

    for device in devices.itertuples():
        # Get the according overload per phase in a pandas dataframe
        overload.loc[device.Index, 'overload_A'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsA", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_B'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsB", device.device_number, int(device.device_type_id))
        overload.loc[device.Index, 'overload_C'] = cympy.study.QueryInfoDevice(
            "OverloadAmpsC", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['overload_A', 'overload_B', 'overload_C']:
        overload[column] = overload[column].apply(lambda x: None if x is '' else float(x))

    # Sort out the overload
    overload['maximum_overload_ABC'] = overload[['overload_A', 'overload_B', 'overload_C']].max(axis=1)
    overload = overload.sort_values('maximum_overload_ABC', ascending=False)
    overload = overload.drop(['maximum_overload_ABC'], axis=1)

    return overload[0:first_n_devices]


def get_load(devices):
    """
    Args:
        devices (DataFrame): list of all the devices to include

    Return:
        devices_voltage (DataFrame): devices and their corresponding load for
            each phase
    """
    # Create a new frame to hold the results 
    load = devices.copy()

    # Reset or create new columns to hold the result
    load['MWA'] = [0] * len(load)
    load['MWB'] = [0] * len(load)
    load['MWC'] = [0] * len(load)
    load['MWTOT'] = [0] * len(load)
    load['MVARA'] = [0] * len(load)
    load['MVARB'] = [0] * len(load)
    load['MVARC'] = [0] * len(load)
    load['MVARTOT'] = [0] * len(load)

    for device in devices.itertuples():
        # Get the according load per phase in a pandas dataframe
        load.loc[device.Index, 'MWA'] = cympy.study.QueryInfoDevice(
            "MWA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWB'] = cympy.study.QueryInfoDevice(
            "MWB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWC'] = cympy.study.QueryInfoDevice(
            "MWC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MWTOT'] = cympy.study.QueryInfoDevice(
            "MWTOT", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARA'] = cympy.study.QueryInfoDevice(
            "MVARA", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARB'] = cympy.study.QueryInfoDevice(
            "MVARB", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARC'] = cympy.study.QueryInfoDevice(
            "MVARC", device.device_number, int(device.device_type_id))
        load.loc[device.Index, 'MVARTOT'] = cympy.study.QueryInfoDevice(
            "MVARTOT", device.device_number, int(device.device_type_id))

    # Cast the right type
    for column in ['MWA', 'MWB', 'MWC', 'MWTOT', 'MVARA', 'MVARB', 'MVARC', 'MVARTOT']:
        load[column] = load[column].apply(lambda x: None if x is '' else float(x))

    return load


def get_unbalanced_line(devices, first_n_devices=10):
    """
    Args:
        devices (DataFrame): list of all the devices to include
        first_n_devices (Int): number of row to return

    Return:
        overload_device (DataFrame): return the n devices with the highest load 
    """
    # Get all the voltage
    voltage = get_voltage(devices)
    
    # Get the mean voltage accross phase
    voltage['mean_voltage_ABC'] = voltage[['voltage_A', 'voltage_B', 'voltage_C']].mean(axis=1)
    
    # Get the max difference of the three phase voltage with the mean
    def _diff(value):
        diff = []
        for phase in ['voltage_A', 'voltage_B', 'voltage_C']:
            diff.append(abs(value[phase] - value['mean_voltage_ABC']) * 100 / value['mean_voltage_ABC'])
        return max(diff)
    voltage['diff_with_mean'] = voltage[['mean_voltage_ABC', 'voltage_A', 'voltage_B', 'voltage_C']].apply(_diff, axis=1)
    voltage = voltage.sort_values('diff_with_mean', ascending=False)

    return voltage[voltage.diff_with_mean >= 2][0:first_n_devices]


def get_report(report_name, verbose=True):
    """
    """
    # Filename for the report
    report_filename = 'D:\\Users\\Jonathan\\Documents\\GitHub\\cymdist\\my_report.xml'

    # Saves the report
    cympy.rm.Save(report_name, cympy.study.ListNetworks(), cympy.enums.ReportModeType.XML, report_filename)

    if verbose:
        print('Report successfully saved!')
