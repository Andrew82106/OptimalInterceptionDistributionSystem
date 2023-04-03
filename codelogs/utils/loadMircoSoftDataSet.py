import json
from basicFun import dirTool, locationConfig
import os
import tqdm
import random
from algorithm import MarkovModel
conf = locationConfig.config()


def loadDataset(upDate=False):
    """

    读取微软的出租车数据集

    :param upDate: 是否要更新数据集，如果False的话那么就直接从处理好的文件中读取

    :return: 返回一个dict，包含了每一个出租车一年内的位置数据

    """
    if not upDate:
        print("直接从文件中读取数据")
        with open(conf.RouteSum, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    RouteList = {}
    TXT_List = dirTool.ToolBags.ls(conf.DataLogs)
    for name in tqdm.tqdm(TXT_List, desc="读取数据中"):
        with open(os.path.join(conf.DataLogs, name)) as f:
            try:
                content = f.read()
            except:
                continue
            List_of_content = content.split("\n")
            for point_i in List_of_content:
                if len(point_i) == 0:
                    continue
                try:
                    name = point_i.split(",")[0]
                    point_x = point_i.split(",")[-2]
                    point_y = point_i.split(",")[-1]
                except Exception as e:
                    print(point_i)
                    raise e
                if name not in RouteList:
                    RouteList[name] = []
                RouteList[name].append([point_x, point_y])
    if upDate:
        JsonOBJ = json.dumps(RouteList)
        with open(conf.RouteSum, "w") as f:
            f.write(JsonOBJ)
    return RouteList


def MiniDataset(RouteListIn=-1, Save=False):
    """
    随机取数据集中的一部分，将多余的点和路径进行删除，返回一个小的优质数据集

    :param RouteListIn: 大数据集

    :param Save: 是否将数据集保存在本地，如果是False则直接从文件中返回数据

    :return: 返回修剪后的数据集
    """
    maxRoute = 100
    maxPoint = 100
    if not Save:
        with open(conf.RouteSumMini, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    NewRouteList = {}
    if RouteListIn == -1:
        RouteListIn = loadDataset()
    for i in tqdm.tqdm(RouteListIn, desc="选取小数据集ing"):
        if random.randint(0, 10) % 2 == 0:
            continue
        NewRouteList[i] = []
        for Point_x, Point_y in RouteListIn[i]:
            if (not conf.latRange[0] < float(Point_y) < conf.latRange[1]) or (not conf.lngRange[0] < float(Point_x) < conf.lngRange[1]):
                break
            if len(NewRouteList[i]) > maxPoint:
                break
            NewRouteList[i].append([Point_x, Point_y])
        if len(NewRouteList[i]) == 0:
            del NewRouteList[i]
        if len(NewRouteList) > maxRoute:
            break
    if Save:
        JsonOBJ = json.dumps(NewRouteList)
        with open(conf.RouteSumMini, "w") as f:
            f.write(JsonOBJ)
    return NewRouteList


def OneRoute(RouteListIn=MiniDataset(), RouteLength=10):
    """

    从小数据集中找一条路径，路径点数为10

    :param RouteListIn: 输入数据集，不填默认为小数据集
    :param RouteLength: 路径长度，默认为10
    :return: 返回一条路径
    """
    while 1:
        Route = -1
        while 1:  # 找到长度大于RouteLength的路径为止
            ID = random.randint(2, len(RouteListIn))
            cnt = 0
            for i in RouteListIn:
                cnt += 1
                if cnt == ID:
                    Route = RouteListIn[i]
            if len(Route) > RouteLength:
                break

        if Route == -1:
            raise Exception(f"没找到ID为{ID}的这条路径")
        if len(Route) <= RouteLength:
            raise Exception(f"小数据集中的路径太短了，小于了{RouteLength}的长度限制")
        left = random.randint(0, len(Route)-RouteLength)
        y = Route[left: left+RouteLength]
        for i in range(len(y)):
            y[i][0] = float(y[i][0])
            y[i][1] = float(y[i][1])
        if len(y) >= RouteLength:
            return [y]


def FormatDataset(RoutListIn=-1):
    """
    将粗数据（dict装的从json里面弄出来的数据）转化为可以被Bmap直接用于画轨迹的数据

    :param RoutListIn: 粗数据,默认-1返回小数据集，填1返回全数据集

    :return: 格式化后的数据
    """
    if RoutListIn == -1:
        RoutListIna = MiniDataset()
    elif RoutListIn == 1:
        RoutListIna = loadDataset()
    else:
        RoutListIna = RoutListIn
    NewRouteList = []
    for i in RoutListIna:
        if type(RoutListIna) == list:
            # NewRouteList[-1].append([float(i[0]), float(i[1])])
            NewRouteList.append(i)
        else:
            NewRouteList.append([])
            for j in RoutListIna[i]:
                try:
                    NewRouteList[-1].append([float(j[0]), float(j[1])])
                except Exception as e:
                    print(j)
                    print(e)
    return NewRouteList


if __name__ == '__main__':
    # x = FormatDataset()
    # z = loadDataset(upDate=False)
    # x = MiniDataset(Save=True)
    # x = MiniDataset(Save=True)
    x = FormatDataset(MiniDataset())
    """MarkovModel.Train(
        FormatDataset(
            loadDataset(upDate=True)
            # MiniDataset()
        ),
        conf.RoutePKL
    )"""
    # z = OneRoute()
    """
    微软数据集大小：
    10337个轨迹
    17662985个轨迹点
    """
    print("end")