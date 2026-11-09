# QR, códigos de barras y escáner Android/Python

## 1. Generación de QR en Python

Para generar códigos QR estándar en Python se puede usar `qrcode`.

### Instalación

```bash
pip install qrcode[pil] pillow
```

### QR básico y pequeño

```python
import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=2,
    border=4
)

qr.add_data("https://example.com")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_mini.png")
```

Los parámetros principales son:

- `version=1`: QR de 21 x 21 módulos, si el contenido cabe.
- `box_size`: píxeles utilizados por cada módulo.
- `border`: quiet zone alrededor del QR. El valor recomendado para QR estándar es 4 módulos.
- `ERROR_CORRECT_L`: corrección de errores baja y menor densidad cuando el contenido lo permite.

Por ejemplo, un QR Version 1 con `border=4` ocupa 29 x 29 módulos. Con `box_size=2`, la imagen será aproximadamente 58 x 58 píxeles.

---

## 2. QR con texto a la derecha usando `qrcode`

```python
import qrcode
from PIL import Image, ImageDraw, ImageFont

# Configuración
data = "123456"
texto = "SN: 123456"

QR_BOX_SIZE = 3
QR_BORDER = 4
FONT_SIZE = 16
GAP = 8

# Crear QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=QR_BOX_SIZE,
    border=QR_BORDER
)

qr.add_data(data)
qr.make(fit=True)

qr_img = qr.make_image(
    fill_color="black",
    back_color="white"
).convert("RGB")

# Fuente Windows
font = ImageFont.truetype(
    r"C:\Windows\Fonts\arial.ttf",
    FONT_SIZE
)

# Calcular dimensiones del texto
tmp = Image.new("RGB", (1, 1), "white")
draw_tmp = ImageDraw.Draw(tmp)

bbox = draw_tmp.textbbox((0, 0), texto, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# Crear imagen final
width = qr_img.width + GAP + text_width
height = max(qr_img.height, text_height)

img = Image.new("RGB", (width, height), "white")
img.paste(qr_img, (0, 0))

# Texto
draw = ImageDraw.Draw(img)
x = qr_img.width + GAP
y = (height - text_height) // 2 - bbox[1]

draw.text((x, y), texto, fill="black", font=font)

img.save("qr_texto.png")

print(f"QR: {qr_img.size}")
print(f"Imagen final: {img.size}")
```

### Error de Pillow al cargar la fuente

Si aparece:

```text
OSError: cannot open resource
```

al utilizar:

```python
ImageFont.truetype("DejaVuSans.ttf", FONT_SIZE)
```

es porque Pillow no encuentra la fuente. En Windows puede indicarse una ruta explícita:

```python
font = ImageFont.truetype(
    r"C:\Windows\Fonts\arial.ttf",
    FONT_SIZE
)
```

Para etiquetas pequeñas puede utilizarse Arial Bold:

```python
font = ImageFont.truetype(
    r"C:\Windows\Fonts\arialbd.ttf",
    FONT_SIZE
)
```

---

## 3. Micro QR

Si se necesita específicamente Micro QR, una alternativa es `Segno`:

```bash
pip install segno
```

```python
import segno

qr = segno.make("123456", micro=True)
qr.save("microqr.png", scale=4, border=2)
```

Para QR estándar se puede seguir utilizando `qrcode`.

---

## 4. Generación de códigos de barras en Python

Para códigos de barras 1D se puede usar `python-barcode`.

```bash
pip install python-barcode pillow
```

Para números de serie, `Code 128` es especialmente adecuado porque permite contenido alfanumérico y ofrece una representación relativamente compacta.

### Ejemplo Code 128

```python
from barcode import Code128
from barcode.writer import ImageWriter

serial_number = "SN12345678"

barcode = Code128(
    serial_number,
    writer=ImageWriter()
)

filename = barcode.save(
    "barcode",
    options={
        "module_width": 0.25,
        "module_height": 8.0,
        "quiet_zone": 2.0,
        "font_size": 8,
        "text_distance": 2.0,
        "write_text": True,
        "dpi": 300
    }
)

print(filename)
```

