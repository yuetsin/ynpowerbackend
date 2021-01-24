# APIs

## BaseURL

请求的基地址总是 `/api`。

> 例如 `http://localhost:5000/api/login`。

## BaseResponse

响应的基本格式是：

```python
BaseResponse:
    "msg": str         # 可读的信息
    "code": int        # 返回代码。除了 200 均代表错误
    "data": dict       # 可选，返回的数据。以下所有的 RESPONSE with 指的就是这一部分。
```

## Features

### Account Stuff

#### Login

```python
POST '/login' with
    username: str
    password: str
RESPONSE with
    None
```

#### Logout

```python
POST '/logout' with
    None
RESPONSE with
    None
```

#### Load Recent Files

```python
GET '/recent' with
    None
RESPONSE with
    [
        {
            'name': 'FOO',
            'url': 'https://xxcdn.net/123'
        }, {
            ...
        }
    ]
```

### Tags Stuff

#### Tags Query

```python
GET '/tags/query' with
    tagType: str		# [Optional] 默认 ALL
RESPONSE with
	[
        {
            'id': 'v1.0',
            'tagType': 'MIX'
    	},
        {
            'id': 'v1.1',
            'tagType': 'LONGTERM'
    	}, ...
    ]
```

#### Tag Detail

```python
GET '/tags/detail' with
	tag: str
RESPONSE with
	{
        tagType: 'AAA',
        params: {
            v1: ...,
            v2: ...
        },
        graphData: [
            {
                'xName': '横轴标签',
                'yValue': '纵轴数字值'
            }, ...
        ],
        tableOneData: [
            {
                'index': '评价指标',
                'r2': '就是 R2',
                'mape': '就是 MAPE',
                'rmse': '就是 RMSE'
            }
        ],
        tableTwoData: [
            {
                'year': '年份',
                'predict': '预测值（MVW）'
            }
        ]
    }
```

>   注意，只有「电力预测」部分的 `tag` 才能读出 Data。

#### Tag Rename

```python
POST '/tags/rename' with
    tag: 'v3.3a'
    newTag: 'v3.3b'
RESPONSE with
    None
```

#### Tag Delete

```python
POST '/tags/delete' with
    tag: 'v1.0'
RESPONSE with
    None
```

### MetadataCRUD

#### Get Metadata

```python
GET '/db/metadata' with
    None
RESPONSE with
    [{
        value: 'value',
        label: 'label',
        children: [{
            ...
        }]
    },
        ...
    ]
```

#### Create Metadata

```python
POST '/db/metadata/create' with
    path: ['its', 'parent', 'node', 'path']
    name: 'newName'
RESPONSE with
    None
    # now it looks like 'its' -> 'parent' -> 'node' -> 'path' -> 'newName'
```

#### Rename Metadata

```python
POST '/db/metadata/rename' with
    path: ['the', 'very', 'node', 'path']
    name: 'newName'
RESPONSE with
    None
    # now it looks like 'the' -> 'very' -> 'node' -> 'newName'
```

#### Delete Metadata

```python
POST '/db/metadata/delete' with
    path: ['the', 'unlucky', 'node', 'path']
RESPONSE with
    None
```

#### Upload Metadata

```python
POST '/db/metadata/upload' with
    FILE
RESPONSE with
    None
```

### DataBaseCRUD

#### Upload Data

```python
POST '/db/upload' with
	FILE
RESPONSE with
	None
```

#### Perform Query

```python
POST '/db/query' with
    region: '红河州'
    grain: '月'
    beginYear: 2020
    endYear: 2028, 
    category: ['行政', '总统']
RESPONSE with
    [
        {
            key: '2020-12-11',
            value: 'some value'
        },
        ...
    ]
```

#### Perform Update

```python
POST '/db/update' with
    category: list[str]
    originData: dict {
        key: str
        value: str
    }
    modifiedData: dict {
        key: str
        value: str
    }
RESPONSE with
    None
```

#### Perform Delete

```python
POST '/db/delete' with
    category: list[str]
    originData: dict {
        key: str
        value: str
    }
RESPONSE with
    None
```

#### Perform Create

```python
POST '/db/create' with
    category: list[str]
    newData: dict {
        key: str
        value: str
    }
RESPONSE with
    None
```

