from flask import Flask, request, abort, send_from_directory, render_template
import requests
import json
import os
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.models import (
    UnknownEvent
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    LocationMessageContent,
    StickerMessageContent,
    ImageMessageContent,
    VideoMessageContent,
    AudioMessageContent,
    FileMessageContent,
    UserSource,
    RoomSource,
    GroupSource,
    FollowEvent,
    UnfollowEvent,
    JoinEvent,
    LeaveEvent,
    PostbackEvent,
    BeaconEvent,
    MemberJoinedEvent,
    MemberLeftEvent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    PushMessageRequest,
    MulticastRequest,
    BroadcastRequest,
    TextMessage,
    ApiException,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    TemplateMessage,
    FlexMessage,
    Emoji,
    QuickReply,
    QuickReplyItem,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    FlexBubble,
    FlexImage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    ErrorResponse
)

# Get environment variables
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
liff_id = os.getenv('LIFF_ID', None)
rest_station_api = os.getenv('REST_STATION_URI', None)
rest_asset_api = os.getenv('REST_ASSET_URI', None)
if channel_secret is None or channel_access_token is None or rest_station_api is None or rest_asset_api is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

# init app
app = Flask(__name__)
handler = WebhookHandler(channel_secret)
configuration = Configuration(
    access_token=channel_access_token
)

# standard LINE webhook
@app.route('/webhook', methods=['POST'])
def line_webhook():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# text message handler
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    text = event.message.text     
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # check station
        if text.startswith('#'):
            req = requests.get(rest_station_api + text[1:])
            print("from station:",rest_station_api + text[1:])
            data = req.json()
            print("from station data:",data)
            # return number of devices
            count = len(data['data'])
            resp_text = 'Number of devices: ' + str(count)
            #resp_text = str(data['data'])            
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=resp_text)]
                )
            )
        # check asset
        elif text.startswith('*'):
            parts = text.split(' ', 1)  # Split into asset code and additional text
            asset_code = parts[0][1:]  # Remove '*' from asset code
            user_input = parts[1] if len(parts) > 1 else ""

            asset_data = get_asset_data(asset_code)
            
            # Convert JSON data to string format
            context_json = str(asset_data)  

            # Construct prompt with context
            prompt = f'''
            Now, answer the following question based on the JSON data:
            {user_input}
            Do not give JSON data in the answer.

            Here is the info about the asset tracking with Bluetooth Low Energy (BLE) technology.
            {context_json}

            JSON data contains the following fields:
            "asset" is the asset ID
            "status" is the status of query operation
            "data" is the record of observations containing the following three fields:
                "timestamp" is the time of observation
                "rssi" is the received signal strength indicator, bigger is closer to the station
                "station" is the id of BLE station that made the observation
            '''

            # Get AI response
            resp_text = ai_chat(prompt)

            # Send reply
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=resp_text)]
                )
            )
        # not commands
        else:
            # line_bot_api.reply_message(
            #     ReplyMessageRequest(
            #         reply_token=event.reply_token,
            #         messages=[TextMessage(text=text)]
            #     )
            # )
            print(text, ai_chat(text))
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=ai_chat(text))]
                )
            )

# LIFF
@app.route('/liff', methods=['GET'])
def liff():
    return render_template('liff.html', liff_id=liff_id)



# Function to fetch user data from an API
def fetch_asset_data(asset_id):
    response = requests.get( rest_asset_api + asset_id + '?mins=100000&rssi=-100')
    return response.json()

def ai_chat(text):
    api_key = os.getenv("GOOGLE_API_KEY")  # Store API key in environment variables
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    response = llm.invoke([HumanMessage(content=text)])
    return response.content if response else "No response received."


# Function to fetch asset data
def get_asset_data(asset_code):
    req = requests.get(rest_asset_api + asset_code  + '?mins=100000&rssi=-100')
    print("from asset:", rest_asset_api + asset_code)
    data = req.json()
    print("from asset data:", data)
    return str(data['data'])