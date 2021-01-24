import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent,
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
)

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


action_menu_buttom_template = TemplateSendMessage(
    alt_text = "Buttons template cannot be shown. Please check smartphone.",
    template = ButtonsTemplate(
        title = "Actions Menu",
        text = "Please select an action:",
        actions = [
            MessageTemplateAction(
                label = "Self Introduction",
                text = "Self Introduction"
            ),
            MessageTemplateAction(
                label = "Photo",
                text = "Photo"
            ),
            MessageTemplateAction(
                label = "Stiker",
                text = "Stiker"
            ),
        ]
    )
)


@handler.add(FollowEvent)
def handle_follow(event):
    reply_arr=[]

    greeting_text = "Hello! This is the Line chat bot channel of Ching-Chu, Lin!"
    reply_arr.append(TextSendMessage(text = greeting_text))
    reply_arr.append(action_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


@handler.add(MessageEvent, message = TextMessage)
def handle_echo_message(event):
    reply_arr=[]
    if event.message.text == "Self Introduction":
        pass

    elif event.message.text == "Photo":
        message = ImageSendMessage(
            original_content_url='https://imgur.com/ZvCOf6r',
            preview_image_url='https://imgur.com/ZvCOf6r'
        )
        reply_arr.append(message)

    elif event.message.text == "Stiker":
        message = StickerSendMessage(
            package_id='11537',
            sticker_id='52002738'
        )
        reply_arr.append(message)

    else:
        invalid_input_text = "Sorry! You can only choose (or enter) the options on Actions Menu!"
        reply_arr.append(TextSendMessage(text = invalid_input_text))

    reply_arr.append(action_menu_buttom_template)
    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)
