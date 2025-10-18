from datasets import load_from_disk
import trimesh

def load_annotation(ann_dir: str):
    """Load PartNeXt annotation"""
    return load_from_disk(ann_dir)

def load_glb(glb_path: str):
    """Load PartNeXt glb data"""
    return trimesh.load(glb_path)
