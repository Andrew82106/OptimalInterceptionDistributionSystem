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
from jinja2.utils import markupsafe
from pyecharts.globals import CurrentConfig
import addFeaturesToMap
from data import *

# 获取当前脚本所在的目录，并添加上级目录

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

app = Flask(__name__, static_folder="static", template_folder="templates")

"""@app.route("/oneroute")
def index():
    c = addFeaturesToMap.GenerateTheMap_Old([3])
    return markupsafe.Markup(c.render_embed())


@app.route("/routeS")
def K():
    c = addFeaturesToMap.GenerateTheMap_Old([1, 2])
    return markupsafe.Markup(c.render_embed())


@app.route("/points")
def KF():
    c = addFeaturesToMap.GenerateTheMap_Old([4])
    return markupsafe.Markup(c.render_embed())


@app.route("/jjj")
def KFC():
    c = addFeaturesToMap.GenerateTheMap_Old([5])
    return markupsafe.Markup(c.render_embed())"""


@app.route('/')
def index0():
    data = SourceData()
    c = addFeaturesToMap.GenerateTheMap()
    return render_template(
        'index.html',
        form=data,
        title=data.title,
        MainMap=c.render_embed()
    )


if __name__ == "__main__":
    app.run()
