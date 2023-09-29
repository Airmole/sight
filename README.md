# 全国5A景区数据列表

```commandline
├── data                         // 5A景点完整信息Excel文件
│   ├── 5A.json                  // 5A景点完整信息JSON文件
│   └── 5A_simple.json           // 5A景点简易信息JSON文件
└── script                       // 脚本
    ├── exportXlsxFromJson.py    // 读取JSON文件导出为Excel文件
    ├── fillLocationFromAmap.py  // 调用高德接口填充城市&位置坐标
    └── get5AFromGov.py          // 爬取网页更新5A景区数据文件
```

## 脚本用法

### 数据更新

```commandline
python script/get5AFromGov.py
```

> 脚本执行完成后data目录文件即为最新数据。

### 填充坐标

>执行前请先确保存在 `data/5A.json` 数据文件，否则请先执行“数据更新”操作

```commandline
python script/fillLocationFromAmap.py
```

## 数据直接下载

- [5A级景点完整JSON](https://raw.githubusercontent.com/Airmole/sight/main/data/5A.json)
- [5A级景点简略JSON](https://raw.githubusercontent.com/Airmole/sight/main/data/5A_simple.json)
- [5A级景点完整Excel](https://raw.githubusercontent.com/Airmole/sight/main/data/5A.xlsx)

完整JSON适用于需要景点详细情况的情况，简略JSON则适用于下拉选择列表等情况。

> 后续有空将逐步完善补充4A，3A景点列表数据。以及所在位置经纬度坐标信息。