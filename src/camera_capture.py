import cv2
import os
import time
from datetime import datetime


COUNTDOWN_SECONDS = 3


def draw_countdown(frame, seconds_left):
    overlay = frame.copy()
    text = str(seconds_left)

    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 4
    thickness = 8
    color = (0, 0, 255)

    text_size = cv2.getTextSize(text, font, scale, thickness)[0]
    x = (frame.shape[1] - text_size[0]) // 2
    y = (frame.shape[0] + text_size[1]) // 2

    cv2.putText(overlay, text, (x, y), font, scale, color, thickness)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    os.makedirs("photos", exist_ok=True)

    print("Câmera iniciada.")
    print("[ESPAÇO] iniciar contagem")
    print("[ESC] sair")

    countdown_active = False
    countdown_start_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()

        if countdown_active:
            elapsed = now - countdown_start_time
            remaining = COUNTDOWN_SECONDS - int(elapsed)

            if remaining > 0:
                draw_countdown(frame, remaining)
            else:
                # Captura foto
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"photos/photo_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Foto salva: {filename}")
                countdown_active = False

        cv2.imshow("Camera - Photo Clinic", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break

        if key == 32 and not countdown_active:
            countdown_active = True
            countdown_start_time = now

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
