import open3d as o3d

def visualize_mesh(mesh):
    print("Opening interactive 3D visualizer...")

    if not mesh.has_triangles() or not mesh.has_vertices():
        print("Mesh is empty or invalid.")
        return

    mesh.compute_vertex_normals()

    o3d.visualization.draw_geometries(
        [mesh],
        window_name="3D Mesh Viewer",
        width=800,
        height=600,
        mesh_show_back_face=True
    )

