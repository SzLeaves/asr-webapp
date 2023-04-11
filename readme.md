# ASR Web APP
中文语音识别实验室APP，使用Django构建

## 技术框架
* Django:    后端框架
* Django-Channels: 聊天室组件 (WebSocket)
* MySQL:     数据持久化
* Redis:     消息缓存
* jQuery/BootStrap5: 前端组件库
* Tensorflow: 语音识别模型
* PaddlePaddle ([ppasr](https://github.com/yeyupiaoling/PPASR)): 标点符号预测模型

## 运行环境
测试环境：
* Python 3.9 **(必须)**
* Django == 4.17
* Tensorflow == 2.9.3

使用`pip install -r requirements.txt`安装所有依赖  
