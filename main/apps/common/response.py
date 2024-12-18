from rest_framework.response import Response



class PostResponse(Response):
    def __init__(self, data=None, status_code=None, message=None, add_suffix=True, **kwargs):
        final_message = f"{message} Successfully created!" if add_suffix else message
        response_data = {
            'status_code': status_code,
            'message': final_message,
            'data': data
        }
        super().__init__(response_data, **kwargs)



class ListResponse(Response):
    def __init__(self, data=None, message="", status_code=None, **kwargs):
        response_data = {
            'status_code': status_code,
            'message': message if message else None,  
            'data': data
        }
        if response_data["message"] is None:
            del response_data["message"]
        super().__init__(response_data, **kwargs)


class PutResponse(Response):
    def __init__(self, data=None, status_code=None, message=None, **kwargs):
        data = {'status_code': status_code, 'message': f"{message} Successfully updated!", 'data': data}
        super().__init__(data, **kwargs)



class DestroyResponse(Response):
    def __init__(self, status_code=None, message=None, **kwargs):
        data = {'status_code': status_code, 'message': f"{message} Successfully deleted!"}
        super().__init__(data, **kwargs)