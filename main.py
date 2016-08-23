# -*- coding: utf-8 -*-
from __future__ import division
import cympy

import sys
sys.path.append("D:\\Users\\Jonathan\\Documents\\GitHub\\cymdist")
import function

# Open a study
filename = 'C:\\Users\\emma\\Documents\\SCE Cymdist\\PIANO_20140718.sxst'
cympy.study.Open(filename)

# Get a list of all the devices
devices = function.list_devices()

# Get device [index] from the list
device = function.get_device(devices[0].DeviceNumber, devices[0].DeviceType)

# Set values for load allocations
values = {'value1_A': 3000,
          'value2_A': 97.0,
          'value1_B': 3300,
          'value2_B': 98.0,
          'value1_C': 3200,
          'value2_C': 95.0}
function.load_allocation(values)

# Visualize the results
report_name = 'Load Allocation - Spot Load Differences'
function.get_report(report_name)