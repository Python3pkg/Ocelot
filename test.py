# -*- coding: utf-8 -*-
import ocelot
from copy import copy
import numpy as np
import scipy as sp
import pandas as pd
import os
import time
import re
#data_format = ocelot.utils.read_format_definition()
#dirpath = r'C:\Ocelot\test_cases'
#datasets = ocelot.io.extract_excel.extract_excel(dirpath, data_format)
def adjust_mandatory_by_uncertainty_type(data_format):
    data_format_uncertainty = data_format[data_format['parent'] == 'uncertainty']
    uncertainty_types = data_format_uncertainty[data_format_uncertainty['in dataset'
        ] == 'type'].iloc[0]['allowed values']
    uncertainty_types = uncertainty_types.split(', ')
    data_format_uncertainty_by_type = {}
    for uncertainty_type in uncertainty_types:
        df = data_format_uncertainty.copy()
        for index in data_format_uncertainty.index:
            if uncertainty_type in str(data_format_uncertainty.loc[index, 'description']):
                df.loc[index, 'mandatory/optional'] = 'mandatory'
        data_format_uncertainty_by_type[uncertainty_type] = df.copy()
    return data_format_uncertainty_by_type
def separate_data_format(data_format):
    data_formats = {}
    for parent in ['exchanges', 'dataset', 'production volume', 'properties', 'parameters']:
        data_formats[parent] = data_format[data_format['parent'] == parent]
    data_formats['uncertainty'] = adjust_mandatory_by_uncertainty_type(data_format)
    return data_formats
def validate_exchanges(dataset, compartments, data_formats, local_report):
    for exc in dataset['exchanges']:
        for i in range(len(data_formats['exchanges'])):
            sel = data_formats['exchanges'].iloc[i]
            local_report = validate(exc, sel, local_report, 'exchanges')
        local_report = validate_elementary_exchange(exc, compartments, local_report)
        local_report = validate_uncertainty(exc, data_formats, local_report)
        local_report = validate_PV(exc, data_formats, local_report)
        local_report = validate_properties(exc, data_formats, local_report)
    return local_report
def validate_elementary_exchange(exc, compartments, local_report):
    if 'elementary' in exc['tag']:
        index = []
        for field in ['compartment', 'subcompartment']:
            if field not in exc:
                1/0 #missing field
            else:
                index.append(exc[field])
        if len(index) == 2:
            if tuple(index) not in compartments.index:
                1/0 #wrong compartment/subcompartment combination
    return local_report
def validate_uncertainty(element, data_formats, local_report):
    if 'uncertainty' in element:
        u = element['uncertainty']
        for i in range(len(data_formats['uncertainty'][u['type']])):
            sel = data_formats['uncertainty'][u['type']].iloc[i]
            local_report = validate(u, sel, local_report, 'uncertainty')
    return local_report
def validate_PV(exc, data_formats, local_report):
    if exc['type'] in ['reference product', 'byproduct']:
        if 'production volume' not in exc:
            1/0 #missing field
        else:
            PV = exc['production volume']
            for i in range(len(data_formats['production volume'])):
                sel = data_formats['production volume'].iloc[i]
                local_report = validate(PV, sel, local_report, 'production volume')
            local_report = validate_uncertainty(PV, data_formats, local_report)
    return local_report
def validate_parameters(dataset, data_formats, local_report):
    if 'parameters' in dataset:
        for p in dataset['parameters']:
            for i in range(len(data_formats['parameters'])):
                sel = data_formats['parameters'].iloc[i]
                local_report = validate(p, sel, local_report, 'parameters')
            local_report = validate_uncertainty(p, data_formats, local_report)
    return local_report
def validate_properties(exc, data_formats, local_report):
    if 'properties' in exc:
        for p in exc['properties']:
            for i in range(len(data_formats['properties'])):
                sel = data_formats['properties'].iloc[i]
                local_report = validate(p, sel, local_report, 'properties')
            local_report = validate_uncertainty(p, data_formats, local_report)
    return local_report
def find_selected_type(s):
    if s == 'str':
        expected_type = str
    elif s == 'dict':
        expected_type = dict
    elif s == 'list':
        expected_type = list
    elif s == 'float':
        expected_type = float
    elif s == 'int':
        expected_type = int
    else:
        1/0
    return expected_type
