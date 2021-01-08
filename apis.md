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

### VCS Stuff

#### Get Versions

```python
GET '/vcs/get' with
    None
RESPONSE with
	list[str]
```

#### Put Version

```python
POST '/vcs/post' with
    VersionName: str
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

### Schemas

#### Schema Query

```python
GET '/schema/query' with
	None
RESPONSE with
    ['Schema A', 'Schema B', 'Schema C', 'Schema D']
```

#### Schema Create

```python
POST '/schema/create' with
	CurrentSchema: 'Schema A'
    NewSchemaName: str
RESPONSE with
	None
```

#### Schema View

```python
GET '/schema/view' with
    name: 'Schema A'
RESPONSE with
	# Everything about this schema
```

#### Schema Rename

```python
POST '/schema/rename' with
	CurrentSchema: 'Schema A'
    NewSchemaName: str
RESPONSE with
	None
```

#### Schema Delete

```python
POST '/schema/delete' with
	DeleteSchema: 'Schema A'
RESPONSE with
	None
```

