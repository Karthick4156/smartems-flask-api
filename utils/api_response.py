def success_response(message="", data=None):
    return {
        "success": True,
        "message": message,
        "data": data,
        "errors": []
    }, 200

def error_response(message="", errors=None, status=400):
    return {
        "success": False,
        "message": message,
        "data": None,
        "errors": errors or []
    }, status