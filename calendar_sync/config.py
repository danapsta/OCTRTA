from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    # Default to a public client ID for device code flow if none provided
    outlook_client_id: str = os.getenv(
        "OUTLOOK_CLIENT_ID", "04f0c124-f2bc-4f3b-90c3-817a96fd19c6"
    )
    outlook_client_secret: str = os.getenv("OUTLOOK_CLIENT_SECRET", "")
    app_env: str = os.getenv("APP_ENV", "development")
    apple_caldav_url: str = os.getenv("APPLE_CALDAV_URL", "")
    apple_username: str = os.getenv("APPLE_USERNAME", "")
    apple_password: str = os.getenv("APPLE_PASSWORD", "")

settings = Settings()
