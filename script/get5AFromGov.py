#!/usr/bin/python3
import json
import time
import requests


def requestData(page=1):
    #  文旅部5A景区名单：https://www.mct.gov.cn/tourism/#/list?drid=4
    url = "https://www.mct.gov.cn/tourism/api/content/getContentListByDirId"
    para = {
        'directoryId': '4',
        'page': page,
        'size': 20,
        'searchList': []
    }
    return post(url, para)


def post(url, json):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.mct.gov.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://www.mct.gov.cn/tourism/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
    }
    response = requests.post(url, headers=headers, json=json)
    return response.json()


def saveFile(filename, content=""):
    file = open('../data/' + filename + ".json", "w+")
    file.write(content)
    file.close()


# main
page = 1
lastPage = False

list = []
simpleList = []
while not lastPage:
    print("请求第" + str(page) + "页...")
    data = requestData(page)
    lastPage = data['data']['contentList']['last']
    time.sleep(2)  # 休息两秒，以免过快调用接口触发反爬虫风控
    list.extend(data['data']['contentList']['content'])
    for item in data['data']['contentList']['content']:
        simpleList.append({'name': item['name'], 'id': item['id'], 'province': item['provinceName']})
    print("第" + str(page) + "页请求完成.OK!")
    if not lastPage:
        page = page + 1

print("开始写入完整5A景区列表...")
saveFile('5A', json.dumps(list, indent=4, ensure_ascii=False))
print("写入完整5A景区列表完成.OK!")

print("开始写入简略5A景区列表...")
saveFile('5A_simple', json.dumps(simpleList, indent=4, ensure_ascii=False))
print("写入简略5A景区列表完成.OK!")
