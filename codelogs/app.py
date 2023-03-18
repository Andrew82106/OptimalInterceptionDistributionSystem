from flask import Flask, render_template
from data import *
import addFeaturesToMap

app = Flask(__name__)


@app.route('/')
def index():
    data = SourceData()
    c = addFeaturesToMap.GenerateTheMap([3])
    return render_template('index.html', form=data, title=data.title, MainMap=c)


@app.route('/corp')
def corp():
    data = CorpData()
    return render_template('index.html', form=data, title=data.title)


@app.route('/job')
def job():
    data = JobData()
    return render_template('index.html', form=data, title=data.title)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=False)
