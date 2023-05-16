import os
import time
import numpy as np
import cv2
import face_recognition
import pickle

def main():
    known_faces_dir = "known_faces"
    known_faces = save_encodings_dict(known_faces_dir)
    recognize_unknown(known_faces, tolerance=0.6)

def save_encodings_dict(known_faces_dir: str) -> dict:
    """Runs through all folders and images to save the generated encodings"""
    known_faces = {}

    print(f"Looping through all folders in {known_faces_dir} folder")
    for person_identifier in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_identifier)
        if not os.path.isdir(person_dir):
            print(f"The item {person_dir} is not a valid directory.")
            continue

    known_faces[person_identifier] = []
    
    for filename in os.listdir(person_dir):
        encodings = generate_encodings(os.path.join(person_dir, filename))
        if len(encodings) == 0:
            print(f"No faces found in image {filename}")
            continue
        encoding = encodings[0]
        save_encoding(person_dir, filename, encoding)
        known_faces[person_identifier].append(encoding)
    return known_faces

def generate_encodings(path: str) -> list:
    """Generates encodings from a photo"""
    image = face_recognition.load_image_file(path, mode='RGB')
    encodings = face_recognition.face_encodings(image)
    return encodings

def save_encoding(path: str, filename: str, encoding):
    """Saves encoding in pickle format"""
    path_file = path.replace("known_faces", "encodings")
    if not os.path.exists(path_file):
        os.makedirs(path_file)
    path_file += f"/{filename}.pkl"
    pickle.dump(encoding, open(path_file, 'wb'))

def load_encoding(path: str, filename: str):
    """Loads encoding from pickle format"""
    path_file = path.replace("known_faces", "encodings") + f"/{filename}.pkl"
    encoding = pickle.load(open(path_file, 'rb'))
    return encoding

def recognize_unknown(known_faces: dict, tolerance: float = 0.6):
    """Takes a photo and recognizes the unknown person"""
    while True:
        print("Take the picture of the unknown person")
        img_name = "unknown_face/data.png"
        key = input()
        key = "COMP"
        if key == "ESC":
            print("EXIT")
            break

        elif key == "COMP":
            cam = cv2.VideoCapture(0)
            num = 5
            print("Look at the camera")
            print("Taking foto in:")
            while num > 0:
                print(num)
                time.sleep(1)
                num -= 1
            ret,frame = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imwrite(img_name,frame)
            cam.release()

            unknown_face_encodings = generate_encodings(img_name)
            print("Cycling through all face encodings in unknown image")
            for unknown_face_encoding in unknown_face_encodings:
                found_match = False

                for identifier, face_encodings in known_faces.items():
                    matches = face_recognition.compare_faces(face_encodings, unknown_face_encoding, tolerance=tolerance)
                    if True in matches:
                        found_match = True
                        print(f"This is the image of {identifier}!")
                        average_distance = np.average(face_recognition.face_distance(face_encodings, unknown_face_encoding))
                        print(f"Has an average distance of {round(average_distance, 3)}")
                        break

                if not found_match:
                    print("This person is not recognized")
            print("Press ESC to exit or COMP to take photo")

        else:
            print("Invalid command")
            print("Press ESC to exit or COMP to take photo")


if __name__ == "__main__":
    main()