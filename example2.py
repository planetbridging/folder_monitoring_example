import os
import pyinotify
import configparser
import syslog

class EventHandler(pyinotify.ProcessEvent):
    ignore_patterns = ['^\..*']  # Regex pattern to match dot files

    def process_default(self, event):
        # Ignore dot files
        if any(event.name.startswith(p) for p in self.ignore_patterns):
            syslog.syslog(syslog.LOG_INFO, f"Ignored {event.pathname}")
        else:
            syslog.syslog(syslog.LOG_INFO, f"Processing {event.pathname}")
            # Call the stub function to process the file
            self.process_file(event.pathname)
            syslog.syslog(syslog.LOG_INFO, f"Finished processing {event.pathname}")

    def process_file(self, pathname):
        # Stub function for file processing logic
        # Add your file processing code here
        pass

# Read the configuration file
config = configparser.ConfigParser()
config.read('monitor_config.ini')
monitor_dir = config.get('monitor', 'directory')

# Function to process existing files in the directory
def process_existing_files(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            if not name.startswith('.'):
                file_path = os.path.join(root, name)
                syslog.syslog(syslog.LOG_INFO, f"Processing existing file {file_path}")
                # Call the stub function to process the file
                EventHandler().process_file(file_path)
                syslog.syslog(syslog.LOG_INFO, f"Finished processing existing file {file_path}")

# Check if the directory exists before adding a watch
if os.path.exists(monitor_dir):
    process_existing_files(monitor_dir)  # Process pre-existing files
    # Set up inotify stuff
    wm = pyinotify.WatchManager()
    eh = EventHandler()
    notifier = pyinotify.Notifier(wm, eh)
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
    wm.add_watch(monitor_dir, mask, rec=True, auto_add=True)
    notifier.loop()
else:
    syslog.syslog(syslog.LOG_ERR, f"The directory {monitor_dir} does not exist.")
