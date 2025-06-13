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

## Obtaining OAuth credentials

### Google

1. Visit [Google Cloud Console](https://console.cloud.google.com/) and create or select a project.
2. Enable the **Google Calendar API** for that project.
3. Under **APIs & Services > Credentials** choose **Create credentials > OAuth client ID**.
4. Select **Web application** and add `http://localhost:8000/google/callback` as an authorized redirect URI.
5. After creating the client, copy the **Client ID** and **Client secret** into your `.env` file as `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.

### Outlook (Microsoft)

1. Open the [Azure Portal](https://portal.azure.com/) and navigate to **Azure Active Directory > App registrations**.
2. Register a new application and include `http://localhost:8000/outlook/callback` as a redirect URI.
3. Once the app is created, note the **Application (client) ID** and generate a **Client secret** under **Certificates & secrets**.
4. In **API permissions**, add the delegated permission `Calendars.ReadWrite` for Microsoft Graph.
5. Set these values in your `.env` file as `OUTLOOK_CLIENT_ID` and `OUTLOOK_CLIENT_SECRET`.

## Using Apple Calendar

Apple Calendar integration uses CalDAV. Create an app-specific password from <https://appleid.apple.com/> and set the following variables in your `.env` file:

- `APPLE_CALDAV_URL` – typically `https://caldav.icloud.com/`
- `APPLE_USERNAME` – your Apple ID email address
- `APPLE_PASSWORD` – the generated app-specific password

With these configured, you can call the `/apple/events` endpoint to list events from your calendar.

The same variables can also be configured in `docker-compose.yml` when running with Docker.


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

