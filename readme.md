# ASR Web APP
中文语音识别实验室APP，使用Django构建，包含中文语音转文字与中文语音聊天机器人模块

## 技术框架
* Django:    后端框架
* Django-Channels: 聊天室组件 (WebSocket)
* MySQL:     数据持久化
* Redis:     消息缓存
* jQuery/Bootstrap5: 前端组件库
* Tensorflow: 语音识别模型
* PaddlePaddle ([ppasr](https://github.com/yeyupiaoling/PPASR)): 标点符号预测模型

## 运行
测试环境：
* Python 3.9 **(必须)**
* Django == 4.17
* Tensorflow == 2.9.3

使用`pip install -r requirements.txt`安装所有依赖  
**编辑根目录下的`config.json`配置文件，写入数据库配置等信息**
```javascript
{
    "DATABASE": {
        // MySQL数据库配置
        "MYSQL": {
            // 填写地址, 端口, 用户名, 密码
            "HOST": "",
                "PORT": 3306,
                "USER": "",
                "PASSWORD": ""
        },
            // Redis数据库配置
            "REDIS": {
                // 填写地址, 端口, 密码
                "HOST": "",
                "PORT": 6379,
                "PASSWORD": ""
            }
    },
        // 邮件服务器配置
        "EMAIL": {
            // 填写邮件服务器地址, 用户名, 密码
            "HOST": "",
            "PORT": 25,
            "USER": "",
            "PASSWORD": ""
        },
}
```

## 使用ChatGPT Bot
* 在`config.json`中配置好`BOT`，填入调用的API路径与授权`key`即可  
```javascript
// Bot访问配置
"BOT": {
    // 填写OpenAI Chat API调用地址
    "API_URL": "",
    // 填写OpenAI API授权Key
    "API_KEY": ""
}
```
* **`API_URL`必须是[官方的Chat接口](https://platform.openai.com/docs/api-reference/chat/create)**，即路径中包含`v1/chat/completions`  
* 默认使用的会话模型是`gpt-3.5-turbo-0301`  
* `API_URL`可以使用代理
