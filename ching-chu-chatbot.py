import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, TextMessage, TextSendMessage

app = Flask(__name__)


line_bot_api = LineBotApi('HomCZgjaLVxclg7EdrKWyHk+YQqwt6ZAAGcJu8TB/eTqEcC8886RTSJt7Z7nkNwtMjhKZncWsLd/RIa/DiUlkkpL8AS+MQpEpL6DgAhCo1haCNbW1vMa/v/enXI9PuNhg8x6TudU8ZJU/yf3nIEKQQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6115d530922cf075ce8fb427106743b6')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    message = TextSendMessage(text="Hello! This is the Line chat bot of Ching-Chu, Lin!\n")
    line_bot_api.reply_message(event.reply_token, message)

    message = TemplateSendMessage(
        alt_text='Buttons template cannot be shown. Please check smartphone.',

        template=ButtonsTemplate(
            title='Menu',
            text='Please select an action:',
            actions=[
                MessageTemplateAction(
                    label='Resume Link',
                    text='Resume Link'
                ),
                MessageTemplateAction(
                    label='Photo',
                    text='Photo'
                ),
                MessageTemplateAction(
                    label='Stiker',
                    text='Stiker'
                ),
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, message)
    return


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # webhook verify
    if event.source.user_id == "Udeadbeefdeadbeefdeadbeefdeadbeef":
        return

    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
    return


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
