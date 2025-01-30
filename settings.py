

import tkinter as tk
import os
import sys
import yaml 
from PIL import Image, ImageTk
from ruamel.yaml import YAML
import os
from ruamel.yaml.comments import CommentedMap, CommentedSeq



# Declaring the relevant paths to find the other scripts that are necessary for GUI to function
script_dir = os.path.dirname(os.path.abspath(__file__))

# Logo paths
logo1_path = os.path.join(script_dir,'imgs', '1.png')
logo2_path = os.path.join(script_dir,'imgs', '2.png')
logo3_path = os.path.join(script_dir,'imgs', '3.png')

# Declaring package relative import for import sibling directories of the sub-package parser
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-1]))

file_path = os.path.join(script_dir, "config", "config.yaml")

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


# Color Palette
bg_color = "#666666"
frame_bg_color = "#505050"
btn_bg_color = "#286EB1"
btn_fg_color = "#ffffff"
start_bg_color = "#3fada7"
stop_bg_color = "#e7311b"

# Creating the settings frame for configuration
def create_settings_frame(container, update_display):


    # Load the configuration values from the YAML file
    config = load_config(file_path)

    # Assign YAML values to variables for GUI use
    cam_url_entrance = config["CAM_URL_ENTRANCE"]
    cam_url_exit =  config["CAM_URL_EXIT"]
    api_key_slt = config['API_KEY_SLT']
    api_user_slt = config['API_USER_SLT']
    api_dd_slt = config['API_DD_SLT']

    settings_window = tk.Frame(container, bg=bg_color)
    settings_window.pack(fill='x', padx=10, pady=10)
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(settings_window, text="Manual Configuration Panel", font=('Arial', 20, 'bold'), bg=bg_color)
    title_label.pack(pady=5)

    config_frame = tk.Frame(settings_window, bg=frame_bg_color)
    config_frame.pack(fill='x', padx=20,pady=20)
    config_frame.grid_rowconfigure(0, weight=1)
    config_frame.grid_rowconfigure(1, weight=1)
    config_frame.grid_rowconfigure(2, weight=1)
    config_frame.grid_rowconfigure(3, weight=1)
    config_frame.grid_rowconfigure(4, weight=1)
    config_frame.grid_rowconfigure(5, weight=1)

    config_frame.grid_columnconfigure(0, weight=1)
    config_frame.grid_columnconfigure(1, weight=1)


    # Load current configuration
    config = load_config(file_path)

    entry_font = ('Arial', 12)  # Increase the size if needed

    # Camera IN URL Input
    camera_IN_url_label = tk.Label(config_frame, text="Camera IN URL:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    camera_IN_url = tk.Entry(config_frame, font=entry_font)
    camera_IN_url_label.grid(row=0, column=0, sticky='ew', padx=10,pady=10)
    camera_IN_url.grid(row=0, column=1, sticky='ew', padx=10, pady=10)
    camera_IN_url.insert(0, cam_url_entrance)

    # Camera OUT URL Input
    camera_OUT_url_label = tk.Label(config_frame, text="Camera OUT URL:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    camera_OUT_url = tk.Entry(config_frame, font=entry_font)
    camera_OUT_url_label.grid(row=1, column=0,  sticky='ew',padx=10, pady=10)
    camera_OUT_url.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
    camera_OUT_url.insert(0, cam_url_exit)

    
    # API Key Input
    api_key_label = tk.Label(config_frame, text="API_KEY_SLT:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    api_key_entry = tk.Entry(config_frame, font=entry_font)
    api_key_label.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
    api_key_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)
    api_key_entry.insert(0, api_key_slt)

    # API Key Input
    api_user_label = tk.Label(config_frame, text="API_USER_SLT:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    api_user_entry = tk.Entry(config_frame, font=entry_font)
    api_user_label.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
    api_user_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)
    api_user_entry.insert(0, api_user_slt)

    # API Key Input
    api_dd_label = tk.Label(config_frame, text="API_DD_SLT:", font=('Arial', 16), bg=bg_color, fg="#ffffff")
    api_dd_entry = tk.Entry(config_frame, font=entry_font)
    api_dd_label.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
    api_dd_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)
    api_dd_entry.insert(0, api_dd_slt)

    def restore_changes():
        config = load_config(file_path)
        
        # Reset USER values to their defaults
        config['CAM_URL_ENTRANCE'] = config.get('ORIGINAL_CAM_URL_ENTRANCE')
        config['CAM_URL_EXIT'] = config.get('ORIGINAL_CAM_URL_EXIT')
        config['API_KEY_SLT'] = config.get('ORIGINAL_API_KEY_SLT')
        config['API_USER_SLT'] = config.get('ORIGINAL_API_USER_SLT')
        config['API_DD_SLT'] = config.get('ORIGINAL_API_DD_SLT')
        
        # Save the restored config
        save_config(config, file_path)
        
        # Update the GUI fields with the restored values
        camera_IN_url.delete(0, tk.END)
        camera_IN_url.insert(0, config['CAM_URL_ENTRANCE'])
        
        camera_OUT_url.delete(0, tk.END)
        camera_OUT_url.insert(0, config['CAM_URL_EXIT'])
        
        api_key_entry.delete(0, tk.END)
        api_key_entry.insert(0, config['API_KEY_SLT'])
        
        api_user_entry.delete(0, tk.END)
        api_user_entry.insert(0, config['API_USER_SLT'])
        
        api_dd_entry.delete(0, tk.END)
        api_dd_entry.insert(0, config['API_DD_SLT'])

        update_display("Default values are saved again successfully.")




    # Function to save YAML configuration
    def save_changes():
        config = load_config(file_path)
        
        # Update USER values based on the current inputs
        config['CAM_URL_ENTRANCE'] = camera_IN_url.get()
        config['CAM_URL_EXIT'] = camera_OUT_url.get()
        config['API_KEY_SLT'] = api_key_entry.get()
        config['API_USER_SLT'] = api_user_entry.get()
        config['API_DD_SLT'] = api_dd_entry.get()
        
        # Save the updated config
        save_config(config, file_path)

        update_display("Input values saved successfully.")


    # Save Button
    save_button = tk.Button(config_frame, text="Save", command=save_changes, bg=btn_bg_color, fg=btn_fg_color)
    save_button.grid(row=5, column=0, sticky='ew', padx=10, pady=20)  # Corrected 'pday' to 'pady'

    # Restore Button
    restore_button = tk.Button(config_frame, text="Restore", command=restore_changes, bg=btn_bg_color, fg=btn_fg_color)
    restore_button.grid(row=5, column=1, sticky='ew', pady=10, padx=20)

    # Footer LOGO and other details
    logo_frame = tk.Frame(settings_window, bg=bg_color)
    logo_frame.pack(side='bottom', fill='x', padx=20)
    logo_frame.rowconfigure(0, weight=1)
    logo_frame.columnconfigure(0, weight=1)
    logo_frame.columnconfigure(1, weight=1)
    logo_frame.columnconfigure(2, weight=1)

    footer_frame = tk.Frame(logo_frame, bg=bg_color)
    footer_frame_2 = tk.Frame(logo_frame, bg=bg_color)
    footer_frame.grid(row=0, column=0, sticky='ew', pady=10)
    footer_frame_2.grid(row=0, column=1, sticky='ew', pady=10)
    footer_frame_3 = tk.Frame(logo_frame, bg=bg_color)
    footer_frame_3.grid(row=0, column=2, sticky='ew', pady=10)

    try:
        # Load and resize logos
        logo1_img = Image.open(logo1_path).convert("RGBA")
        logo2_img = Image.open(logo2_path).convert("RGBA")
        logo3_img = Image.open(logo3_path).convert("RGBA")

        logo1_img = logo1_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed
        logo2_img = logo2_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed
        logo3_img = logo3_img.resize((100, 75), Image.ANTIALIAS)  # Resize as needed

        # Convert to ImageTk.PhotoImage
        logo1_photo = ImageTk.PhotoImage(logo1_img)
        logo2_photo = ImageTk.PhotoImage(logo2_img)
        logo3_photo = ImageTk.PhotoImage(logo3_img)

        # Create labels for logos and text
        logo1_label = tk.Label(footer_frame, image=logo1_photo, bg=bg_color)
        logo1_label.image = logo1_photo  # Keep a reference to the image
        logo2_label = tk.Label(footer_frame_2, image=logo2_photo, bg=bg_color)
        logo2_label.image = logo2_photo  # Keep a reference to the image
        logo3_label = tk.Label(footer_frame_3, image=logo3_photo, bg=bg_color)
        logo3_label.image = logo3_photo  # Keep a reference to the image

        # Create a container frame to center the logos
        logo_container = tk.Frame(footer_frame)
        logo_container.pack(expand=True)  # Expand to fill available space

        # Pack the logos into the container frame horizontally centered
        logo1_label.pack(side='right', padx=10)
        logo2_label.pack(side='top', padx=10)
        logo3_label.pack(side='left', padx=15)

        # Pack the container frame into the footer frame
        logo_container.pack()

        print("Footer logos and text loaded successfully.")
    except Exception as e:
        print(f"Error loading footer logos: {e}")

    return settings_window

