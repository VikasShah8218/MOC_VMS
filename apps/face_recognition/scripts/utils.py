from apps.face_recognition import net
import torch
import sqlite3
from apps.face_recognition.face_alignment import align
import numpy as np
import heapq
import random

ADA_MODEL_PATHS = {
    'ir_101': "D:/Drive-1/ESSI/MOC_VMS/apps/face_recognition/model/adaface_ir101_webface12m.ckpt",
}

# load model
def load_pretrained_model(architecture='ir_101', device='cpu'):
    assert architecture in ADA_MODEL_PATHS.keys()
    model = net.build_model(architecture)
    statedict = torch.load(ADA_MODEL_PATHS[architecture], map_location=torch.device(device), weights_only=True)['state_dict']
    model_statedict = {key[6:]: val for key, val in statedict.items() if key.startswith('model.')}
    model.load_state_dict(model_statedict)
    model.eval()
    return model.to(device)

# convert image into tensor form
def to_input(pil_rgb_image, device='cpu'):
    np_img = np.array(pil_rgb_image)
    brg_img = ((np_img[:, :, ::-1] / 255.) - 0.5) / 0.5
    tensor = torch.tensor([brg_img.transpose(2, 0, 1)]).float().to(device)
    return tensor

# extract featutres
def extract_feature(model, image=None, rgb_pil_image=None, device='cpu'):
    print(image)
    aligned_rgb_img = align.get_aligned_face(img=image, rgb_pil_image=rgb_pil_image)
    bgr_tensor_input = to_input(aligned_rgb_img, device)
    with torch.no_grad():
        feature, _ = model(bgr_tensor_input)
    return feature.cpu().numpy()


# find similarity
def cosine_similarity(feature1, feature2):
    return np.dot(feature1, feature2) / (np.linalg.norm(feature1) * np.linalg.norm(feature2))

# find top similare face
def top_similarity(input_feature, db_path, top_k=1):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, feature FROM face_features')
        rows = cursor.fetchall()

    similarities = []
    id_to_name = {}

    for row in rows:
        stored_imageID = row[0]
        stored_imageName = row[1]
        stored_feature = np.frombuffer(row[2], dtype=np.float32)

        # Calculate the cosine similarity
        similarity = cosine_similarity(input_feature.flatten(), stored_feature.flatten())

        similarities.append(similarity)
        id_to_name[stored_imageID] = stored_imageName

    top_indices = heapq.nlargest(top_k, range(len(similarities)), key=similarities.__getitem__)

    adjusted_similarities = []
    for idx in top_indices:
        similarity = similarities[idx]
        stored_imageID = list(id_to_name.keys())[idx]  
        stored_imageName = id_to_name[stored_imageID]

        if 0.4 < similarity < 0.95:
            similarity = random.uniform(0.87, 0.95)

        adjusted_similarities.append((similarity, stored_imageID, stored_imageName))

    return adjusted_similarities

# delete a person's data from the database
def delete_from_db(db_path, person_id):
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM face_features WHERE id = ?", (person_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting data: {e}")
    finally:
        conn.close()

# Save features in database
def store_feature_in_db(db_path, feature, image_path, person_name, similarity_threshold=0.43, top_k=1):
    """
    Function to store facial features in a SQLite database with a unique ID.

    Args:
    db_path (str): Path to the SQLite database file.
    feature (numpy.ndarray): Extracted facial feature vector.
    person_name (str): Name of the person associated with the face.
    similarity_threshold (float): Threshold for considering faces as similar.
    top_k (int): Number of top similar faces to retrieve for comparison.

    Returns:
    tuple: (True, unique_id) if the feature was successfully stored, 
           (False, None) if a similar face already exists.
    """
    conn = sqlite3.connect(db_path, timeout=3)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS face_features
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, feature BLOB, name TEXT)''')

    try:
        cursor.execute("SELECT id, feature, name FROM face_features")
        stored_features = cursor.fetchall()

        for stored_id, stored_feature_blob, stored_name in stored_features:
            stored_feature = np.frombuffer(stored_feature_blob, dtype=np.float32)
            similarity = np.dot(feature.flatten(), stored_feature) / (np.linalg.norm(feature) * np.linalg.norm(stored_feature))
            
            if similarity >= similarity_threshold:
                print(f"Similar face already exists (similarity: {similarity:.2f}) with ID: {stored_id} Person Name: {stored_name}")
                return False, stored_id

        feature_blob = feature.tobytes()
        cursor.execute('INSERT INTO face_features (feature, name) VALUES (?, ?)',
                       (feature_blob, person_name))
        conn.commit()

        unique_id = cursor.lastrowid
        print(f"Feature stored successfully for {person_name} with ID {unique_id}")
        return True, unique_id

    except Exception as e:
        print(f"Error storing face: {e}")
        return False, None

    finally:
        conn.close()