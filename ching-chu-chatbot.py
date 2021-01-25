import os

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    FollowEvent,
    MessageEvent,
    PostbackEvent,

    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ImageSendMessage,
    StickerSendMessage,

    ButtonsTemplate,

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


main_menu_buttom_template = TemplateSendMessage(
    alt_text = "Buttons template cannot be shown. Please check smartphone.",
    template = ButtonsTemplate(
        title = "Main Menu",
        text = "Please select an action:",
        actions = [
            PostbackTemplateAction(
                label = "Brief Introduction",
                displayText = "Brief Introduction",
                data = "action=BriefIntroduction"
            ),
            URIAction(
                label = "Resume Link",
                uri = "https://drive.google.com/uc?export=download&id=1AB_XRvgKfKGKPj4BA8Tk6BIA32DhhPp_"
            ),
            URIAction(
                label = "GitHub Link",
                uri = "https://github.com/Ching-Chu-Lin"
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
        title = "Other Function Menu",
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
                label = "Back To Main Menu",
                displayText = "Back To Main Menu",
                data = "action=BackToMainMenu"
            ),
        ]
    )
)


@handler.add(FollowEvent)
def handle_follow(event):
    reply_arr=[]

    greeting_text = (
        "Hello! This is the Line chat bot channel of Ching-Chu, Lin!\n"
        "You can choose one of the options on Main Menu!"
    )
    reply_arr.append(TextSendMessage(text = greeting_text))
    reply_arr.append(main_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return
    

@handler.add(PostbackEvent)
def handle_postback_from_buttom_menu(event):
    reply_arr=[]

    if event.postback.data == "action=BriefIntroduction":
        brief_intro_text = (
            "The Brief Introduction of Ching-Chu, Lin:\n"
        )
        reply_arr.append(TextSendMessage(text = brief_intro_text))
        brief_intro_text = (
            "Majoring in Computer Science, I am expected to graduate from National Taiwan University (NTU) in 2021 June. "
            "The average GPA of 2019 winter and 2020 summer semester is 4.12. "
            "I had worked as undergraduate research assistant in Laboratory of Algorithm Research and Laboratory of Cyber-Physical System. "
            "I am in the Wired Network Team in Network Administration and System Administration Program, "
            "where the team in charge of the wired network in the building of the department. "
            "I also work in NTU COOL (the course website organization of NTU) as AI team intern. "
        )
        reply_arr.append(TextSendMessage(text = brief_intro_text))
        brief_intro_text = (
            "In course project, I had developed applications in both front-end and back-end. "
            "My top 3 primary languages are C, Python and Java. "
            "I am experienced in Linux environment, Git, Machine Learning techniques, and MySQL. "
            "For more information, please refer to the Resume Link and Github Link in Main Menu! "
        )
        reply_arr.append(TextSendMessage(text = brief_intro_text))

        contact_info_text = (
            "Please contact me if there is any question.\n"
            "The Contact Information:\n"
            "E-Mail: b06902111@ntu.edu.tw\n"
            "Mobile Phone: 0909040070"
        )
        reply_arr.append(TextSendMessage(text = contact_info_text))

        reply_arr.append(main_menu_buttom_template)

    elif event.postback.data == "action=OtherFunction":
        reply_arr.append(other_function_buttom_template)

    
    if event.postback.data == "action=Photo":
        message = ImageSendMessage(
            original_content_url = "https://drive.google.com/uc?export=view&id=1K1nBXXS6PUqa01oXvuP30D6qOJgrX98n",
            preview_image_url = "https://drive.google.com/uc?export=view&id=1K1nBXXS6PUqa01oXvuP30D6qOJgrX98n"
        )
        reply_arr.append(message)
        reply_arr.append(main_menu_buttom_template)

    elif event.postback.data == "action=Stiker":
        message = StickerSendMessage(
            package_id = "11537",
            sticker_id = "52002738"
        )
        reply_arr.append(message)
        reply_arr.append(main_menu_buttom_template)

    elif event.postback.data == "action=BackToMainMenu":
        reply_arr.append(main_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


@handler.add(MessageEvent)
def handle_text_message(event):
    reply_arr=[]

    invalid_input_text = "Sorry! You can only choose the options on buttom template!"
    reply_arr.append(TextSendMessage(text = invalid_input_text))
    reply_arr.append(main_menu_buttom_template)

    line_bot_api.reply_message(event.reply_token, reply_arr)
    return


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host = '0.0.0.0', port = port)
