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


def get_settings(files):
    label = []
    for file in files:
        gap = file.split('gap')[1].split('graph')[0]
        graph = file.split('graph')[1].split('.csv')[0]
        label.append(gap + '\n' + graph)
    return label


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
    endings = ['Local/One_Extra_Bit/', 'Local/Two_Extra_Bits/', 'Local/No_Extra_Bit/',
               'DW2000/One_Extra_Bit/', 'DW2000/Two_Extra_Bits/', 'DW2000/No_Extra_Bit/',
               'Advantage_System/One_Extra_Bit/', 'Advantage_System/Two_Extra_Bits/', 'Advantage_System/No_Extra_Bit/']
    xLabel = ['.01\n6', '.01\n7', '.01\n8', '.01\n9', '.1\n6', '.1\n7',
              '.1\n8', '.1\n9', '1\n6', '1\n7', '1\n8', '1\n9', '2\n6',
              '2\n7', '2\n8', '2\n9']
    dir = "/Users/peterelgar/PycharmProjects/QuantumProject1/D-Wave/results/"
    for ending in endings:
        folder = dir + ending
        files = list_files(folder)

        files.sort()
        labels = get_settings(files)
        # print(files)
        print(labels)
        # true_results, false_results = list_true_false_results(folder, files)
        # plt.bar(xLabel[:len(true_results)], true_results)
        # plt.title(ending.replace('/', ' '))
        # plt.ylabel('number of correct results')
        # plt.xlabel('settings gap size and graph size')
        # plt.show()
        # plt.savefig(ending.replace('/', '_', 1).replace('/', ''), bbox_inches='tight', pad_inches=0.2)
        # plt.clf()
