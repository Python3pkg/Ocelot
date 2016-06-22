# -*- coding: utf-8 -*-
from copy import copy

def f():
    return ''
def allocation_method(datasets, logger):
    """Finds the allocation method, based on a few characteristics of outputs to technosphere"""
    for dataset in datasets:
        #initializing some variables
        nb_reference_products = 0
        nb_allocatable_byproducts = 0
        has_conditional_exchange = False
        has_true_value = False
        
        #gathering the necessary information to find the allocation method
        for exc in dataset['exchanges']:
            if exc['amount'] != 0.:
                if exc['type'] == 'reference product':
                    nb_reference_products += 1
                    if exc['amount'] < 0.:
                        reference_product_amount_sign = -1
                    else:
                        reference_product_amount_sign = 1
                    reference_product_classification = exc['byproduct classification']
                elif exc['type'] == 'byproduct':
                    nb_allocatable_byproducts += 1
                    if 'activity link' in exc and dataset['type'] == 'market activity' and exc['amount'] < 0.:
                        has_conditional_exchange = True
                if 'properties' in exc and 'true value relation' in exc['properties']:
                    has_true_value = True
        
        #settin the allocation method
        if dataset['type'] == 'market group':
            dataset['allocation method'] = 'no allocation'
        elif dataset['type'] == 'market activity':
            if has_conditional_exchange:
                dataset['allocation method'] = 'constrained market'
            else:
                dataset['allocation method'] = 'no allocation'
        else:
            if nb_reference_products + nb_allocatable_byproducts == 1:
                dataset['allocation method'] = 'no allocation'
            elif nb_reference_products > 1:
                if nb_allocatable_byproducts > 0:
                    dataset['allocation method'] = 'combined production with byproducts'
                else:
                    dataset['allocation method'] = 'combined production without byproducts'
            elif reference_product_amount_sign == 1:
                if has_true_value:
                    dataset['allocation method'] = 'true value allocation'
                else:
                    dataset['allocation method'] = 'economic allocation'
            else:
                if reference_product_classification == 'waste':
                    dataset['allocation method'] = 'waste treatment'
                else:
                    dataset['allocation method'] = 'recycling activity'
        
        #removing superfluous information from the dataset
        if not 'combined' in dataset['allocation method']:
            if 'parameters' in dataset:
                del dataset['parameters'] #parameters are only useful in the case of combined production
            for exc in dataset['exchanges']:
                #mathematical relation and variable names not necessary
                for field in ['mathematical relation', 'variable']:
                    if field in exc:
                        del exc[field]
                if 'properties' in exc:
                    properties_to_keep = []
                    if dataset['allocation method'] in ['recycling activity', 'economic allocation']:
                        properties_to_keep = ['price']
                    elif dataset['allocation method'] in ['true value allocation']:
                        properties_to_keep = ['price', 'true value relation']
                    #deleting unnecessary properties, mathematical relation and variable
                    properties = copy(exc['properties'])
                    exc['properties'] = {}
                    for property_name in properties:
                        if property_name in properties_to_keep:
                            exc['properties'][property_name] = copy(properties[property_name])
    return datasets