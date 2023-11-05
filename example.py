import os
import pyinotify

class IgnorePatterns(pyinotify.ProcessEvent):
    # Define the patterns you want to ignore
    _ignore_patterns = ['.tempfile']

    def process_default(self, event):
        # Check if the event's filename ends with any of the ignore patterns
        if any(event.pathname.endswith(p) for p in self._ignore_patterns):
            print(f"Ignored {event.pathname}")
        else:
            # Print out the event type and path for all other files
            print(f"Event {event.maskname} occurred on {event.pathname}.")

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# The folder to be monitored is "example" within the current directory
monitor_dir = os.path.join(current_dir, 'example')

# Set up the watch manager
wm = pyinotify.WatchManager()

# Set up the event handler
eh = IgnorePatterns()

# Set up the notifier
notifier = pyinotify.Notifier(wm, eh)

# Define the mask for the events you want to catch
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY

# Check if the directory exists before adding a watch
if os.path.exists(monitor_dir):
    # Add a watch to monitor the "example" directory
    wm.add_watch(monitor_dir, mask, rec=True, auto_add=True)
else:
    print(f"The directory {monitor_dir} does not exist.")

# Loop forever and handle events
notifier.loop()
