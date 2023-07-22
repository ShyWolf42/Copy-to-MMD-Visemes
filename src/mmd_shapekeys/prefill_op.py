import logging

import bpy

from .copy_as_mmd_settings import CopyAsMMDSettings, determine_prefix

log = logging.getLogger(__name__)


def prefill_form(context):
    obj = context.active_object
    obj_shape_keys = obj.data.shape_keys.key_blocks
    settings: CopyAsMMDSettings = obj.CopyAsMMDSettings

    prefix = determine_prefix(obj_shape_keys)

    # Filter by length as well in case there is no prefix
    for sk in [sk for sk in obj_shape_keys
               if sk.name.startswith(prefix)
                  and len(prefix) + 1 < len(sk.name) <= len(prefix) + 2]:
        viseme_name = sk.name.removeprefix(prefix)
        settings.set_attribute(viseme_name.lower(), sk.name)

    for shapekey in obj_shape_keys:
        settings.set_attribute(shapekey.name.lower(), shapekey.name)


class PrefillMmdShapekey(bpy.types.Operator):
    bl_idname = "mesh.duplicate_mmd_shapekeys_prefill"
    bl_label = "Prefill Values"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        prefill_form(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(PrefillMmdShapekey.bl_idname, text=PrefillMmdShapekey.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(PrefillMmdShapekey)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(PrefillMmdShapekey)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
