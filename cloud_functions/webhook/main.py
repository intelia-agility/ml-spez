import functions_framework
import os

@functions_framework.http
def webhook(request):
    request_json = request.get_json(silent=True)
    print(request_json)
    return 'OK'