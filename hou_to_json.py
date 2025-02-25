import json
import os
import time
from PySide2.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QFileDialog

def test(kwargs, myHda):

    hda_node = hou.pwd()
    input_hda_node = hda_node.input(0)
    if input_hda_node is None:
        raise Exception("No input connected to the HDA. Please connect a node to the input.")

    class OutputBox(QWidget):
        def __init__(self, ):
            super().__init__()
            self.setWindowTitle("Locator Exporter")

            hip_file_path = hou.hipFile.path()
            self.default_directory = os.path.dirname(hip_file_path)
            self.data_point_name = f"Locatie_{int(time.time())}"

            self.layout()
            self.setLayout(self.created_layout)

        def output_name_line(self):
            self.line_edit = QLineEdit(self.data_point_name)

        def select_path_button_func(self):
            self.output_name_button = QPushButton("Select a Path")
            self.output_name_button.clicked.connect(self.select_path)

        def select_path(self):
            self.select_path_dialog = QFileDialog()
            self.select_path_dialog.setWindowTitle("Select a Path")
            self.select_path_dialog.setFileMode(QFileDialog.FileMode.Directory)
            self.select_path_dialog.setOptions(QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
            self.select_path_dialog.setDirectory(self.default_directory)
            self.select_path_dialog.exec_()
            if self.select_path_dialog.selectedFiles()[0]:
                self.new_default_directory_func(self.select_path_dialog.selectedFiles()[0])
            
        
        def confirm_output_name_button(self):
            self.confirm_path_button = QPushButton("Confirm Output Name and Continue")
            self.confirm_path_button.clicked.connect(self.exit_app)
            self.confirm_path_button.clicked.connect(self.hou_abc_function)
            self.confirm_path_button.clicked.connect(self.export_transforms_to_json)

        def new_default_directory_func(self, input):
            self.default_directory = input

        def exit_app(self):
            self.close()

        def layout(self):
            self.output_name_line()
            self.select_path_button_func()
            self.confirm_output_name_button()

            self.created_layout = QVBoxLayout()
            self.created_layout.addWidget(self.line_edit)
            self.created_layout.addWidget(self.output_name_button)
            self.created_layout.addWidget(self.confirm_path_button)
            return self.created_layout
        
        def hou_abc_function(self):
            rop_alembic_node = input_hda_node.createOutputNode("rop_alembic")
            rop_alembic_node.parm("trange").set(1) 
            rop_alembic_node.parm("filename").set(f"{self.default_directory}/Axisfile_{self.line_edit.text()}.abc")
            rop_alembic_node.render()

        
        def export_transforms_to_json(self):
            """JSON File Export"""
            output_file = os.path.join(self.default_directory, f"{self.line_edit.text()}.json")

            start_frame, end_frame = hou.playbar.frameRange()
            start_frame = int(start_frame)
            end_frame = int(end_frame)
            
            data = {}
            
            for frame in range(start_frame, end_frame + 1):
                hou.setFrame(frame)
                
                if input_hda_node.parmTuple("t") and input_hda_node.parmTuple("r") and input_hda_node.parmTuple("s"):
                    translate = list(input_hda_node.parmTuple("t").eval())
                    rotate = list(input_hda_node.parmTuple("r").eval())
                    scale = list(input_hda_node.parmTuple("s").eval())
                else:
                    print(f"Node at frame {frame} has no transform parameters.")
                    continue
                    
                data[frame] = {
                    "translate": translate,
                    "rotate": rotate,
                    "scale": scale
                }
            
            with open(output_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            
            print(f"Transforms exported to {output_file}")
        

    global form
    form = OutputBox()
    form.show()
