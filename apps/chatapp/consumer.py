from datetime import datetime
from json import loads, dumps
from time import time

import requests
from channels.generic.websocket import WebsocketConsumer

from asrlab.settings import BOT_API_URL, BOT_API_HEADERS
from asrlab.settings import REDIS_POOL
from asrlab.settings import TIME_FORMAT, ZONE_INFO
from asrlab.settings import logger
from chatapp.models import Conversation, Message


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        """
        客户端请求websocket连接
        """
        isSuccess = False
        user = self.scope['user']

        # 初始化会话状态
        if len(self.scope['url_route']['kwargs']) == 0:
            # 获取当前用户

            # 获取用户会话
            userSession = Conversation.objects.filter(username=user)
            if len(userSession) == 0:
                # 当前用户无会话时新建
                self.scope['conversation'] = Conversation(username=user)
                self.scope['conversation'].save()
            else:
                self.scope['conversation'] = userSession[0]

            isSuccess = True

        # 切换会话状态
        else:
            sessionId = self.scope['url_route']['kwargs']['session_id']
            sessionList = Conversation.objects.filter(sessionId=sessionId)
            if len(sessionList) == 1:
                self.scope['conversation'] = sessionList[0]
                isSuccess = True

        if isSuccess:
            # 新建会话缓存连接
            self.scope['cache'] = REDIS_POOL
            # 新建消息缓存
            self.scope['messages_payload'] = None

            # 服务器允许客户端创建连接
            self.accept()
            logger.info(user.email + " 连接已建立 ID=" + self.scope['conversation'].sessionId)

        else:
            logger.error(user.email + " 会话创建失败")
            raise ConnectionRefusedError("Session create failed.")

    def websocket_receive(self, message):
        """
        触发前端响应,获取bot响应返回前端
        """
        # 缓存用户消息数据
        self.scope['cache'].lpush(
            self.scope['conversation'].sessionId,
            dumps({"sender": "user", "text": message['text'], "sendTime": ChatConsumer.getTimeStamp()})
        )

        # 调用Bot API
        try:
            isSuccess, botMessage = self.getBotMessages(message['text'])
            if isSuccess:
                # 缓存Bot返回消息数据
                self.scope['cache'].lpush(
                    self.scope['conversation'].sessionId,
                    dumps({"sender": "bot", "text": botMessage, "sendTime": ChatConsumer.getTimeStamp()})
                )

                # 返回调用内容结果
                self.send(ChatConsumer.getResponseContent(botMessage))
            else:
                self.send(ChatConsumer.getResponseContent(botMessage))
        except Exception as e:
            logger.error(e)
            self.send(ChatConsumer.getResponseContent(e))

    def websocket_disconnect(self, message):
        """
        客户端断开连接自动触发
        """
        # 有消息记录时, 将缓存的消息数据持久化至数据库
        if self.scope['cache'].llen(self.scope['conversation'].sessionId) != 0:
            try:
                cahceMessage = self.scope['cache'].lrange(self.scope['conversation'].sessionId, 0, -1)
                cahceMessage = [loads(str(msg, "utf-8")) for msg in cahceMessage]

                savedMessage = Message.objects.filter(conversation=self.scope['conversation'])
                if len(savedMessage) == 1:
                    # 将新消息添加到历史消息之前
                    cahceMessage.extend(loads(savedMessage[0].content))
                    # 更新消息
                    savedMessage[0].content = dumps(cahceMessage)
                    savedMessage[0].save()
                else:
                    newMessage = Message(
                        conversation=self.scope['conversation'],
                        content=dumps(cahceMessage)
                    )
                    newMessage.save()

            except Exception as e:
                logger.error(e)

        # 记录会话结束时间
        self.scope['conversation'].endTime = datetime.now()
        self.scope['conversation'].save()

        # 清除缓存
        self.scope['cache'].delete(self.scope['conversation'].sessionId)
        logger.info(self.scope['user'].email + ' 连接已断开 ID=' + self.scope['conversation'].sessionId)

    def getBotMessages(self, message):
        """
        获取Bot API响应信息
        """
        # request body
        if self.scope['messages_payload'] is None:
            self.scope['messages_payload'] = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}]
            }
        else:
            self.scope['messages_payload']['messages'].extend([{'role': 'user', 'content': message}])

        logger.info(self.scope['user'].email + ' 请求bot')
        startTime = time()
        responses = requests.post(url=BOT_API_URL, timeout=120,
                                  data=dumps(self.scope['messages_payload']), headers=BOT_API_HEADERS)
        endTime = time() - startTime
        # response text
        botMessge = loads(responses.text)['choices'][0]['message']['content']

        if responses.status_code == 200:
            logger.info(self.scope['user'].email + ' 请求成功, 耗时: %.2fs' % endTime)
            self.scope['messages_payload']['messages'].extend([{'role': 'assistant', 'content': botMessge}])
            return True, botMessge

        return False, botMessge

    @staticmethod
    def getTimeStamp():
        return str(datetime.now(ZONE_INFO).strftime(TIME_FORMAT))

    @staticmethod
    def getResponseContent(content):
        return dumps({
            "content": content,
            "timeStamp": ChatConsumer.getTimeStamp()
        }, ensure_ascii=False)
