from __future__ import unicode_literals
from django.http import JsonResponse
import json
import os
from sklearn.cluster import KMeans
import random


def jsonRes(data=None, result=True, reason=None):
    res = dict()
    if result:
        if data:
            res['data'] = data
            res['code'] = 0
            res['msg'] = 'ok'
            return JsonResponse(res)
        else:
            res['code'] = -1
            res['msg'] = 'no data'
            return JsonResponse(res)
    else:
        res['code'] = 1
        res['msg'] = reason or 'error'
    return JsonResponse(res)


def everyday(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        res = trafficVisApi.getEveryDayData(req['date'], req['classfilier'])
        return jsonRes(res)
    else:
        return jsonRes(result=False)


class TrafficVisApi:
    def __init__(self, path):
        self.path = path
        self.dateDict = dict()
        self.date = self.process()

    def readFile(self):
        all_file = os.listdir(self.path)
        absolutePath = [self.path + subPath for subPath in all_file]
        cur_data_dir = 0
        while cur_data_dir < 1:
            with open(absolutePath[cur_data_dir], 'r') as f:
                yield f.readlines()
            cur_data_dir += 1

    def process(self):
        for data in self.readFile():
            for line in data:
                order = line.strip('\n').split()
                if order[11] not in self.dateDict.keys():
                    try:
                        self.dateDict[order[11]] = [[[float(order[-6]), float(order[-7])], [float(order[-4]), float(order[-5])]]]
                    except:
                        pass
                else:
                    try:
                        self.dateDict[order[11]].append([[float(order[-6]), float(order[-7])], [float(order[-4]), float(order[-5])]])
                    except:
                        pass
        return sorted(self.dateDict.keys())

    def getEveryDayData(self, cur_data, k):
        grouping = dict()
        resultData = dict(o=[], d=[], o_kmens=[], d_kmens=[])
        rawData = self.dateDict[cur_data]
        for res in rawData:
            resultData['o'].append(res[0])
            resultData['d'].append(res[1])
        resultData['o_kmens'] = KMeans(n_clusters=k, random_state=9).fit_predict(resultData['o']).tolist()
        resultData['d_kmens'] = KMeans(n_clusters=k, random_state=9).fit_predict(resultData['d']).tolist()
        # print(set(resultData['o_kmens']))
        for index, ores in enumerate(resultData['o_kmens']):
            if ores not in grouping.keys():
                grouping[ores] = [[[resultData['o'][index], resultData['d'][index]], [ores, resultData['d_kmens'][index]]]]
            else:
                grouping[ores].append([[resultData['o'][index], resultData['d'][index]], [ores, resultData['d_kmens'][index]]])
        for key in grouping.keys():
            grouping[key] = random.sample(grouping[key], int(0.3 * len(grouping[key])))
        return [resultData, grouping]
        # return resultData


PATH = 'G:/data_xu/haikou/haikou/'
trafficVisApi = TrafficVisApi(PATH)

if __name__ == "__main__":
    # PATH = 'G:/data_xu/haikou/haikou/'
    # trafficVisApi = TrafficVisApi(PATH)
    # trafficVisApi.getEveryDayData('2017-05-01', 10)
    # a = [[1, 2], [3, 4], [5, 6], [8, 0], [10, 10]]
    # b = random.sample(a, int(0.5*len(a)))
    print(b)
    pass