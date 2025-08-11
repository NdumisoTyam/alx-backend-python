# chats/middleware.py
from datetime import datetime
from pathlib import Path
from django.conf import settings

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Path to requests.log in project root (or override via settings.REQUEST_LOG_FILE)
        default_path = Path(settings.BASE_DIR) / "requests.log"
        self.log_file = Path(getattr(settings, "REQUEST_LOG_FILE", default_path))

    def __call__(self, request):
        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False):
            user_repr = user.get_username()
        else:
            user_repr = "AnonymousUser"

        log_line = f"{datetime.now()} - User: {user_repr} - Path: {request.path}\n"

        try:
            # Ensure parent directory exists, then append
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception:
            # Never break the request/response cycle because of logging
            pass

        return self.get_response(request)