Si el texto se va a generar posteriormente con Pillow:

```python
"write_text": False
```

---

## 5. Limitar un barcode a 30 píxeles de altura

Se puede generar primero el Code128 y posteriormente redimensionarlo con Pillow.

```python
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

serial_number = "SN12345678"
MAX_HEIGHT = 30

barcode = Code128(
    serial_number,
    writer=ImageWriter()
)

filename = barcode.save(
    "barcode_tmp",
    options={
        "module_width": 0.25,
        "module_height": 8.0,
        "quiet_zone": 2.0,
        "font_size": 8,
        "text_distance": 1.0,
        "write_text": False,
        "dpi": 300
    }
)

img = Image.open(filename)

if img.height > MAX_HEIGHT:
    ratio = MAX_HEIGHT / img.height
    new_width = round(img.width * ratio)

    img = img.resize(
        (new_width, MAX_HEIGHT),
        Image.Resampling.NEAREST
    )

img = img.convert("1")
img.save("barcode.png")

print("Tamaño final:", img.size)
```

Para códigos de barras es preferible `NEAREST` frente a interpolaciones con antialiasing, ya que interesa conservar bordes limpios entre blanco y negro.

---

## 6. Lectura de QR y códigos de barras con webcam

Una primera alternativa es:

- OpenCV para capturar la webcam.
- `pyzbar` / ZBar para decodificar códigos.

Sin embargo, en Windows puede aparecer un problema como:

```text
FileNotFoundError: Could not find module
'...pyzbar\libzbar-64.dll'
```

Esto significa que `pyzbar` no puede cargar `libzbar-64.dll` o alguna de sus dependencias.

### Alternativa recomendada: ZXing-C++

Para evitar estos problemas de DLL se puede usar `zxing-cpp`:

```powershell
pip uninstall pyzbar
pip install zxing-cpp opencv-python
```

Comprobación:

```powershell
conda activate sumo310
python -m pip install zxing-cpp opencv-python
python -c "import zxingcpp; print('ZXing OK')"
```

### Lector webcam con ZXing-C++

```python
import cv2
import zxingcpp

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error leyendo la webcam")
        break

    results = zxingcpp.read_barcodes(frame)

    for result in results:
        data = result.text
        code_type = str(result.format)

        print(f"{code_type}: {data}")

        pos = result.position

        points = [
            (pos.top_left.x, pos.top_left.y),
            (pos.top_right.x, pos.top_right.y),
            (pos.bottom_right.x, pos.bottom_right.y),
            (pos.bottom_left.x, pos.bottom_left.y),
        ]

        for i in range(4):
            cv2.line(
                frame,
                points[i],
                points[(i + 1) % 4],
                (0, 255, 0),
                2
            )

        x = points[0][0]
        y = max(points[0][1] - 10, 20)

        cv2.putText(
            frame,
            f"{code_type}: {data}",
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    cv2.imshow("Barcode / QR Scanner", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

La arquitectura queda:

```text
Webcam
  -> OpenCV
  -> ZXing-C++
  -> QR / Code128 / EAN / DataMatrix / etc.
  -> contenido decodificado
```

---

## 7. Aplicación Android open source: Binary Eye

Para Android se identificó Binary Eye como una alternativa open source especialmente interesante.

Características relevantes comentadas:

- Open source.
- Sin anuncios.
- Utiliza ZXing-C++.
- Permite leer códigos QR y múltiples tipos de barcode.
- Soporta, entre otros, Code128, QR, Micro QR, Data Matrix, PDF417, Aztec, EAN, UPC, Code39 y Code93.
- Puede generar códigos.
- Puede trabajar con códigos invertidos.
- Dispone de mecanismos para enviar/reenviar las lecturas a otros sistemas.

Esto permite usar el teléfono Android como frontal de lectura y delegar el procesamiento en una aplicación Python.

---

## 8. Envío de lecturas desde Android a Python

Aunque se planteó Bluetooth, para un PC resulta especialmente sencillo utilizar HTTP sobre Wi-Fi.

La arquitectura propuesta es:

```text
Android / Binary Eye
        |
        | scan
        v
      Wi-Fi
        |
        | HTTP POST JSON
        v
   Python / Flask
        |
        +--> mostrar lectura
        +--> validar SN
        +--> MariaDB
        +--> generar etiqueta
        +--> DYMO
