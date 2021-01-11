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

### VCS Stuff

#### Version Query

```python
GET '/version/query' with
	None
RESPONSE with
    ['v1.0', 'v1.1', 'v2.0', 'v2.2a']
```

#### Version Create

```python
POST '/version/create' with
	CurrentSchema: 'v3.3'
    NewSchemaName: str
RESPONSE with
	None
```

#### Version Rename

```python
POST '/version/rename' with
	CurrentSchema: 'v3.3a'
    NewSchemaName: 'v3.3b'
RESPONSE with
	None
```

#### Version Delete

```python
POST '/version/delete' with
	DeleteSchema: 'v1.0'
RESPONSE with
	None
```

### DataBaseCRUD

#### Get Metadata

```python
GET '/db/metadata' with
	Category: str		# SocialEco / ElecPower / GeoWeather / All
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

#### Perform Query

```python
GET '/db/query' with
	Metadata: str		# 类似"甲,乙,丙"这样用逗号分开的数组
    Category: str		# SocialEco / ElecPower / GeoWeather / All
RESPONSE with
	[
        {
            date: '2020-12-11',
        	value: 'some value'
        },
        ...
    ]
```

#### Perform Update

```python
POST '/db/update' with
	Category: str		# SocialEco / ElecPower / GeoWeather / All
	OriginData: dict
        date: str
        value: str
    ModifiedData: dict
        date: str
        value: str
RESPONSE with
	None
```

#### Perform Delete

```python
POST '/db/delete' with
	Category: str		# SocialEco / ElecPower / GeoWeather / All
	OriginData: dict
        date: str
        value: str
RESPONSE with
	None
```

#### Perform Create

```python
POST '/db/create' with
	Category: str		# SocialEco / ElecPower / GeoWeather / All
	NewData: dict
        date: str
        value: str
RESPONSE with
	None
```

#### Data Type Query

```python
GET '/db/dtype' with
	None
RESPONSE with
	list[str]			# ["int", "float", "double", "string"]
```

#### Exception Query

```python
GET '/db/except/query' with
	Category: str
    Year: int
RESPONSE with
	[
        {
            date: '2020-12-11',
            type: 'int',
        	value: 'some value',
            suggest: 'some new value'
        },
        ...
    ]
```

#### Exception Resolve

```python
POST '/db/except/resolve' with
	OriginData: dict
        date: str
        type: str
        value: str
        suggest: str
    ModifiedData: dict
        date: str
        value: str
RESPONSE with
	None
```

#### Exception Accept

```python
POST '/db/except/accept' with
	AcceptData:
        date: str
        type: str
        value: str
        suggest: str
RESPONSE with
	None
```

### Data Mining

#### Factors Query

```python
GET '/mining/factor/query' with
	None
RESPONSE with
	['Factor 1', 'Factor 2', ...]
```

#### KMeans: Suggested Category Count

```python
GET '/mining/factor/kmeans/suggest' with
	factors: 'factor1,factor2,factor3'
RESPONSE with
	{
        Count: 4
    }
```

#### Mining Request

```python
POST '/mining/request' with
	Region: str
    Factors: list[str]
    Method: str							# Pearson / KMeans / PCA / ARL
    Pearson: {
        threshold: float				# 皮尔逊系数阈值
    }
    KMeans: {
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
	Not Sure
```

### Shared

#### Region Selection

```python
GET '/region/query' with
	None
RESPONSE with
	['云南省', '丽江市', '红河州', '内比都']
```