#### Exception Query

```python
POST '/db/except/query' with
    category: list[str]
    beginYear: int
    endYear: int
    grain: str
    region: str
RESPONSE with
    [
        {
            category: ['A', 'ii'],
            grain: '秒',
            key: '2020-12-11',
            value: 'some value',
            suggest: 'some new value'
        },
        ...
    ]
```

#### Exception Resolve

```python
POST '/db/except/resolve' with
    originData: dict {
        category: list[str]
        grain: str
        region: str
        key: str
        value: str
        suggest: str
    }
    modifiedData: dict {
        category: list[str]
        grain: str
        region: str
        key: str
        value: str
        suggest: str
    }
RESPONSE with
    None
```

#### Exception Accept

```python
POST '/db/except/accept' with
    acceptData: dict {
        category: list[str]
        grain: str
        region: str
        key: str
        value: str
        suggest: str
    }
RESPONSE with
    None
```

### Data Mining

#### KMeans: Suggested Category Count

```python
GET '/mining/factor/kmeans/suggest' with
    factors: 'factor1,factor2,factor3'
RESPONSE with
    {
        count: 4
    }
```

#### Mining Request

```python
POST '/mining/request' with
    tag: str
    tagType: 'MINING'
    region: str
    factors: list[str]
    method: str                         # Pearson / KMeans / PCA / ARL
    pearson: {
        threshold: float                # 皮尔逊系数阈值
    }
    kMeans: {
        suggestCategoryCount: int       # 推荐最佳分类数
        categoryCount: int              # 分类数
    }
    PCA: {
        absThreshold: float             # 系数绝对值阈值
    }
    ARL: {
        minSupport: float               # 最小支持度
        minConfidence: float            # 最小置信度
    }
    beginYear: int
    endYear: int
RESPONSE with
    ['因素 1', '因素 2']
```

#### Mining Results

```python
GET '/mining/results' with
    None
RESPONSE with
    [
        {
            plan: '挖掘计划',
            results: ['因素 1', '因素 2']
        }
    ]
```

### Predict

#### Region Single Model Predict

```python
POST '/predict/region/single' with
    {
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
        region: '',
        industry: '',
        method: '',
        factor1: {
            name: '',
            hasValue: true,
            value: '',
        },
        factor2: {
            name: '',
            hasValue: true,
            value: '',
        },
        tag: 'v2.1',
        tagType: 'STATIC_REGIONAL'
      },
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Region Mix Model Validate

```python
POST '/predict/region/mix/validate' with
    methods: ['梯度提升', '模糊指数平滑', ...]
RESPONSE with
    ok: True # or False
```

#### Region Mix Model Predict

```python
POST '/predict/region/mix' with
    postParams: {
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
        region: '',
        industry: '',
        selectedMethods: [],
        tag: 'v2.1',
        tagType: 'MIX'
      },
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Industry Single Model Predict

```python
POST '/predict/industry/single' with
    {
        'beginYear': 2024,
        'endYear': 2029,
        'historyBeginYear': 2020,
        'historyEndYear': 2024,
        'industry': '农业',
        'method': '基于EEMD的行业用电量预测',
        'parameters': [..., ...],
        'tag': 'v2.1',
        'tagType': 'DYNAMIC_INDUSTRIAL'
    }
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Industry Mix Model Validate

```python
POST '/predict/industry/mix/validate' with
    methods: ['梯度提升', '模糊指数平滑', ...]
RESPONSE with
    ok: True # or False
```

#### Industry Mix Model Predict

```python
POST '/predict/industry/mix' with
    postParams: {
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
        region: '',
        industry: '',
        selectedMethods: [],
        tag: 'v2.1',
        tagType: 'MIX'
      },
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Saturation Curve Predict

```python
POST '/predict/saturation' with
    postParams: {
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
        region: '',
        industry: '',
        method: '',
        tag: 'v2.1',
        tagType: 'LONGTERM'
      },
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Payload Density Predict

```python
POST '/predict/payload' with
    postParams: {
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
        region: '',
        industry: '',
        method: '',
        tag: 'v2.1',
        tagType: 'LONGTERM'
      },
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

#### Municipal Data Upload

