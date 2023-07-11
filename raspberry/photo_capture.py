import cv2
import time

from config import POTHO_PATH, TIME_TO_TAKE_PHOTO

def show_and_capture():
    """Display webcam video and capture photo."""
    cap = cv2.VideoCapture(0)

    time_start = time.time()
    time_end = time.time()

    while True:
        ret, frame = cap.read()
        if frame is None:
            continue

        time_end = time.time()

        height, width, _ = frame.shape
        message = "Fique olhando para a camera e espere alguns segundos"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
        x = 10
        y = height - text_size[1] - 10

        cv2.rectangle(frame, (x - 4, y - 4), (x + text_size[0] + 4, y + text_size[1] + 4), (0, 0, 0), -1)
        cv2.putText(frame, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.imshow("Webcam", frame)

        if (time_end - time_start) >= TIME_TO_TAKE_PHOTO:
            cv2.imwrite(POTHO_PATH, frame)
            cap.release()
            cv2.destroyAllWindows()
            break

def show_photo_and_get_response(keyboard):
    """Display captured photo and get response."""
    img = cv2.imread(POTHO_PATH)
    height, width, _ = img.shape
    message = "Essa foto ficou boa? Aperte 2 para continuar ou 3 para tirar outra foto."
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    thickness = 1
    text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
    x = 10
    y = height - text_size[1] - 10

    cv2.rectangle(img, (x - 4, y - 4), (x + text_size[0] + 4, y + text_size[1] + 4), (0, 0, 0), -1)
    cv2.putText(img, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    cv2.imshow("Captured Photo", img)

    while True:
        key2 = cv2.waitKey(1)
        key = keyboard.get_key()
        print("Opção escolhida:", key)
        return key


def main(keyboard):
    """Main function."""
    show_and_capture()
    response = show_photo_and_get_response(keybord)

    if response == "2":
        print("Foto aceita!")

    elif response == "3":
        print("Tirando outra foto...")
        main()

if __name__ == '__main__':
    main()
