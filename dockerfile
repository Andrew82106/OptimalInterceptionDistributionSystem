FROM python:3.8
WORKDIR /Project/mutiAGVallocator/


COPY requirements.txt ./
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

WORKDIR /Project/mutiAGVallocator/codelogs

CMD ["mkdir", "localSources"]
CMD ["gunicorn", "visiableMain:app", "-c", "./gunicorn.conf.py"]