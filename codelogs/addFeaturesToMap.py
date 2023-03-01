from utils import h3Related, GeneratePyeCharts, loadMircoSoftDataSet
from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import ChartType


def AddHexToMap(MapIn: BMap) -> BMap:
    polygon = h3Related.Separate()
    # polygon = GeneratePyeCharts.SampleData()
    MapIn.add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=polygon,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color="red", opacity=0.6, width=1),
    )
    return MapIn


def AddRouteToMap(MapIn: BMap, RouteDataset=loadMircoSoftDataSet.FormatDataset()) -> BMap:
    print(RouteDataset)
    MapIn.add(
        series_name="",
        type_=ChartType.LINES,
        data_pair=RouteDataset,
        is_polyline=True,
        is_large=True,
        linestyle_opts=opts.LineStyleOpts(color="purple", opacity=0.6, width=1),
    )
    return MapIn


def GenerateTheMap():
    # return AddHexToMap(GeneratePyeCharts.GenerateBasicMap())
    # return AddRouteToMap(GeneratePyeCharts.GenerateBasicMap())
    # return AddRouteToMap(AddHexToMap(GeneratePyeCharts.GenerateBasicMap()))
    """
        [[116.58655, 40.07923], [116.58111, 40.07663], [116.58055, 40.07225], [116.58054, 40.07224], [116.58211, 40.0769], [116.58616, 40.07719], [116.58616, 40.07719]]
    """
    return AddRouteToMap(GeneratePyeCharts.GenerateBasicMap(), loadMircoSoftDataSet.OneRoute())
