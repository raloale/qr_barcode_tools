import qrcode
from PIL import Image, ImageDraw, ImageFont

# -------------------------
# Configuración
# -------------------------
data = "25NECS-0001P"
texto = "SN: 25NECS-0001P"

QR_BOX_SIZE = 1
QR_BORDER = 2
FONT_SIZE = 16
GAP = 8

# -------------------------
# Crear QR
# -------------------------
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

# -------------------------
# Fuente
# -------------------------
font = ImageFont.truetype(
    r"C:\Windows\Fonts\arial.ttf",
    FONT_SIZE
)

# Calcular dimensiones del texto
tmp = Image.new("RGB", (1, 1), "white")
draw_tmp = ImageDraw.Draw(tmp)

bbox = draw_tmp.textbbox(
    (0, 0),
    texto,
    font=font
)

text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

# -------------------------
# Crear imagen final
# -------------------------
width = qr_img.width + GAP + text_width
height = max(qr_img.height, text_height)

img = Image.new(
    "RGB",
    (width, height),
    "white"
)

# QR a la izquierda
img.paste(qr_img, (0, 0))

# -------------------------
# Texto a la derecha
# -------------------------
draw = ImageDraw.Draw(img)

x = qr_img.width + GAP
y = (height - text_height) // 2 - bbox[1]

draw.text(
    (x, y),
    texto,
    fill="black",
    font=font
)

# -------------------------
# Guardar
# -------------------------
img.save("qr_texto.png")

print(f"Tamaño QR: {qr_img.size}")
print(f"Tamaño final: {img.size}")