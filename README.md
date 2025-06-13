# Calendar Sync

This project provides a simple FastAPI service for authenticating with and syncing calendar events between Google, Outlook (Microsoft), and Apple calendars. It is intended as a starting point for further development.

## Running locally

1. Install the requirements:
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

Environment variables for API credentials can be configured in `docker-compose.yml` or using a `.env` file.

The service stores OAuth tokens in a local SQLite database (`calendar_sync.db` by
default). You can change the location by setting the `DATABASE_URL` environment
variable.

