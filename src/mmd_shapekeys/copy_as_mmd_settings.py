import logging
import re

import bpy

log = logging.getLogger(__name__)

VISEMES_LIST = ["ah", "ch", "u", "e", "oh"]
VISEME_PREFIX_REGEX = re.compile(f"^(.*[._-])?(?:{'|'.join(VISEMES_LIST)})$", re.IGNORECASE)

# (PropertyName , DisplayText)
SHAPEKEY_LIST = [("blink_happy", "blink happy"),
                 ("blink", None),
                 ("close_X", "close><"),
                 ("calm", None),
                 ("stare", None),
                 ("wink", None),
                 ("wink_right", "wink right"),
                 ("wink_2", "wink 2"),
                 ("wink_2_right", "wink 2 right"),
                 ("cheerful", None),
                 ("serious", None),
                 ("upper", None),
                 ("lower", None),
                 ("anger", None),
                 ("sadness", None)]


def determine_prefix(shapekeys) -> str:
    for sk in shapekeys:
        matches = re.match(VISEME_PREFIX_REGEX, sk.name)
        if matches:
            return matches.group(1) or ""

    # prefix could not be determined
    return ""


class CopyAsMMDSettings(bpy.types.PropertyGroup):
    # Visemes
    # @formatter:off
    ah: bpy.props.StringProperty()
    ch: bpy.props.StringProperty()
    u:  bpy.props.StringProperty()
    e:  bpy.props.StringProperty()
    oh: bpy.props.StringProperty()

    # Shapekeys
    blink_happy:    bpy.props.StringProperty(description="Close eyes, ^.^ shaped")
    blink:          bpy.props.StringProperty()
    close_X:        bpy.props.StringProperty(description="Close Eyes, >.< shaped")
    calm:           bpy.props.StringProperty()
    stare:          bpy.props.StringProperty()
    wink:           bpy.props.StringProperty(description="Wink left eye")
    wink_right:     bpy.props.StringProperty(description="Wink right eye")
    wink_2:         bpy.props.StringProperty(description="Happy wink left eye")
    wink_2_right:   bpy.props.StringProperty(description="Happy wink right eye")
    cheerful:       bpy.props.StringProperty()
    serious:        bpy.props.StringProperty()
    upper:          bpy.props.StringProperty(description="Eyebrows up")
    lower:          bpy.props.StringProperty(description="Eyebrows lowered")
    anger:          bpy.props.StringProperty()
    sadness:        bpy.props.StringProperty()
    # @formatter:on

    prefill_existing_JP_shapekeys: bpy.props.BoolProperty(
        default=True,
        description="Prefill with existing Japanese shape keys? \n"
                    "(Those shape keys will not be duplicated, only act as a placeholder)")

    def set_attribute(self, attribute: str, value: str) -> None:
        if not attribute:
            return

        attribute = attribute.lower().replace(" ", "_")
        # Set variable if empty
        if hasattr(self, attribute):
            if not getattr(self, attribute):
                setattr(self, attribute, value)
            return

        # common variations
        if attribute == "aa":
            self.set_attribute("ah", value)
        elif attribute == "ee":
            self.set_attribute("e", value)
        elif attribute.startswith("wink2"):
            self.set_attribute(attribute.replace("wink2", "wink_2"), value)
