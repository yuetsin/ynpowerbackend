# APIs

## BaseURL

在未设定当前版本的情况下（默认情况下），请求的基地址是 `/api`。

> 例如 `http://localhost:5000/api/login`。

在设定了版本号（例如，`v3`）时，将其嵌入到 `/api` 之后、功能路径之前。

> 例如 `http://localhost:5000/api/v3/logout`。

> 所有的 HTTP 请求（包括那些和版本控制不相关的）都依照此形式传输。

## BaseResponse

响应的基本格式是：

```python
BaseResponse:
    "msg": str 		# 可读的信息
    "code": int		# 返回代码。除了 200 均代表错误
    "data": dict	# 可选，返回的数据
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

### Schema Stuff

#### Schema Query

```python
GET '/schema/query' with
    None
RESPONSE with
    ['v1.0', 'v1.1', 'v2.0', 'v2.2a']
```

#### Schema Create

```python
POST '/schema/create' with
    newSchemaName: str
RESPONSE with
    None
```

#### Schema Rename

```python
POST '/schema/rename' with
    currentSchema: 'v3.3a'
    newSchemaName: 'v3.3b'
RESPONSE with
    None
```

#### Schema Delete

```python
POST '/schema/delete' with
    deleteSchema: 'v1.0'
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
        key: str
        value: str
        suggest: str
    }
    modifiedData: dict {
        category: list[str]
        grain: str
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
    region: str
    factors: list[str]
    method: str							# Pearson / KMeans / PCA / ARL
    pearson: {
        threshold: float				# 皮尔逊系数阈值
    }
    kMeans: {
        suggestCategoryCount: int		# 推荐最佳分类数
        categoryCount: int				# 分类数
    }
    PCA: {
        absThreshold: float				# 系数绝对值阈值
    }
    ARL: {
        minSupport: float				# 最小支持度
        minConfidence: float			# 最小置信度
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
    postParams: {
        beginYear: undefined,
        endYear: undefined,
        historyBeginYear: undefined,
        historyEndYear: undefined,
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
        beginYear: undefined,
        endYear: undefined,
        historyBeginYear: undefined,
        historyEndYear: undefined,
        region: '',
        industry: '',
        selectedMethods: [],
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
        'parameters': [..., ...]
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
        beginYear: undefined,
        endYear: undefined,
        historyBeginYear: undefined,
        historyEndYear: undefined,
        region: '',
        industry: '',
        selectedMethods: [],
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
        beginYear: undefined,
        endYear: undefined,
        historyBeginYear: undefined,
        historyEndYear: undefined,
        region: '',
        industry: '',
        selectedMethods: [],
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
        beginYear: undefined,
        endYear: undefined,
        historyBeginYear: undefined,
        historyEndYear: undefined,
        region: '',
        industry: '',
        selectedMethods: [],
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

#### Municipal Project Upload

```python
POST '/predict/project/upload' with
    FILE
RESPSONSE with
    None
```

#### Province & Municipal Project Upload

```python
POST '/predict/provmuni' with
    {
        'provPlan': '预测专案一',
        'muniPlans': [
            {
                'muniName': '昆明市',
                'planName': '预测专案'
            },
            ...
        ],
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
         'region': '丽江市'
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
    beginDay: '20200416'    # yyyyMMdd
    endDay: '20200816'      # yyyyMMdd
RESPOSNE with
    [
        {
            'day': '2020 年 4 月 14 日',
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
    beginMonth: '202004',   # yyyyMM
    endMonth: '202009',     # yyyyMM
RESPONSE with
    [
        {
            'month': '2020 年 9 月',
            'monthAverageDailyPayload': 148.03,
            'monthMaxPeekValleyDiff': 0.3010,
            'monthAverageDailyPayloadRate': 0.4044,
            'monthImbaRate': 0.4444,
            'monthMinPayloadRate': 0.1034
            'monthAveragePayloadRate': 0.1034
            # 这里文档截图不全，漏了几个数据项
            # 后端开发时补全
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
            'year': '2020 年',
            'yearMaxPayload': 489138401,
            'yearAverageDailyPayloadRate': 49.10,
            'seasonImbaRate': 46656,
            'yearMaxPeekValleyDiff': 1000,
            'yearMaxPeekValleyDiffRate': 0.424
            # 这里文档截图不全，漏了几个数据项
            # 后端开发时补全
        }, ...
    ]
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

#### Predict Projects Query

```python
GET '/predict/project/query' with
    None
RESPONSE with
    ['完美计划', '更完美计划', '非常完美计划', ...]
```

#### Big Data Methods Query

```python
GET '/method/bigdata/query' with
    None
RESPONSE with
    ['猜测法', '穷举法', ...]
```

