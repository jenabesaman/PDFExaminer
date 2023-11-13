import subprocess
import base64
import os
from flask import Flask, request, jsonify


app = Flask(__name__)
app.debug = True


@app.errorhandler(404)
def invalid_route(e):
    return jsonify({'errorCode': 404, 'message': 'Invalid Input Url'})


@app.errorhandler(400)
def invalid_route(e):
    return jsonify({'errorCode': 400, 'message': 'Bad Request,input json text is not correct'})


@app.errorhandler(500)
def invalid_route(e):
    return jsonify({'errorCode': 500, 'message': 'Internal Server Error'})


@app.route("/ping")
def ping():
    return "This is a api test only"


@app.route("/pdfexaminer", methods=["post"])
def pdfexaminer():
    try:
        data = request.get_json(force=True)
        base64_string = data["base64_string"]
        extensions=data["extensions"]
        def base64_to_file_to_php(base64_string, extensions):
            filename = f"file.{extensions}"
            with open(filename, "wb") as f:
                f.write(base64.b64decode(base64_string))
            command = f"php pdfex.php {filename}"
            result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
            return result.stdout.decode('utf-8')

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

        result = base64_to_file_to_php(base64_string=base64_string, extensions=extensions)
        return jsonify({'result': result})
    except:
        return "some unknown thing wrong"




# @app.route("/pdfexaminer", methods=["post"])
# def pdfexaminer():
#     try:
#         def base64_to_php(base64_string):
#             decoded_data = base64.b64decode(base64_string)
#             mime_type = magic.from_buffer(decoded_data, mime=True)
#             file_extension = mimetypes.guess_extension(mime_type)
#             filename = f"file{file_extension}"
#             with open(filename, "wb") as f_out:
#                 f_out.write(decoded_data)
#             command = "php pdfex.php file.pdf"
#             result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
#             return result.stdout.decode('utf-8')
#
#         os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#         data = request.get_json(force=True)
#         base64_string = data["base64_string"]
#
#         result = base64_to_php(base64_string=base64_string)
#         return jsonify({'result': result})
#     except:
#         return "some unknown thing wrong"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8536, use_reloader=False)
