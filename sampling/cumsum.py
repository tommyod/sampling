#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 14:40:33 2020

@author: tommy
"""

import numpy as np


class CumulativeSum:
    def __init__(self, weights):
        self.weights = np.array(weights)
        if np.any(self.weights < 0):
            raise ValueError("all weights must be greater than or equal to zero.")
        self.cumulative_weights = np.cumsum(self.weights)

    def get_sum(self):
        return self.cumulative_weights[-1]

    def query(self, search_weight):
        if not 0 <= search_weight <= self.get_sum():
            raise ValueError(f"queried weight must be between 0 and {self.get_sum()}")

        index = np.searchsorted(self.cumulative_weights, search_weight, side="left", sorter=None)
        return index

    def update_weight(self, index, weight):
        self.weights[index] = weight
        self.cumulative_weights = np.cumsum(self.weights)

    def __getitem__(self, index):
        return self.weights[index]

    def remove(self, index):
        self.weights = np.delete(self.weights, index)
        self.cumulative_weights = np.cumsum(self.weights)

    def extend(self, weights):
        self.weights = np.append(self.weights, weights)
        self.cumulative_weights = np.cumsum(self.weights)
