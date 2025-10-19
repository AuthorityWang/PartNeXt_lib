import trimesh
from partnext.utils import scene2meshes, meshes2scene, normalize_meshes_diag, normalize_meshes_max_axis

class PartNeXtObject:
    def __init__(self, glb_id, mesh, masks, hierarchyList):
        self.glb_id = glb_id
        self.geometry_list = scene2meshes(mesh)
        self.mesh = meshes2scene(self.geometry_list)
        self.masks = masks
        self.hierarchyList = hierarchyList

    def visualize(self):
        self.mesh.show()

    def get_mesh(self):
        return self.mesh
    
    def get_hierarchy(self):
        return self.hierarchyList

    def normalize_diag(self, norm_diag_len: float = 1.0):
        self.geometry_list, scale, shift = normalize_meshes_diag(self.geometry_list, norm_diag_len)
        self.mesh = meshes2scene(self.geometry_list)
        return self.mesh, scale, shift

    def normalize_max_axis(self, norm_max_axis_len: float = 1.0):
        self.geometry_list, scale, shift = normalize_meshes_max_axis(self.geometry_list, norm_max_axis_len)
        self.mesh = meshes2scene(self.geometry_list)
        return self.mesh, scale, shift
    
    def get_all_parts(self):
        all_parts = {}
        for part_id in self.masks:
            part_meshes = []
            for mesh_idx in self.masks[part_id]:
                part_meshes.append(self.geometry_list[int(mesh_idx)].submesh([self.masks[part_id][mesh_idx]], append = True))

            part_mesh = trimesh.util.concatenate(part_meshes)
            all_parts[part_id] = part_mesh
        return all_parts