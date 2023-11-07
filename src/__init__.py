# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public LICENSE as published by
# the Free Software Foundation; either version 3 of the LICENSE, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public LICENSE for more details.
#
# You should have received a copy of the GNU General Public LICENSE
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name": "Copy to MMD Shape Keys",
    "author": "ShyWolf42",
    "description": "Copies English shape keys to their Japanese counterparts for MMD animations.",
    "blender": (3, 0, 0),
    "version": (1, 1, 0),
    "location": "",
    "warning": "",
    "category": "Mesh"
}

from .mmd_shapekeys import (mmd_shapekeys_ui, mmd_shapekeys_op, copy_as_mmd_settings, prefill_op,
                            json_export_op, json_import_op)

if "bpy" in locals():
    import importlib

    importlib.reload(mmd_shapekeys_op)
    importlib.reload(mmd_shapekeys_ui)
    importlib.reload(copy_as_mmd_settings)
    importlib.reload(prefill_op)
    importlib.reload(json_export_op)
    importlib.reload(json_import_op)

import bpy

CLASSES_TO_REGISTER = [
    mmd_shapekeys_op.DuplicateVisemeAsMmdShapekey,
    mmd_shapekeys_ui.DuplicateVisemeAsMmdPanel,
    copy_as_mmd_settings.CopyAsMMDSettings,
    prefill_op.PrefillMmdShapekey,
    json_export_op.JsonClipboardExport,
    json_import_op.JsonClipboardImport
]


def register():
    for clazz in CLASSES_TO_REGISTER:
        bpy.utils.register_class(clazz)

    bpy.types.Object.CopyAsMMDSettings = bpy.props.PointerProperty(type=copy_as_mmd_settings.CopyAsMMDSettings)


def unregister():
    for clazz in CLASSES_TO_REGISTER:
        bpy.utils.unregister_class(clazz)

    del bpy.types.Object.CopyAsMMDSettings
