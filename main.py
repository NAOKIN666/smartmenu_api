from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage, PostbackEvent
)
from openai import OpenAI
import os
from dotenv import load_dotenv
# import constants as ct

# 修理料金や所要時間を回答するための外部データ読み込み
from repair_data import search_repair_info
# ★ tracebackをインポートして、より詳細なエラー情報を表示
import traceback
import utils as ut

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# if os.getenv("USE_NGROK") == "true":
#     from pyngrok import ngrok
#     # ngrokトークンを環境変数から取得して設定
#     ngrok_token = os.getenv("NGROK_AUTHTOKEN")
#     ngrok.set_auth_token(ngrok_token)

# プルダウンメニュー呼び出し
@app.get("/smartmenu", response_class=HTMLResponse)
async def show_dropdown(request: Request):
    return templates.TemplateResponse("dropdown.html", {"request": request})

@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_decode = body.decode("utf-8")
    print("📩 ユーザからのメッセージ受信:", body_decode)
    try:
        handler.handle(body_decode, x_line_signature)
    except InvalidSignatureError:
        print("❌ Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    # 2. ★ あらゆる例外をキャッチするブロックを追加
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")
        # 詳細なエラーの発生箇所（トレースバック）をコンソールに出力
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")  
    return {"message": "OK"}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ut.handle_user_message(event, line_bot_api, client, search_repair_info)

# ポストバックイベント（ボタンが押されたとき）
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    print("🔁 ポストバック受信:", data)

    if data == "back_to_menu":
        ut.reply_flex_menu(event, line_bot_api)
    elif data in ["repair_search", "back_to_repair_category"]:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="修理可能か調べたい",
                contents=ut.reply_repair_category_menu(event, line_bot_api)
            )
        )
    elif data == "repair_display":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="画面・表示系の不良",
                contents=ut.create_screen_issue_menu()
            )
        )
    elif data in  ["screen_crack", "screen_broken", "screen_response", "screen_flicker"]:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="画面・表示系の不良",
                contents=ut.create_model_select_menu()
            )
        )
    elif data == "campaign":
            line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="キャンペーン情報",
                contents=ut.reply_flex_campaign(event, line_bot_api)
                )
        )
    elif data == "store_info":
            line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="店舗情報",
                contents=ut.reply_flex_store_info(event, line_bot_api)
                )
        )