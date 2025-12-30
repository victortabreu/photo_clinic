import cv2
import os
from datetime import datetime


def main():
    # Abre a câmera padrão (0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Erro: Não foi possível acessar a câmera.")
        return

    print("Câmera iniciada com sucesso.")
    print("Pressione:")
    print("  [ESPACO] para capturar a foto")
    print("  [ESC] para sair")

    # Cria pasta para salvar fotos
    os.makedirs("photos", exist_ok=True)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Erro ao capturar frame da câmera.")
            break

        cv2.imshow("Camera - Photo Clinic", frame)

        key = cv2.waitKey(1) & 0xFF

        # ESC para sair
        if key == 27:
            break

        # ESPAÇO para capturar foto
        if key == 32:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photos/photo_{timestamp}.jpg"

            cv2.imwrite(filename, frame)
            print(f"Foto salva: {filename}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
