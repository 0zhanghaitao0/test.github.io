import pandas as pd
import csv
import math
import datetime as d
import time as t
input_file = open(r'F:\data\20180827\part-00000.csv', 'rt', encoding='utf8')
csv_file = csv.reader(input_file)
def scan_alldoucument(csv_file):#所有记录中用户分类
    data=[]
    dataframes=[] #存储了所有用户的数据
    list=[]
    for content in csv_file:
        dataframes.append(content)
    dataframes=remove_noise_1(dataframes)
    for i in range(1 , len(dataframes)-1):
        if dataframes[i][0] == dataframes[i+1][0]:
            list.append(dataframes[i])
        else:
            list.append(dataframes[i])
            data.append(list)
            list=[]

    print(len(data))
    return data

def remove_noise_1(dataframes):#去除所有经纬度伟0的记录
    length = len(dataframes)
    m=1
    while m < length:
        if float(dataframes[m][3])==0 or float(dataframes[m][7])==0:
            dataframes.remove(dataframes[m])
            length=len(dataframes)
        else:
            m=m+1

    # i = 0
    # for content in dataframes:  #先找出一条记录的起始基站经纬度为0，并且其上一条记录的结束位置为0的情况，然后将两条记录合并
    #     if dataframes.index(content)!=0:
    #         JA = float(content[3])
    #         WA = float(content[4])
    #         JB = float(content[7])
    #         WB = float(content[8])
    #         Time = float(content[9])
    #         index = dataframes.index(content)
    #
    #         if Time!=0:
    #             if JA==0 and WA==0 :#如果起始基站经纬度为0 则先判断他的上以记录的结束基站经纬度是否为0，如果为0，则将这两条记录合并，
    #                 # 合并方法是将这条记录的结束基站经纬度给上条记录的结束基站经纬度，并且两条记录的时间也要叠加
    #                 if float(dataframes[index-1][7])==0 and float(dataframes[index-1][8])==0:
    #                     dataframes[index-1].pop(7)
    #                     dataframes[index-1].insert(7,content[7])
    #                     dataframes[index-1].pop(8)
    #                     dataframes[index-1].insert(8,content[8])
    #                     dataframes.remove(dataframes[index])
    #                 else: # 如果上条记录的结束基站的经纬度不为0，则将上调记录的结束基站经纬度赋予给此条记录的起始基站，目的是为了提高用户行走路线的精确度，降低下次去噪将其误判为漂移点的可能性
    #                     content.pop(3)
    #                     content.insert(3,dataframes[index-1][7])
    #                     content.pop(4)
    #                     content.insert(4,dataframes[index-1][8])
    #             elif JB==0 and WB==0 :
    #                 if index < len(dataframes)-1-i:
    #                     if float(dataframes[index+1][3])!=0 and float(dataframes[index+1][4])!=0:
    #                         content.pop(7)
    #                         content.insert(7,dataframes[index+1][3])
    #                         content.pop(8)
    #                         content.insert(8,dataframes[index+1][4])
    #         else:
    #             dataframes.remove(content)
    #             i=i+1
    #     else:
    #         if float(dataframes[0][3])==0 or float(dataframes[0][7])==0:
    #             dataframes.remove(dataframes[0])
    #             i = i + 1
    #

    return dataframes
def remove_duplicateData(dataframes,T): #除去重复元素
    index=0
    length = len(dataframes)-2

    while index<length:
        if length > 0:
            if float(dataframes[index][3])==float(dataframes[index+1][3]) and float(dataframes[index][4])==float(dataframes[index+1][4]):
                # if float(dataframes[index+1][2])-float(dataframes[index][2])<T:
                dataframes.remove(dataframes[index+1])
                length=length-1
            else:index=index+1
    return dataframes

def remove_pingPong(dataframes,T):#除去乒乓效应
    index = 0
    # for content in dataframes:
    length = len(dataframes)
    while index < length - 1:
        if index > 0:
            if index < length - 2:
                if dataframes[index - 1][3] == dataframes[index + 1][3] and dataframes[index - 1][4] == dataframes[index + 1][4] and myDate(dataframes[index-1],dataframes[index+1]).seconds<T:
                    dataframes.remove(dataframes[index+1])
        index = index + 1
        length = len(dataframes)
    return dataframes

#定义时间差函数
def myDate(content1, content2):
    date1=content1[1]
    date2=content2[1]
    date1 = t.strptime(date1, "%Y%m%d%H%M%S")
    date2 = t.strptime(date2, "%Y%m%d%H%M%S")
    startTime = t.strftime("%Y%m%d%H%M%S", date1)
    endTime = t.strftime("%Y%m%d%H%M%S", date2)
    startTime = d.datetime.strptime(startTime,"%Y%m%d%H%M%S")
    endTime = d.datetime.strptime(endTime,"%Y%m%d%H%M%S")
    date = endTime- startTime
    return date