```

### Servidor Flask básico

Instalación:

```powershell
pip install flask
```

Servidor:

```python
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
```

Si el PC tuviese, por ejemplo, IP `192.168.1.35`, el endpoint sería:

```text
http://192.168.1.35:5000/scan
```

---

## 9. Escribir automáticamente la lectura en la posición del cursor

El servidor Python puede comportarse de forma similar a un lector USB HID: recibe el código desde Android y lo escribe en la aplicación de Windows que tenga el foco.

Para ello se puede usar `pyautogui`.

### Instalación

```powershell
pip install flask pyautogui
```

### Servidor completo

```python
from flask import Flask, request, jsonify
import pyautogui
import threading

app = Flask(__name__)

# Simular Enter después de cada lectura
SEND_ENTER = True


def escribir_en_cursor(texto):
    """Escribe el texto en la aplicación con foco de teclado."""

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
```

### Uso con Excel

Con `SEND_ENTER = True`, el flujo práctico sería:

1. Seleccionar una celda en Excel.
2. Escanear el QR/Code128 desde Android.
3. Binary Eye envía el valor al servidor Python.
4. Python escribe el contenido donde está el cursor.
5. Python simula `Enter`.
6. Excel mueve la selección a la siguiente celda.
7. Se puede escanear la siguiente etiqueta.

Por ejemplo, una lectura:

```text
SN12345678
```

se convierte de forma efectiva en:

```python
pyautogui.write("SN12345678")
pyautogui.press("enter")
```

Si no se quiere enviar Enter:

```python
SEND_ENTER = False
```

### Precaución

`pyautogui` escribe en la ventana que tenga el foco en ese momento. Si el usuario cambia de Excel a otra aplicación, el código se escribirá en esa otra aplicación. Una evolución posible sería comprobar que la aplicación esperada tiene el foco antes de escribir.

---

## 10. Arquitectura global propuesta

El conjunto permite montar un sistema sencillo de identificación y etiquetado:

```text
                  GENERACION

Python
  |
  +--> qrcode ----------> QR
  |
  +--> python-barcode --> Code128
  |
  +--> Pillow ----------> composición de etiqueta
  |
  +--> DYMO ------------> impresión


                  LECTURA

Android
Binary Eye
  |
  | QR / Code128 / DataMatrix / etc.
  v
HTTP POST
  |
  v
Python / Flask
  |
  +--> registro / validación
  +--> MariaDB
  +--> lógica aplicación
  |
  v
PyAutoGUI
  |
  v
Aplicación con foco
Excel / navegador / aplicación corporativa / etc.
```

## 11. Librerías utilizadas

| Necesidad | Librería / aplicación |
|---|---|
| Generar QR | `qrcode` |
| Generar Micro QR | `segno` |
| Componer imágenes/texto | `Pillow` |
| Generar Code128 | `python-barcode` |
| Capturar webcam | `opencv-python` |
| Decodificar QR/barcodes en Python | `zxing-cpp` |
| Servidor HTTP | `Flask` |
| Simular entrada de teclado | `pyautogui` |
| Escáner Android open source | Binary Eye |

## 12. Instalación Python conjunta

Para reunir las principales funciones del proyecto:

```powershell
pip install qrcode[pil] pillow python-barcode opencv-python zxing-cpp flask pyautogui
```

Si se utiliza Conda:

```powershell
conda activate sumo310
python -m pip install qrcode[pil] pillow python-barcode opencv-python zxing-cpp flask pyautogui
```

