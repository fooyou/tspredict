## 公共数据分析 - 使用 python 封装算法服务

### 目标

轻量方式实现一个 http 服务，通过 python 封装第三方算法库（pandas, numpy, scipy 等），实现针对时间序列数据的预测分析工作。

### 选型

- 轻量级 http 服务：使用 flask 提供 Restful 接口
- 第三方算法库：[待定]

### 使用方法

#### 环境安装

建议使用 virtualenv 建立虚拟环境

```
$ pip install -r requirements.txt
```

**启动 flask**

```
(tspredict) $ python tspredict.py
```

TODO:

- 添加更多的 API

### 服务接口

#### 查看 API 帮助文档

```
http://localhost:5000/
参数: 无
方式: GET
返回: API 帮助文档
```

#### 上传数据文件

```
http://localhost:5000/data/
参数: file=/path/to/csv
方式: POST
返回: 数据 id
```

示例：

```
$ curl http://localhost:5000/data/ -F file=/path/to/csv -X POST -v 
```

返回数据 id：

```
95755ccd
```

#### ARIMA 模型 API

```
http://localhost:5000/arima/<api>
参数: id，既数据 id
方式: GET
返回: 数据处理结果
```

示例：

请求：

```
$ curl http://localhost:5000/arima/95755ccd -d api=acf -X GET -v
```

返回:

```
{                               
    "acf": [                    
        1.0,                    
        0.9480473407524915,     
        0.8755748351253506,     
        0.8066811554965004,     
        0.7526254173883075,     
        0.7137699726519646,     
        0.6817336033310042,     
        0.662904386368449,      
        0.6556104843250863,     
        0.6709483279245044,     
        0.7027199209090714,     
        0.7432401890069327,     
        0.7603950422625558,     
        0.7126608704038239,     
        0.6463422792677535,     
        0.5859234238634493,     
        0.5379551907815617,     
        0.49974752598517996,    
        0.46873401291508704,    
        0.44987066497666167,    
        0.44162879574604624     
    ]                           
}        
```

### 参考：

> https://mart.coding.net/project/10359

> https://shimo.im/doc/AXFFUcat7eIUXK6D

> https://github.com/aarshayj/Analytics_Vidhya/

