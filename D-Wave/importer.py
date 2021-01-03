# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:05:19 2021

@author: Fabian
"""
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

# import numpy

def list_files(dir):
    files = []
    for file in os.listdir(dir):
        if file.endswith(".csv"):
            files.append(file)
    return files


def list_true_false_results(dir, files):
    trueresults = []
    falsefrequencies = []
    truefrequencies = []
    for j in range(len(files)):
        file0 = []
        i = 0
        with open(dir + files[j], newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if i > 2:
                    file0.append(row)
                i = i + 1

        truefrequency = 0
        for i in range(len(file0)):
            if file0[i][2] == 'True':
                trueresults.append([file0[i][0], file0[i][1], file0[i][3]])
                truefrequency = truefrequency + int(file0[i][3])
        falsefrequencies.append(2000 - truefrequency)
        truefrequencies.append(truefrequency)
    return truefrequencies, falsefrequencies


if __name__ == '__main__':
    endings = ['Local/Extra_Bit/', 'Local/No_Extra_Bit/', 'DW2000/Extra_Bit/', 'DW2000/No_Extra_Bit/',
               'Advantage_System/Extra_Bit/', 'Advantage_System/No_Extra_Bit/']
    xLabel = ['0.01-6', '0.01-7', '0.01-8', '0.01-9', '0.1-6', '0.1-7',
              '0.1-8', '0.1-9', '1-6', '1-7', '1-8', '1-9', '2-6',
              '2-7', '2-8', '2-9']
    dir = "/Users/peterelgar/PycharmProjects/QuantumProject1/D-Wave/results/"
    for ending in endings:
        folder = dir + ending
        files = list_files(folder)
        true_results, false_results = list_true_false_results(folder, files)
        plt.bar(xLabel[:len(true_results)], true_results)
        plt.title(ending)
        plt.ylabel('number of correct results')
        plt.xlabel('settings gap size-graph size')
        plt.show()
