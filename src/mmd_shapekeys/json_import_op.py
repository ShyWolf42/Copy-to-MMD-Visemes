import bpy

from .copy_as_mmd_settings import CopyAsMMDSettings


class JsonClipboardImport(bpy.types.Operator):
    bl_idname = "mesh.duplicate_mmd_shapekeys_import_clipboard_json"
    bl_label = "Import From Clipboard"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        obj = context.object
        obj_shape_keys = obj.data.shape_keys.key_blocks
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings
        settings.import_from_json(bpy.context.window_manager.clipboard, obj_shape_keys)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(JsonClipboardImport.bl_idname, text=JsonClipboardImport.bl_label)


def register():
    bpy.utils.register_class(JsonClipboardImport)


def unregister():
    bpy.utils.unregister_class(JsonClipboardImport)


if __name__ == "__main__":
    register()
