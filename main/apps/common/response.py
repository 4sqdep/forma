from rest_framework.response import Response



class BaseResponse(Response):
    """Base response structure to ensure consistency across API responses."""
    
    def __init__(self, data=None, status_code=200, message=None, **kwargs):
        response_data = {
            "status_code": status_code,
            "message": message if message else None,  
            "data": data
        }
        if response_data["message"] is None:
            del response_data["message"]
        super().__init__(response_data, status=status_code, **kwargs)


class PostResponse(BaseResponse):
    """Response for successful POST (creation) operations."""
    
    def __init__(self, data=None, status_code=201, message="Created", add_suffix=True, **kwargs):
        final_message = f"{message} Successfully created!" if add_suffix else message
        super().__init__(data, status_code, final_message, **kwargs)


class ListResponse(BaseResponse):
    """Response for listing data (GET requests)."""
    
    def __init__(self, data=None, status_code=200, message=None, **kwargs):
        super().__init__(data, status_code, message, **kwargs)


class PutResponse(BaseResponse):
    """Response for successful PUT (update) operations."""

    def __init__(self, data=None, status_code=200, message="Updated", **kwargs):
        final_message = f"{message} Successfully updated!"
        super().__init__(data, status_code, final_message, **kwargs)


class DestroyResponse(BaseResponse):
    """Response for successful DELETE operations."""
    
    def __init__(self, status_code=204, message="Deleted", **kwargs):
        final_message = f"{message} Successfully deleted!"
        super().__init__(None, status_code, final_message, **kwargs)


class ErrorResponse(BaseResponse):
    """Response for errors (e.g., validation, authentication, etc.)."""
    
    def __init__(self, message="An error occurred", status_code=400, errors=None, **kwargs):
        data = {"errors": errors} if errors else None
        super().__init__(data, status_code, message, **kwargs)
