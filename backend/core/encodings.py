import os
import face_recognition
import pickle

def generate_encodings(path: str) -> list:
    """Generates encodings from a photo"""
    image = face_recognition.load_image_file(path, mode='RGB')
    encodings = face_recognition.face_encodings(image)
    return encodings


def save_encoding(path: str, filename: str, encoding) -> None:
    """Saves encoding in pickle format"""
    path_file = path.replace("photo", "encoding")
    path_file += f"{filename}.pkl"
    pickle.dump(encoding, open(path_file, 'wb'))
    

def delete_encoding(path: str, filename: str) -> None:
    """Delete encoding in pickle format"""
    print("delete")
    print(filename)
    path += f"{filename}.pkl"
    print(path)
    if os.path.exists(path):
        print("existe")
        os.remove(path)