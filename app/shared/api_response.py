def api_response(data=None, success=True, error=None):
    return {
        "success": success,
        "data": data if success else None,
        "error": error if not success else None,
    }
