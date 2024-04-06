default_status_code = 500
default_message = 'Failed to process your request, an error occurred inside the application'


class APIException(Exception):

    def __init__(self, message=None, status_code=None, error=None):
        super().__init__()
        self.error = error
        self.message = message
        if self.message is None:
            self.message = default_message
        self.status_code = status_code
        if status_code is None:
            self.status_code = default_status_code

    def to_dict(self):
        response = dict(())
        if self.error is None:
            response["message"] = self.message
        else:
            response['message'] = self.message + ": " + str(self.error)
        response['status_code'] = self.status_code
        return response
