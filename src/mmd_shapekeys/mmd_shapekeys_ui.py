import logging

import bpy

from . import copy_as_mmd_settings
from .copy_as_mmd_settings import CopyAsMMDSettings, determine_prefix

log = logging.getLogger(__name__)


class DuplicateVisemeAsMmdPanel(bpy.types.Panel):
    bl_info = ""
    bl_label = "MMD Shape Keys"
    bl_idname = "OBJECT_PT_MMD_Shapekeys"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        obj = context.active_object
        obj_shape_keys = obj.data.shape_keys
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings

        if not obj_shape_keys:
            row = layout.row()
            row.label(text="No Shape Keys On Object")
            return

        # self.prefill_form(context)
        row = layout.row()
        row.prop(settings, "prefill_existing_JP_shapekeys", text="Fill Existing Target Shape Keys As Placeholder")
        row = layout.row()
        row.operator("mesh.duplicate_mmd_shapekeys_prefill")

        row = layout.row()
        row.scale_y = 2.0
        row.operator("mesh.duplicate_mmd_shapekeys")

        # Import / Export
        row = layout.row()
        row.operator("mesh.duplicate_mmd_shapekeys_import_clipboard_json")
        row.operator("mesh.duplicate_mmd_shapekeys_export_clipboard_json")

        row = layout.row()
        row.label(text="Visemes")
        for viseme in copy_as_mmd_settings.VISEMES_LIST:
            row = layout.row()
            row.prop_search(settings, viseme, obj_shape_keys, "key_blocks", text=viseme)

        row = layout.row()
        row.label(text="Other Shape Keys:")
        for shapekey in copy_as_mmd_settings.SHAPEKEY_LIST:
            row = layout.row()
            row.prop_search(settings, shapekey[0], obj_shape_keys, "key_blocks", text=shapekey[1] or shapekey[0])

    @classmethod
    def poll(cls, context: bpy.types.Context):
        obj = context.active_object
        if obj is None:
            return False

        return hasattr(obj.data, "shape_keys")

    @classmethod
    def prefill_form(cls, context: bpy.types.Context):
        obj = context.active_object
        obj_shape_keys = obj.data.shape_keys.key_blocks
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings

        if settings.hasBeenAutoFilled:
            return

        prefix = determine_prefix(obj_shape_keys)
        # Filter by length as well in case there is no prefix
        for sk in [sk for sk in obj_shape_keys
                   if sk.name.startswith(prefix)
                      and len(prefix) + 1 < len(sk.name) <= len(prefix) + 2]:
            viseme_name = sk.name.removeprefix(prefix)

            setting_name = viseme_name.lower()
            settings.set_attribute(setting_name, sk.name)

        for shapekey in obj_shape_keys:
            shapekey_name = shapekey.name.lower()
            settings.set_attribute(shapekey_name, shapekey.name)


def register():
    bpy.utils.register_class(DuplicateVisemeAsMmdPanel)


def unregister():
    bpy.utils.unregister_class(DuplicateVisemeAsMmdPanel)


if __name__ == "__main__":
    register()
