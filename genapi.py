import logging
import sys

#remove later
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class genApiHandler:

    def __init__(self, db_connection, api_conf):

        self.db_connection = db_connection
        self.api_conf = api_conf
        self.logger = logging.getLogger(__name__)
        

    def format_api_response(self, status_code: int, status_message: str):
        return {"statusCode": status_code, "body": status_message}

    def handle_request(self, request_type: str, request_name: str, request_body: dict):
        """
        This function handles any type of request and then calls the appropriate flow.
        request_type should be one of GET,POST or PUT, request_name should be any of the endpoint in the conf file
        and request_body is the content of the request
        """

        if 'request_name' not in self.api_conf:
            return self.format_api_response(404, f"The endpoint \"{request_name}\" does not exist.")
        
        if request_type == 'GET':
            return self.handle_get(request_name, request_body)
        
    def handle_get(self, request_name, request_body):

        """
        Validates and then handle get requests
        """

        template = self.api_conf[request_name]

        if 'filters' not in request_body:
            return self.format_api_response(500, f"Wrong query format: \"filters\" not provided.") 
        
        if 'fields' not in request_body:
            return self.format_api_response(500, f"Wrong query format: \"fields\" not provided.") 
        
        page_size = request_body['page_size'] if 'page_size' in request_body else 50

        #Check if the user asked for inexistent fields
        inexistent_fields = [v for v in request_body['filters'] if v not in template['fields']]
        if len(inexistent_fields) > 0:
            return self.format_api_response(500, f"Invalid fields asked: {','.join(inexistent_fields)}") 
        
        for query_block in request_body['filters']:
            for query in 

        




