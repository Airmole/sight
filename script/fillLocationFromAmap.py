#!/usr/bin/python3
import json
import os
import sys
import time
import requests

# 高德 Api Key (https://lbs.amap.com/dev/key)
amap_key = ""  # 请填入自己的高德接口Key
# 5A景点列表JSON文件
json_path = "../data/5A.json"


# main
def main():
    data = readListJson()
    for index in range(len(data)):
        name = data[index]['name']
        adcode = data[index]['provinceCode']
        # 已有location坐标跳过不查询更新
        if 'location' in data[index]:
            continue
        response = requestApi(name, adcode)
        time.sleep(2)  # 休息2秒
        if response['status'] == '0':
            print("请求高德API接口错误，" + response)
            break
        location = response['pois'][0]['location']
        cityname = response['pois'][0]['cityname']
        data[index]['location'] = location  # 补充经纬度坐标
        data[index]['cityName'] = cityname  # 补充城市名
        print('%s. %s -> %s' % (index, name, location))
    saveFile(json_path, json.dumps(data, indent=4, ensure_ascii=False))
    print(json_path + " 文件已保存更新")


def readListJson():
    if not os.path.exists(json_path):
        print(json_path + " 文件不存在或未找到，请先执行")
        print("python get5AFromGov.py")
        sys.exit()
    fo = open(json_path, "r+", encoding="utf-8")
    jsonStr = fo.read()
    fo.close()
    return json.loads(jsonStr)


def requestApi(keyword="", adcode=""):
    url = "https://restapi.amap.com/v3/place/text"
    query = '?key=%s&keywords=%s&city=%s' % (amap_key, keyword, adcode)
    url = url + query
    response = requests.request("GET", url, headers={}, data={})
    return response.json()


def saveFile(filepath, content=""):
    file = open(filepath, "w+")
    file.write(content)
    file.close()


main()
