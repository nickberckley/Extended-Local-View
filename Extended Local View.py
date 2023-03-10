'''
Created by Nika Kutsniashvili (nickberckley)
License : GNU General Public License version3 (http://www.gnu.org/licenses/)
'''

bl_info = {
    "name": "Extended Local View",
    "author": "Nika Kutsniashvili (nickberckley)",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "Ctrl + /",
    "description": "Local View with Lights Included",
    "category": "3D View"
}

import bpy


def extended_local_view(obj):
    current_area = bpy.context.area.type
    original_cursor_location = bpy.context.scene.cursor.location.copy()
    selected_objects = bpy.context.selected_objects
    
    visible_lights = [obj for obj in bpy.context.scene.objects if obj.type == 'LIGHT' and obj.visible_get(view_layer=bpy.context.view_layer)]
    
    if bpy.context.space_data.local_view is None:
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in selected_objects + visible_lights:
            obj.select_set(True)

        bpy.ops.view3d.localview()
        for light in visible_lights:
            light.select_set(False)
        bpy.ops.view3d.view_selected()
    else:
        bpy.ops.view3d.localview()
        bpy.context.scene.cursor.location = original_cursor_location
        

class ExtendedLocalView(bpy.types.Operator):
    """Take the selected object(s) and lights visible in the viewport to the local view"""
    bl_idname = "object.extended_local_view"
    bl_label = "Extended Local View"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return bpy.context.mode == 'OBJECT' and len(bpy.context.selected_objects) > 0

    def execute(self, context):
        for obj in context.selected_objects:
            extended_local_view(obj)
        return {'FINISHED'}


addon_keymaps = []

classes = (ExtendedLocalView,
            )
            
def register():
    from bpy.utils import register_class
    for cls in classes :
        register_class(cls)
        
    # KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        # Keymap for 3D View
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("object.extended_local_view", type='SLASH', value='PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))
        
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes) :
        unregister_class(cls)
        
    # KEYMAP
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()