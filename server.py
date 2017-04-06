from flask import Flask
import miner.advancedMiner as Miner

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()

# print(Miner.process_text("Hello World"))