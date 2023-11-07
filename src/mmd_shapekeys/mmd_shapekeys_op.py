import logging
from typing import Dict

import bpy

from . import copy_as_mmd_settings
from .copy_as_mmd_settings import CopyAsMMDSettings

log = logging.getLogger(__name__)

# Keep all lowercase
VISEMES = {
    "ah": "あ",
    "ch": "い",
    "u": "う",
    "e": "え",
    "oh": "お",
}

MMD_SHAPEKEYS = {
    "blink happy": "笑い",
    "blink": "まばたき",
    "close><": "はぅ",
    "calm": "なごみ",
    "stare": "じと目",
    "wink": "ウィンク",
    "wink right": "ウインク右",
    "wink 2": "ウインク２",
    "wink 2 right": "ウインク２右",
    "cheerful": "にこり",
    "serious": "真面目",
    "upper": "上",
    "lower": "下",
    "anger": "怒り",
    "angry": "怒り",  # = anger
    "sadness": "困る",
    "sad": "困る",  # = sadness
}


def copy_shapekey(shapekey: bpy.types.ShapeKey, target: str):
    if (not shapekey
            or target is None
            or shapekey.name == target):
        return

    shapekey.value = 1
    bpy.ops.object.shape_key_add(from_mix=True)
    bpy.context.object.active_shape_key.name = target
    shapekey.value = 0


class DuplicateVisemeAsMmdShapekey(bpy.types.Operator):
    bl_idname = "mesh.duplicate_mmd_shapekeys"
    bl_label = "Duplicate Shape Keys With MMD Names"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context: bpy.types.Context):
        obj = context.object
        settings: CopyAsMMDSettings = obj.CopyAsMMDSettings
        shapekeys: Dict = obj.data.shape_keys.key_blocks

        copy_shapekey(shapekeys.get(settings.ah), VISEMES['ah'])
        copy_shapekey(shapekeys.get(settings.ch), VISEMES['ch'])
        copy_shapekey(shapekeys.get(settings.u), VISEMES['u'])
        copy_shapekey(shapekeys.get(settings.e), VISEMES['e'])
        copy_shapekey(shapekeys.get(settings.oh), VISEMES['oh'])

        # Text Separator Shapekey
        bpy.ops.object.shape_key_add(from_mix=False)
        bpy.context.object.active_shape_key.name = " ^ MMD Visemes / Other v"

        for (key, name) in copy_as_mmd_settings.SHAPEKEY_LIST:
            sk = getattr(settings, key)
            if sk:
                copy_shapekey(shapekeys.get(sk), MMD_SHAPEKEYS.get(name or key))

        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(DuplicateVisemeAsMmdShapekey.bl_idname, text=DuplicateVisemeAsMmdShapekey.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access)
def register():
    bpy.utils.register_class(DuplicateVisemeAsMmdShapekey)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(DuplicateVisemeAsMmdShapekey)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
