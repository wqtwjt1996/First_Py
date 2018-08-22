#!/usr/bin/python3

import torch
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import os, datetime

VecDocPath = "D:/Studying/Courseware/大四/毕业设计/exp_data/train/IRdivdir"
Keyword = "淄博市"

def loadData():
    files = os.listdir(VecDocPath + "/" + Keyword)
    VecList = []
    NameList = []
    for file in files:
        f = open(VecDocPath + "/" + Keyword + "/" + file, 'r', encoding="utf-8")
        vlist = []
        NameList.append(os.path.join(VecDocPath + "/" + Keyword, file)[59:])
        for line in f.readlines():
            vlist.append(round(float(line), 30))
        VecList.append(vlist)
    NumList = []
    i = 0
    while i < len(VecList):
        NumList.append(VecList[i][-1])
        VecList[i].pop(-1)
        i += 1
    i = 0
    for list in VecList:
        for i in range(len(list)):
            list[i] *= 30000
    p = 0
    q = 0
    pairVecList = []
    pairNumList = []
    pairNameList = []
    for p in range(len(NumList)):
        for q in range(len(NumList)):
            if p >= q:
                q += 1
                continue
            else:
                pairVecList.append(VecList[p] + VecList[q])
                if NumList[p] > NumList[q]:
                    pairNumList.append(1)
                else:
                    pairNumList.append(0)
                ntl = []
                ntl.append(NameList[p])
                ntl.append(NameList[q])
                pairNameList.append(ntl)
                q += 1
        p += 1
    for z in NumList:
        print(z)
    pairVecTensor = torch.FloatTensor(pairVecList)
    pairNumTensor = torch.LongTensor(pairNumList)
    X, Y = Variable(pairVecTensor), Variable(pairNumTensor)
    return X, Y, len(VecList[0])

def buildNN(x, y, len):
    net = torch.nn.Sequential(
            torch.nn.Linear(2 * len, 1000),
            torch.nn.ReLU(),
            torch.nn.Linear(1000, 500),
            torch.nn.ReLU(),
            torch.nn.Linear(500, 500),
            torch.nn.ReLU(),
            torch.nn.Linear(500, 200),
            torch.nn.ReLU(),
            torch.nn.Linear(200, 2)
        )
    print("神经网络开始训练，请耐心等候。。。")
    start = datetime.datetime.now()

    optimizer = torch.optim.SGD(net.parameters(), lr=0.0001)
    loss_func = torch.nn.CrossEntropyLoss()


    for t in range(200):
        prediction = net(x)  # input x and predict based on x
        #print(prediction)
        #print(prediction.data.numpy().tolist())
        #print(y.data.numpy().tolist())
        #r = prediction.data.numpy().tolist()
        loss = loss_func(prediction, y)  # must be (1. nn output, 2. target)

        optimizer.zero_grad()  # clear gradients for next train
        loss.backward()  # backpropagation, compute gradients
        optimizer.step()  # apply gradients

    end = datetime.datetime.now()

    r = prediction.data.numpy().tolist()
    for z in r:
        print(z)

    print("神经网络训练完成！用时：" + str(end - start))

    restore_net(net)

def restore_net(net):
    torch.save(net, "D:/Studying/Courseware/大四/毕业设计/NET/淄博市p.pkl")

if __name__ == '__main__':
    x, y, len = loadData()
    buildNN(x, y ,len)