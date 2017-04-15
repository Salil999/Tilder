from flask import Flask
from flask_cors import CORS, cross_origin
import miner.advancedMiner as Miner

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/<text>")
@cross_origin()
def process_text(text):
    return Miner.process_text(text)

if __name__ == "__main__":
    app.run()