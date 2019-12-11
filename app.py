import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=[
        "start", "description", "background", "16_18", "kaohsiung", 
        "18_20_win", "battle_win", "fish_win",
        "18_20_lose", "battle_lose", "fish_lose",
        "event_16_18", "event_18_20_win", "event_18_20_lose",
        "result_win", "result_lose","yes_event_16_18", "no_event_16_18",
        "yes_event_18_20_win", "no_event_18_20_win",
        "yes_event_18_20_lose", "no_event_18_20_lose"
    ],
    transitions=[
        {
            "trigger": "advance",
            "source": ["start", "description"],
            "dest": "background",
            "conditions": "is_going_to_background",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "description",
            "conditions": "is_going_to_description",
        },
        {
            "trigger": "advance",
            "source": ["background", "yes_event_16_18", "no_event_16_18"],
            "dest": "16_18",
            "conditions": "is_going_to_16_18",
        },
        {   
            "trigger": "advance",
            "source": "16_18",
            "dest": "event_16_18",
            "conditions": "is_going_to_event_16_18",
        },
        {
            "trigger": "advance",
            "source": "16_18",
            "dest": "kaohsiung",
            "conditions": "is_going_to_kaohsiung",
        },
        {        
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "fish_win",
            "conditions": "is_going_to_fish_win",
        },
        {        
            "trigger": "advance",
            "source": "18_20_win",
            "dest": "event_18_20_win",
            "conditions": "is_going_to_event_18_20_win",
        },
        {        
            "trigger": "advance",
            "source": ["fish_win", "yes_event_18_20_win", "no_event_18_20_win"],
            "dest": "18_20_win",
            "conditions": "is_going_to_18_20_win",
        },
        {        
            "trigger": "advance",
            "source": "18_20_win",
            "dest": "battle_win",
            "conditions": "is_going_to_battle_win",
        },
        {
            "trigger": "advance",
            "source": "kaohsiung",
            "dest": "fish_lose",
            "conditions": "is_going_to_fish_lose",
        },
        {
            "trigger": "advance",
            "source": "18_20_lose",
            "dest": "event_18_20_lose",
            "conditions": "is_going_to_event_18_20_lose",
        },
        {
            "trigger": "advance",
            "source": ["fish_lose", "yes_event_18_20_lose", "no_event_18_20_lose"],
            "dest": "18_20_lose",
            "conditions": "is_going_to_18_20_lose",
        },
        {
            "trigger": "advance",
            "source": "18_20_lose",
            "dest": "battle_lose",
            "conditions": "is_going_to_battle_lose",
        },
        {
            "trigger": "advance",
            "source": ["battle_win", "battle_lose"],
            "dest": "result_win",
            "conditions": "is_going_to_result_win"
        },
        {
            "trigger": "advance",
            "source": ["battle_win", "battle_lose"],
            "dest": "result_lose",
            "conditions": "is_going_to_result_lose"
        },
        {
            "trigger": "go_back",
            "source": ["result_win", "result_lose"],
            "dest": "start"
        },
        {
            "trigger": "advance",
            "source": "event_16_18",
            "dest": "yes_event_16_18",
            "conditions": "is_going_to_yes_event_16_18",
        },
        {
            "trigger": "advance",
            "source": "event_16_18",
            "dest": "no_event_16_18",
            "conditions": "is_going_to_no_event_16_18",
        },
        {
            "trigger": "advance",
            "source": "event_18_20_win",
            "dest": "yes_event_18_20_win",
            "conditions": "is_going_to_yes_event_18_20_win",
        },
        {
            "trigger": "advance",
            "source": "event_18_20_win",
            "dest": "no_event_18_20_win",
            "conditions": "is_going_to_no_event_18_20_win",
        },
        {
            "trigger": "advance",
            "source": "event_18_20_lose",
            "dest": "yes_event_18_20_lose",
            "conditions": "is_going_to_yes_event_18_20_lose",
        },
        {
            "trigger": "advance",
            "source": "event_18_20_lose",
            "dest": "no_event_18_20_lose",
            "conditions": "is_going_to_no_event_18_20_lose",
        },
    ],
    initial="start",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
