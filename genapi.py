import logging
import sys
import uuid
import datetime

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

        if request_name not in self.api_conf:
            return self.format_api_response(404, f"The endpoint \"{request_name}\" does not exist.")
        
        if request_type == 'GET':
            return self.handle_get(request_name, request_body)
        
    def check_format_value(self, field_name: str, field_value, fields_obj: dict):

        field_type = fields_obj[field_name]

        try:
            if field_type == 'integer':
                return int(field_value)
            elif field_type == 'float':
                return float(field_value)
            elif field_type == 'varchar':
                return str(field_value)
            elif field_type == 'datetime':
                return datetime.datetime.strptime(field_value,'%Y-%m-%dT%H:%M:%S').strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
                
    def handle_get(self, request_name: str, request_body: dict):

        """
        Validates and then handle get requests
        """

        template = self.api_conf[request_name]

        if 'filters' not in request_body:
            return self.format_api_response(500, f"Wrong query format: \"filters\" not provided.") 
        
        if 'fields' not in request_body:
            return self.format_api_response(500, f"Wrong query format: \"fields\" not provided.") 
        
        try:
            page_size = int(request_body['page_size']) if 'page_size' in request_body and int(request_body['page_size']) <= 50 else 50

            if page_size < 0:
                raise ValueError("Invalid page size number")

        except ValueError:
            return self.format_api_response(500, f"Invalid page size provided: \"{request_body['page_size']}\".")  

        try:
            page = int(request_body['page']) if 'page' in request_body else 0

            if page < 0:
                raise ValueError("Invalid page number")
            
        except ValueError:
            return self.format_api_response(500, f"Invalid page size provided: \"{request_body['page_size']}\".")  
        
        queries_and = []
        query_values = []
        i = 0

        for field in request_body['fields']:
            if field not in template['fields']:
                return self.format_api_response(500, f"Field does not exist: \"{field}\".")

        for query_block in request_body['filters']:
            query_or = []
            j = 0
            for key,value in query_block.items():

                if key not in template['fields']:
                    return self.format_api_response(500, f"Invalid field provided: \"{key}\".")  

                formatted_value = self.check_format_value(key, value, template['fields'])

                if not formatted_value:
                    return self.format_api_response(500, f"Invalid value provided of type \"{template['fields'][key]}\" for field \"{key}\": {value}") 
                
                query_or.append(f"{key} = ?")
                query_values.append(formatted_value)
                j += 1

            queries_and.append('(' + ' AND '.join(query_or) + ')')
            i += 1
        
        query_where = ' OR '.join(queries_and)

        cursor = self.db_connection.cursor()
        print(query_values)
        print(f"SELECT {','.join(request_body['fields'])} FROM {template['table_name']} WHERE " + query_where)
        cursor.execute(f"SELECT {','.join(request_body['fields'])} FROM {template['table_name']} WHERE " + query_where, query_values)

        return_body =  []

        result_query = cursor.fetchall() or []
        print(f"result query: {result_query}")

        for element in result_query:
            data_element = {}
            for i in range(len(request_body['fields'])):
                data_element[request_body['fields'][i]] = element[i]
            return_body.append(data_element)
            
        print(f"Response: {return_body}")


        




