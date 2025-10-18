import trimesh

class PartNeXtObject:
    def __init__(self, glb_id, mesh, mesh_face_num, masks, hierarchyList):
        self.glb_id = glb_id
        self.mesh = mesh
        self.mesh_face_num = mesh_face_num
        self.masks = masks
        self.hierarchyList = hierarchyList

    def visualize(self):
        self.mesh.show()

    def get_mesh(self):
        return self.mesh

    def normalize_mesh(self):
        return self.mesh