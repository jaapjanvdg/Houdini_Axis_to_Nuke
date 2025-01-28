import nuke
import json
import os

def create_file_dialog():
    p = nuke.Panel("Choose JSON File Location")
    
    p.addFilenameSearch("File Location", "")
    
    if p.show():
        file_location = p.value("File Location")
        
        apply_json_data(file_location)
        
        find_and_apply_abc(file_location)
        
    else:
        nuke.message("No file location selected.")
        return None

def apply_json_data(json_file_path):
    try:
        axis_node = nuke.createNode('Axis3')

        with open(json_file_path) as file:
            data = json.load(file)

        axis_node['translate'].setAnimated()
        axis_node['rotate'].setAnimated()
        axis_node['scaling'].setAnimated()

        for key, transform in data.items():
            frame = int(key)

            translate = transform["translate"]
            rotate = transform["rotate"]
            scale = transform["scale"]

            axis_node['translate'].setValueAt(translate[0], frame, 0)  # X
            axis_node['translate'].setValueAt(translate[1], frame, 1)  # Y
            axis_node['translate'].setValueAt(translate[2], frame, 2)  # Z

            axis_node['rotate'].setValueAt(rotate[0], frame, 0)  # X
            axis_node['rotate'].setValueAt(rotate[1], frame, 1)  # Y
            axis_node['rotate'].setValueAt(rotate[2], frame, 2)  # Z

            axis_node['scaling'].setValueAt(scale[0], frame, 0)  # X
            axis_node['scaling'].setValueAt(scale[1], frame, 1)  # Y
            axis_node['scaling'].setValueAt(scale[2], frame, 2)  # Z
        
        nuke.message("Transformation successful!")

    except Exception as e:
        nuke.message("Error loading JSON file: " + str(e))

def find_and_apply_abc(json_file_path):
    try:
        json_dir = os.path.dirname(json_file_path)
        json_base = os.path.basename(json_file_path)

        base_name, _ = os.path.splitext(json_base)
        abc_filename = f"Axisfile_{base_name}.abc"
        abc_file_path = os.path.join(json_dir, abc_filename)

        abc_file_path = abc_file_path.replace("\\", "/")

        if os.path.exists(abc_file_path):
            read_geo_node = nuke.createNode('ReadGeo2')
            read_geo_node['file'].setValue(abc_file_path)
            nuke.message(f".abc file successfully loaded: {abc_filename}")
        else:
            nuke.message(f"No corresponding .abc file found: {abc_filename}")

    except Exception as e:
        nuke.message("Error loading .abc file: " + str(e))

create_file_dialog()
