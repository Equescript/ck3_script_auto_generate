from ck3_script_generator.ck3_backend_definitions.action import *
from ck3_script_generator.utils import *
import os

gal_effect_enable_my_galgame = Effect("gal_effect_enable_my_galgame", [
    SetVariableAction("gal_attraction", 0),
    LiteralAction("add_trait = gal_trait_my_galgame"),
])

gal_effect_disable_my_galgame = Effect("gal_effect_disable_my_galgame", [
    LiteralAction("remove_trait = gal_trait_my_galgame"),
    RemoveVariableAction("gal_attraction"),
])

EFFECTS = [
    gal_effect_enable_my_galgame,
    gal_effect_disable_my_galgame,
]

def generate(path: str):
    gal_effects_data = "\n\n".join([effect.format(0) for effect in EFFECTS])
    write_file(os.path.join(path, "common/scripted_effects/gal_effects.txt"), gal_effects_data)
