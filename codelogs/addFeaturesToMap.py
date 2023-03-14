from utils import h3Related, GeneratePyeCharts, loadMircoSoftDataSet
from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import ChartType
import h3
from utils.algorithm import MarkovModel
from utils.loadPOI_Data import loadTrafficPoliceData
from utils.algorithm import calcDistance


def AddHexToMap(MapIn: BMap, polygon=None, color='red', width=1) -> BMap:
    if polygon is None:
        polygon = h3Related.Separate()
    # polygon = GeneratePyeCharts.SampleData()
    MapIn.add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=polygon,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color=color, opacity=0.3, width=width),
    )
    return MapIn


def AddRouteToMap(MapIn: BMap, RouteDataset=loadMircoSoftDataSet.FormatDataset(), width=1, color='blue') -> BMap:
    print(RouteDataset)
    MapIn.add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=RouteDataset,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color=color, opacity=0.2, width=width),
        effect_opts=opts.EffectOpts(trail_length=0.5),
    )
    return MapIn


def AddPointToMap(MapIn: BMap, PointDictIn: dict):
    data_pairs = []
    cnt = 0
    for POS_i in PointDictIn:
        data_pairs.append([POS_i['name'], [POS_i['location']['lng'], POS_i['location']['lat'], cnt]])
        cnt += 1
    MapIn.add(
        type_="effectScatter",
        series_name="警力点",
        data_pair=data_pairs,
        symbol_size=10,
        effect_opts=opts.EffectOpts(),
        label_opts=opts.LabelOpts(formatter="{a}", position="right", is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(color="blue"),
    )
    return MapIn


def GenerateTheMap(type_=None):
    """
    生成地图

    :param type_: 1 in type，生成路径；2 in type，生成Hex Grid；3 in type：生成OneRoute；4 in type：生成警力点；5 in type：生成规划的路径
    :return: 返回添加好元素的BMap对象
    """
    if type_ is None:
        type_ = [1]
    res = GeneratePyeCharts.GenerateBasicMap()
    if 1 in type_:
        res = AddRouteToMap(res, loadMircoSoftDataSet.FormatDataset(loadMircoSoftDataSet.MiniDataset()))
    if 2 in type_:
        res = AddHexToMap(res)
    if 3 in type_:

        model = MarkovModel.LoadModel()
        DTset = loadMircoSoftDataSet.OneRoute()
        NRouteList = [model.Map_Hex_to_ID[h3.geo_to_h3(i[1], i[0], resolution=7)] for i in DTset[0]]
        predictRES = MarkovModel.Predict(model, NRouteList)
        # 预测路径走向

        sorted_keys = sorted(predictRES, key=predictRES.get, reverse=False)
        res = AddRouteToMap(res, DTset, width=1)
        color = ["#00ff46", "#c0ff00", "#deed00", "#fcda00", "#fcb400", "#fc7c00", "#fc0000"]
        cnt = 0
        for i in sorted_keys:
            x = [[i[1], i[0]] for i in h3.h3_to_geo_boundary(i)]
            res = AddHexToMap(res, polygon=[x + [x[0]]], color=color[cnt], width=5)
            cnt += 1
        # 根据预测的路径走向将周围的几个框画出来

        LastPoint = DTset[0][-1]
        ori = loadTrafficPoliceData.loadPOI_Data()
        policeForces = []
        for i in ori:
            if calcDistance.calcDisBetween(LastPoint[1], LastPoint[0], i['location']['lat'], i['location']['lng']) <= 6:
                policeForces.append(i)
        res = AddPointToMap(res, policeForces)
        # 显示附近3km范围内的Police POI，并且给每个POI随机分配可调动警力

        danger_zones = sorted_keys[-3:]
        for i in danger_zones:
            center_of_zone = calcDistance.hex_center(h3.h3_to_geo_boundary(i))
            minn_dis = -1
            policeforces = -1
            for j in policeForces:
                dis = calcDistance.calcDisBetween(j['location']['lat'], j['location']['lng'], center_of_zone[0], center_of_zone[1])
                if minn_dis == -1:
                    minn_dis = dis
                    policeforces = j
                if minn_dis > dis:
                    minn_dis = dis
                    policeforces = j
            if policeforces == -1:
                raise Exception("没选到police force！")
            res = AddRouteToMap(res, calcDistance.getRoute(policeforces['location']['lat'], policeforces['location']['lng'], center_of_zone[0], center_of_zone[1]), color='red')
        # 选取前6个可分配警力最多的POI进行分配
    if 4 in type_:
        res = AddPointToMap(res, loadTrafficPoliceData.loadPOI_Data())

    if 5 in type_:
        res = AddRouteToMap(res, calcDistance.getRoute(40.01116, 116.339303, 39.936404, 116.452562))
    return res
