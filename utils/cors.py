from bottle import response, request

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, function, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.set_header('Access-Control-Allow-Origin','*')
            response.set_header('Access-Control-Allow-Methods','GET, POST, PUT, OPTIONS')
            response.set_header('Access-Control-Allow-Headers','Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token, Access-Control-Allow-Origin')

            if request.method == 'OPTIONS':
                return
            return function(*args, **kwargs)

        return _enable_cors
