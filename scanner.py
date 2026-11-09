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

    # ZXing funciona directamente sobre la imagen
    results = zxingcpp.read_barcodes(frame)

    for result in results:

        data = result.text
        code_type = str(result.format)

        print(f"{code_type}: {data}")

        # Obtener las cuatro esquinas
        pos = result.position

        points = [
            (pos.top_left.x, pos.top_left.y),
            (pos.top_right.x, pos.top_right.y),
            (pos.bottom_right.x, pos.bottom_right.y),
            (pos.bottom_left.x, pos.bottom_left.y),
        ]

        # Dibujar contorno
        for i in range(4):
            cv2.line(
                frame,
                points[i],
                points[(i + 1) % 4],
                (0, 255, 0),
                2
            )

        # Texto
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
