import tkinter as tk
import sys
import subprocess
import threading
import psutil
import os
import signal
from PIL import Image, ImageTk
import yaml
import requests
import time




class ConsoleText(tk.Text):
    def write(self, msg):
        self.insert(tk.END, msg)
        self.see(tk.END)
    def flush(self):
        pass

def create_gui():
    root = tk.Tk()
    root.title("Visage GUI")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.resizable(True, True)

    for i in range(10):
        root.grid_rowconfigure(i, weight=1)
    for j in range(4):
        root.grid_columnconfigure(j, weight=1)

    def run_in_thread(target):
        thread = threading.Thread(target=target)
        thread.start()
    
    # Setting the app icon into the window
    # app icon path declaration
    
    icon_path = "images/icon.png"

    try:
        icon_image = Image.open(icon_path)  # Load the icon image
        icon = ImageTk.PhotoImage(icon_image)
        root.iconphoto(True, icon)  # Set the loaded image as the icon
    except Exception as e:
        print(f"Error loading icon: {e}")

    # Color Palette
    bg_color = "lightgray"#"#666666" #background color
    frame_bg_color = "#505050"# setting frame background
    display_bg_color = "#C5E8FC" #color for display
    common_btn = "#0097b2" #after button clicked
    common_btn_clicked = "#286EB1"
    stop_btn="#ff3131"
    font = ('Arial', 16, 'bold')
    font_fg = "#121212"
    btn_fg = "#ffffff"
    title_bg = "lightgray"
    text_fg_color = "#121212"
    
    console_output = ConsoleText(root, height=18, width=0, bg=display_bg_color, fg=text_fg_color, font=("Helvetica", 12), wrap=tk.WORD)
    console_output.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=25, pady=0)
    console_output.config(state=tk.DISABLED)

    status_label = tk.Label(root, text="Server Status: ", font=("Helvetica", 12))
    status_label.grid(row=0, column=0, sticky="w", padx=25, pady=15)
    # Create a canvas for the round status icon
    status_canvas = tk.Canvas(root, width=20, height=20, highlightthickness=0)
    status_canvas.grid(row=0, column=0, sticky="w", padx=140, pady=15)

    # Draw a round status icon (initially gray)
    status_icon = status_canvas.create_oval(2, 2, 18, 18, fill="gray")

    def check_server(url, interval=5):
        """
        Continuously checks if the server is working.
        
        Args:
            url (str): The URL of the server to check.
            interval (int): Time interval (in seconds) between checks.
        """
        while True:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    #print("Server works fine.")
                    status_canvas.itemconfig(status_icon, fill="green")
                    
                else:
                    print(f"Server is not working. Status code: {response.status_code}")
                    status_canvas.itemconfig(status_icon, fill="red")
            except requests.exceptions.RequestException as e:
                print("Server is not working. Error:", e)
                status_canvas.itemconfig(status_icon, fill="red")
            
            time.sleep(interval)  # Wait for the specified interval before checking again


    def check_server_status():
        url = "https://ientrada.raccoon-ai.io/api"
        check_server(url, interval=5)
    
    

    run_in_thread(check_server_status)
    

    def write(msg):
        console_output.config(state=tk.NORMAL)
        console_output.insert(tk.END, msg)
        console_output.config(state=tk.DISABLED)
        console_output.see(tk.END)

    console_output.write = write
    sys.stdout = console_output

    frame_main = tk.Frame(root)
    frame_chklst = tk.Frame(root)

    def main():
        frame_chklst.grid_forget()
        frame_main.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        main_button.config(bg=common_btn_clicked)
        checklist_button.config(bg=common_btn)
        

    def chklst():
        frame_main.grid_forget()
        frame_chklst.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        main_button.config(bg=common_btn)
        checklist_button.config(bg=common_btn_clicked)
        
        
    
    
    def clear_console(message):
        console_output.config(state=tk.NORMAL)
        console_output.delete('1.0', tk.END)
        console_output.config(state=tk.DISABLED)
        
        button_chk_int_stat_t.config(bg="lightgray")
        button_chk_int_stat_f.config(bg="lightgray")
        button_chk_api_stat_t.config(bg="lightgray")
        button_chk_api_stat_f.config(bg="lightgray")
        button_chk_cam1_stat_t.config(bg="lightgray")
        button_chk_cam1_stat_f.config(bg="lightgray")
        button_chk_cam2_stat_t.config(bg="lightgray")
        button_chk_cam2_stat_f.config(bg="lightgray")

    def settings():
        if hasattr(settings, 'popup') and settings.popup.winfo_exists():
            settings.popup.lift()
            return
        
        # Initialize config
        try:
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f) or {}
        except FileNotFoundError:
            config = {
                'server': {'url': '', 'username': '', 'api_key': ''},
                'camera': {'entrance_url': '', 'exit_url': ''},
                'RPI_ENABLE': 0
            }
        except Exception as e:
            print(f"Error loading config: {e}")
            config = {
                'server': {'url': '', 'username': '', 'api_key': ''},
                'camera': {'entrance_url': '', 'exit_url': ''},
                'RPI_ENABLE': 0
            }

        settings.popup = tk.Toplevel(root)
        settings.popup.title("Settings")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        settings.popup.geometry(f"{screen_width}x{screen_height}")
        
        # Configure grid
        settings.popup.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = tk.Label(settings.popup, text="Settings", font=font)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Text boxes with titles
        tk.Label(settings.popup, text="Server Url:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        text_box1 = tk.Entry(settings.popup, width=70, font=("Helvetica", 14))
        text_box1.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        text_box1.insert(0, config.get('server', {}).get('url', ''))

        tk.Label(settings.popup, text="Server Username:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        text_box2 = tk.Entry(settings.popup, width=50, font=("Helvetica", 14))
        text_box2.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        text_box2.insert(0, config.get('server', {}).get('username', ''))

        tk.Label(settings.popup, text="API Key:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        text_box3 = tk.Entry(settings.popup, width=50, font=("Helvetica", 14))
        text_box3.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        text_box3.insert(0, config.get('server', {}).get('api_key', ''))

        tk.Label(settings.popup, text="Entrance Camera Url:", font=("Helvetica", 12)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        text_box4 = tk.Entry(settings.popup, width=50, font=("Helvetica", 14))
        text_box4.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        text_box4.insert(0, config.get('camera', {}).get('entrance_url', ''))

        tk.Label(settings.popup, text="Exit Camera Url:", font=("Helvetica", 12)).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        text_box5 = tk.Entry(settings.popup, width=50, font=("Helvetica", 14))
        text_box5.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        text_box5.insert(0, config.get('camera', {}).get('exit_url', ''))

        # Dropdown for logging
        tk.Label(settings.popup, text="Logging:", font=("Helvetica", 12)).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        logging_var = tk.StringVar(settings.popup)
        initial_logging = "Enable" if config.get('logging', "false") == "true" else "Disable"
        logging_var.set(initial_logging)
        logging_dropdown = tk.OptionMenu(settings.popup, logging_var, "Enable", "Disable")
        logging_dropdown.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        def save_url():
            try:
                config['server']['url'] = text_box1.get()
                config['server']['username'] = text_box2.get()
                config['server']['api_key'] = text_box3.get()
                config['camera']['entrance_url'] = text_box4.get()
                config['camera']['exit_url'] = text_box5.get()
                config['logging'] = "true" if logging_var.get() == "Enable" else "false"
                
                with open('config.yaml', 'w') as f:
                    yaml.dump(config, f)
                settings.popup.destroy()
                print("Settings saved successfully")
            except Exception as e:
                print(f"Error saving config: {e}")

        def close_popup():
            settings.popup.destroy()

        # Save button
        save_button = tk.Button(settings.popup, text="Save", width=20, height=2, command=save_url)
        save_button.grid(row=7, column=0,  pady=20, padx=15, sticky="w")

        # Close button
        close_button = tk.Button(settings.popup, text="Back", width=20, height=2, command=close_popup)
        close_button.grid(row=7, column=1,  pady=20, padx=15, sticky="w")

    main_button = tk.Button(root, text="Main", width=25, height=2, command=main, bg=common_btn_clicked, font=font, fg=btn_fg)
    main_button.grid(row=2, column=0, padx=0, pady=25)

    checklist_button = tk.Button(root, text="Checklist", width=25, height=2, command=chklst, bg=common_btn, font = font, fg=btn_fg)
    checklist_button.grid(row=2, column=1, padx=0, pady=0)

    settings_button = tk.Button(root, text="Settings", width=25, height=2, command=settings, bg=common_btn, font = font, fg=btn_fg)
    settings_button.grid(row=2, column=2, padx=0, pady=0)

    clear_button = tk.Button(root, text="Clear", width=25, height=2, command=lambda: clear_console(""), bg=common_btn, font = font, fg=btn_fg)
    clear_button.grid(row=2, column=3, padx=0, pady=0)

    #================================ Main Frame ====================================

    frame_main = tk.Frame(root)
    frame_main.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=10, pady=30)

    for i in range(5):
        frame_main.grid_rowconfigure(i, weight=1)
    for j in range(20):
        frame_main.grid_columnconfigure(j, weight=1)

    # Add a title above the buttons
    title_label = tk.Label(frame_main, text="Main", font=font, bg=title_bg)
    title_label.grid(row=0, column=0, columnspan=20, sticky="nsew", padx=0, pady=0)

    verify_face_button = tk.Button(frame_main, text="Start", font=font, width=30, height=2, bg=common_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: verify_face(check_internet_button, "Starting Verification...")))
    verify_face_button.grid(row=3, column=8, pady=20)
    stop_verify_face_button = tk.Button(frame_main, text="Stop", font=font, width=30, height=2, bg=stop_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: stop_verify_face(check_internet_button, "Program Stopping...")))
    stop_verify_face_button.grid(row=3, column=11, pady=20)

    # Load the image
    image_path = "images/embryo.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((200, 100), Image.LANCZOS)  # Resize the image to fit the grid
    photo = ImageTk.PhotoImage(image)

    image_path1 = "images/visage.png"  # Replace with the path to your image
    image1 = Image.open(image_path1)
    image1 = image1.resize((200, 150), Image.LANCZOS)  # Resize the image to fit the grid
    photo1 = ImageTk.PhotoImage(image1)

    image_path2 = "images/SLT_Mobitel.png"  # Replace with the path to your image
    image2 = Image.open(image_path2)
    image2 = image2.resize((200, 80), Image.LANCZOS)  # Resize the image to fit the grid
    photo2 = ImageTk.PhotoImage(image2)

    # Create a label to display the image
    image_label = tk.Label(frame_main, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.grid(row=5, column=3, columnspan=5, pady=0)

    # Create a label to display the image
    image1_label = tk.Label(frame_main, image=photo1)
    image1_label.image = photo1  # Keep a reference to avoid garbage collection
    image1_label.grid(row=5, column=8, columnspan=4, pady=0)

    # Create a label to display the image
    image2_label = tk.Label(frame_main, image=photo2)
    image2_label.grid(row=5, column=12, columnspan=5, pady=0)

    def verify_face(button, message):
        print(message)

        def stream_output():
            process = subprocess.Popen(
                ['python', 'verifyFaceNew.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered output
            )

            for line in process.stdout:
                print(line.strip())  # Print each line in real time

            process.stdout.close()
            process.wait()

        run_in_thread(stream_output)

    def stop_verify_face(button, message):
        print("Program Stopping...")
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['cmdline'] and 'python' in proc.info['name'] and 'verifyFaceNew.py' in proc.info['cmdline']:
                    print(f"Program Interrupted (PID: {proc.info['pid']})")
                    os.kill(proc.info['pid'], signal.SIGTERM)  # Gracefully terminate the process
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        print("Program is not running.")

    #================================ Test Cases Frame ==============================

    for i in range(5):
        frame_chklst.grid_rowconfigure(i, weight=1)
    for j in range(20):
        frame_chklst.grid_columnconfigure(j, weight=1)

    # Add a title above the buttons
    title_label = tk.Label(frame_chklst, text="Test Cases", bg=title_bg, font=font)
    title_label.grid(row=0, column=0, columnspan=20, sticky="nsew", padx=0, pady=0)

    # test title
    # Load the image
    image_path = "images/correct.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((30, 30), Image.LANCZOS)  # Resize the image to fit the grid
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(frame_chklst, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.grid(row=2, column=7,pady=0)

    # Load the image
    image_path = "images/wrong.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((30, 30), Image.LANCZOS)  # Resize the image to fit the grid
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(frame_chklst, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.grid(row=2, column=8,pady=0)

    # Load the image
    image_path = "images/correct.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((30, 30), Image.LANCZOS)  # Resize the image to fit the grid
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(frame_chklst, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.grid(row=2, column=12,pady=0)

    # Load the image
    image_path = "images/wrong.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((30, 30), Image.LANCZOS)  # Resize the image to fit the grid
    photo = ImageTk.PhotoImage(image)

    # Create a label to display the image
    image_label = tk.Label(frame_chklst, image=photo)
    image_label.image = photo  # Keep a reference to avoid garbage collection
    image_label.grid(row=2, column=13,pady=0)

    check_internet_button = tk.Button(frame_chklst, text="Check Internet", font=font, width=30, height=2, bg=common_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: chk_int(check_internet_button, "Checking Internet Connection...")))
    check_internet_button.grid(row=3, column=6, pady=10)
    button_chk_int_stat_t = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_int_stat_t.grid(row=3, column=7, padx=0, pady=0)
    button_chk_int_stat_f = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_int_stat_f.grid(row=3, column=8, padx=0, pady=0)

    check_cam1_button = tk.Button(frame_chklst, text="Check Camera Entrance", font=font, width=30, height=2, bg=common_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: chk_cam1(check_cam1_button, "")))
    check_cam1_button.grid(row=3, column=11, padx=0, pady=0)
    button_chk_cam1_stat_t = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_cam1_stat_t.grid(row=3, column=12, padx=0, pady=0)
    button_chk_cam1_stat_f = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_cam1_stat_f.grid(row=3, column=13, padx=0, pady=0)

    check_api_button = tk.Button(frame_chklst, text="Check API", font=font, width=30, height=2, bg=common_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: chk_api(check_api_button, "")))
    check_api_button.grid(row=5, column=6, padx=0, pady=10)
    button_chk_api_stat_t = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_api_stat_t.grid(row=5, column=7, padx=0, pady=0)
    button_chk_api_stat_f = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_api_stat_f.grid(row=5, column=8, padx=0, pady=0)

    check_cam2_button = tk.Button(frame_chklst, text="Check Camera Exit", font=font, width=30, height=2, bg=common_btn, fg=btn_fg, command=lambda: run_in_thread(lambda: chk_cam2(check_cam2_button, "")))
    check_cam2_button.grid(row=5, column=11, padx=0, pady=0)
    button_chk_cam2_stat_t = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_cam2_stat_t.grid(row=5, column=12, padx=0, pady=0)
    button_chk_cam2_stat_f = tk.Button(frame_chklst, width=5, bg="lightgray", height=2, state=tk.DISABLED)
    button_chk_cam2_stat_f.grid(row=5, column=13, padx=0, pady=0)

    def chk_int(button, message):
        print(message)
        if button.cget('state') == tk.NORMAL:
            button.config(state=tk.DISABLED)
            button.after(5000, lambda: button.config(state=tk.NORMAL))
            result = subprocess.run(['python', 'test_cases/check_internet.py'], capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if output == 'Internet is connected':
                button_chk_int_stat_t.config(bg="green")
                button_chk_int_stat_f.config(bg="lightgray")
            else:
                button_chk_int_stat_f.config(bg="red")
                button_chk_int_stat_t.config(bg="lightgray")
        else:
            button.config(state=tk.NORMAL)

    def chk_api(button, message):
        print("Checking API Connection...")
        if button.cget('state') == tk.NORMAL:
            button.config(state=tk.DISABLED)
            button.after(5000, lambda: button.config(state=tk.NORMAL))
            result = subprocess.run(['python', 'test_cases/api_test.py'], capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if output == 'API is functioning properly':
                button_chk_api_stat_t.config(bg="green")
                button_chk_api_stat_f.config(bg="lightgray")
            else:
                button_chk_api_stat_f.config(bg="red")
                button_chk_api_stat_t.config(bg="lightgray")
        else:
            button.config(state=tk.NORMAL)

    def chk_cam1(button, message):
        print("Checking Camera [Entrance]...")
        if button.cget('state') == tk.NORMAL:
            button.config(state=tk.DISABLED)
            button.after(5000, lambda: button.config(state=tk.NORMAL))
            result = subprocess.run(['python', 'test_cases/camera_test.py'], capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if output == 'Entrance Camera is connected':
                button_chk_cam1_stat_t.config(bg="green")
                button_chk_cam1_stat_f.config(bg="lightgray")
            else:
                button_chk_cam1_stat_f.config(bg="red")
                button_chk_cam1_stat_t.config(bg="lightgray")
        else:
            button.config(state=tk.NORMAL)

    def chk_cam2(button, message):
        print("Checking Camera [Exit]...")
        if button.cget('state') == tk.NORMAL:
            button.config(state=tk.DISABLED)
            button.after(5000, lambda: button.config(state=tk.NORMAL))
            result = subprocess.run(['python', 'test_cases/check_camera_out.py'], capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            if output == 'Exit Camera is connected':
                button_chk_cam2_stat_t.config(bg="green")
                button_chk_cam2_stat_f.config(bg="lightgray")
            else:
                button_chk_cam2_stat_f.config(bg="red")
                button_chk_cam2_stat_t.config(bg="lightgray")
        else:
            button.config(state=tk.NORMAL)

    #================================ Settings ====================================

    # Run the main loop
    root.mainloop()

def main():
    create_gui()
    

if __name__ == "__main__":
    main()