#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 18:05:11 2019

@author: colin
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def least_squares(data):
    '''Calculate the least squares (linear) regression for a data set
    the data should be a single list containing two sublists, the first sublist
    should be the x data and the second the y data'''

    x_sum = 0
    y_sum = 0
    x_sq_sum = 0
    xy_sum = 0

    # the list of data should have two equal length columns
    assert len(data[0]) == len(data[1])
    assert len(data) == 2

    n = len(data[0])
    # least squares regression calculation
    for i in range(0, n):
        x = data[0][i]
        y = data[1][i]
        if x == math.NaN or y == math.NaN:
            continue
        x_sum = x_sum + x
        y_sum = y_sum + y
        x_sq_sum = x_sq_sum + (x**2)
        xy_sum = xy_sum + (x*y)

    m = ((n * xy_sum) - (x_sum * y_sum))
    m = m / ((n * x_sq_sum) - (x_sum ** 2))
    c = (y_sum - m * x_sum) / n

    print("Results of linear regression:")
    print("x_sum=", x_sum, "y_sum=", y_sum, "x_sq_sum=", x_sq_sum, "xy_sum=",
          xy_sum)
    print("m=", m, "c=", c)

    return m, c


def measure_error(data1, data2):
    '''Measure the RMS error between data1 and data2'''
    assert len(data1) == len(data2)
    err_total = 0
    for i in range(0, len(data1)):
        err_total = err_total + (data1[i] - data2[i]) ** 2

    err = math.sqrt(err_total / len(data1))
    return err


def make_graph(x_data, y_data):

    # rotate the x labels to fit better
    plt.xticks(rotation=90)

    # calculate the minimum and maximum life expectancy
    # floor rounds down, ceil rounds up
    min_y = math.floor(min(y_data))
    max_y = math.ceil(max(y_data))

    # evenly space y axis, interval of 1, between the min and max life exp
    plt.yticks(np.linspace(min_y, max_y,
                           (max_y - min_y)+1))

    plt.xlim(min(x_data), max(x_data))
    plt.ylim(min_y, max_y)

    # draw the line
    plt.plot(x_data, y_data, label="Original Data")
    #plt.plot(x_data, y_model, label="Line of best fit")

    plt.grid()

    # enable the legend
    plt.legend()

    # draw the graph
    plt.show()


def read_data(gdp_file,life_expectancy_file, year):
    df_gdp = pd.read_csv(gdp_file, index_col="Country Name")

    gdp = df_gdp.loc[:, year]

    df_life_expt = pd.read_csv(life_expectancy_file, index_col="Life expectancy")

    # get the life expectancy for the specified country/dates
    # we have to convert the dates to strings as pandas treats them that way
    life_expectancy = df_life_expt.loc[:, year]

    data = []
    for country in life_expectancy.index:
        if country in gdp.index:
            data.append((country, life_expectancy[country], gdp[country]))
        else:
            print(country,"is not in the GDP country data")

    combined = pd.DataFrame.from_records(data,columns=("Country","Life Expectancy","GDP"))
    combined = combined.set_index("Country")
    return combined

data = process_gdp_data("../data/worldbank-gdp.csv", "../data/gapminder-life-expectancy.csv", "2016")

gdp_log = data["GDP"].apply(math.log).tolist()
life_exp = data["Life Expectancy"].tolist()

#least_squares([life_exp,gdp_log])
make_graph(life_exp,gdp_log)