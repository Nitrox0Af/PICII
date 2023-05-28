import face_recognition
import pickle

def generate_encodings(path: str) -> list:
    """Generates encodings from a photo"""
    image = face_recognition.load_image_file(path, mode='RGB')
    encodings = face_recognition.face_encodings(image)
    return encodings


def save_encoding(path: str, filename: str, encoding):
    """Saves encoding in pickle format"""
    path_file = path.replace("photo", "encoding")
    path_file += f"{filename}.pkl"
    pickle.dump(encoding, open(path_file, 'wb'))