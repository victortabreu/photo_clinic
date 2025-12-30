import cv2
import time

PREVIEW = 0
COUNTDOWN = 1
REVIEW = 2


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro: câmera não encontrada")
        return

    state = PREVIEW
    captured_frame = None

    countdown_start = None
    countdown_seconds = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display_frame = frame.copy()

        if state == PREVIEW:
            cv2.putText(
                display_frame,
                "Pressione ESPACO para tirar a foto",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        elif state == COUNTDOWN:
            elapsed = time.time() - countdown_start
            remaining = countdown_seconds - int(elapsed)

            if remaining > 0:
                text = f"Foto em {remaining}"

                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 3
                thickness = 5

                (text_width, text_height), _ = cv2.getTextSize(
                    text, font, font_scale, thickness
                )

                h, w, _ = display_frame.shape
                x = (w - text_width) // 2
                y = (h + text_height) // 2

                cv2.putText(
                    display_frame,
                    text,
                    (x, y),
                    font,
                    font_scale,
                    (0, 0, 255),
                    thickness,
                    cv2.LINE_AA,
                )
            else:
                captured_frame = frame.copy()
                state = REVIEW


        elif state == REVIEW:
            display_frame = captured_frame.copy()
            cv2.putText(
                display_frame,
                "A: Aceitar | R: Refazer",
                (30, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2,
            )

        cv2.imshow("Photo Clinic", display_frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break

        if state == PREVIEW and key == 32:  # ESPACO
            state = COUNTDOWN
            countdown_start = time.time()

        elif state == REVIEW:
            if key == ord("a"):
                filename = f"foto_{int(time.time())}.jpg"
                cv2.imwrite(filename, captured_frame)
                print(f"Foto salva: {filename}")
                state = PREVIEW

            elif key == ord("r"):
                state = PREVIEW

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
