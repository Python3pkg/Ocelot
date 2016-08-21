# -*- coding: utf-8 -*-
from ocelot.errors import InvalidExchange, InvalidMultioutputDataset
from ocelot.transformations.cutoff.validation import (
    ready_for_market_linking,
    valid_combined_production_activity,
    valid_economic_activity,
    valid_recycling_activity,
)
import pytest


def test_recycling_activity_validation_errors():
    @valid_recycling_activity
    def f(dataset):
        return dataset

    no_byproduct = {'exchanges': [
        {
            'type': 'reference product',
            'amount': 1
        }
    ]}
    with pytest.raises(InvalidExchange):
        f(no_byproduct)

    negative_value = {'exchanges': [
        {
            'type': 'reference product',
            'amount': -1
        }
    ]}
    with pytest.raises(InvalidExchange):
        f(negative_value)

    wrong_classification = {'exchanges': [
        {
            'type': 'reference product',
            'amount': 1
        },
        {
            'type': 'byproduct',
            'byproduct classification': 'waste'
        }
    ]}
    with pytest.raises(InvalidExchange):
        f(wrong_classification)

def test_recycling_activity_validation():
    @valid_recycling_activity
    def f(dataset):
        return dataset

    correct = {'exchanges': [
        {
            'type': 'reference product',
            'amount': 1
        },
        {
            'type': 'byproduct',
            'byproduct classification': 'allocatable product'
        }
    ]}
    assert f(correct) is correct
    assert f(dataset=correct) is correct

def test_economic_activity_validation_errors():
    @valid_economic_activity
    def f(dataset):
        return dataset

    missing_price = {'exchanges': [
        {
            'type': 'reference product',
            'properties': [{
                'name': 'wrong',
            }]
        },
    ]}
    with pytest.raises(InvalidExchange):
        f(missing_price)

    no_price_amount = {'exchanges': [
        {
            'type': 'reference product',
            'properties': [{
                'name': 'price',
            }]
        },
    ]}
    with pytest.raises(InvalidExchange):
        f(no_price_amount)

def test_economic_activity_validation():
    @valid_economic_activity
    def f(dataset):
        return dataset

    data = {'exchanges': [
        {
            'type': 'reference product',
            'properties': [{
                'name': 'price',
                'amount': 1
            }]
        },
    ]}
    assert f(data) is data
    assert f(dataset=data) is data

def test_combined_production_validation_errors():
    @valid_combined_production_activity
    def f(dataset):
        return dataset

    no_variable = {'exchanges': [
        {
            'type': 'reference product',
            'amount': 1
        }
    ]}
    with pytest.raises(InvalidExchange):
        f(no_variable)

    yes_variable = {'exchanges': [
        {
            'type': 'reference product',
            'variable': 'yes minister!',
            'amount': 1
        }
    ]}
    assert f(yes_variable)

def test_ready_for_market_linking():
    valid = [{
        'type': 'transforming activity',
        'reference product': True,
        'exchanges': [{'type': 'reference product'}]
    }]
    assert ready_for_market_linking(valid)

def test_ready_for_market_linking_no_rp_attribute():
    invalid = [{
        'type': 'transforming activity',
        'exchanges': [{'type': 'reference product'}]
    }]
    with pytest.raises(ValueError):
        ready_for_market_linking(invalid)

def test_ready_for_market_linking_no_exchanges():
    invalid = [{
        'type': 'transforming activity',
        'reference product': True,
        'exchanges': [{'type': 'nope'}]
    }]
    with pytest.raises(ValueError):
        ready_for_market_linking(invalid)

def test_ready_for_market_linking_multiple_rp():
    invalid = [{
        'name': 'one',
        'type': 'transforming activity',
        'reference product': True,
        'exchanges': [
            {'type': 'reference product'},
            {'type': 'reference product'},
        ]
    }]
    with pytest.raises(InvalidMultioutputDataset):
        ready_for_market_linking(invalid)