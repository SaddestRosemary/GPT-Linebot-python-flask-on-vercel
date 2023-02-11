from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

import os

line_bot_api = LineBotApi(os.getenv(CgT33YlIXcmaQQFx3B6zSNY5UyfnXMaZGDBx6aZjpefuH7uk9AnCAUXOJccA7QEbW336cll9C3a/prEBT5zWAAfEp1YCdib9Zc5Ena0xR7qF+kv/xo2ZulWr+M4kAo6mgJHA2x/JqL2Eyf9Iktv+5QdB04t89/1O/w1cDnyilFU=))
line_handler = WebhookHandler(os.getenv(d727f3b30dd37089923001c3f4a1e965))
working_status = os.getenv("DEFALUT_TALKING", default = "true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# domain root
@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    if event.message.type != "text":
        return

    if event.message.text == "พูด":
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ได้เลย ^_^ "))
        return

    if event.message.text == "เงียบ":
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="โอเคฉันไม่พูดละ > <"))
        return

    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))


if __name__ == "__main__":
    app.run()
