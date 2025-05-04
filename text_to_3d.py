import open3d as o3d
import os

def process_text_to_3d(prompt):
    prompt = prompt.lower()
    print(f"Received prompt: {prompt}")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    mesh = None

    if "ball" in prompt:
        print("Creating sphere for 'ball'")
        mesh = o3d.geometry.TriangleMesh.create_sphere(radius=0.5)
        mesh.paint_uniform_color([1.0, 0.1, 0.1])

    elif "car" in prompt:
        print("Creating mock car")
        body = o3d.geometry.TriangleMesh.create_box(width=2.0, height=0.5, depth=1.0)
        body.translate([-1.0, 0, -0.5])
        body.paint_uniform_color([0.2, 0.2, 0.8])

        wheels = []
        for dx in [-0.8, 0.8]:
            for dz in [-0.4, 0.4]:
                wheel = o3d.geometry.TriangleMesh.create_sphere(radius=0.2)
                wheel.translate([dx, -0.3, dz])
                wheel.paint_uniform_color([0.1, 0.1, 0.1])
                wheels.append(wheel)

        mesh = body
        for wheel in wheels:
            mesh += wheel

    elif "box" in prompt or "cube" in prompt:
        print("Creating cube")
        mesh = o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
        mesh.paint_uniform_color([0.6, 0.6, 0.6])

    elif "cylinder" in prompt:
        print("Creating cylinder")
        mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=0.4, height=1.2)
        mesh.paint_uniform_color([0.5, 0.2, 0.8])

    elif "cone" in prompt:
        print("Creating cone")
        mesh = o3d.geometry.TriangleMesh.create_cone(radius=0.5, height=1.0)
        mesh.paint_uniform_color([0.9, 0.5, 0.2])

    elif "bottle" in prompt:
        print("Creating bottle (tall cylinder)")
        mesh = o3d.geometry.TriangleMesh.create_cylinder(radius=0.3, height=1.5)
        mesh.paint_uniform_color([0.1, 0.6, 1.0])

    elif "pyramid" in prompt:
        print("Creating pyramid")
        mesh = create_pyramid()

    elif "chair" in prompt:
        print("Creating simple chair")
        mesh = create_chair()

    else:
        print("No known shape keyword found. Using default cube.")
        mesh = o3d.geometry.TriangleMesh.create_box(width=1.0, height=1.0, depth=1.0)
        mesh.paint_uniform_color([0.5, 0.5, 0.5])

    mesh.compute_vertex_normals()

    output_path = os.path.join(output_dir, "text_placeholder.stl")
    o3d.io.write_triangle_mesh(output_path, mesh)

    print(f"3D model saved to {output_path}")
    return mesh


def create_pyramid():
 
    vertices = [
        [0, 0, 0],    
        [1, 0, 0],   
        [1, 0, 1],   
        [0, 0, 1],   
        [0.5, 1, 0.5] 
    ]
    triangles = [
        [0, 1, 4],
        [1, 2, 4],
        [2, 3, 4],
        [3, 0, 4],
        [0, 1, 2],  
        [2, 3, 0]     
    ]
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)
    mesh.paint_uniform_color([0.9, 0.7, 0.2])
    return mesh


def create_chair():
    parts = []

    seat = o3d.geometry.TriangleMesh.create_box(1.0, 0.2, 1.0).translate([0, 0.5, 0])
    seat.paint_uniform_color([0.6, 0.3, 0.1])
    parts.append(seat)

    back = o3d.geometry.TriangleMesh.create_box(1.0, 1.0, 0.2).translate([0, 0.7, -0.4])
    back.paint_uniform_color([0.4, 0.2, 0.1])
    parts.append(back)

    for x in [-0.4, 0.4]:
        for z in [-0.4, 0.4]:
            leg = o3d.geometry.TriangleMesh.create_box(0.1, 0.5, 0.1).translate([x, 0, z])
            leg.paint_uniform_color([0.2, 0.2, 0.2])
            parts.append(leg)

    chair = parts[0]
    for part in parts[1:]:
        chair += part

    return chair
