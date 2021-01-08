# APIs

## BaseURL

在未设定当前版本的情况下（默认情况下），请求的基地址是 `/api`。

> 例如 `http://localhost:5000/api/login`。

在设定了版本号（例如，`v3`）时，请求的地址嵌入在 `/api` 之后、实际功能之前。

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
	Metadata: str		# 类似"立法,下院,多数党"这样用逗号分开的数组
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
POST '/db/Update' with
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
	OriginData: dict
        date: str
        value: str
RESPONSE with
	None
```

#### Perform Create

```python
POST '/db/create' with
	NewData: dict
        date: str
        value: str
RESPONSE with
	None
```

