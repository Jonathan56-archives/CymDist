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


def get_report(report_name, verbose=True):
    """
    """
    # Filename for the report
    report_filename = 'D:\\Users\\Jonathan\\Documents\\GitHub\\cymdist\\my_report.xml'

    # Saves the report
    cympy.rm.Save(report_name, cympy.study.ListNetworks(), cympy.enums.ReportModeType.XML, report_filename)
    
    if verbose:
        print('Report successfully saved!')
