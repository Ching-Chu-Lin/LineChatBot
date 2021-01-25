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
    ImageSendMessage,
    StickerSendMessage,
    URITemplateAction,
    PostbackTemplateAction,
    MessageTemplateAction,
    URIAction,
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
            PostbackTemplateAction(
                label = "Brief Introduction",
                displayText = "Brief Introduction",
                data = "action=BriefIntroduction"
            ),
            URIAction(
                label = "GitHub Link",
                uri = "https://github.com/Ching-Chu-Lin"
            ),
            URIAction(
                label = "Resume Link",
                uri = "https://drive.google.com/uc?export=download&id=1AB_XRvgKfKGKPj4BA8Tk6BIA32DhhPp_"
            ),
            PostbackTemplateAction(
                label = "Other Function",
                displayText = "Other Function",
                data = "action=OtherFunction"
            ),
        ]
    )
)

other_function_buttom_template = TemplateSendMessage(
    alt_text = "Buttons template cannot be shown. Please check smartphone.",
    template = ButtonsTemplate(
        title = "Other Functinos",
        text = "Please select an action:",
        actions = [
            PostbackTemplateAction(
                label = "Photo",
                displayText = "Photo",
                data = "action=Photo"
            ),
            PostbackTemplateAction(
                label = "Stiker",
                displayText = "Stiker",
                data = "action=Stiker"
            ),
            PostbackTemplateAction(
                label = "Back To Action Menu",
                displayText = "Back To Action Menu",
                data = "action=BackToActionMenu"
            ),
        ]
    )
)


@handler.add(FollowEvent)
def handle_follow(event):
    reply_arr=[]

    greeting_text = "Hello! This is the Line chat bot channel of Ching-Chu, Lin!\nYou can one of the options on Actions Menu!"
    reply_arr.append(TextSendMessage(text = greeting_text))
    reply_arr.append(action_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return
    

@handler.add(PostbackEvent)
def handle_postback_from_buttom_menu(event):
    reply_arr=[]

    if event.postback.data == "action=BriefIntroduction":
        brief_intro_text = "The Brief Introduction of Ching-Chu, Lin:\n"
        reply_arr.append(TextSendMessage(text = brief_intro_text))
        reply_arr.append(action_menu_buttom_template)

    elif event.postback.data == "action=OtherFunction":
        reply_arr.append(other_function_buttom_template)

    
    if event.postback.data == "action=Photo":
        message = ImageSendMessage(
            original_content_url = "https://i.imgur.com/ZvCOf6r.jpg",
            preview_image_url = "https://i.imgur.com/ZvCOf6r.jpg"
        )
        reply_arr.append(message)
        reply_arr.append(action_menu_buttom_template)

    elif event.postback.data == "action=Stiker":
        message = StickerSendMessage(
            package_id = "11537",
            sticker_id = "52002738"
        )
        reply_arr.append(message)
        reply_arr.append(action_menu_buttom_template)

    elif event.postback.data == "action=BackToActionMenu":
        reply_arr.append(action_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


@handler.add(MessageEvent, message = TextMessage)
def handle_text_message(event):
    reply_arr=[]

    invalid_input_text = "Sorry! You can only choose the options on Actions Menu!"
    reply_arr.append(TextSendMessage(text = invalid_input_text))
    reply_arr.append(action_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)
