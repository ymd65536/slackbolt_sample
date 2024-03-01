import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")
PORT = os.environ.get("PORT", 8080)

app = App(token=SLACK_BOT_TOKEN)


@app.event("app_mention")
def handle_mention(event, say):
    print("handle_mention")
    query = "test"
    say(query)


# アプリを起動します
if __name__ == "__main__":
    if APP_ENVIRONMENT == "prod":
        app.start(port=int(PORT))
    else:
        print("SocketModeHandler")
        SocketModeHandler(app, SLACK_APP_TOKEN).start()
