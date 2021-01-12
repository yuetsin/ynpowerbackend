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
RESPSONSE with
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

#### Place Single Model Predict

```python
POST '/predict/place/single' with
	postParams: {
        beginYear: undefined,
        endYear: undefined,
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

#### Place Mix Model Validate

```python
POST '/predict/place/mix/validate' with
	methods: ['梯度提升', '模糊指数平滑', ...]
RESPONSE with
	ok: True # or False
```

#### Place Mix Model Predict

```python
POST '/predict/place/mix' with
	postParams: {
        beginYear: undefined,
        endYear: undefined,
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

