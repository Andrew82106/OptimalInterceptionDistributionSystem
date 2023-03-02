import requests

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


if __name__ == '__main__':
    x = getRoute(40.01116, 116.339303, 39.936404, 116.452562)
    print("end")