import logging

import bpy

from .copy_as_mmd_settings import CopyAsMMDSettings, determine_prefix
from .mmd_shapekeys_op import MMD_SHAPEKEYS, VISEMES

log = logging.getLogger(__name__)


def prefill_form(context):
    obj = context.active_object
    obj_shape_keys = obj.data.shape_keys.key_blocks
    settings: CopyAsMMDSettings = obj.CopyAsMMDSettings

    # Fill existing japanese MMD Shapekeys to show which ones are already correctly set
    # later matches will not overwrite the previously set values.
    if settings.prefill_existing_JP_shapekeys:
        fill_existing_jp_shapekeys(obj_shape_keys, settings)

    prefix = determine_prefix(obj_shape_keys)
    for shapekey in obj_shape_keys:
        # Viseme with prefix?
        if prefix != "":
            viseme_name = shapekey.name.removeprefix(prefix)
            settings.set_attribute(viseme_name.lower(), shapekey.name)

        # other shapekey
        settings.set_attribute(shapekey.name.lower(), shapekey.name)


def fill_existing_jp_shapekeys(obj_shape_keys, settings):
    existing_shapekey_names = [sk.name for sk in obj_shape_keys]
    for (name, target) in MMD_SHAPEKEYS.items():
        if target in existing_shapekey_names:
            settings.set_attribute(name, target)
    for (name, target) in VISEMES.items():
        if target in existing_shapekey_names:
            settings.set_attribute(name, target)


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
