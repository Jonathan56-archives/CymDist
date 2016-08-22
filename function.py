# -*- coding: utf-8 -*-
from __future__ import division
import cympy
import lookup


def list_devices(device_type=False, verbose=True):
    """List all devices and return a break down of their type

    Args:
        device_type (Device): if passed then list of device with the same type
        verbose (Boolean): if True print result (default True)

    Return:
        list <devices>
    """
    
    # Get the list of devices
    if device_type:
        devices = cympy.study.ListDevices(device_type)
    else:
        # Get all devices
        devices = cympy.study.ListDevices()

    # Get the break down of each type (would be easier with pandas)
    if verbose:
        # Get all the different types in the list of devices
        device_types = [value.DeviceType for value in devices]

        # Get a dictionnary with unique ID
        d = {key: value for (key, value) in zip(set(device_types), [0] * len(device_types))}

        # Get the rigth count for each category
        for value in device_types:
            d[value] += 1

        for key, value in d.iteritems():
            print('There are ' + str(value) + ' ' + lookup.type_table[key])

    return devices


def get_device(id, device_type, verbose=True):
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
        print(cympy.dm.Describe(device.GetObjType()))

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
    demand.DemandA.Value1 = values['value1_A']
    demand.DemandA.Value2 = values['value2_A']
    demand.DemandB = cympy.sim.LoadValue()
    demand.DemandB.Value1 = values['value1_B']
    demand.DemandB.Value2 = values['value2_B']
    demand.DemandC = cympy.sim.LoadValue()
    demand.DemandC.Value1 = values['value1_C']
    demand.DemandC.Value2 = values['value2_C']
    demand.LoadValueType = cympy.enums.LoadValueType.KVA_PF

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
