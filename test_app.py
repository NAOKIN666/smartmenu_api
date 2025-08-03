from fastapi import FastAPI, Request

# FastAPIのインスタンスを作成
app = FastAPI()

# シンプルなテスト用エンドポイント
@app.post("/callback")
async def simple_callback(request: Request):
    # このprint文が表示されるかどうかが重要
    print("🎉🎉🎉 テスト用の/callbackが呼び出されました！ 🎉🎉🎉")
    
    # リクエストのボディを読み取って表示
    body = await request.body()
    print(f"受信したデータ: {body.decode()}")
    
    # 正常な応答を返す
    return {"status": "ok", "message": "Test received successfully"}
