# Slack Bolt for Python Memo

Simple Slack bot using slack_bolt

## SetUp

```bash
pip install slack_bolt
```

## Usage

Socket mode enabled bot.
environment variables are required before running the bot.

```bash
export SLACK_BOT_TOKEN=your-bot-token
export SLACK_APP_TOKEN=your-app-token
```

Socket mode disabled bot.
environment variables are required before running the bot.

```bash
export SLACK_SIGNING_SECRET=your-signing-secret
```

## reference

- [slack_bolt](https://slack.dev/bolt-python/tutorial/getting-started)

## Visual Studio Code Debug Configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        }
    ]
}
```
