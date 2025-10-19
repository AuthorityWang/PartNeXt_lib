from datasets import load_from_disk
import ast
import trimesh

def load_annotation(ann_dir: str):
    """Load PartNeXt annotation"""
    return load_from_disk(ann_dir)

def load_glb(glb_path: str):
    """Load PartNeXt glb data"""
    return trimesh.load(glb_path, force='scene')

def parse_str(str: str):
    """Parse string in annotation to data"""
    return ast.literal_eval(str)