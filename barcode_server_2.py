from flask import Flask, request, jsonify
import pyautogui
import threading

app = Flask(__name__)

# Si quieres simular ENTER después de cada lectura
SEND_ENTER = True


def escribir_en_cursor(texto):
    """
    Escribe el texto en la aplicación que tenga actualmente
    el foco de teclado.
    """
    pyautogui.write(texto, interval=0.01)

    if SEND_ENTER:
        pyautogui.press("enter")


@app.route("/scan", methods=["POST"])
def scan():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "status": "ERROR",
            "message": "JSON no recibido"
        }), 400

    content = data.get("content", "")
    barcode_format = data.get("format", "")
    scan_id = data.get("scanId", "")

    if not content:
        return jsonify({
            "status": "ERROR",
            "message": "Codigo vacio"
        }), 400

    print(
        f"Recibido: {content} "
        f"[{barcode_format}] "
        f"scanId={scan_id}"
    )

    # Ejecutarlo aparte permite contestar inmediatamente
    # al callback HTTP
    threading.Thread(
        target=escribir_en_cursor,
        args=(content,),
        daemon=True
    ).start()

    return jsonify({
        "status": "OK"
    }), 200


if __name__ == "__main__":

    print("Servidor esperando lecturas...")
    print("Endpoint: http://0.0.0.0:5000/scan")

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )

    