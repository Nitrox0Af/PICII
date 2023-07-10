import cv2
import time

from config import POTHO_PATH

def show_and_capture():
    """Display webcam video and capture photo."""
    cap = cv2.VideoCapture(0)
    flag = 0
    while True:
        ret, frame = cap.read()
        if frame is None:
            continue

        height, width, _ = frame.shape
        message = "Approach within 40cm and press A"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1
        text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
        x = 10
        y = height - text_size[1] - 10

        cv2.rectangle(frame, (x - 4, y - 4), (x + text_size[0] + 4, y + text_size[1] + 4), (0, 0, 0), -1)
        cv2.putText(frame, message, (x, y + text_size[1]), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        cv2.imshow("Webcam", frame)

        key = cv2.waitKey(1)
        # key2 = get_char(R1, ["1", "2", "3", "A"])

        if key == ord('2'): #or (dist < 40 and key2 == "A"):
            cv2.imwrite("foto.jpg", frame)
            cap.release()
            cv2.destroyAllWindows()
            break

def show_photo_and_get_response():
    """Display captured photo and get response."""
    img = cv2.imread(POTHO_PATH)
    height, width, _ = img.shape
    message = "Press A to continue the process or B to capture another photo"
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
        key = cv2.waitKey(1)
        # key2 = get_char(R1, ["1", "2", "3", "A"])

        if key == ord('2'): #or key2 == "A":
            cv2.destroyAllWindows()
            return "continue"

        # key2 = get_char(R2, ["4", "5", "6", "B"])

        if key == ord('1') or key == ord('2'): #or key2 == "B":
            cv2.destroyAllWindows()
            return "capture another photo"

def main():
    while True:
        print("\nSelect an option:")
        print("1. Take photo and display")
        print("2. Show photo and get response")
        print("3. Quit")

        option = input("Selected option: ")

        if option == "1":
            show_and_capture()

        elif option == "2":
            response = show_photo_and_get_response()
            print("Response obtained:", response)

        elif option == "3":
            break

        else:
            print("Invalid option. Please enter a valid option number.")

if __name__ == '__main__':
    main()
