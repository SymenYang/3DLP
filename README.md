# 3DLP 三维点线模型渲染
## 介绍
3DLP是一个使用python、numpy与OpenCV，离线渲染三维点线模型的工具。3DLP简单的渲染点线模型，不计算遮挡关系。3DLP支持更改点的位置、颜色、大小；支持更改线的端点位置、颜色、粗细、是否为虚线；支持更改相机的位置、焦距、角度、渲染范围、输出像素大小、输出图片路径等。同时3DLP支持定义包含多个点与线的模型，支持模型的旋转与三个方向上的缩放。
## 使用方法
```
python 3DLP.py -i [scene json]
```
## 场景描述文件
场景描述文件使用json描述场景，例如样例中的scene.json
```
{
    "path" : "./", # 指定import的文件查找路径
    "import" : {
        "box" : "ModelJsons/box.json", # 引入模型文件，并使用一个定制的名字表示，例如box
        "camera" : "ModelJsons/cameraModel.json",
        "plane" : "ModelJsons/plane.json"
    },
    "nodes" : [ # 指定场景包含的各个模型（模型依然可以包含模型）
        {
            "name" : "box", # 调用box模型
            "pos" : [0,-0.5,0] # 指定模型在世界坐标的位置
        },
        {
            "name" : "box",
            "pos" : [1.4,-0.5,1],
            "rotation" : [0,45,0] # 指定模型的旋转欧拉角度
        },
        {
            "name" : "box",
            "pos" : [-2,-0.5,2],
            "rotation" : [0,45,0]
        },
        {
            "name" : "camera",
            "pos" : [-3,-0,-3],
            "rotation" : [0,40,0]
        },
        {
            "name" : "camera",
            "pos" : [2,0,-3],
            "rotation" : [0,-40,0]
        },
        {
            "name" : "plane",
            "pos" : [-0.5,0,-3],
            "rotation" : [90,0,90],
            "scale" : [1,4,4] # 指定模型在三个维度上的缩放
        }
    ],
    "cameras":[ # 指定各个相机的参数
        {
            "pos": [-8,5,-1.5], # 相机在世界坐标系的位置
            "filename" : "test.png", # 输出的文件路径
            "f" : 0.8, # 焦距
            "eular" : [0,107,35], # 旋转欧拉角
            "w" : 1, # 在世界坐标系中，相机的横向可视范围
            "h" : 1, # 在世界坐标系中，相机的纵向可视范围
            "dx" : 0.5, # 光心x坐标
            "dy" : 0.5, # 光心y坐标
            "width" : 2048, # 输出图片宽度（px）
            "height" : 2048 # 输出图片高度（px）
        },
        {
            "pos": [-0.5,5,1],
            "filename" : "test2.png",
            "f" : 0.5,
            "eular" : [90,0,0],
            "w" : 1,
            "h" : 1,
            "dx" : 0.5,
            "dy" : 0.5,
            "width" : 2048,
            "height" : 2048
        }
    ]
}
```
## 模型文件
模型描述文件使用一个json进行描述，例如样例中的cameraTop.json
```
{
    "lineStyle" :{ # 批量指定一个模型中线的各个参数，优先级低于在线描述中指定的值
        "color" : [10,20,10], # 颜色（RGB）
        "width" : 3 # 线的粗细（px) 
    },
    "pos":[0,0,0], # 模型在自身坐标系标定的位置，在旋转中会绕自身坐标系原点旋转
    "lines":[ # 描述模型中的线
        {
            "start" : [0,0,0], # 在自身坐标系下，线段的起点坐标
            "end" : [-0.8,0,1], # 在自身坐标系下，线段的终点坐标
            "type" : "dash" # 线形，暂时支持dash与solid，默认solid
        },
        {
            "start" : [0,0,0],
            "end" : [0.8,0,1],
            "type" : "dash"
        },
        {
            "start" : [-0.8,0,1],
            "end" : [0.8,0,1],
            "type" : "dash"
        }
    ],
    "points":[ # 描述模型中的点
        {
            "pos" :[0,0,0], # 点的位置
            "width" : 10, # 点的半径（px）
            "color" : [13,23,13] # 颜色RGB
        }
    ]
}
```
## 3DLP渲染效果
scene.json渲染的结果如下：
![test.png](https://github.com/SymenYang/3DLP/blob/master/test.png)
![test2.png](https://github.com/SymenYang/3DLP/blob/master/test2.png)

## 更新：
新增点线渲染的画家算法，在调用`renderAll`函数时输入非"Normal"的字符串即可使用。其中点的大小由距离和焦距决定。