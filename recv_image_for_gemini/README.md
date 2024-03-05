# Memo

## how to use

Set Envrioment Variables.

```bash
export PROJECT_ID=google_project_id
export BUCKET_NAME=image_bucket
export SLACK_BOT_TOKEN=xoxb-XXXXX
export SLACK_APP_TOKEN=xapp-XXXXX
```

## abount SLACK_BOT_TOKEN and SLACK_APP_TOKEN

- SLACK_BOT_TOKEN: Bot User OAuth Access Token
- SLACK_APP_TOKEN: OAuth Access Token

Slack Page

- [Slack | Slack App](https://api.slack.com/apps)

You get SLACK_BOT_TOKEN from "OAuth & Permissions" page.
Bot Token Scopes for SLACK_BOT_TOKEN is chat:write, files:read, app_mentions:read.

You get SLACK_APP_TOKEN from "Basic Information" page.
Applicaiton Scope for SLACK_APP_TOKEN is connections:write.

## attension

- Event Subscription is required
  - Set `Enable Events` to `On`
- When Scope is changed, you need to reinstall the app.
