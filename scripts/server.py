from flask import Flask, request, jsonify, make_response

import bids_convert

app = Flask(__name__)

@app.route("/convert", methods = ['POST'])
def convert():
    try:
        data = request.get_json()
        bids_convert.convert(data)
    except Exception as e:
        print (e)
        return (e)
    else:
        return make_response(jsonify(data), 200)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4001)
