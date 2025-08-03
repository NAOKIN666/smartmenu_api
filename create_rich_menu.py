from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, MessageAction, URIAction, RichMenuBounds
import os
from dotenv import load_dotenv

load_dotenv()
# LINE BotのチャネルアクセストークンでAPIクライアントを初期化
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))

# 1. リッチメニューの定義
# 画像サイズは2500x1686を想定
rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1686),
    selected=False, # デフォルトで表示するかどうか
    name="teacher_support_menu", # 管理用の名前
    chat_bar_text="メニュー", # チャット画面下部のバーに表示されるテキスト
    areas=[
        # 左上のボタン：「教室について」（ウェブサイトへ）
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1667, height=843),
            action=URIAction(label='ご利用のご感想', uri='https://g.page/r/CdmOtKacw7igEAE/review')
        ),
        # 右上のボタン：「ご予約」（予約ページへ）
            RichMenuArea(
            bounds=RichMenuBounds(x=1668, y=0, width=833, height=843),
            action=URIAction(label='予約する', uri='https://ipanda-toride.ootaka-gift.jp/')
        ),
        # 左下のボタン：「お問い合わせ」（問い合わせ開始のメッセージを送信）
            RichMenuArea(
            bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
            action=MessageAction(label='お問い合わせ', text='お問い合わせ')
        ),
        # 左中のボタン：「アクセス」（問い合わせ開始のメッセージを送信）
            RichMenuArea(
            bounds=RichMenuBounds(x=833, y=843, width=834, height=843),
            action=URIAction(label='アクセス', uri='https://maps.app.goo.gl/RTtmFWZeLv7vS4759')
        ),
        # 右下のボタン：「料金プラン」（メッセージを送信）
        RichMenuArea(
            bounds=RichMenuBounds(x=1667, y=843, width=833, height=843),
            action=URIAction(label='料金プラン', uri='https://ipanda-toride.ootaka-gift.jp/iphone-repair-price/')
        )
        ]
    )

# 2. リッチメニューを作成し、richMenuIdを取得
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
# ステップ1：画像アップロード
with open("line_rich_menu.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, "image/png", f)
print("✅ リッチメニュー画像をアップロードしました。")
print(f"Rich Menu Created. ID: {rich_menu_id}")
# 出力例: Rich Menu Created. ID: richmenu-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# --- デフォルトとしてユーザーに表示設定（←ここを追加）---
line_bot_api.set_default_rich_menu(rich_menu_id)
print("✅ デフォルトのリッチメニューとして設定しました。")







# ボタン３行✕２列のリッチメニューの例
# # 左上
# RichMenuArea(
#     bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
#     action=MessageAction(label='button1', text='ボタン1が押されました')
# ),
# # 中央上
# RichMenuArea(
#     bounds=RichMenuBounds(x=833, y=0, width=834, height=843),
#     action=MessageAction(label='button2', text='ボタン2が押されました')
# ),
# # 右上
# RichMenuArea(
#     bounds=RichMenuBounds(x=1667, y=0, width=833, height=843),
#     action=MessageAction(label='button3', text='ボタン3が押されました')
# ),
# # 左下
# RichMenuArea(
#     bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
#     action=MessageAction(label='button4', text='ボタン4が押されました')
# ),
# # 中央下
# RichMenuArea(
#     bounds=RichMenuBounds(x=833, y=843, width=834, height=843),
#     action=MessageAction(label='button5', text='ボタン5が押されました')
# ),
# # 右下
# RichMenuArea(
#     bounds=RichMenuBounds(x=1667, y=843, width=833, height=843),
#     action=MessageAction(label='button6', text='ボタン6が押されました')
# )