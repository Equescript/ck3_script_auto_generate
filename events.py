import os

from ck3_script_generator.ck3_backend_definitions.scope import Scope
from ck3_script_generator.ck3_backend_definitions.action import *
from ck3_script_generator.ck3_backend_definitions.event import *
from effects import *

GalTestEvent = EventNamespace("gal_event_intro_scene", [
Event("0001", EventType.character_event, theme="court", portraits=[
        Portrait(PortraitPos.left_portrait, "root", "flirtation"),
        Portrait(PortraitPos.right_portrait, "scope:recipient", "interested_left"),
    ],
    title="My Galgame Title",
    description="My Galgame 初始互动界面",
    options=[
        Option("增加5好感", [
            Scope("scope:recipient", ChangeVariableAction("gal_attraction", "+", 5)),
            LiteralAction("# Some Other Action"),
            TriggerEventAction("gal_event_intro_scene.0001"),
        ]),
        Option("减少5好感", [
            Scope("scope:recipient", ChangeVariableAction("gal_attraction", "+", -5)),
            LiteralAction("# Some Other Action"),
            TriggerEventAction("gal_event_intro_scene.0001"),
        ]),
        Option("下一个事件", TriggerEventAction("gal_event_intro_scene.0002")),
        Option("结束事件"),
    ]
),
Event("0002", EventType.character_event, theme="court", portraits=[
        Portrait(PortraitPos.left_portrait, "root", "flirtation"),
        Portrait(PortraitPos.right_portrait, "scope:recipient", "interested_left"),
    ],
    title="My Galgame Title",
    description="My Galgame 初始互动界面",
    options=[
        Option("结束事件"),
        Option("结束My Galgame互动", Scope("scope:recipient", gal_effect_disable_my_galgame())),
    ]
)
])

""" def generate(path: str):
    GalTestEvent.generate(
        os.path.join(path, "events/gal_interaction_event.txt"),
        os.path.join(path, "localization/simp_chinese/event_localization/gal_interaction_event_l_simp_chinese.yml")
    ) """




