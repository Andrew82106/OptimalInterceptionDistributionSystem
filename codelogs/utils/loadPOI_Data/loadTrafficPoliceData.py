import config
import requests
import pickle
import tqdm


def Pull_POI_Data():
    res = []
    for i in tqdm.tqdm(range(23500), desc=f"读取百度地图POI数据中"):
        command = f"https://api.map.baidu.com/place/v2/search?query=公检法机构&tag=政府机构&region=北京&output=json&ak={config.ak_of_Explo}&page_size=20&page_num={i}"
        r = requests.request(method='get', url=command)
        x = r.json()
        res += x['results']

    with open(config.poi_pkl, 'wb') as f:
        pickle.dump(res, f)


def Pull_Gaode_PoiData():
    key = "f363a72669deebaa43a6294110b799f7"

    res = []
    for i in tqdm.tqdm(range(20), desc=f"读取百度地图POI数据中"):
        command = f"https://restapi.amap.com/v3/place/text?key={key}&city=北京&citylimit=true&keywords=派出所&offset=20&page={i}"
        r = requests.request(method='get', url=command)
        x = r.json()
        res += x['pois']

    res1 = []
    for i in res:
        res1.append({
            'name': i['name'],
            'location': {
                'lat': float(i['location'].split(',')[1]),
                'lng': float(i['location'].split(',')[0])
            }
        })
    with open(config.poi_pkl, 'wb') as f:
        pickle.dump(res1, f)


def loadPOI_Data():
    try:
        with open(config.poi_pkl, 'rb') as f:
            loaded_obj = pickle.load(f)
    except:
        with open("/Project/mutiAGVallocator/datalogs/release/taxi_log_2008_by_id/POI.pkl", 'rb') as f:
            loaded_obj = pickle.load(f)
    res = loaded_obj
    return res


def loadGaode_POI_Data():
    with open(config.poi_pkl, 'rb') as f:
        loaded_obj = pickle.load(f)
    res = loaded_obj
    return res


if __name__ == '__main__':
    # Pull_POI_Data()
    # x = loadPOI_Data()

    # Pull_Gaode_PoiData()
    x = loadGaode_POI_Data()
    for i in x:
        print(
            f"""
            "{i['name']}": [
            {i['location']['lng']},
            {i['location']['lat']}
        ],
        """
        )

    print("end")
