import pandas as pd
import csv
import math
import datetime
import time as t
from datetime import datetime

input_file = open(r'F:\data\20180827\part-00000.csv', 'rt', encoding='utf8')
csv_file = csv.reader(input_file)

#读取数据，返回数据列表datasList
def readData(csv_file):
    datasList=[]
    for data in csv_file:
        datasList.append(data)
    datasList.remove(datasList[0]) #去除第一行中文标识
    return datasList

#去除起始基站经纬度或结束基站经纬度为0的数据




if __name__ == '__main__':
    datasList = readData(csv_file) #读取数据,datasList为接收的数据列表




