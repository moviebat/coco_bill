#coco_bill

## 功能说明
1、处理图片挑选；  
2、数据增强；  
3、COCO格式数据生成；  


## 使用步骤
1、先使用RegularFileName对图片文件进行规整，形成frame_8位整数格式，写入到revised.txt;
2、分别用augment目录下的文件进行数据增强;
3、使用coco下的文件进行转换;



## 目录说明
### augment
数据增强目录

### coco
COCO格式数据生成

#### RegularFileName
从标注的目录执行后，将图片名称的frame_添加到points文件中去，统一格式

#### CheckImageLabel
从points文件种读取图片名称，然后去1目录下检查该文件是否存在

#### Label2Train
从目录下读取图片和points文件，生成COCO格式的训练数据

#### Label2Val
从目录下读取图片和points文件，生成COCO格式的Val数据

#### Label2Test
从目录下读取图片和points文件，生成COCO格式的Test数据

### utils
工具

