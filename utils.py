"""
このファイルは、画面表示以外の様々な関数定義のファイルです。
"""
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, PostbackAction,
    QuickReply, QuickReplyButton, MessageAction,
    FlexSendMessage
)
from openai import OpenAI

############################################################
# ライブラリの読み込み
############################################################

############################################################
# 設定関連
############################################################

############################################################
# 関数定義
############################################################

# ユーザからのメッセージを処理する関数（メッセージ整形）
def handle_user_message(event, line_bot_api, client, search_repair_info):
    user_message = event.message.text
    print("💬 受信メッセージ:", user_message)

    if user_message == "お問い合わせ":
        reply_contact_flex_menu(event, line_bot_api)
        return

    if user_message == "キャンペーン":
        flex_msg = reply_flex_campaign()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="キャンペーン情報", contents=flex_msg)
        )
        return

    if user_message == "場所・営業時間":
        flex_msg = reply_flex_store_info()
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="店舗情報", contents=flex_msg)
        )
        return

    # 修理系の問い合わせか？
    if any(kw in user_message for kw in ["割れ", "充電", "カメラ", "映らない", "バッテリー", "電池", "ホームボタン", "水没", "背面", "データ"]):
        results = search_repair_info(user_message)

        if len(results) > 1:
            reply_lines = [
                "🔍 複数ヒットしました。\n"
                "該当する症状をタップしてください。\n"
            ]

            for idx, r in enumerate(results, start=1):
                reply_lines.append(
                    f"""\
            {idx}. 📱 {r['model']}
            🔧 修理内容：{r['category']}
            💰 金額　　：¥{r['price']}
            🕒 修理時間：約 {r['time']}

            """
                )
            reply_text = "\n".join(reply_lines).strip()

        elif len(results) == 1:
            r = results[0]
            reply_text = f"""
                📱 {r['model']} の「{r['category']}」

                💰 修理料金：{r['price']}
                🕒 修理時間：約 {r['time']}

                ※ 店舗の混雑状況により前後する場合があります。
                """.strip()
        else:
            reply_text = "申し訳ありません。もう一度、機種名（例：iPhone 12）や症状（例：画面割れ）を含めてお問い合わせください。"

    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response.choices[0].message.content.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

# --- 「お問い合わせ」のFlex Message ---
def reply_contact_flex_menu(event, line_bot_api):
    bubble = create_main_menu_bubble()
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="お問い合わせメニュー", contents=bubble)
    )

# 内容はreply_flex_store_info()と同じだが、メニューに戻るで戻った時のメニューを表示
def reply_flex_menu(event, line_bot_api):
    bubble = create_main_menu_bubble()
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="メニューに戻るからのメインメニュー", contents=bubble)
    )

def reply_flex_store_info(event, line_bot_api):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://nagareyama-repair.ootaka-gift.jp/img/store_front2.jpg", # 店舗外観など
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
            {
                "type": "text",
                "text": "📍 店舗情報",
                "weight": "bold",
                "size": "lg"
            },
            {
                "type": "text",
                "text": "スマホ修理のおおたかギフト",
                "wrap": True,
                "margin": "md"
            },
                        {
                "type": "text",
                "text": "千葉県流山市東初石4-198-26",
                "wrap": True,
                "margin": "md"
            },
            {
                "type": "text",
                "text": "🕒 営業時間：9:00〜18:00\n　　（火曜定休）",
                "wrap": True,
                "margin": "sm"
            }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
            {
                "type": "button",
                "style": "primary",
                "height": "sm",
                "action": {
                "type": "uri",
                "label": "地図を見る",
                "uri": "https://maps.app.goo.gl/RTtmFWZeLv7vS4759"
                }
            },
            {
                "type": "button",
                "style": "secondary",
                "height": "sm",
                "action": {
                "type": "uri",
                "label": "予約ページへ",
                "uri": "https://ipanda-toride.ootaka-gift.jp/"
                }
            },
            {
                "type": "button",
                "style": "primary",
                "action": {
                "type": "postback",
                "label": "🔙 メニューに戻る",
                "data": "back_to_menu"
                }
            }
            ],
            "flex": 0
        }
    }