```python
POST '/predict/munidata/upload' with
    FILE
RESPONSE with
    None
```

#### Municipal Data Upload Files

```python
GET '/predict/munidata/files' with
	None
RESPONSE with
	['红河州.csv', '迪庆州.json', ...]
```

#### Province & Municipal Project Upload

```python
POST '/predict/provmuni' with
    {
        'historyBeginYear': 2019,
        'historyEndYear': 2020,
        'predictYear': 2023,
        'provPlan': '预测专案一', # 如果设置为 `__byUpload__` 则从上传文件中读取
        'provFile': '省.csv',	# 如果 provPlan 是 __byUpload__，那么从这里读
        'muniData': {
            '昆明市': '昆明.csv',
            ...
        },
    }
RESPONSE with
    tableThreeData: [
        {
            'year': '时间',
            'region': '地区',
            'predictValueBefore': '协调前预测值（MW）',
            'predictErrorBefore': '协调前预测误差',
            'predictValueAfter': '协调後预测值',
            'predictErrorAfter': '协调後预测误差',
        }
    ],
    tableFourData: [
        {
            'year': '年份',
            'region': '地区',
            'predictBefore': '协调前预测值（MVW）',
            'predictAfter': '协调後预测值'
        }
    ]
```

#### Big Data Predict

```python
POST '/predict/bigdata' with
    {
        'beginYear': 2020,
         'endYear': 2020,
         'historyBeginYear': 2023,
         'historyEndYear': 2023,
         'method': '猜测法',
         'patches': [
            {
                'grain': '年',
                'metaData': ['三', 'ii'],
                'value': 'NV',
                'year': 2023
            }, ...
         ],
         'region': '丽江市',
         'tag': 'v2.1',
        'tagType': 'BIGUSER'
    }
RESPONSE with
    graphData: [
        {
            'xName': '横轴标签',
            'yValue': '纵轴数字值'
        }, ...
    ],
    tableOneData: [
        {
            'index': '评价指标',
            'r2': '就是 R2',
            'mape': '就是 MAPE',
            'rmse': '就是 RMSE'
        }
    ],
    tableTwoData: [
        {
            'year': '年份',
            'predict': '预测值（MVW）'
        }
    ]
```

### Payload Traits

#### Daily Payload Traits

```python
GET '/payload/traits/daily' with
    beginDay: 'yyyy/MM/dd'    # yyyy/MM/dd
    endDay: 'yyyy/MM/dd'      # yyyy/MM/dd
RESPOSNE with
    [
        {
            'day': '2020/4/14',
            'dayMaxPayload': 42.4,
            'dayAveragePayload': 40.0,
            'dayPayloadRate': 0.5342,
            'dayMinPayloadRate': 0.3023,
            'dayPeekValleyDiff': 0.3010,
            'dayPeekValleyDiffRate': 0.1044
        }, ...
    ]
```

#### Monthly Payload Traits

```python
GET '/payload/traits/monthly' with
    beginMonth: '2020/04',   # yyyy/MM
    endMonth: '2020/09',     # yyyy/MM
RESPONSE with
    [
        {
            'month': '2020/9',
            'monthAverageDailyPayload': 148.03,
            'monthMaxPeekValleyDiff': 0.3010,
            'monthAverageDailyPayloadRate': 0.4044,
            'monthImbaRate': 0.4444,
            'monthMinPayloadRate': 0.1034
            'monthMaxPeekValleyDiffRate': 0.1034
        }, ...
    ]
```

#### Yearly Payload Traits

```python
GET '/payload/traits/year' with
    beginYear: '2020',  # yyyy
    endYear: '2024',    # yyyy
RESPONSE with
    [
        {
            'year': '2020',
            'yearMaxPayload': 489138401,
            'yearAverageDailyPayloadRate': 49.10,
            'seasonImbaRate': 46656,
            'yearMaxPeekValleyDiff': 1000,
            'yearMaxPeekValleyDiffRate': 0.424,
            'yearMaxPayloadUsageHours': 1000,
        }, ...
    ]
```

### Payload Charts

#### Daily Charts

