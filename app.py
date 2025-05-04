import argparse
from image_to_3d import process_image_to_3d
from text_to_3d import process_text_to_3d
from visualize import visualize_mesh

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', help='Path to image file')
    parser.add_argument('--text', help='Text prompt input')
    args = parser.parse_args()

    if args.image:
        mesh = process_image_to_3d(args.image)
        visualize_mesh(mesh)
    elif args.text:
        mesh = process_text_to_3d(args.text)
        visualize_mesh(mesh)
    else:
        print("Please provide --image or --text")

if __name__ == "__main__":
    main()

