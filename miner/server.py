from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import advancedMiner as Miner

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/text/<text>")
@cross_origin()
def process_text(text):
    return jsonify(Miner.process_text(text))


@app.route("/wiki/<text>")
@cross_origin()
def wiki_search(text):
    return jsonify(Miner.wiki_lookup(text))


if __name__ == "__main__":
    app.run()
