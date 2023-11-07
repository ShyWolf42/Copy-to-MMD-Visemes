import bpy

from .copy_as_mmd_settings import CopyAsMMDSettings


class JsonClipboardExport(bpy.types.Operator):
    bl_idname = "mesh.duplicate_mmd_shapekeys_export_clipboard_json"
    bl_label = "Export Settings To Clipboard"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        obj = context.object
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings
        bpy.context.window_manager.clipboard = settings.export_to_json()
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(JsonClipboardExport.bl_idname, text=JsonClipboardExport.bl_label)


def register():
    bpy.utils.register_class(JsonClipboardExport)


def unregister():
    bpy.utils.unregister_class(JsonClipboardExport)


if __name__ == "__main__":
    register()
