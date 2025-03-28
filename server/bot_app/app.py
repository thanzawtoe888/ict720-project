from flask import Flask, request, abort, send_from_directory, render_template, jsonify
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
user_id_env = os.getenv('LINE_USER_ID', None)
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
        # not commands
        print(text, ai_chat(text))
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=ai_chat(text))]
            )
        )

@app.route('/emergency_alert', methods=['POST'])
def emergency_alert():
    # Get form data from the request
    data = request.json
    spo2 = data.get("spo2")  # Spo2 value
    bpm = data.get("bpm")  # BPM value
    activity = data.get("activity")  # Activity type (1 for walking, 2 for running)

    # Check if all required fields are present
    if not spo2 or not bpm or not activity:
        return jsonify({"error": "Missing required data: spo2, bpm, or activity"}), 400

    # Compose the alert message
    alert_message = f"Emergency Alert!\nSpo2: {spo2}\nBPM: {bpm}\nActivity: {activity}"

    # Optional: Send this alert to a LINE user or another service
    # For example, you could send the alert to a LINE user using the LINE Messaging API
    try:
        user_id = user_id_env  # Replace with the actual user ID
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            push_message_request = PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=alert_message)]
            )
            line_bot_api.push_message(push_message_request)
    except ApiException as e:
        return jsonify({"error": "Failed to send alert via LINE"}), 500

    # Return the result as a JSON response
    response = {
        "status": "Emergency alert sent successfully!",
        "spo2": spo2,
        "bpm": bpm,
        "activity": activity
    }
    return jsonify(response), 200

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

