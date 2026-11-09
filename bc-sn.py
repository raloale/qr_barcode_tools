from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image

serial_number = "SN12345678"

MAX_HEIGHT = 30

# Generar código de barras
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

# Abrir imagen
img = Image.open(filename)

# Reducir hasta un máximo de 30 px de altura
if img.height > MAX_HEIGHT:
    ratio = MAX_HEIGHT / img.height

    new_width = round(img.width * ratio)

    img = img.resize(
        (new_width, MAX_HEIGHT),
        Image.Resampling.LANCZOS
    )

img.save("barcode.png")

print("Tamaño final:", img.size)