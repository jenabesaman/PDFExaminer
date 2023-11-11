import subprocess
import base64
import io
from flask import Flask, request, jsonify, Response
app = Flask(__name__)
app.debug = True
import os




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
        def base64_to_pdf_command(base64_string):
            decoded = base64.b64decode(base64_string)
            command = "php pdfex.php file.pdf"
            if decoded[0:4] != b'%PDF':
                raise ValueError('Input is not a PDF')
            with open('file.pdf', 'wb') as f:
                f.write(decoded)
            result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
            return result.stdout.decode('utf-8')

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        data = request.get_json(force=True)
        base64_string = data["base64_string"]

        result = base64_to_pdf_command(base64_string=base64_string)
        return jsonify({'result': result})
    except:
        return "cant predict"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8536, use_reloader=False)