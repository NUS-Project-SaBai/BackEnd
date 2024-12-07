import requests
from sabaibiometrics.settings import TELEGRAM_API_TOKEN, TELEGRAM_CHAT_ID

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        msg = None
        if request.method != "GET":
            msg = f"{request.method} {request.path} {request.body}"

        response = self.get_response(request)

        if (msg):
            if response.status_code != 200:
                msg+=f"\n\nError:\n{response.content}"
            reply_url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"    
            data = {"chat_id": TELEGRAM_CHAT_ID, "message_thread_id":357, "text": msg.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp")}
            requests.post(reply_url, data=data)

        # Code to be executed for each request/response after
        # the view is called.

        return response