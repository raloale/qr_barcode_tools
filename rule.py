from PIL import Image, ImageDraw, ImageFont

# =========================================
# Configuración
# =========================================

DPI = 300

WIDTH_MM = 57
HEIGHT_MM = 32

OUTPUT = "dymo_regla.png"

# =========================================
# Conversión mm -> pixels
# =========================================

def mm_to_px(mm):
    return round(mm * DPI / 25.4)


WIDTH = mm_to_px(WIDTH_MM)
HEIGHT = mm_to_px(HEIGHT_MM)

print(f"Tamaño imagen: {WIDTH} x {HEIGHT} px")

# =========================================
# Crear imagen
# =========================================

img = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    "white"
)

draw = ImageDraw.Draw(img)

# Fuente Windows
font = ImageFont.truetype(
    r"C:\Windows\Fonts\arial.ttf",
    14
)

# =========================================
# Regla horizontal
# =========================================

Y_RULE = mm_to_px(6)

draw.line(
    (0, Y_RULE, WIDTH - 1, Y_RULE),
    fill="black",
    width=1
)

for mm in range(WIDTH_MM + 1):

    x = mm_to_px(mm)

    if mm % 10 == 0:
        tick = mm_to_px(4)
    elif mm % 5 == 0:
        tick = mm_to_px(3)
    else:
        tick = mm_to_px(2)

    draw.line(
        (x, Y_RULE, x, Y_RULE - tick),
        fill="black",
        width=1
    )

    # numeración cada 10 mm
    if mm % 10 == 0:
        draw.text(
            (x + 2, Y_RULE + 2),
            str(mm),
            fill="black",
            font=font
        )


# =========================================
# Regla vertical
# =========================================

X_RULE = mm_to_px(8)

draw.line(
    (X_RULE, 0, X_RULE, HEIGHT - 1),
    fill="black",
    width=1
)

for mm in range(HEIGHT_MM + 1):

    y = mm_to_px(mm)

    if mm % 10 == 0:
        tick = mm_to_px(4)
    elif mm % 5 == 0:
        tick = mm_to_px(3)
    else:
        tick = mm_to_px(2)

    draw.line(
        (X_RULE, y, X_RULE - tick, y),
        fill="black",
        width=1
    )

    # numeración cada 10 mm
    if mm % 10 == 0:
        draw.text(
            (X_RULE + 3, y),
            str(mm),
            fill="black",
            font=font
        )


# =========================================
# Borde de referencia
# =========================================

draw.rectangle(
    (0, 0, WIDTH - 1, HEIGHT - 1),
    outline="black",
    width=1
)

# =========================================
# Marca central
# =========================================

cx = WIDTH // 2
cy = HEIGHT // 2

cross = mm_to_px(2)

draw.line(
    (cx - cross, cy, cx + cross, cy),
    fill="black"
)

draw.line(
    (cx, cy - cross, cx, cy + cross),
    fill="black"
)

# =========================================
# Guardar con información DPI
# =========================================

img.save(
    OUTPUT,
    dpi=(DPI, DPI)
)

print(f"Generado: {OUTPUT}")
print(f"Dimensiones físicas: {WIDTH_MM} x {HEIGHT_MM} mm")
print(f"Resolución: {DPI} DPI")
