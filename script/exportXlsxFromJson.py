#!/usr/bin/python3
import json
import os
import sys
from openpyxl import Workbook

# 5A景点列表JSON文件
json_path = "../data/5A.json"
export_path = "../data/5A.dwdaxlsx"

def main():
    data = readListJson()
    # 创建一个 workbook
    wb = Workbook()
    # 获取被激活的 worksheet
    ws = wb.active
    # 设置单元格内容
    ws.append(["id", "景区", "省市地区码", "省(直辖市)", "市", "级别", "获评年份", "内容来源", "所属省编码", "经纬坐标"])

    for index in range(len(data)):
        id = data[index]['id']
        name = data[index]['name']
        provinceCode = data[index]['provinceCodeDb']
        provinceName = data[index]['provinceName']
        cityName = data[index]['cityName']
        gradesName = data[index]['gradesName']
        year = data[index]['year']
        contentSource = data[index]['contentSource']
        adcode = data[index]['provinceCode']
        location = data[index]['location']
        # 设置一行内容
        ws.append([id, name, provinceCode, provinceName, cityName, gradesName, year, contentSource, adcode, location])
    # 保存 Excel 文件
    wb.save(export_path)


def readListJson():
    if not os.path.exists(json_path):
        print(json_path + " 文件不存在或未找到，请先执行")
        print("python get5AFromGov.py")
        sys.exit()
    fo = open(json_path, "r+", encoding="utf-8")
    jsonStr = fo.read()
    fo.close()
    return json.loads(jsonStr)


main()