def reply_flex_campaign(event, line_bot_api):
    return {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "🎁 キャンペーン情報",
            "weight": "bold",
            "size": "lg",
            "margin": "md"
        },
        {
            "type": "text",
            "text": "① 口コミ投稿で1,000円OFF！\n修理後にGoogle口コミをご投稿で、1,000円引きいたします✨",
            "wrap": True,
            "margin": "md"
        },
        {
            "type": "text",
            "text": "② 同時修理で2,000円OFF！\n画面割れ＋バッテリー交換など2箇所目以降は各2,000円割引🎁",
            "wrap": True,
            "margin": "md"
        }
        ]
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
        {
            "type": "button",
            "style": "primary",
            "action": {
            "type": "postback",
            "label": "🔙 メニューに戻る",
            "data": "back_to_menu"
            }
        }
        ]
    }
    }

def reply_repair_category_menu(event, line_bot_api):
    flex_content = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "🔧 故障カテゴリを選んでください",
                    "weight": "bold",
                    "size": "lg",
                    "wrap": True
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "📱 画面・表示系",
                        "data": "repair_display"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "🔋 バッテリー・充電",
                        "data": "repair_battery"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "🚫 起動しない",
                        "data": "repair_boot"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "❓ その他",
                        "data": "repair_other"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "postback",
                        "label": "🔙 メニューに戻る",
                        "data": "back_to_menu"
                    }
                }
            ]
        }
    }

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="故障カテゴリを選択",
            contents=flex_content
        )
    )

def create_main_menu_bubble():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "md",
                    "action": {
                        "type": "postback",
                        "label": "🔧 修理可能か調べたい",
                        "data": "repair_search"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "md",
                    "action": {
                        "type": "postback",
                        "label": "🎁 キャンペーン",
                        "data": "campaign"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "height": "md",
                    "action": {
                        "type": "postback",
                        "label": "📍 場所・営業時間",
                        "data": "store_info"
                    }
                }
            ]
        }
    }

# 画面に関する不良の2階層目メニュー
def create_screen_issue_menu():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "画面・表示系の不具合",
                    "weight": "bold",
                    "size": "lg",
                    "margin": "md"
                },
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "📱 割れ・ヒビ",
                        "data": "screen_crack"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "⚫ 真っ黒（映らない）",
                        "data": "screen_black"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "🙅 無反応",
                        "data": "screen_no_response"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "✨ 点滅・線",
                        "data": "screen_flicker"
                    }
                },
                {
                    "type": "separator"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "flex": 1,
                            "style": "secondary",
                            "action": {
                                "type": "postback",
                                "label": "🔙 1つ戻る",
                                "data": "back_to_repair_category"
                            }
                        },
                        {
                            "type": "button",
                            "flex": 1,
                            "style": "secondary",
                            "action": {
                                "type": "postback",
                                "label": "🏠 トップに戻る",
                                "data": "back_to_menu"
                            }
                        }
                    ]
                }
            ]
        }
    }

# 修理機種選択メニュー
def create_model_select_menu():
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "修理する機種を選んでください",
                    "weight": "bold",
                    "wrap": True,
                    "size": "md"
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "uri",
                        "label": "iPhone",
                        "uri": "https://liff.line.me/2007870078-m2zAQllJ"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "iPad",
                        "data": "device_ipad"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "Android",
                        "data": "device_android"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "Nintendo Switch",
                        "data": "device_switch"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "その他",
                        "data": "device_other"
                    }
                },
                {
                    "type": "separator"
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "postback",
                        "label": "⬅ 1つ戻る（画面の症状）",
                        "data": "back_to_screen_issue"
                    }
                },
                {
                    "type": "button",
                    "style": "secondary",
                    "action": {
                        "type": "postback",
                        "label": "🏠 トップメニューに戻る",
                        "data": "back_to_menu"
                    }
                }
            ]
        }
    }