def compute_twopoint_distance(content1,content2): #计算两点之间的距离，content1和content2是每一行的记录
    JA = float(content1[3]) / 180 * math.pi
    WA = float(content1[4]) / 180 * math.pi
    JB = float(content2[3]) / 180 * math.pi
    WB = float(content2[4]) / 180 * math.pi
    L = 2 * 6378137 * math.asin(
        math.sqrt(
            math.pow(math.sin((WA - WB) / 2), 2) + math.cos(WA) * math.cos(WB) * math.pow(math.sin((JA - JB) / 2), 2))
    )
    return L

def remove_driftData(dataframes):
    index=0
    while index<len(dataframes)-1:
        if float(dataframes[index][12])>33.33:
            dataframes.remove(dataframes[index])
        index=index+1
    return dataframes


def grid(dataframes,lng,lat):#网格化
    Cm=[]
    cluster = []
    cluster.append(dataframes[0]) #第一条记录默认为起始点
    index=0
    while(index<len(dataframes)-1):
        content1=float(dataframes[index+1][3])
        content2=float(dataframes[index+1][4])
        if content1>=float(dataframes[index][3])-lng and content1<=float(dataframes[index][3])+lng and content2>=float(dataframes[index][4])-lat and content2<=float(dataframes[index][4])+lat:
            cluster.append(dataframes[index+1])
            index=index+1
        else:
            Cm.append(cluster)
            cluster=[]
            cluster.append(dataframes[index+1])
            index=index+1
    return Cm
def parse_Cm(Cm):
    index=1
    length = len(Cm)
    while index<length-1:
        content0=Cm[index-1][-1]
        content01=Cm[index][0]
        content1=Cm[index][-1]
        content2=Cm[index+1][0]
        distance01 = compute_twopoint_distance(content0,content01)
        distance12=compute_twopoint_distance(content1,content2)
        if distance12>=700 and distance01>=700:
            #if len(Cm[index])>= len(Cm[index+1]) and len(Cm[index]):
            Cm.remove(Cm[index])
        else:
            index=index+1
        length = len(Cm)
    cm=[]
    for content1 in Cm:
        for content2 in content1:
            cm.append(content2)
        # if len(content1)!=1:
        #     print(len(content1))
        #     cm.append(content1[0])
        #     cm.append(content1[-1])
        # else:
        #     cm.append(content1[0])
    return cm

def compute_L_V(dataframes):#根据经纬度计算距离和速度
    index = 0
    while index < len(dataframes) - 1:
        content1 = dataframes[index]
        content2 = dataframes[index + 1]
        distance = compute_twopoint_distance(content1, content2)
        time = myDate(content1,content2).seconds
        if time == 0:
            v = 0
        else:
            v = distance / time
        dataframes[index].append(time)
        dataframes[index].append(distance)
        dataframes[index].append(v)
        index = index + 1
    return dataframes

def write_csv(dataframes):#向csv表写数据
    cols = ['用户号码', '开始时间', '开始基站', '开始基站经度', '开始基站纬度', '结束时间', '结束基站', '结束基站经度', '结束基站纬度','停留时间:s', '最新的停留时间','距离:m','速度:m/s'] #'停留时间:s','新的停留时间','距离:m','速度:m/s',
    data_frame = pd.DataFrame(dataframes)
    data_frame.columns = cols
    data_frame.to_csv(r'F:\data\20180827\1' + '.csv', index=None, encoding='utf_8_sig')


# if __name__ == '__main__':
#     data = scan_alldoucument(csv_file)
#     print(data)

if __name__ == '__main__':
     T=5*60#？
     D1=600#？
     D2=50#？
     sizeLat=0.0045487013  #500m x 500m 的网格
     sizeLng=0.0045487002
     list=[]
     list1=[]
     m=0
     data = scan_alldoucument(csv_file)
     for dataframes in data:
        #print(dataframes)
        #dataframes=remove_noise_1(dataframes) #对一些缺失的数据进行了处理
        #dataframes=remove_duplicateData(dataframes,T) #去除重复数据
        #for i in range(50): #迭代100次
        dataframes=remove_pingPong(dataframes,T) #去除乒乓效应
        #     dataframes = remove_duplicateData(dataframes, T)  # 去除重复数据
        #dataframes=compute_L_V(dataframes) #计算停留时间、距离、速度
        #dataframes=remove_driftData(dataframes)#去除漂移数据
        if len(dataframes)!=0:
            dataframes=grid(dataframes, sizeLng, sizeLat) #网格化 网格大小为500m x 500m 主要去除漂移点
            dataframes=parse_Cm(dataframes) #解析网格簇
            dataframes = compute_L_V(dataframes)
            list.append(dataframes)
        m=m+1
        print(m)

     for content in list:
         for content1 in content:
            list1.append(content1)


     write_csv(list1)


