# Calendar Sync

This project provides a simple FastAPI service for authenticating with and syncing calendar events between Google, Outlook (Microsoft), and Apple calendars. It is intended as a starting point for further development.

## Running locally

1. Install the requirements (run this again whenever `requirements.txt` changes):
   ```bash
   pip install -r requirements.txt
   ```
2. Start the API with uvicorn:
   ```bash
   uvicorn calendar_sync.app.main:app --reload
   ```

You can also use Docker:

```bash
docker-compose up --build
```

Environment variables for API credentials **must** be set before using the authentication routes.
You can create a `.env` file by copying `.env.example` and filling in your credentials:

```bash
cp .env.example .env
# then edit .env and provide real OAuth values
```

The same variables can also be configured in `docker-compose.yml` when running with Docker.

For Apple Calendar access you need CalDAV credentials:

- `APPLE_CALDAV_URL` - Base CalDAV URL (e.g. `https://caldav.icloud.com/`)
- `APPLE_USERNAME` - Your Apple ID
- `APPLE_PASSWORD` - App-specific password for CalDAV access

The service stores OAuth tokens in a local SQLite database (`calendar_sync.db` by
default). You can change the location by setting the `DATABASE_URL` environment
variable.

## Troubleshooting

### `ModuleNotFoundError: No module named 'sqlalchemy'`

If you see this error when starting the server, it usually means the
dependencies haven't been installed since `requirements.txt` was updated.
Run the following command inside your virtual environment to ensure all
packages are available:

```bash
pip install -r requirements.txt
```

