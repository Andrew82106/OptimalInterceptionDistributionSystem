from utils import h3Related, GeneratePyeCharts, loadMircoSoftDataSet
from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import ChartType
import h3
from utils.algorithm import MarkovModel


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


def AddRouteToMap(MapIn: BMap, RouteDataset=loadMircoSoftDataSet.FormatDataset(), width=1) -> BMap:
    print(RouteDataset)
    MapIn.add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=RouteDataset,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color="blue", opacity=0.2, width=width),
        effect_opts=opts.EffectOpts(trail_length=0.5),
    )
    return MapIn


def GenerateTheMap(type_=None):
    """
    生成地图

    :param type_: 1 in type，生成路径；2 in type，生成Hex Grid；3 in type：生成OneRoute
    :return:
    """
    # return AddHexToMap(GeneratePyeCharts.GenerateBasicMap())
    # return AddRouteToMap(GeneratePyeCharts.GenerateBasicMap())
    # return AddRouteToMap(AddHexToMap(GeneratePyeCharts.GenerateBasicMap()))
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
        sorted_keys = sorted(predictRES, key=predictRES.get, reverse=False)
        res = AddRouteToMap(res, DTset, width=1)
        color = ["#00ff46", "#c0ff00", "#deed00", "#fcda00", "#fcb400", "#fc7c00", "#fc0000"]
        # ner = h3.k_ring(h3Related.encode_to_h3(DTset[-1][-1][1], DTset[-1][-1][0]))
        """cnt = 0
        for i in ner:
            x = [[i[1], i[0]] for i in h3.h3_to_geo_boundary(i)]
            res = AddHexToMap(res, polygon=[x+[x[0]]], color=color[cnt], width=5)
            cnt += 1"""
        cnt = 0
        for i in sorted_keys:
            x = [[i[1], i[0]] for i in h3.h3_to_geo_boundary(i)]
            res = AddHexToMap(res, polygon=[x + [x[0]]], color=color[cnt], width=5)
            cnt += 1
    return res
