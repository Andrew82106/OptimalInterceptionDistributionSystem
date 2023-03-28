import asyncio
from aiohttp import TCPConnector, ClientSession
from pyecharts.charts import BMap, Radar
from pyecharts import options as opts
from pyecharts.globals import BMapType


async def get_json_data(url: str) -> dict:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()


def SampleData():
    data = asyncio.run(
        get_json_data(
            url="https://echarts.apache.org/examples/data/asset/data/hangzhou-tracks.json"
        )
    )
    map_data = [[y["coord"] for y in x] for x in data]
    return map_data


def GenerateBasicMap(center=None) -> BMap:
    """
    造最基础的地图

    :return: 返回一个BMap地图对象
    """
    if center is None:
        center = [116.38, 39.9]
    ak = "So5nviFUMbkIU4LvDMMooXdwsQkWQQ3Z"
    res = (
        BMap(init_opts=opts.InitOpts(width="1200px", height="800px"))
        .add_schema(
            baidu_ak=ak,
            center=center,
            zoom=13,
            is_roam=True,
            map_style={
                "styleJson": [
                    {
                        "featureType": "water",
                        "elementType": "all",
                        "stylers": {"color": "#d1d1d1"},
                    },
                    {
                        "featureType": "land",
                        "elementType": "all",
                        "stylers": {"color": "#f3f3f3"},
                    },
                    {
                        "featureType": "railway",
                        "elementType": "all",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "highway",
                        "elementType": "all",
                        "stylers": {"color": "#fdfdfd"},
                    },
                    {
                        "featureType": "highway",
                        "elementType": "labels",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "arterial",
                        "elementType": "geometry",
                        "stylers": {"color": "#fefefe"},
                    },
                    {
                        "featureType": "arterial",
                        "elementType": "geometry.fill",
                        "stylers": {"color": "#fefefe"},
                    },
                    {
                        "featureType": "poi",
                        "elementType": "all",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "green",
                        "elementType": "all",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "subway",
                        "elementType": "all",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "manmade",
                        "elementType": "all",
                        "stylers": {"color": "#d1d1d1"},
                    },
                    {
                        "featureType": "local",
                        "elementType": "all",
                        "stylers": {"color": "#d1d1d1"},
                    },
                    {
                        "featureType": "arterial",
                        "elementType": "labels",
                        "stylers": {"visibility": "off"},
                    },
                    {
                        "featureType": "boundary",
                        "elementType": "all",
                        "stylers": {"color": "#fefefe"},
                    },
                    {
                        "featureType": "building",
                        "elementType": "all",
                        "stylers": {"color": "#d1d1d1"},
                    },
                    {
                        "featureType": "label",
                        "elementType": "labels.text.fill",
                        "stylers": {"color": "#999999"},
                    },
                ]
            },
        )
        .add_control_panel(
            copyright_control_opts=opts.BMapCopyrightTypeOpts(position=3),
            maptype_control_opts=opts.BMapTypeControlOpts(
                type_=BMapType.MAPTYPE_CONTROL_DROPDOWN
            ),
            scale_control_opts=opts.BMapScaleControlOpts(),
            overview_map_opts=opts.BMapOverviewMapControlOpts(is_open=True),
            navigation_control_opts=opts.BMapNavigationControlOpts(),
            geo_location_control_opts=opts.BMapGeoLocationControlOpts(),
        )
    )
    return res


def Generate_Radar_Graph(dataLogs=None) -> BMap:
    if dataLogs is None:
        dataLogs = {'v1': [[4300, 10000, 28000]], 'v2': [[5000, 14000, 28000]], 'v3': [[4300, 50000, 19000]],
                    'v4': [[5000, 14000, 21000]]}
    c = (
        Radar(init_opts=opts.InitOpts(width="500px", height="250px"))
        .add_schema(
            schema=[
                opts.RadarIndicatorItem(name="销售", max_=6500),
                opts.RadarIndicatorItem(name="管理", max_=50000),
                opts.RadarIndicatorItem(name="信息技术", max_=30000),
            ]
        )
        .add("预算分配", dataLogs["v1"])
        .add("实际开销", dataLogs["v2"])
        .add("预算分配1", dataLogs['v3'])
        .add("实际开销1", dataLogs['v4'])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            legend_opts=opts.LegendOpts(
                selected_mode="single",
                orient="vertical",
                align="right",
                pos_right="30%"
            ),
        )
        # .render("radar_selected_mode.html")
    )
    return c


if __name__ == '__main__':
    # x = SampleData()
    Generate_Radar_Graph()
    print("end")
