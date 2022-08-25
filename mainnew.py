from flask import Flask,request
import hashlib
import os
import xmltodict
import time

app = Flask(__name__)

@app.route('/wx', methods=["GET", "POST"])
def getinput():
    if (request.method == "GET"):
    # 表示是第一次接入微信服务器的验证
        signature=request.args.get('signature')
        timestamp=request.args.get('timestamp')
        nonce=request.args.get('nonce')
        token = "hhhhh"
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        sha1.update(list[0].encode('utf-8'))
        sha1.update(list[1].encode('utf-8'))
        sha1.update(list[2].encode('utf-8'))
        hashcode = sha1.hexdigest()
        echostr = request.args.get("echostr")
        if hashcode == signature:
            return echostr
        else:
            return ""
    elif request.method == "POST":
        # 表示微信服务器转发消息过来
        xml_str = request.data
        if not xml_str:
            return""
        # 对xml字符串进行解析
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")

        # 提取消息类型
        msg_type = xml_dict.get("MsgType")
        if msg_type == "text":
        # 表示发送的是文本消息
        # 构造返回值，经由微信服务器回复给用户的消息内容
            resp_dict = {
                "xml": {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "you say:" + xml_dict.get("Content")
                }
            }

            # 将字典转换为xml字符串
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str
        else:
            resp_dict = {
                "xml": {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "Dear I Love you so much"
                }
            }
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str
if __name__ == '__main__':
    app.run(port=int(os.environ.get('PORT', 80)))