```python
GET '/payload/charts/daily' with
	day: '2020/10/1'	# 和 /payload/traits/daily 里拿到的格式一样
                              # 「yyyy/MM/dd」
RESPONSE with
	{
        metaData: [
            {
                'key': '日最大负载',
                'value': 42.4
            },
            {
                'key': '日平均负载',
                'value': 11.6
            },
            {
                'key': '日负载率',
                'value': '50.5%'
            },
            {
                'key': '日峰谷差',
                'value': 3000
            },
            {
                'key': '日峰谷差率',
                'value': '50%'
            }
        ],
        xName: '小时',
        xData: ['0', '2', '4', '6', ...],
        yName: '单位：MW',
        yData: [
            {
                'tag': '原始负荷',
                'data': [1, 4, 2, 45, 8, 1]
            },
            {
                'tag': '预测负荷',
                'data': [3, 4, 1, 5, 1, 0]
            }
        ]
    }
```

#### Typical Daily Charts

```python
GET '/payload/charts/daily/typical' with
	year: 2020,
    period: '时期' # 丰水期、汛前枯期、汛后枯期
    category: '类型' # 最大负荷、最小负荷、中位负荷
RESPONSE with
	{
        xName: '小时',
        xData: ['0', '2', '4', '6', ...],
        yName: '单位：MW',
        yData: [
            {
                'tag': '典型负荷',
                'data': [1, 4, 2, 45, 8, 1]
            }
        ]
    }
```

#### Monthly Payload Charts

```python
GET '/payload/charts/monthly' with
	year: 2021,
    category: '类型' # 年负荷曲线、年连续负荷曲线、月平均日负荷曲线、月平均日负荷率曲线、月最大峰谷差曲线、月最大峰谷差率曲线、月不均衡系数曲线
RESPONSE with
	{
        xName: '月份',
        xData: ['1', '2', '3', '4', ...],
        yName: '单位：MW',
        yData: [
            {
                'tag': '负荷',
                'data': [1, 4, 2, 45, 8, 1]
            }
        ]
    }
```

#### Yearly Payload Charts

```python
GET '/payload/charts/yearly' with
	beginYear: 2021,
    endYear: 2024,
    category: '类型' # 历年最大负荷曲线、历年平均日负荷率曲线、历年最大峰谷差曲线、历年最大峰谷差率曲线、历年季不平衡系数曲线
RESPONSE with
	{
        xName: '年份',
        xData: ['1972', '1973', '1974', '1975', ...],
        yName: '单位：MW',
        yData: [
            {
                'tag': '负荷',
                'data': [1, 4, 2, 45, 8, 1]
            }
        ]
    }
```

### Payload Predicts

#### Database Query Method

```python
POST '/payload/predict/dbquery' with
    startYear: 2019,
    endYear: 2023,
    season: 1 # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload: 42,
    predictDailyAmonut: 100,
    gammaValue: 0.490,
    betaValue: 0.121,
    tag: str,
    tagType: 'SOKU'
RESPONSE with
    [
        {
            'time': 12,
            'actualPayload': 4244,
            'predictPayload': 1000
        }, ...
    ]
```

#### Clamping Method

```python
POST '/payload/predict/clamping' with
    startYear: 2019,
    endYear: 2023,
    season: 1 # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload: 42,
    predictDailyAmonut: 100
	tag: str,
    tagType: 'CLAMP'
RESPONSE with
    [
        {
            'time': 12,
            'actualPayload': 4244,
            'predictPayload': 1000
        }, ...
    ]
```

#### Interpolation Method

```python
POST '/payload/predict/interp' with
    startYear: 2019,
    endYear: 2023,
    season: 1 # 2 or 3 or 4, Spring, Summer, Autumn, Winter
    predictMaxPayload: 42,
    predictDailyAmonut: 100
    tag: str,
    tagType: 'INTERP'
RESPONSE with
    [
        {
            'time': 12,
            'actualPayload': 4244,
            'predictPayload': 1000
        }, ...
    ]
```

#### Yearly Continuous Payload Curve Prediction

```python
POST '/payload/predict/yearly' with
    startYear: 2019,
    endYear: 2023,
    predictMaxPayload: 42
    tag: str,
    tagType: 'YEARCONT'
RESPONSE with
    [
        {
            'time': '2023',
            'payload': 30.23
        }, ...
    ]
```

### Tags Parameter Loading

#### Data Mining Page

