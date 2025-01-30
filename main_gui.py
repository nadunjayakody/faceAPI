import tkinter as tk
import subprocess
import os
import threading
import sys
from ruamel.yaml import YAML
import os
from ruamel.yaml.comments import CommentedMap, CommentedSeq

# Get the directory where the current script is located
script_directory = os.path.dirname(os.path.abspath(__file__))


# Change the working directory to the script's directory
os.chdir(script_directory)
settings_mode_path = script_directory

# Declaring package relative import for import sibling directories of the sub-package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-1]))

file_path = os.path.join(script_directory, "config.yaml")

# Global variable to store the process
process = None


# Color Palette
bg_color = "#666666"
upper_btn_bg_color = "#25416F"
frame_bg_color = "#505050"
bg_root = "#121212"
display_bg_color = "#C5E8FC"
nav_bg_color = "#d9d9d9"
btn_bg_color = "#286EB1"
btn_fg_color = "#ffffff"
text_fg_color = "#121212"
highlight_color = "#ff9800"

# Initialize YAML instance
yaml = YAML()
yaml.preserve_quotes = True


def load_config(file_path):
    """Load YAML file while preserving comments."""
    with open(file_path, 'r') as file:
        return yaml.load(file)


def save_config(data, file_path):
    """Save YAML data with custom formatting, ensuring quotes around strings and adding extra line spaces for clarity."""
    with open(file_path, 'w') as file:
        if isinstance(data, CommentedMap):
            # Write top-level comments if they exist
            if data.ca.comment and len(data.ca.comment) > 1:
                for comment in data.ca.comment[1]:
                    file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment

            for key, value in data.items():
                # Write comments before the key-value pair
                pre_comment = data.ca.items.get(key, [None, None, None, None])[0]
                if pre_comment:
                    file.write(f"\n{pre_comment.value.strip()}\n")  # Add an extra line space before the comment

                # Write the key and value, ensuring quotes around strings
                if isinstance(value, str):
                    file.write(f"{key}: '{value}'\n")
                elif isinstance(value, CommentedSeq):
                    yaml.dump({key: value}, file)  # Preserve structure for lists
                else:
                    yaml.dump({key: value}, file)  # Preserve structure for other types

                # Write comments after the key-value pair
                post_comment = data.ca.items.get(key, [None, None, None, None])[2]
                if post_comment:
                    file.write(f"\n{post_comment.value.strip()}\n")  # Add an extra line space before the comment

            # Handle comments at the end of the document
            if data.ca.comment and len(data.ca.comment) > 3:
                for comment in data.ca.comment[3]:
                    file.write(f"\n{comment.value.strip()}\n")  # Add an extra line space before the comment


# Function to display messages in the Text widget
def display_message(message):
    message_text.delete(1.0, tk.END)  # Clear the existing text
    message_text.insert(tk.END, message)  # Insert the new message


# Add the custom path to sys.path
sys.path.append(settings_mode_path)
try:
    import settings
except ImportError:
    print(f"settings.py not found in {settings_mode_path}")


# Function to handle specific responses from the terminal output
def handle_specific_responses(line):
    if "Ohh. This user is not registered." in line:
        display_message("API test successful.")
    elif "Internet is connected" in line:
        display_message("Internet is connected")
    elif "Camera is not connected" in line:
        display_message("Cameras not connected")
    else:
        display_message(line)


# Function to start the script
def start_script(script_name, message):
    global process
    if process is None or process.poll() is not None:  # Check if the process is not already running
        process = subprocess.Popen(["python", script_name])
        display_message(message)


# Function to update the Text widget with output from the subprocess
def update_text_from_process(process):
    for line in iter(process.stdout.readline, ''):
        handle_specific_responses(line)
    process.stdout.close()


