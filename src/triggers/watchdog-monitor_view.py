from datetime import datetime
import time
import os

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from ..pipeline_scripts.bronze_store_view import extract_and_store_bronze
from ..pipeline_scripts.silver_store_view import transform_bronze_to_silver_with_metadata

BRONZE_DIR = os.getenv('BRONZE_DIR')

if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
    patterns=["*"], 
    ignore_patterns=None, 
    ignore_directories=False, 
    case_sensitive=True
)


# trigger event on creation of new file in the directory
def on_created(event):
    # User Message
    print(f"[ {datetime.now()} ]-------- {event.src_path} has been created!")
    # User Message
    print('[', datetime.now(), ']--------',
          "New Batch of Data is Loaded - Event Notification - ", event.src_path)
    # User Message
    print(f'[ {datetime.now()} ]-------- Data Extraction Phase Commenced - Import Data From Raw Data Store - Event Notification ')
    # Call a Data Extaction Function - Argument as File Path of New Batch of Data
    try:
        extract_and_store_bronze(event.src_path)
    except Exception as exceptmessage:
        # Exception Message
        print(f"Data Extraction - Failure with {exceptmessage}")


    # User Message
    print(f'[ {datetime.now()} ]-------- Data Transformation Phase Commenced - Import Data From Bronze Store - Event Notification ')
    # Call a Data Extaction Function - Argument as File Path of New Batch of Data
    try:
        print(f"[ {datetime.now()} ]-------- Starting metadata-based transformation and loading to Silver Store...")
        transform_bronze_to_silver_with_metadata(BRONZE_DIR, event.src_path)
    except Exception as exceptmessage:
        # Exception Message
        print(f"Data Extraction - Failure with {exceptmessage}")


# Watchdog configuration parameters
my_event_handler.on_created = on_created
path = "/RAKEZ_BI_Works/datastore/raw_store"
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

print("******************Data Pipeline Log Messages*********************")

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
