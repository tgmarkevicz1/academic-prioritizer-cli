# academic-prioritizer-cli

A command-line tool that integrates with Google Tasks, Calendar, and Drive to surface what you should be working on right now.

## How it works

- **Google Tasks** are the primary work items — deadlines drive the score
- **Google Calendar events** (meetings, classes) are shown below tasks with their time
- **Google Drive files** are correlated to tasks via fuzzy name matching and boost a task's score when a related file is found
- Completed tasks are automatically skipped

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable: **Google Drive API**, **Google Calendar API**, **Google Tasks API**
3. Create OAuth 2.0 credentials (Desktop app) and download as `secrets/credentials.json`

### 3. Environment variables

Create a `.env` file:

```env
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
GOOGLE_CREDENTIALS_PATH=secrets/credentials.json
GOOGLE_TOKEN_PATH=token.json
```

### 4. First run / re-authentication

> ⚠️ If you have an existing `token.json`, delete it before running. The Google Tasks scope was added and your old token will not include it.

```bash
rm token.json
python -m src.main
```

## Usage

```bash
# Normal run
python -m src.main

# Hide an item permanently by ID
python -m src.main --hide <id>
python -m src.main -ht <id>

# Unhide an item
python -m src.main --unhide <id>
python -m src.main -uh <id>

# See all hidden items
python -m src.main --list-hidden
```

## Interactive commands

- Type a **number** to select an item
- In the item sub-menu: **`h`** to hide permanently, **`b`** to go back
- **`q`** to quit

## Scoring

| Situation | Points |
|---|---|
| Task due today | +15 |
| Task due in N days | +max(0, 15-N) |
| Task has no due date | -2 |
| Matched Drive file found | +3 per match (max 2) |
| Calendar event | anchored below all tasks |
