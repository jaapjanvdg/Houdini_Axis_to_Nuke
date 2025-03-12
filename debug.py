import hou


start_frame, end_frame = hou.playbar.frameRange()
start_frame = int(start_frame)
end_frame = int(end_frame)

for frame in range(start_frame, end_frame + 1):
    hou.setFrame(frame)
    selected = hou.selectedNodes()[0]

    obj_node = selected.parent()

    display = obj_node.displayNode()

    geo = display.geometry()
    pivot = geo.boundingBox().center()
    print(geo)


import hou

selected = hou.selectedNodes()[0]
geo = selected.geometry()
bbox = geo.orientedBoundingBox()
print(bbox.rotation())