# Function to start test case scripts with their respective outputs
def start_test_script(script_name, start_message):
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen(["python", script_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        display_message(start_message)
        threading.Thread(target=update_text_from_process, args=(process,), daemon=True).start()


# Function to stop the script
def stop_script():
    global process
    if process is not None:
        process.terminate()
        process = None
        display_message("Stopped.")


# Function to create the test cases frame
def create_test_cases_frame(parent):
    test_frame = tk.Frame(parent, bg=bg_color)

    # Configure the grid to center everything
    test_frame.grid_columnconfigure(0, weight=1)  # Left empty column
    test_frame.grid_columnconfigure(1, weight=3)  # Main column for content
    test_frame.grid_columnconfigure(2, weight=1)  # Right empty column

    # Center the title label
    test_case_label = tk.Label(test_frame, text="Test case window", font=('Arial', 20, 'bold'), bg=bg_color)
    test_case_label.grid(row=0, column=1, pady=10, sticky='ew')  # Centered and expanded

    # Buttons spread horizontally and centered
    api_button = tk.Button(test_frame, text="API Test", command=lambda: start_test_script("test_cases/api_test.py", "API Test started..."))
    internet_button = tk.Button(test_frame, text="Internet Test", command=lambda: start_test_script("test_cases/check_internet.py", "Internet Test started..."))
    camera_button = tk.Button(test_frame, text="Camera Test", command=lambda: start_test_script("test_cases/camera_test.py", "Camera Test started..."))
    leds_button = tk.Button(test_frame, text="LEDs Test", command=lambda: start_test_script("test_cases/check_LED.py", "LEDs Test started..."))
    back_button = tk.Button(test_frame, text="Back", command=lambda: [show_frame(main_frame), display_message("")])

    # Add buttons with padding and make them expand horizontally
    api_button.grid(row=1, column=1, pady=10, sticky='ew', padx=20)
    internet_button.grid(row=2, column=1, pady=10, sticky='ew', padx=20)
    camera_button.grid(row=3, column=1, pady=10, sticky='ew', padx=20)
    leds_button.grid(row=4, column=1, pady=10, sticky='ew', padx=20)
    back_button.grid(row=5, column=1, pady=10, sticky='ew', padx=20)

    return test_frame



def show_main_frame():
    # Hide settings frame and show main frame
    settings_frame.pack_forget()  # Hide the settings frame
    main_frame.pack(fill='both', expand=True)  # Show the main frame




# Creating the settings frame for configuration
def create_settings_frame(container, show_main_frame_callback):

    # Load the configuration values from the YAML file
    config = load_config(file_path)

    # Assign values from the config file
    server_url = config['server']['url']
    server_username = config['server']['username']
    server_api_key = config['server']['api_key']
    camera_IN_url = config['camera']['entrance_url']
    camera_OUT_url = config['camera']['exit_url']

    settings_window = tk.Frame(container, bg=bg_color)
    settings_window.pack(fill='x', padx=10, pady=10)
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(settings_window, text="Manual Configuration Panel", font=('Arial', 20, 'bold'), bg=bg_color)
    title_label.pack(pady=5)

    config_frame = tk.Frame(settings_window, bg=frame_bg_color)
    config_frame.pack(fill='x', padx=20, pady=20)
    config_frame.grid_rowconfigure(0, weight=1)
    config_frame.grid_rowconfigure(1, weight=1)
    config_frame.grid_rowconfigure(2, weight=1)
    config_frame.grid_rowconfigure(3, weight=1)
    config_frame.grid_rowconfigure(4, weight=1)
    config_frame.grid_rowconfigure(5, weight=1)

    config_frame.grid_columnconfigure(0, weight=1)
    config_frame.grid_columnconfigure(1, weight=1)

    entry_font = ('Arial', 12)  # Increase the size if needed

    # Camera IN URL Input
    camera_IN_url_label = tk.Label(config_frame, text="Camera IN URL:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    camera_IN_url_entry = tk.Entry(config_frame, font=entry_font)
    camera_IN_url_label.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
    camera_IN_url_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
    camera_IN_url_entry.insert(0, camera_IN_url)

    # Camera OUT URL Input
    camera_OUT_url_label = tk.Label(config_frame, text="Camera OUT URL:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    camera_OUT_url_entry = tk.Entry(config_frame, font=entry_font)
    camera_OUT_url_label.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
    camera_OUT_url_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
    camera_OUT_url_entry.insert(0, camera_OUT_url)

    # Server API Key Input
    server_api_key_label = tk.Label(config_frame, text="Server API Key:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    server_api_key_entry = tk.Entry(config_frame, font=entry_font)
    server_api_key_label.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
    server_api_key_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)
    server_api_key_entry.insert(0, server_api_key)

    # Server Username Input
    server_username_label = tk.Label(config_frame, text="Server Username:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    server_username_entry = tk.Entry(config_frame, font=entry_font)
    server_username_label.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
    server_username_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)
    server_username_entry.insert(0, server_username)

    # Server Username Input
    server_url_label = tk.Label(config_frame, text="Server URL:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    server_url_entry = tk.Entry(config_frame, font=entry_font)
    server_url_label.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
    server_url_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)
    server_url_entry.insert(0, server_url)


    # Function to save YAML configuration
    def save_changes():
        config = load_config(file_path)

        # Update values based on the current inputs
        config['server']['url'] = camera_IN_url_entry.get()
        config['server']['username'] = server_username_entry.get()
        config['server']['api_key'] = server_api_key_entry.get()
        config['camera']['entrance_url'] = camera_IN_url_entry.get()
        config['camera']['exit_url'] = camera_OUT_url_entry.get()

        # Save the updated config
        save_config(config, file_path)

    # Save Button
    save_button = tk.Button(config_frame, text="Save", command=save_changes, bg=btn_bg_color, fg=btn_fg_color)
    save_button.grid(row=5, column=0, columnspan=2, sticky='ew', padx=10, pady=20)

    # Back Button to go back to the main frame
    back_button = tk.Button(config_frame, text="Back", command=show_main_frame_callback, bg=btn_bg_color, fg=btn_fg_color)
    back_button.grid(row=6, column=0, columnspan=2, sticky='ew', padx=10, pady=10)

    return settings_window









# Function to switch frames
# Example of switching between frames
def show_frame(frame):
    # Hide all frames
    main_frame.pack_forget()
    test_cases_frame.pack_forget()
    settings_frame.pack_forget()

    # Show the desired frame
    frame.pack(fill='both', expand=True)

# Create the main window
root = tk.Tk()
root.configure(bg=frame_bg_color)
root.title("Simple GUI")

# # Create and place the Text widget
# message_text = tk.Text(root, height=4, width=40)
# message_text.grid(row=1, column=1, columnspan=10, sticky="ew", padx=10, pady=10)
# message_text.insert(tk.END, "FaceAPI")


# Calculate 100% of the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 1)
window_height = int(screen_height * 1)

# Calculate the position to center the window
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

# Set the window size and position
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
# Configure rows and columns in the root window to allow frames to expand
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create frames
main_frame = tk.Frame(root, bg=bg_color)
test_cases_frame = create_test_cases_frame(root)
settings_frame = create_settings_frame(root, show_main_frame)

# Configure rows and columns in the main_frame to allow mini display and buttons to be placed correctly
main_frame.grid_rowconfigure(0, weight=1)  # Row for the mini display
main_frame.grid_rowconfigure(1, weight=1)  # Row for the buttons
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)
main_frame.grid_columnconfigure(3, weight=1)


# Create and place the Text widget (mini screen) at the top, spanning across all columns
message_text = tk.Text(main_frame, height=10, width=40)
message_text.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)  # Adjusted to row 0, spanning 4 columns
message_text.insert(tk.END, "FaceAPI")


# Place the buttons below the mini screen (in row 1) and spread them across the grid
start_button = tk.Button(main_frame, text="Start Verification", command=lambda: start_script("verifyFace.py", "Verification started..."))
stop_button = tk.Button(main_frame, text="Stop Verification", command=stop_script)
test_cases_button = tk.Button(main_frame, text="Test Cases", command=lambda: show_frame(test_cases_frame))
settings_button = tk.Button(main_frame, text="Settings", command=lambda: show_frame(settings_frame))

# Place the buttons in the second row (row=1) across the grid columns
start_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")
stop_button.grid(row=1, column=1, pady=10, padx=10, sticky="new")
test_cases_button.grid(row=1, column=2, pady=10, padx=10, sticky="new")
settings_button.grid(row=1, column=3, pady=10, padx=10, sticky="new")

# # Place each frame manually in the root window
# main_frame.grid(row=0, column=0, sticky='nsew')
# test_cases_frame.grid(row=0, column=0, sticky='nsew')
# settings_frame.grid(row=0, column=0, sticky='nsew')

# Main frame using pack
main_frame.pack(fill='both', expand=True)
test_cases_frame.pack(fill='both', expand=True)
settings_frame.pack(fill='both', expand=True)

# Show the main frame initially
show_frame(main_frame)

# Run the GUI loop
root.mainloop()
