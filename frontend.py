import json
import os
import logging
from flask import Flask, request, jsonify
from flask.logging import create_logger
from push import mainPush

app = Flask(__name__)
LOG = create_logger(app)

# Create logging, log key value if wanted
script_dir = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=f'{script_dir}\\filename.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    return jsonify({'name': 'knox',
                    'email': 'knox@knoxsdata.com',
                    'locale': 'https://youtube.com/c/dataknox'})


@app.route('/ios', methods=['POST'])
def iosPost():
    try:
        message = json.loads(request.data)
        print(f"{message['hostname']} has issue {message['messages']}")
        new_mess = f"{message['hostname']} has issue {message['messages']}"
        LOG.info(f'inbound record {message}')
        r = mainPush(new_mess)
        LOG.info(f"Pushed {r.text}")
        logging.info(f"Pushed {r.text}")
        return jsonify(r.text), 201
    except Exception as err:
        return jsonify({"error":err}),500
        print(err)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
