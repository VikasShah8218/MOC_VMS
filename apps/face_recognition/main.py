import argparse
import torch
from scripts import (
    store_features_in_db,   #sotre in db    Kam Ka Function
    find_top_similar_faces, # find top similar img
    webcam_face_finding, # 
    webcam_face_registration, #
    webcam_RegAndFind,
    FACE_MODEL_PATH,  # change with req
    load_pretrained_model # load pre trained models
)


def main():
    parser = argparse.ArgumentParser(description="Face recognition database operations")
    parser.add_argument("--reg", action="store_true", help="Store features in database from image")
    parser.add_argument("--person_name", help="person name")
    parser.add_argument("--img_path", help="Path to the image data")
    parser.add_argument("--webcam_frs", action="store_true", help="Register and recognition face via webcam and store in database")
    parser.add_argument("--webcam_find", action="store_true", help="Run face recognition on webcam feed")
    parser.add_argument("--webcam_reg", action="store_true", help="Register face via webcam and store in database")
    parser.add_argument("--find", action="store_true", help="Find similar faces in database")
    parser.add_argument("--db_path", default="face_features.db", help="Path to the database")
    parser.add_argument("--input_image", help="Path to the input image for finding similar faces")
    args = parser.parse_args()

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
     

    print(f"Using device: {device}")

    # Validate input paths
    if args.reg and (not args.img_path or not args.person_name):
        print("Error: --img_path and --person_name is required when using --reg")
        return

    if args.find and not args.input_image:
        print("Error: --input_image is required when using --find")
        return

    # Load model once
    model = load_pretrained_model('ir_101', device)

    if args.reg:
        print("Storing features in database from image...")
        store_features_in_db(args.db_path, args.img_path, args.person_name, device)

    elif args.find:
        print("Finding similar faces in database...")
        find_top_similar_faces(args.input_image, args.db_path, model, device, topK=5)

    elif args.webcam_reg:
        print("Registering face via webcam...")
        webcam_face_registration(args.db_path, model, device, FACE_MODEL_PATH)

    elif args.webcam_find:
        print("Running face recognition on webcam feed...")
        webcam_face_finding(args.db_path, model, device, FACE_MODEL_PATH)

    elif args.webcam_frs:
        print("Registering and recognizing face via webcam...")
        webcam_RegAndFind(args.db_path, model, device, FACE_MODEL_PATH)

    else:
        print("Please specify at least one action: --reg, --find, --webcam_find, --webcam_reg, or --webcam_frs")

if __name__ == "__main__":
    main()