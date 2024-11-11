from apps.face_recognition.scripts.utils import extract_feature, top_similarity

def find_top_similar_faces(image_path, db_path, model, device='cpu', topK=5):
    try:
        input_feature = extract_feature(model, image_path=image_path, device=device)
        top_similar = top_similarity(input_feature, db_path, top_k=topK)
        print(f"Top {len(top_similar)} similar faces for {image_path}:")
        for similarity, imageID, imageName in top_similar:
            print(f"ID: {imageID}, Name: {imageName}, Similarity: {similarity:.4f}")

        return top_similar

    except Exception as e:
        print(f"An error occurred while finding similar faces: {str(e)}")
        return []