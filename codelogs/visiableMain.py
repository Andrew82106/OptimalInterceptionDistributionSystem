import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)
sys.path.append(os.path.join(current_dir, "utils"))
sys.path.append(os.path.join(current_dir, "utils", "basicFun"))

from flask import Flask
from jinja2 import Environment, FileSystemLoader
from jinja2.utils import markupsafe
from pyecharts.globals import CurrentConfig
import addFeaturesToMap
# 获取当前脚本所在的目录，并添加上级目录

CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

app = Flask(__name__, static_folder="templates")


@app.route("/")
def index():
    c = addFeaturesToMap.GenerateTheMap()
    return markupsafe.Markup(c.render_embed())


if __name__ == "__main__":
    app.run()
