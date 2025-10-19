import os
import json
import trimesh
import colorsys
import numpy as np

def scene2meshes(scene):
    if not isinstance(scene, trimesh.Scene):
        raise ValueError("Input must be trimesh.Scene")
    meshes = []
    geometry_nodes = scene.graph.geometry_nodes
    for name, geometry in scene.geometry.items():
        if isinstance(geometry, trimesh.Trimesh):
            if name not in geometry_nodes:
                raise ValueError(f"Transform of geometry node {name} not found")
            object_node_name = geometry_nodes[name]
            # should only have exactly one object node
            if (len(object_node_name) != 1):
                raise ValueError(f"Expected one object node for geometry node {name}")
            object_node_name = object_node_name[0]
            if object_node_name not in scene.graph:
                raise ValueError(f"Object node {object_node_name} not found")
            
            # in gltf, geometry name can be different from object node name
            # so find the object node of the geometry
            # and apply the transform of the object node to the geometry
            transform, _ = scene.graph[object_node_name]
            geometry.apply_transform(transform)
            meshes.append(geometry)
        else:
            raise ValueError("Scene must contain only trimesh.Trimesh")
    return meshes

def meshes2scene(meshes):
    scene = trimesh.Scene()
    for mesh in meshes:
        scene.add_geometry(mesh)
    return scene

def get_bbox(vertices: np.ndarray):
    min_vals = np.min(vertices, axis=0)
    max_vals = np.max(vertices, axis=0)
    return min_vals, max_vals

# normalize meshes to a fixed diagonal length
def normalize_meshes_diag(meshes: list, norm_diag_len: float = 1.0) -> tuple:
    verts_all = []
    for mesh in meshes:
        verts_all.append(np.asarray(mesh.vertices, dtype=np.float32))
    
    if len(verts_all) == 0:
        return None
    
    verts_all = np.vstack(verts_all)
    
    # calculate diag length
    bbox_min = np.min(verts_all, axis=0)
    bbox_max = np.max(verts_all, axis=0)
    diag_vec = bbox_max - bbox_min
    diag_len = float(np.linalg.norm(diag_vec))
    
    if diag_len <= 0:
        scale = norm_diag_len
    else:
        scale = norm_diag_len / diag_len
    
    # scale and shift
    verts_all_scaled = verts_all * scale
    bbox_min2 = np.min(verts_all_scaled, axis=0)
    bbox_max2 = np.max(verts_all_scaled, axis=0)
    center_after_scale = (bbox_min2 + bbox_max2) / 2.0
    shift = -center_after_scale
    
    # perform normalization
    normalized_meshes = []
    for mesh in meshes:
        new_mesh = mesh.copy()
        v = np.asarray(new_mesh.vertices, dtype=np.float32)
        v = v * scale + shift
        new_mesh.vertices = v
        normalized_meshes.append(new_mesh)
    
    return normalized_meshes, scale, shift


def normalize_meshes_max_axis(meshes: list, norm_max_axis_len: float = 1.0) -> tuple:
    verts_all = []
    for mesh in meshes:
        verts_all.append(np.asarray(mesh.vertices, dtype=np.float32))
    
    if len(verts_all) == 0:
        return None
    
    verts_all = np.vstack(verts_all)
    
    # calculate max axis
    bbox_min = np.min(verts_all, axis=0)
    bbox_max = np.max(verts_all, axis=0)
    original_max_axis = np.max(bbox_max - bbox_min)

    # scale and shift
    scale = norm_max_axis_len / original_max_axis
    verts_all_scaled = verts_all * scale
    bbox_min2 = np.min(verts_all_scaled, axis=0)
    bbox_max2 = np.max(verts_all_scaled, axis=0)
    center_after_scale = (bbox_min2 + bbox_max2) / 2.0
    shift = -center_after_scale
    
    # perform normalization
    normalized_meshes = []
    for mesh in meshes:
        new_mesh = mesh.copy()
        v = np.asarray(new_mesh.vertices, dtype=np.float32)
        v = v * scale + shift
        new_mesh.vertices = v
        normalized_meshes.append(new_mesh)
    
    return normalized_meshes, scale, shift

def generate_mask_color(num_masks):
    hues = np.linspace(0, 1, num_masks, endpoint=False)
    colors = []
    for hue in hues:
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        colors.append([r, g, b])
    colors = np.array(colors)
    return colors

def generate_pcd_mask_color(masks):
    n_masks = len(masks)
    num_points = masks[0].shape[0]
    colors = generate_mask_color(n_masks)
    part_vis_colors = np.zeros((num_points, 3))
    for i in range(n_masks):
        mask = masks[i]
        part_vis_colors[mask] = colors[i]
    return part_vis_colors