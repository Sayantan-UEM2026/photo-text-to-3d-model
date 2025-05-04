import cv2
import numpy as np
import open3d as o3d
import os

def extract_depth_map(image_path, save_path='output/depth_map.png'):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Failed to read image at " + image_path)

    img_blur = cv2.GaussianBlur(img, (7, 7), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_img = clahe.apply(img_blur)

    depth = contrast_img.astype(np.float32) / 255.0

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    debug_view = (depth * 255).astype(np.uint8)
    cv2.imwrite(save_path, debug_view)

    return depth

def depth_to_point_cloud(depth_map, scale=1.0, depth_scale=5.0):
    h, w = depth_map.shape
    points = []

    for y in range(h):
        for x in range(w):
            z = depth_map[y, x] * depth_scale
            points.append([x * scale, -y * scale, z]) 

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(np.array(points))
    return pcd

def point_cloud_to_mesh(pcd):
    pcd.estimate_normals()
    mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
    bbox = pcd.get_axis_aligned_bounding_box()
    mesh = mesh.crop(bbox)
    return mesh

def save_mesh(mesh, output_path='output/image3d.obj'):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    o3d.io.write_triangle_mesh(output_path, mesh)
    print(f"Saved mesh to {output_path}")

def process_image_to_3d(image_path):
    print(f"Processing image: {image_path}")
    depth = extract_depth_map(image_path)
    pcd = depth_to_point_cloud(depth)
    mesh = point_cloud_to_mesh(pcd)
    save_mesh(mesh)
    return mesh 
