import os
import time
import subprocess

import numpy as np
# import cv2
import face_recognition
import pickle

import requests
import json


OWNER = "00000000000"

def main():
    known_faces_dir = "./encoding/"
    known_faces = save_encodings_dict(known_faces_dir)
    recognize_unknown(known_faces, tolerance=0.6)


def save_encodings_dict(known_faces_dir: str) -> dict:
    """Runs through all folders and images to save the generated encodings"""
    known_faces = {}
    for filename in os.listdir(known_faces_dir):
        encoding = load_encoding(known_faces_dir, filename)
        person_identifier = filename.split("--")[0]
        if person_identifier not in known_faces:
            known_faces[person_identifier] = []
        known_faces[person_identifier].append(encoding)
    return known_faces


def generate_encodings(path: str) -> list:
    """Generates encodings from a photo"""
    image = face_recognition.load_image_file(path, mode='RGB')
    encodings = face_recognition.face_encodings(image)
    return encodings


def load_encoding(path: str, filename: str):
    """Loads encoding from pickle format"""
    encoding = pickle.load(open(path+filename, 'rb'))
    print(encoding)
    print(type(encoding))
    # encoding = pickle.load(encoding)
    return encoding


def recognize_unknown(known_faces: dict, tolerance: float = 0.6):
    """Takes a photo and recognizes the unknown person"""
    while True:
        print("Take the picture of the unknown person")
        img_name = "unknown_face/data.jpg"
        # key = input()
        key = "COMP"
        if key == "ESC":
            print("EXIT")
            break

        elif key == "COMP":
            # cam = cv2.VideoCapture(0)
            # num = 5
            # print("Look at the camera")
            # print("Taking foto in:")
            # while num > 0:
            #     print(num)
            #     time.sleep(1)
            #     num -= 1
            # ret,frame = cam.read()
            # if not ret:
            #     print("Failed to grab frame")
            #     break
            # cv2.imwrite(img_name,frame)
            # cam.release()

            unknown_face_encodings = generate_encodings(img_name)
            if len(unknown_face_encodings) == 0:
                print(f"No faces found in image!")
                return False
            
            print("Cycling through all face encodings in unknown image")
            for unknown_face_encoding in unknown_face_encodings:
                found_match = False

                for identifier, face_encodings in known_faces.items():
                    matches = face_recognition.compare_faces(face_encodings, unknown_face_encoding, tolerance=tolerance)

                    if np.any(matches):
                        found_match = True
                        if identifier == OWNER:
                            identifier = "Você"
                        else:
                            guest = get_guest(identifier)
                            identifier = guest["name"]
                        print(f"This is the image of {identifier}!")
                        average_distance = np.average(face_recognition.face_distance(face_encodings, unknown_face_encoding))
                        print(f"Has an average distance of {round(average_distance, 3)}")

                        print("Opening Telegram Bot")
                        run_telegram_bot(identifier)
                        break

                if not found_match:
                    print("This person is not recognized")

                    print("Opening Telegram Bot")
                    run_telegram_bot("unknown")

            print("Press ESC to exit or COMP to take photo")

        else:
            print("Invalid command")
            print("Press ESC to exit or COMP to take photo")

def get_guest(identifier):
    """Get the guest's infos from the server"""
    url = "http://127.0.0.1:8000/guest/json/{identifier}/" 
    print(identifier)

    response = requests.get(url)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print("Falha ao obter informações do guest.")

    return False


def run_telegram_bot(person):
    """RunS Telegram Bot to send the photo of the person you want to enter. Ask the owner if you can open the gate or not"""
    command = ["python", "telegram_bot.py", person]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 1:
        print("Abrir Portão")
    elif result.returncode == 2:
        print("Manter Portão Fechado")
    else:
        print("Error:")
        print(result.stderr)


if __name__ == "__main__":
    main()
