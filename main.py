# -*- coding: utf-8 -*-
from __future__ import division
import cympy

# Open a study
filename = 'C:\\Users\\emma\\Documents\\SCE Cymdist\\PIANO_20140718.sxst'
cympy.study.Open(filename)

# # List all the ?
# sw_1532 = cympy.study.ListDevices(cympy.enums.DeviceType.Transformer)

# # Gets the transformer '10925'
# xfo = cympy.study.GetDevice("10925", cympy.enums.DeviceType.Transformer)

# # Get object attributes
# cympy.dm.Describe(device.GetObjType())

# Find out how to launch a load thing
# Create Load Allocation object
la = cympy.sim.LoadAllocation()

# Create the Demand object
demand = cympy.sim.Meter()

# Fill in the demand values
demand.IsTotalDemand = False
demand.DemandA = cympy.sim.LoadValue()
demand.DemandA.Value1 = 3000
demand.DemandA.Value2 = 77.7
demand.DemandB = cympy.sim.LoadValue()
demand.DemandB.Value1 = 3300
demand.DemandB.Value2 = 88.8
demand.DemandC = cympy.sim.LoadValue()
demand.DemandC.Value1 = 3500
demand.DemandC.Value2 = 99.9

demand.LoadValueType = cympy.enums.LoadValueType.KVA_PF

networks = cympy.study.ListNetworks()

# Set the first feeders demand
la.SetDemand(networks[0], demand)

# Run the load allocation
la.Run([networks[0]])

# Visualize the results