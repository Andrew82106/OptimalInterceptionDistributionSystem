import config
import requests
import pickle
import tqdm


def Pull_POI_Data():
    res = []
    for i in tqdm.tqdm(range(350), desc=f"读取百度地图POI数据中"):
        command = f"https://api.map.baidu.com/place/v2/search?query=公检法机构&tag=政府机构&region=北京&output=json&ak={config.ak_of_Explo}&page_size=20&page_num={i}"
        r = requests.request(method='get', url=command)
        x = r.json()
        res += x['results']

    with open(config.poi_pkl, 'wb') as f:
        pickle.dump(res, f)


def loadPOI_Data():
    with open(config.poi_pkl, 'rb') as f:
        loaded_obj = pickle.load(f)
    for KL in range(len(loaded_obj)-1, -1, -1):
        if KL > len(loaded_obj):
            break
        if not (("治安" in loaded_obj[KL]['name']) or ("警" in loaded_obj[KL]['name']) or ("公安" in loaded_obj[KL]['name']) or ("派出所" in loaded_obj[KL]['name'])):
            loaded_obj.pop(KL)
    return loaded_obj


if __name__ == '__main__':
    # Pull_POI_Data()
    x = loadPOI_Data()
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