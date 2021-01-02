# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 18:05:19 2021

@author: Fabian
"""
import os
import csv
#import numpy


files=[]
for file in os.listdir("Results"):
    if file.endswith(".csv"):
        files.append(file)

trueresults = []
falsefrequencies = []
for j in range(len(files)):
    file0 = []
    i = 0
    with open('Results/'+files[j], newline='') as csvfile:
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
    falsefrequencies.append([len(file0) - truefrequency])