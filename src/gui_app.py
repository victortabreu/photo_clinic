import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
import time


# ================= CONFIGURAÇÕES =================
PREVIEW_WIDTH = 960
PREVIEW_HEIGHT = 540
PHOTO_DIR = "photos"
JPEG_QUALITY = 95
COUNTDOWN_SECONDS = 3

PREVIEW = 0
COUNTDOWN = 1
REVIEW = 2
# =================================================


class PhotoClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Clinic")

        os.makedirs(PHOTO_DIR, exist_ok=True)

        self.state = PREVIEW
        self.countdown_start = None

        # ===== VIDEO FRAME =====
        self.video_frame = tk.Frame(root, bg="black")
        self.video_frame.pack(padx=10, pady=10)

        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack()

        # ===== CONTROLS FRAME =====
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(pady=10)

        self.info_label = tk.Label(
            self.controls_frame,
            text="Posicione-se e clique em CAPTURAR",
            font=("Arial", 14)
        )
        self.info_label.pack(pady=5)

        self.capture_button = tk.Button(
            self.controls_frame,
            text="CAPTURAR",
            font=("Arial", 14),
            width=20,
            command=self.start_countdown
        )
        self.capture_button.pack()

        self.accept_button = tk.Button(
            self.controls_frame,
            text="ACEITAR",
            font=("Arial", 14),
            width=20,
            command=self.accept_photo
        )

        self.retry_button = tk.Button(
            self.controls_frame,
            text="REFAZER",
            font=("Arial", 14),
            width=20,
            command=self.retry_photo
        )

        # ===== CAMERA =====
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Erro: câmera não encontrada")

        # Preview rápido
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


        actual_w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Câmera ativa em {actual_w}x{actual_h}")

        self.full_frame = None
        self.captured_frame = None

        self.update_frame()

    # ================= UTIL =================
    def resize_with_aspect_ratio(self, image, max_width, max_height):
        h, w = image.shape[:2]
        scale = min(max_width / w, max_height / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # ================= LOOP =================
    def update_frame(self):
        if self.state != REVIEW:
            ret, frame = self.cap.read()
            if not ret:
                return
            self.full_frame = frame.copy()
        else:
            frame = self.captured_frame

        display = cv2.flip(frame, 1)  # espelha horizontalmente (efeito espelho)

        if self.state == COUNTDOWN:
            elapsed = time.time() - self.countdown_start
            remaining = COUNTDOWN_SECONDS - int(elapsed)

            if remaining > 0:
                cv2.putText(
                    display,
                    str(remaining),
                    (display.shape[1] // 2 - 50, display.shape[0] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    5,
                    (0, 0, 255),
                    8,
                    cv2.LINE_AA
                )
            else:
                self.captured_frame = frame.copy()
                self.state = REVIEW
                self.show_review_controls()

        preview = self.resize_with_aspect_ratio(
            display, PREVIEW_WIDTH, PREVIEW_HEIGHT
        )

        canvas = Image.new("RGB", (PREVIEW_WIDTH, PREVIEW_HEIGHT), (0, 0, 0))
        preview_rgb = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)
        preview_img = Image.fromarray(preview_rgb)

        x = (PREVIEW_WIDTH - preview_img.width) // 2
        y = (PREVIEW_HEIGHT - preview_img.height) // 2
        canvas.paste(preview_img, (x, y))

        imgtk = ImageTk.PhotoImage(image=canvas)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(15, self.update_frame)

    # ================= AÇÕES =================
    def start_countdown(self):
        if self.state != PREVIEW:
            return
        self.state = COUNTDOWN
        self.countdown_start = time.time()
        self.info_label.config(text="Prepare-se...")

    def show_review_controls(self):
        self.capture_button.pack_forget()
        self.accept_button.pack(pady=5)
        self.retry_button.pack(pady=5)
        self.info_label.config(text="Aceitar ou refazer a foto?")

    def accept_photo(self):
        filename = f"foto_{int(time.time())}.jpg"
        path = os.path.join(PHOTO_DIR, filename)

        cv2.imwrite(
            path,
            self.captured_frame,
            [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
        )

        print("Foto salva:", path)
        self.reset_to_preview()

    def retry_photo(self):
        self.reset_to_preview()

    def reset_to_preview(self):
        self.state = PREVIEW
        self.captured_frame = None
        self.accept_button.pack_forget()
        self.retry_button.pack_forget()
        self.capture_button.pack()
        self.info_label.config(text="Posicione-se e clique em CAPTURAR")

    # ================= FINAL =================
    def on_close(self):
        self.cap.release()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = PhotoClinicApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
