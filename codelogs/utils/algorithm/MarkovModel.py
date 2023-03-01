import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(parent_dir, 'algorithm'))
sys.path.append(os.path.join(parent_dir, "basicFun"))

import pickle
import h3Related
import tqdm
import h3


def LoadModel():
    with open("/Users/andrewlee/Desktop/Projects/mutiAGVallocator/datalogs/release/taxi_log_2008_by_id/Markov.pkl",
              'rb') as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


class Markov:
    def __init__(self):
        self.N = 0
        self.Map_Hex_to_ID = {}
        self.Map_ID_to_Hex = {}
        self.Fr = {}
        self.Route = []


def calcPossibility(MarkovModel: Markov, RouteList: list, Aim: int, degree=5):
    assert Aim == RouteList[-1]
    if degree > len(RouteList):
        degree = len(RouteList)
    if degree <= 1:
        return MarkovModel.Fr[Aim] / MarkovModel.N
    else:
        factorA = 0
        factorB = 0
        for Route_i in tqdm.tqdm(MarkovModel.Route, desc=f"计算区域{Aim}中"):
            factorA += str(Route_i).replace("[", '').replace("]", '').count(
                str(RouteList[-degree:]).replace("[", '').replace("]", ''))

            factorB += str(Route_i).replace("[", '').replace("]", '').count(
                str(RouteList[-degree:-1]).replace("[", '').replace("]", ''))

        return factorA / factorB


def Predict(MarkovModel: Markov, RouteList: list, degree=5):
    NearBy = h3.k_ring(MarkovModel.Map_ID_to_Hex[RouteList[-1]])
    for i in NearBy:
        if i not in MarkovModel.Map_Hex_to_ID:
            print(f"FATAl!! Hex ID:{i}")
            raise Exception("出现了不在映射中的位置")
    res = {}
    sum_ = 0
    for i in NearBy:
        res[MarkovModel.Map_Hex_to_ID[i]] = calcPossibility(MarkovModel, RouteList + [MarkovModel.Map_Hex_to_ID[i]], MarkovModel.Map_Hex_to_ID[i], degree)
        sum_ += res[MarkovModel.Map_Hex_to_ID[i]]

    # 浅浅做一个归一化
    for i in res:
        res[i] = res[i] / sum_
    return res


def Train(DataIn, SavePath: str):
    """
    训练Markov模型并且保存为pkl

    模型包括以下数据：

    所有网格出现次数总和：N(int)

    hex unique id和数字id的映射：Map_Hex_to_ID(dict)

    数字和hex unique id的映射：Map_ID_to_Hex(dict)

    某一个网格出现次数总和：Fr[id]

    每一条路径的hex unique id序列：Route[Route_i[[point_x, point_y], [point_x, point_y]]
    :param DataIn: 输入的路径数据
    :param SavePath: pkl的存放位置
    :return: 空
    """
    res = Markov()
    RouteListOfHex = []
    cnt = 0
    for Route_i in tqdm.tqdm(DataIn, desc="处理路径中"):
        RouteListOfHex.append([])
        for point_i in Route_i:
            hex_id = h3Related.encode_to_h3(point_i[0], point_i[1])  # 注意检查这里

            if hex_id not in res.Map_Hex_to_ID:
                res.Map_Hex_to_ID[hex_id] = cnt
                res.Map_ID_to_Hex[cnt] = hex_id
                res.Fr[cnt] = 1
                cnt += 1
            else:
                res.Fr[res.Map_Hex_to_ID[hex_id]] += 1
            RouteListOfHex[-1].append(res.Map_Hex_to_ID[hex_id])
    res.Route = RouteListOfHex
    print("处理完成，数据存储中")
    with open(SavePath, 'wb') as f:
        pickle.dump(res, f)


if __name__ == '__main__':
    x = LoadModel()
    print(Predict(x, [1]))
    print("end")
