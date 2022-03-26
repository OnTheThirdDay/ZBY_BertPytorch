# author - Richard Liao
# Dec 26 2016
import numpy as np
import pandas as pd
from decimal import getcontext, Decimal

from collections import defaultdict
import re

from bs4 import BeautifulSoup

import sys
import os

#os.environ['KERAS_BACKEND'] = 'theano'


import h5py
import csv


MAX_SEQUENCE_LENGTH = 500
MAX_NB_WORDS = 20000
EMBEDDING_DIM = 100
VALIDATION_SPLIT = 0.0




# analysis
labelpredict = []
labelreal = []

predictnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #11
predictandrealnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ]  # 11
realnum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ] #11
data_result = pd.read_csv('./save/predict_result.tsv', encoding='ISO-8859-1', sep='\t', delimiter="\t")



for idx in range(data_result.labelpredict.shape[0]):
    labelpredict.append(data_result.labelpredict[idx])
    labelreal.append(data_result.labelreal[idx])

# print()
# print(len(labelpredict))
# print(len(labelreal))
# part labels
#labelnum  :  label's name
#num  :  sentence's number
#labelpredict labelreal  :  result read
#predictnum predictandrealnum realnum :  labels' quantity
allpredictandrealnum = Decimal(0)
allpredictnum = Decimal(0)
allrealnum = Decimal(0)
allprecision = Decimal(0)
allrecall = Decimal(0)
F_all = Decimal(0)
for labelnum in range(0,11):
    # print(type(labelnum))
    # print(type(labelpredict[0]))

    for num in range(0 , len(labelpredict)):
        if str(labelpredict[num]) == str(labelnum):
            predictnum[labelnum] = predictnum[labelnum] + 1
            if str(labelreal[num]) == str(labelnum): # two label equal simultaneously
                predictandrealnum[labelnum] = predictandrealnum[labelnum] + 1
    for num in range(0 , len(labelpredict)):
        if str(labelreal[num]) == str(labelnum):
            realnum[labelnum] = realnum[labelnum] + 1

    # if predictandrealnum[labelnum] == 0:
    #     F = 0
    # elif realnum[labelnum] == 0:
    #     F = 0
    # elif predictnum[labelnum] == 0:
    #     F = 0
    # else:
    #     F = 2*predictandrealnum[labelnum]*predictandrealnum[labelnum]/(predictnum[labelnum] * realnum[labelnum])/(predictandrealnum[labelnum]/predictnum[labelnum] + predictandrealnum[labelnum]/realnum[labelnum] )
        # F = 0

    # if labelnum != 0:
    allpredictandrealnum += predictandrealnum[labelnum]
    allpredictnum += predictnum[labelnum]
    allrealnum += realnum[labelnum]


    if predictandrealnum[labelnum] != 0:
        # print("label " + str(labelnum) + " Precision: " +  str(predictandrealnum[labelnum]+0.0) + "/" + str(predictnum[labelnum]+0.0))
        # print("label " + str(labelnum) + " Recall: " +  str(predictandrealnum[labelnum]+0.0) + "/" + str(realnum[labelnum]+0.0))

        precision = (Decimal(predictandrealnum[labelnum]))/(Decimal(predictnum[labelnum]))
        recall = (Decimal(predictandrealnum[labelnum]))/(Decimal(realnum[labelnum]))
        F = Decimal(Decimal(2) * (precision * recall) / (precision + recall))
    else:
        # print("label " + str(labelnum) + " Precision: " + str(0.0))
        # print("label " + str(labelnum) + " Recall: " + str(0.0))
        precision = 0
        recall = 0
        F = 0
    print("label " + str(labelnum) + ": ")
    print(str(Decimal(precision * 100).quantize(Decimal('0.00'))) + " & " + str(Decimal(recall * 100).quantize(Decimal('0.00'))) + " & " + str(Decimal(F*100).quantize(Decimal('0.00'))))
    # print("label " + str(labelnum) + " F1: " + str(F))
    print("--------------------------------------------------------------")
    if labelnum == 0:
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("--------------------------------------------------------------")

    allprecision += precision
    allrecall += recall
    F_all += F
    # if predictnum[labelnum] == 0 :  #there will be a error if 0/0
    #     print("label " + str(labelnum) + " precision:  0.0 (0/0)")
    # else:
    #     print("label " + str(labelnum) + " precision:  " +  str((predictandrealnum[labelnum]+0.0)/(predictnum[labelnum]+0.0)))


# print(predictnum)
# print(predictandrealnum)
# print(realnum)
p = Decimal((allpredictandrealnum)/(allpredictnum))
r = Decimal((allpredictandrealnum)/(allrealnum))
micro_f = (Decimal(Decimal(2) * (p * r) / (p + r))*Decimal(100)).quantize(Decimal('0.00'))
# macro_f = (2*(allprecision/Decimal(11)*allrecall/Decimal(11))/(allprecision/Decimal(11) + allrecall/Decimal(11)))
macro_f = Decimal(F_all/Decimal(11)*100).quantize(Decimal('0.00'))

# print("micro precision: " + str(p))
# print("micro recall: " + str(r))
print("micro precision:" + str((p*Decimal(100)).quantize(Decimal('0.00'))))
print("micro recall:" + str((r*Decimal(100)).quantize(Decimal('0.00'))))
print("micro F1: " + str(micro_f))

# print("macro precision: " + str(allprecision/11))
# print("macro recall: " + str(allrecall/11))
print("macro precision: " + str(((allprecision/Decimal(11))*Decimal(100)).quantize(Decimal('0.00'))))
print("macro recall: " + str(((allrecall/Decimal(11)*Decimal(100))).quantize(Decimal('0.00'))))
print("macro F1: " + str((macro_f).quantize(Decimal('0.00'))))