```python
GET '/params/mining' with
    tag: str
RESPONSE with
    {
        region: '',
        factors: [],
        method: '',
        pearson: {
            threshold: 0.5,
        },
        kMeans: {
            categoryCount: 0,
        },
        PCA: {
            absThreshold: 0.5,
        },
        ARL: {
            minSupport: 0.5,
            minConfidence: 0.5,
        },
        beginYear: null,
        endYear: null,
        tag: '',
    }
```

#### Static Regional Prediction Page

> 只用在「地区预测 + 单预测模型」页面。

```python
GET '/params/predict/static/region' with
    tag: str
RESPONSE with
    {
        historyBeginYear: null,
        historyEndYear: null,
        beginYear: null,
        endYear: null,
        region: '',
        industry: '',
        method: '',
        factor1: {
            name: '',
            hasValue: true,
            value: 0.5,
        },
        factor2: {
            name: '',
            hasValue: true,
            value: 0.5,
        },
    }
```

#### Dynamic Industrial Prediction Page

> 只用在「行业预测 + 单预测模型」页面。

```python
GET '/params/predict/dynamic/industry' with
    tag: str
RESPONSE with
    {
        industry: '',
        method: '',
        parameters: ['', ''],
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
    }
```

#### Mix Prediction Page

> 用在「地区预测 + 组合预测模型」页面和「行业预测 + 组合预测模型」两个页面中。
>
> 其中除了 `region` 和 `industry` 字段之外都是共享的。

```python
GET '/params/predict/mix' with
    tag: str
RESPONSE with
    {
        historyBeginYear: null,
        historyEndYear: null,
        beginYear: null,
        endYear: null,
        region: '',
        industry: '',
        selectedMethods: [],
      }
```

#### Long Term Prediction Page

> 用在两个远期规划页面中。

```python
GET '/params/predict/dynamic/region' with
    tag: str
RESPONSE with
    {
        region: '',
        method: '',
        parameters: ['', ''],
        beginYear: null,
        endYear: null,
        historyBeginYear: null,
        historyEndYear: null,
    }
```

#### Big User Prediction Page

> 只用在「大用户预测」一个页面里。

```python
GET '/params/predict/biguser' with
    tag: str
RESPONSE with
    {
        historyBeginYear: null,
        historyEndYear: null,
        beginYear: null,
        endYear: null,
        method: '',
        region: '',
        patches: [
            {
                metaData: ['a', 'b', 'c'],
                grain: '粒度（总是「年」）',
                year: '年份',
                value: '42',
            }
        ],
    }
```

#### Soku Payload Prediction

> 用在「负荷特性预测 / 搜库法」页面里。

```python
GET '/params/predict/soku' with
    tag: str
RESPONSE with
    {
        beginYear: null,
        endYear: null,
        season: null,
        maxPayload: null,
        dailyAmount: null,
        gamma: null,
        beta: null,
    }
```

#### Clamping Payload Prediction

> 用在「负荷特性预测 / 夹逼法」页面里。

```python
GET '/params/predict/clamping' with
    tag: str
RESPONSE with
    {
        beginYear: null,
        endYear: null,
        season: null,
        maxPayload: null,
        dailyAmount: null,
    }
```

#### Interpolating Payload Prediction

> 用在「负荷特性预测 / 插值法」页面里。

```python
GET '/params/predict/interp' with
    tag: str
RESPONSE with
    {
        beginYear: null,
        endYear: null,
        season: null,
        maxPayload: null,
        dailyAmount: null,
    }
```

#### Yearly Continuous Payload Prediction

> 用在「负荷特性预测 / 年度持续预测法」页面里。

```python
GET '/params/predict/yearcont' with
    tag: str
RESPONSE with
    {
        beginYear: null,
        endYear: null,
        maxPayload: null,
    }
```

### Predict Results

>   这里的 Results 只包括「电力电量预测」部分（省市总分协调预测除外）。
>
>   他们的预测结果都遵从同样的格式——一张 x - y 图表，两张数据表。

#### Query All Predictions

```python
GET '/predict/results/query' with
	None
RESPONSE with
	{
        'id': 'v1.0',
        'tagType': 'MIX'
    },
    {
        'id': 'v1.1',
        'tagType': 'LONGTERM'
    }, ...
```

