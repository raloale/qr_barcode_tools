from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    print("Nueva lectura")
    print("--------------")
    print("Contenido :", data.get("content"))
    print("Formato   :", data.get("format"))
    print("Raw       :", data.get("raw"))
    print("Scan ID   :", data.get("scanId"))
    print()

    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
