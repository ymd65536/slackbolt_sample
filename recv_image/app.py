from datetime import datetime
import os
import requests

from slack_bolt import App, Ack
from slack_bolt.adapter.socket_mode import SocketModeHandler

# GCSにファイルを保存するのでGCSのClientを利用
from google.cloud import storage

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.preview.language_models import TextGenerationModel

project_id = os.environ.get("PROJECT_ID", "")
APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")
PORT = os.environ.get("PORT", 8080)
app = App(
    token=SLACK_BOT_TOKEN,
    process_before_response=True
)


def generate(image: Part, file_name: str):
    vertexai.init(project=project_id, location="asia-northeast1")
    responses = GenerativeModel("gemini-1.0-pro-vision-001").generate_content(
        [image, """画像に含まれているテキストを抜き出してください。"""],
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        }
    )

    if responses.candidates:
        response_text = responses.candidates[0].text

        check_prompt = """
質問:以下の情報に含まれてはいけないテキストはありますか？回答は回答方法に従って答えてください。
{}
---
含まれてはいけないテキスト
- メールアドレス
- 会社と名のつくもの
- 個人を特定できる名前
- backlog
---
出力形式
「含まれている」または「含まれていない」のいずれかでお願いします。
含まれている場合は含まれているテキストを抜き出してください。
        """.format(response_text)
        generation_model = TextGenerationModel.from_pretrained(
            'text-bison@002')
        answer = generation_model.predict(
            check_prompt,
            temperature=0.2, max_output_tokens=1024,
            top_k=40, top_p=0.8).text

        res = f"Answer: {answer}\nFile Name:{file_name}"

    else:
        res = "No response:{file_name}"

    return res


def download_from_slack(download_url: str, auth: str):
    """Slackから画像をダウンロードする

    Args:
        download_url (str): 画像のURL
        auth (str): 画像の閲覧に必要なSlackの認証キー

    Returns:
        binary:
    """
    if download_url is None:
        return None

    img_data = requests.get(
        download_url,
        allow_redirects=True,
        headers={"Authorization": f"Bearer {auth}"},
        stream=True,
    ).content

    if len(img_data) > 0:
        return img_data
    else:
        return 0


# @app.event("app_mention")
def handle_mention(event, say):
    print("handle_mention")
    files = event.get('files', [])

    if not files:
        thread_id = event['ts']
        say('画像が添付されていません！', thread_ts=thread_id)
    else:
        file_count = len(files)
        thread_id = event['ts']
        say(f"画像を{file_count}枚受信しました", thread_ts=thread_id)

        for file in files:
            mime_type = file.get('mimetype', None)
            download_file = file.get('url_private_download', None)
            upload_file_name = file.get('name', None)
            image = download_from_slack(download_file, SLACK_BOT_TOKEN)

            if "thread_ts" in event:
                thread_id = event['thread_ts']

            if image is None or not mime_type == "image/png":
                say(f"画像リンクから画像が読み取れませんでした。{upload_file_name}", thread_ts=thread_id)
            else:
                # Slackに送ったファイルを保存しておくバケット名
                bucket_name = os.environ.get("BUCKET_NAME", "")
                storage_client = storage.Client()
                bucket = storage_client.bucket(bucket_name)

                filename = f"slack_{upload_file_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                blob = bucket.blob(filename)
                blob.upload_from_string(image, content_type="image/png")

                gcs_file_name = f"gs://{bucket_name}/{filename}"

                res = generate(Part.from_uri(
                    gcs_file_name, mime_type="image/png"),
                    upload_file_name
                )
                say(res, thread_ts=thread_id)

    say("チェック終了！", thread_ts=thread_id)


def slack_ack(ack: Ack):
    ack()


app.event("app_mention")(ack=slack_ack, lazy=[handle_mention])


# アプリを起動します
if __name__ == "__main__":
    if APP_ENVIRONMENT == "prod":
        app.start(port=int(PORT))
    else:
        print("SocketModeHandler")
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
