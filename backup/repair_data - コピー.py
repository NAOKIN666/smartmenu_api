# repair_data.py
import pandas as pd
import re

# 類義語・言い換えの辞書
SYNONYM_DICT = {
    "バッテリー": ["電池", "バッテリー", "減る", "充電", "持ちが悪い"],
    "画面": ["画面", "フロントパネル", "割れ", "ひび", "映らない"],
    "背面": ["背面", "裏", "リアガラス"],
    "カメラ": ["カメラ", "レンズ", "映らない"],
    "ホームボタン": ["ホームボタン", "反応しない"],
    "水没": ["水没", "濡れた"],
    "データ": ["データ", "消えた", "移行"]
}

# CSVの読み込み
df = pd.read_csv("data/iphone_repair_price.csv")

def search_repair_info(message: str) -> str:
    # 前処理：小文字化・スペース除去（精度向上のため）
    message = message.lower().replace(" ", "").replace("　", "")

    hits = [] # ヒットした修理情報を格納するリスト

    for _, row in df.iterrows():
        model = str(row['機種']).lower().replace(" ", "").replace("　", "")
        symptom = str(row['症状']).lower().replace(" ", "").replace("　", "")
        similar = str(row['類似']).replace("＃", "#").lower()

        # 類似語句リスト作成（#付きのワードを抽出）
        similar_keywords = [kw.strip("#") for kw in similar.split() if kw.startswith("#")]
        all_keywords = symptom.split("・") + similar_keywords

        # ✅ ← この条件文がマッチの本体（ここに入れます）
        if model in message and any(kw in message for kw in all_keywords):
            price = row['修理料金']
            time = row['所要時間']
            hits.append(f"{row['機種']} の「{row['症状']}」の修理料金は {price}、修理時間は約 {time} です。")

    if len(hits) == 1:
        return hits[0]
    elif len(hits) > 1:
        return "以下の修理情報が見つかりました:\n" + "\n".join(hits)
    else:
        return "申し訳ありません。もう一度、機種名（例）：iPhone 12 や症状（例：画面割れ）を含めてお問い合わせください。"