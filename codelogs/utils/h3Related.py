import numpy as np
from h3 import h3
from basicFun import locationConfig as config

conf = config.config()


def encode_to_h3(lat, lng, resolution=7):
    """
    Encode a latitude and longitude into an H3 index.

    :param lat: The latitude of the point in degrees.
    :param lng: The longitude of the point in degrees.
    :param resolution: The H3 resolution (0-15).
    :return: The H3 index for the point.
    """
    h3_index = h3.geo_to_h3(lat, lng, resolution)
    return h3_index


def Separate(resolution=7):
    """
    将一个区域内的所有空间使用六边形填充

    :param resolution: 精度（0-15)）
    :return: 返回一个列表，其中包含了每一个六边形的六个顶点的坐标
    """
    Indexs = []
    polys = []
    for jinDu in np.around(np.arange(conf.lngRange[0], conf.lngRange[1], 0.008), decimals=6):
        for weiDu in np.around(np.arange(conf.latRange[0], conf.latRange[1], 0.008), decimals=6):
            h3_Index = h3.geo_to_h3(weiDu, jinDu, resolution)
            if h3_Index not in Indexs:
                Indexs.append(h3_Index)
                y_ = h3.h3_to_geo_boundary(h3_Index)
                temp = []
                for kk in y_:
                    temp.append([kk[1], kk[0]])
                temp.append([y_[0][1], y_[0][0]])
                polys.append(temp)
                # print(polys[-1])
    return polys


def convertRoute2H3(RouteList):
    """
    将一段路径转为一串连续的h3字符串
    :param RouteList: 输入的路径的经纬度坐标，纬度在前，经度在后。北京地区的经度大于纬度，因此下面的实现中直接取max
    :return: 返回一个列表，包含了h3字符串的list
    """
    H3_List = []
    for i in RouteList:
        H3_List.append(encode_to_h3(max(i[0], i[1]), min(i[0], i[1])))
    return H3_List


if __name__ == '__main__':
    z = Separate()
    print(len(z))
    print(encode_to_h3(113.016776, 40.636556))
    print("end")