def validate(element, sel, local_report, element_type):
    field = sel['in dataset']
    if field not in element:
        if sel['mandatory/optional'] == 'mandatory':
            1/0 #missing field
    elif type(element[field]) != find_selected_type(sel['type']):
        1/0 #wrong type
    elif not ocelot.utils.is_empty(sel['allowed values']):
        allowed = sel['allowed values'].split(', ')
        if str(element[field]) not in allowed:
            1/0 #illegal value
    return local_report
def validate_meta(dataset, data_formats, local_report):
    for i in range(len(data_formats['dataset'])):
        sel = data_formats['dataset'].iloc[i]
        local_report = validate(dataset, sel, local_report, 'dataset')
        field = sel['in dataset']
        if 'date' in field:
            date_pattern = '\d{4}-\d{2}-\d{2}'
            g = re.search(date_pattern, dataset[field])
            if g == None:
                1/0 #date in wrong format
    return local_report
if 0:
    folder = r'C:\python\DB_versions\3.2\undefined\datasets'
    datasets = ocelot.io.extract_ecospold2.extract_directory(folder, False)
    filename = 'ecoinvent_3.2_internal'
    folder = r'C:\ocelot_DB'
    logger = ''
    datasets = ocelot.transformations.find_allocation_method_cutoff.allocation_method(datasets, logger)
    datasets = ocelot.transformations.fix_known_issues_ecoinvent_32.fix_known_issues(
        datasets, '')
    support_excel_folder = r'C:\ocelot_DB'
    support_pkl_folder = r'C:\ocelot_DB'
    data_format = ocelot.utils.read_format_definition()
    if 0:
        ocelot.transformations.activity_overview.build_activity_overview(datasets, 
            support_excel_folder, support_pkl_folder, data_format)
    ocelot.utils.save_file(datasets, folder, filename)
else:
    folder = r'C:\ocelot_DB'
    filename = 'ecoinvent_3.2_internal'
    #filename = 'after_combined_production_without_byproducts'
    #filename = 'ecoinvent_3.2_internal_after_allocation'
    #filename = 'after_allocation_treatment_and_recycling'
    #filename = 'after_combined_production_with_byproducts'
    #filename = 'after_economic_allocation'
    #filename = 'after_true_value_allocation'
    datasets = ocelot.utils.open_file(folder, filename)
    data_formats, compartments = ocelot.io.validate_dataset.prepare_validation()
    for dataset in datasets:
        ocelot.io.validate_dataset.validate_dataset(dataset, data_formats, compartments)
        
    1/0
    data_format = ocelot.utils.read_format_definition()
    support_excel_folder = r'C:\ocelot_DB'
    support_pkl_folder = r'C:\ocelot_DB'
    criteria = {
        #'allocation method': [
            #'recycling activity', 
              #'waste treatment', 
              #'economic allocation', 
                #'true value allocation'
                #'combined production without byproducts'
                #'combined production with byproducts'
              #], 
    'id': '40acc8ff-a89a-421f-8af3-c5b615c38bff'
        #'activity name': ['treatment of residue from mechanical treatment, laser printer, municipal incineration with fly ash extraction'], 
        #'location': ['CH'], 
                }
    activity_overview = ocelot.utils.open_file(folder, 'activity_overview')
    #datasets = ocelot.utils.filter_datasets(datasets, activity_overview, criteria)
    if 0:
        datasets = ocelot.transformations.calculate_available_PV.available_production_volume(
            datasets, '', support_excel_folder, support_pkl_folder)
        1/0
        datasets = ocelot.transformations.allocate_cutoff.allocate_datasets_cutoff(
            datasets, data_format, '')
        folder = 'C:\ocelot_DB'
        filename = 'ecoinvent_3.2_internal_after_allocation'
        ocelot.utils.save_file(datasets, folder, filename)
    if 0:
        system_model_folder = r'C:\python\DB_versions\3.2\cut-off'
        ocelot.utils.validate_against_linking(datasets, system_model_folder, data_format, 
            folder, types_to_validate = ['from environment', 'to environment'])
    #datasets = ocelot.transformations.calculate_available_PV.calculate_available_PV(
    #        datasets, '', support_excel_folder, support_pkl_folder)
    ocelot.transformations.calculate_RoW_PV.calculate_RoW_PV(support_pkl_folder, support_excel_folder)