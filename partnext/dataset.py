import os
from partnext.io import load_annotation, load_glb
from partnext.object import PartNeXtObject

class PartNeXtDataset:
    def __init__(self, glb_dir: str, ann_dir: str):
        self.glb_dir = glb_dir
        self.ann_dir = ann_dir
        self.annotation = load_annotation(ann_dir)
        # construct glbid 2 annotation
        self.index = {row["model_id"]: row for row in self.annotation}

    def get_num_object(self) -> int:
        return self.annotation.num_rows
    
    def get_object_ids(self) -> list:
        return self.annotation["model_id"]

    def load_object(self, glb_id: str) -> PartNeXtObject:
        row = self.index.get(glb_id)
        if row is None:
            print(f"[Warn] GLB ID not found {glb_id}")
            return None
        glb_path = os.path.join(self.glb_dir, row["model_id"], row["type_id"] + ".glb")
        if not os.path.exists(glb_path):
            print(f"[Warn] GLB file not found {glb_path}")
            return None
        mesh = load_glb(glb_path)
        mesh_face_num = row["mesh_face_num"]
        masks = row["masks"]
        hierarchyList = row["hierarchyList"]
        return PartNeXtObject(glb_id, mesh, mesh_face_num, masks, hierarchyList)