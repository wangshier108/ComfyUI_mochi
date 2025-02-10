
from .mochi import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

from . import (
    mochi
)


def update_mappings(module):
    NODE_CLASS_MAPPINGS.update(**module.NODE_CLASS_MAPPINGS)
    NODE_DISPLAY_NAME_MAPPINGS.update(**module.NODE_DISPLAY_NAME_MAPPINGS)


update_mappings(mochi)