#### Get Prediction Details

```python
GET '/predict/results/detail' with
	tag: 'v1.2'
RESPONSE with
	{
        parameters: [
            {
                'key': '方案名称',
                'value': 'v1.2'
            },
            {
                'key': '预测类型',
                'value': '远期预测'
            },
            {
                'key': '预测年份',
                'value': '2015 到 2020'
            },
            {
                'key': '预测方法',
                'value': '猜测法'
            },
            {
                'key': '预测时间',
                'value': '2021 年 1 月 21 日 11:04:33'
            }
        ],
        graphData: [
            {
                'xName': '横轴标签',
                'yValue': '纵轴数字值'
            }, ...
        ],
        tableOneData: [
            {
                'index': '评价指标',
                'r2': '就是 R2',
                'mape': '就是 MAPE',
                'rmse': '就是 RMSE'
            }
        ],
        tableTwoData: [
            {
                'year': '年份',
                'predict': '预测值（MVW）'
            }
        ]
    }
```

#### Prediction Comparison

```python
POST '/predict/results/compare' with
	{
        'tags': ['v1.1', 'v1.2', 'v1.4']
        'trait': '对比特征'
        # R2, or MAPE, or RMSE, or predictMVW
    }
RESPONSE with
	{
        xName: '年份',
        xData: ['2010 年', '2011 年', '2012 年', '2013 年', ...],
        yName: 'RMSE 值',
        yData: [
            {
                'tag': 'v1.1',
                'data': [1, 4, 2, 45, 8, 1]
            },
            {
                'tag': 'v1.2',
                'data': [3, 4, 1, 5, 1, 0]
            }, ...
        ]
    }
```

### Shared

#### Region Query

```python
GET '/region/query' with
    None
RESPONSE with
    ['云南省', '丽江市', '红河州', '内比都']
```

#### Grain Query

```python
GET '/grain/query' with
    None
RESPONSE with
    ['年', '月', '日', '时', '分', '秒']
```

#### Factors Query

```python
GET '/factor/query' with
    None
RESPONSE with
    ['Factor 1', 'Factor 2', ...]
```

#### Regional Methods Query

```python
GET '/method/region/query' with
    None
RESPONSE with
    ['逐步回归模型', ...]
```

#### Industrial Methods Query

```python
GET '/method/industry/query' with
    None
RESPONSE with
    ['基于ARIMA季节分解的行业电量预测', ...]
```

#### Industry Query

```python
GET '/industry/query' with
    None
RESPONSE with
    ['理', '工', '农', '医', ...]
```

#### Big Data Methods Query

```python
GET '/method/bigdata/query' with
    None
RESPONSE with
    ['猜测法', '穷举法', ...]
```

## Misc

### Tag Protocols

约定：「关联因素挖掘」和「电力电量预测」页面（除「省市总分协调预测」外）中所有的页面都拥有 Tag 功能。

一个 Tag 储存着一次请求的参数和结果。如果为空则代表不要保存 Tag。

如果给出的 Tag 已经存在，那么覆盖。

只有「电力电量预测」页面才能进入「预测结果对比和展示」。

由于不同页面的参数格式略有不同，所以 Tag 也分为不同的种类。规定如下：

*   `MINING`，数据挖掘方案。
*   `STATIC_REGIONAL`：地区单模型预测方案。
*   `DYNAMIC_INDUSTRIAL`：行业单预测模型方案。
*   `MIX`：组合预测方案。
*   `LONGTERM`：远期规划方案。
*   `BIGUSER`：大用户预测方案。
*   `SOKU`：用搜库法的负荷特性预测方案。
*   `CLAMP`：用夹逼法的负荷特性预测方案。
*   `INTERP`：用分型插值法的负荷特性预测方案。
*   `YEARCONT`：用年持续负荷预测法的负荷特性预测方案。

---

还有一些用于请求的特殊 Tag。

*   `PROVINCE`：可以用于「省市总分页面」中作为「省级」预测选项的方案。

*   `COMPARE`：「电力电量预测」页面的 Tag。用于「预测结果对比展示」部分。
*   `ALL`：所有的 Tags。

所有`tagType` 字段都在这里面枚举。

