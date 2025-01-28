import hou
import json
import os
import time

selected_nodes = hou.selectedNodes()
if not selected_nodes:
    raise Exception("No nodes selected. Please select a node.")

selected_node = selected_nodes[0]
input_node = selected_node.input(0)

if input_node is None:
    raise Exception("No input connected. Please connect a node with keyframes to the input.")

data_point_name = f"Locatie_{int(time.time())}"
input_node.setName(data_point_name)

obj_lvl = hou.node("/obj")
geo_node = obj_lvl.createNode("geo", node_name=f"geo_{data_point_name}")
obj_merge_ingeo = geo_node.createNode("object_merge")

obj_merge_ingeo.parm("objpath1").set(input_node.path())
obj_merge_ingeo.parm("xformtype").set(1)

rop_alembic_node = obj_merge_ingeo.createOutputNode("rop_alembic")
rop_alembic_node.parm("trange").set(1) 
rop_alembic_node.parm("filename").set(f"$HIP/Axisfile_{data_point_name}.abc")

rop_alembic_node.render()

# ===========================================================================================================
# JSON Export Function
# ===========================================================================================================

def export_transforms_to_json(output_file):
    selected_node = hou.selectedNodes()[0]
    input_node = selected_node.input(0)
    
    if input_node is None:
        print("No input node connected.")
        return
    
    start_frame, end_frame = hou.playbar.frameRange()
    start_frame = int(start_frame)
    end_frame = int(end_frame)
    
    data = {}
    
    for frame in range(start_frame, end_frame + 1):
        hou.setFrame(frame)
        transform = input_node.worldTransform()
        
        translate = list(transform.extractTranslates())
        rotate = list(transform.extractRotates())
        scale = list(transform.extractScales())
        
        data[frame] = {
            "translate": translate,
            "rotate": rotate,
            "scale": scale
        }
    
    with open(output_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    print(f"Transforms exported to {output_file}")

output_dir = hou.getenv('HIP')
if output_dir is None:
    output_dir = "/tmp"  

output_file = os.path.join(output_dir, f"{data_point_name}.json")
export_transforms_to_json(output_file)

geo_node.layoutChildren()
