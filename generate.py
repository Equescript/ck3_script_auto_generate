import os
from ck3_script_generator.utils.file import write_file
from events import GalTestEvent

PATH = os.path.dirname(os.path.abspath(__file__))

write_file(os.path.join(PATH, "gal_events.txt"), GalTestEvent.format())
