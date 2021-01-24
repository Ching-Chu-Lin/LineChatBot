import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
import linebot.models 

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


def get_action_menu_buttom_template():
    return linebot.models.TemplateSendMessage(
        alt_text = "Buttons template cannot be shown. Please check smartphone.",

        template = linebot.models.ButtonsTemplate(
            title = "Actions Menu",
            text = "Please select an action:",
            actions = [
                MessageTemplateAction(
                    label = "Resume Link",
                    text = "Resume Link"
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


@handler.add(linebot.models.FollowEvent)
def handle_follow(event):
    reply_arr=[]

    reply_arr.append(linebot.models.TextSendMessage(text="Hello! This is the Line chat bot of Ching-Chu, Lin!"))
    reply_arr.append( get_Action_Menu_Buttom_Template() )

    line_bot_api.reply_message( token, reply_arr )
    return


@handler.add(linebot.models.MessageEvent, message=linebot.models.TextMessage)
def handle_echo_message(event):
    message = linebot.models.TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)
    return


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
