import requests
from math import radians, cos, sin, asin, sqrt

ak = "lMsmTZUG1eX64cbhVg778VaRKvx1hhde"


def getRoute(origin_min, origin_max, dest_min, dest_max):
    command = f"https://api.map.baidu.com/directionlite/v1/driving?origin={origin_min},{origin_max}&destination={dest_min},{dest_max}&ak={ak}"
    r = requests.get(url=command)
    resList = r.json()['result']['routes'][0]['steps']
    res = []
    for KK in resList:
        path = KK['path']
        aa = path.split(";")
        for ii in aa:
            res.append([float(ii.split(",")[0]), float(ii.split(",")[1])])
    return [res]


def calcDisBetween(lat1, lon1, lat2, lon2):
    """
        Calculate the great circle distance(KM) between two points
        on the earth (specified in decimal degrees)
        """
    # 将经纬度转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为千米
    return c * r

def hex_center(vertices):
    """
    计算六边形中心点经纬度

    :param vertices: 包含六个顶点经纬度的列表
    :return: 中心点经纬度
    """
    # 计算六边形顶点经纬度的平均值
    latitudes = [v[0] for v in vertices]
    longitudes = [v[1] for v in vertices]
    avg_lat = sum(latitudes) / len(latitudes)
    avg_lon = sum(longitudes) / len(longitudes)

    return avg_lat, avg_lon


if __name__ == '__main__':
    x = getRoute(40.01116, 116.339303, 39.936404, 116.452562)
    print("end")