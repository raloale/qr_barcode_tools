import qrcode

qr = qrcode.QRCode(
    version=1,  # QR mínimo: 21x21 módulos
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,  # 2 píxeles por módulo
    border=4     # margen estándar recomendado
)

qr.add_data("25NECS-0001P")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_mini.png")