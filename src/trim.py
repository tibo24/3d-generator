import trimesh

# Load the SVG
def load_svg_as_mesh(path, height) -> trimesh.Trimesh:
    svg = trimesh.load(path)

    # If it's a Path2D, turn into polygons first
    if isinstance(svg, trimesh.path.Path2D):
        # Get a list of 2D polygons (usually only 1)
        polygons = svg.polygons_full
    else:
        # If load() gave a Scene, get the first Path2D
        if isinstance(svg, trimesh.Scene):
            paths = [g for g in svg.graph.nodes_geometry.values()
                    if isinstance(svg.geometry[g], trimesh.path.Path2D)]
            if not paths:
                raise ValueError("No Path2D geometry found in SVG.")
            path = svg.geometry[paths[0]]
            polygons = path.polygons_full
        else:
            raise ValueError("Unsupported SVG load type: " + str(type(svg)))

    # Extrude polygons by height 5
    meshes = []
    for poly in polygons:
        m = trimesh.creation.extrude_polygon(poly, height)
        meshes.append(m)

    # If multiple polygons, combine
    mesh: trimesh.Trimesh
    if len(meshes) == 1:
        mesh = meshes[0]
    else:
        mesh = trimesh.util.concatenate(meshes)
        
    return mesh

def load_stl_as_mesh(path) -> trimesh.Trimesh:
    mesh = trimesh.load(path)
    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Loaded STL is not a Trimesh object.")
    return mesh

def create_stempel(svg_path, height = 50.0) -> trimesh.Trimesh:
    mesh_stempel = load_stl_as_mesh('assets/stempel.stl')
    print(svg_path)
    mesh_top = load_svg_as_mesh(svg_path, height)
    mesh_top.apply_scale(0.075)
    mesh_top.apply_translation([-30, -30, 35])

    mesh = trimesh.util.concatenate([mesh_stempel, mesh_top])
    return mesh
    # Visualize
    # mesh.show()
