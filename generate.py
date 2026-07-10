import os
from ck3_script_generator.utils.file import write_file
from ck3_script_generator.utils.localization import Language
from events import GalTestEvent

PATH = os.path.dirname(os.path.abspath(__file__))

write_file(os.path.join(PATH, "gal_events.txt"), GalTestEvent.format())
write_file(os.path.join(PATH, "gal_events_localization.yml"), GalTestEvent.localization(Language.Chinese))
