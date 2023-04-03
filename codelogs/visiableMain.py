import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "utils"))
sys.path.append(os.path.join(current_dir, "utils", "basicFun"))
sys.path.append(os.path.join(current_dir, "utils", "loadPOI_Data"))
sys.path.append(os.path.join(current_dir, "utils", "algorithm"))

from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
# from jinja2.utils import markupsafe
from pyecharts.globals import CurrentConfig
# from flask_bootstrap import Bootstrap
import addFeaturesToMap
from data import *

# 获取当前脚本所在的目录，并添加上级目录

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

app = Flask(__name__, static_folder="static", template_folder="templates")
# bootstrap = Bootstrap(app)

cache = -1
speed_cache = -1
PF_cache = -1


@app.route('/analysis')
def index0():
    """
    显示目标路线和追逃路线的函数
    :return:
    """
    data = SourceData()
    res = addFeaturesToMap.GenerateTheMap(DTset=cache, cache=(False if cache == -1 else True))
    c = res["Graph"]
    if cache:
        res["speed"] = speed_cache
        # res['policeForce'] = PF_cache
    res['detail_info']['data'] = []
    for kkk in res['policeForce']:
        try:
            pcs_name = kkk+"派出所" if kkk[-1] != ")" else kkk.split("(")[0] + "派出所" + kkk.split("(")[1]
            res['detail_info']['data'].append({"name": pcs_name, "free": res['policeForce'][kkk], "dis": res['dis'][pcs_name]})
        except:
            pcs_name = "北京市公安局" + kkk + "派出所" if kkk[-1] != ")" else "北京市公安局" + (kkk.split("(")[0] + "派出所" + kkk.split("(")[1])
            res['detail_info']['data'].append(
                {"name": pcs_name, "free": res['policeForce'][kkk], "dis": res['dis'][pcs_name]})
    res['time'] = res['dis']
    res1 = {}
    for i in res['time']:
        res1[i.replace("派出所", "").replace("北京市公安局", "")] = res['time'][i]
    res['time'] = res1

    data.echart1_data = {"title": "警力空余度",
                         "data": [{"name": i, "value": res["policeForce"][i]} for i in res["policeForce"]]}
    data.echart2_data = {"title": "时间消耗",
                         "data": [{"name": i, "value": res["time"][i]} for i in res["time"]]}
    data.echart4_data = {"title": "目标速度",
                         "data": [
                             {'name': "speed", 'value': [i for i in res["speed"][0]]},
                             {'name': "speed_avg", 'value': [i for i in res["speed"][1]]}
                         ],
                         "xAxis": [str(i) for i in range(len(res['speed'][0]))]}
    data.echarts3_1_data = res['hex_per']
    return render_template(
        'index.html',
        form=data,
        title=data.title,
        MainMap=c.render_embed(),
        table_info=res['detail_info']
    )


@app.route('/')
def index1():
    """
    只显示目标路线和异常度的函数
    :return:
    """
    global cache
    global speed_cache
    global PF_cache
    data = SourceData()
    res = addFeaturesToMap.GenerateTheMap([1])
    c = res["Graph"]
    cache = res["cache"]
    PF_cache = res['policeForce']
    speed_cache = res['speed']
    data.echart1_data = {"title": "警力空余度",
                         "data": [{"name": i, "value": res["policeForce"][i]} for i in res["policeForce"]]}
    data.echart2_data = {"title": "时间消耗",
                         "data": [{"name": i, "value": res["time"][i]} for i in res["time"]]}
    data.echart4_data = {"title": "目标速度",
                         "data": [
                             {'name': "speed", 'value': [i for i in res["speed"][0]]},
                             {'name': "speed_avg", 'value': [i for i in res["speed"][1]]}
                         ],
                         "xAxis": [str(i) for i in range(len(res['speed'][0]))]}
    data.echarts3_1_data = res['hex_per']
    return render_template(
        'index1.html',
        form=data,
        title=data.title,
        MainMap=c.render_embed(),
        table_info=res['detail_info']
    )


if __name__ == "__main__":
    app.run()
