import sys
import subprocess
import os
import ctypes
import site

def get_user_site_packages():
    """Get the user site-packages directory"""
    return site.getusersitepackages()

def install_package():
    try:
        print("Attempting to install monitorcontrol package...")
        user_site = get_user_site_packages()
        print(f"Installing to user site-packages: {user_site}")
        
        # First try to upgrade pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--user"])
            print("Pip upgraded successfully")
        except Exception as e:
            print(f"Warning: Could not upgrade pip: {e}")

        # Install monitorcontrol
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--no-cache-dir", "monitorcontrol"])
        print("Package installed successfully")
        
        # Add user site-packages to Python path if not already there
        if user_site not in sys.path:
            sys.path.append(user_site)
            print(f"Added {user_site} to Python path")
            
    except Exception as e:
        print(f"Error installing package: {str(e)}")
        print("\nTrying alternative installation method...")
        try:
            os.system(f'"{sys.executable}" -m pip install --user --no-cache-dir monitorcontrol')
            if user_site not in sys.path:
                sys.path.append(user_site)
            print("Alternative installation completed")
        except Exception as e2:
            print(f"Alternative installation failed: {str(e2)}")
            raise

print("Starting script...")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current Python path: {sys.path}")
print("Importing required modules...")

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    print("Tkinter imported successfully")
    
    print("Attempting to import monitorcontrol...")
    try:
        import monitorcontrol
        print("Monitorcontrol imported successfully")
    except ImportError as e:
        print(f"Import error details: {str(e)}")
        print("Monitorcontrol not found. Installing...")
        install_package()
        print("Installation complete. Importing monitorcontrol...")
        import monitorcontrol
        print("Monitorcontrol imported successfully")
    
    import threading
    import time
    print("All modules imported successfully")

except Exception as e:
    print(f"Error during setup: {str(e)}")
    print(f"Current Python path: {sys.path}")
    input("Press Enter to exit...")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class BrightnessController:
    def __init__(self):
        try:
            print("Initializing BrightnessController...")
            self.root = tk.Tk()
            self.root.title("Brightness")
            self.root.geometry("320x240")  # Increased height slightly for status label
            self.root.resizable(False, False)

            # Material Design colors
            bg_color = '#121212'  # Material dark background
            text_color = '#E1E1E1'  # Material text color
            
            self.root.configure(bg=bg_color)
            
            # Configure styles
            style = ttk.Style()
            style.theme_use('default')
            
            # Configure slider style
            style.configure(
                'Material.Horizontal.TScale',
                background=bg_color,
                troughcolor='#333333',
                borderwidth=0,
                lightcolor='#666666',
                darkcolor='#666666',
                sliderthickness=16,
                sliderlength=12
            )
            
            # Configure button style
            style.configure(
                'Material.TButton',
                background=bg_color,
                foreground=text_color,
                borderwidth=1,
                relief='solid',
                padding=(12, 6),
                font=('Segoe UI', 9)
            )
            
            style.map(
                'Material.TButton',
                background=[('active', bg_color)],
                foreground=[('active', text_color)],
                bordercolor=[('active', text_color)]
            )
            
            # Configure label style
            style.configure(
                'Material.TLabel',
                background=bg_color,
                foreground=text_color,
                font=('Segoe UI', 10)
            )

            # Configure frame style
            style.configure(
                'Material.TFrame',
                background=bg_color
            )

            # Create main frame with padding
            self.main_frame = ttk.Frame(self.root, padding="15", style='Material.TFrame')
            self.main_frame.pack(fill=tk.BOTH, expand=True)

            # Title with minimal style
            title_label = ttk.Label(
                self.main_frame,
                text="Brightness Control",
                style='Material.TLabel',
                font=('Segoe UI', 14)
            )
            title_label.pack(pady=(0, 15))

            # Current brightness value with large display
            self.value_label = ttk.Label(
                self.main_frame,
                text="50%",
                style='Material.TLabel',
                font=('Segoe UI', 24, 'bold')
            )
            self.value_label.pack(pady=(0, 15))

            # Brightness slider
            self.brightness_var = tk.IntVar(value=50)
            self.brightness_slider = ttk.Scale(
                self.main_frame,
                from_=0,
                to=100,
                orient=tk.HORIZONTAL,
                variable=self.brightness_var,
                style='Material.Horizontal.TScale'
            )
            self.brightness_slider.pack(fill=tk.X, pady=(0, 15))

            # Buttons frame
            self.button_frame = ttk.Frame(self.main_frame, style='Material.TFrame')
            self.button_frame.pack(fill=tk.X)

            # Center frame for buttons
            center_frame = ttk.Frame(self.button_frame, style='Material.TFrame')
            center_frame.pack(expand=True)

            # Apply button
            self.apply_button = ttk.Button(
                center_frame,
                text="Apply",
                command=lambda: self.update_brightness(self.brightness_var.get()),
                style='Material.TButton'
            )
            self.apply_button.pack(side=tk.LEFT, padx=(0, 8))

            # Reset button
            self.reset_button = ttk.Button(
                center_frame,
                text="Reset",
                command=self.reset_brightness,
                style='Material.TButton'
            )
            self.reset_button.pack(side=tk.LEFT)

            # Status label with more space
            self.status_label = ttk.Label(
                self.main_frame,
                text="",  # Start with empty status
                style='Material.TLabel',
                font=('Segoe UI', 9),
                wraplength=290  # Allow text to wrap if needed
            )
            self.status_label.pack(pady=(15, 0))

            # Initialize monitor control
            print("Initializing monitor control...")
            self.monitors = list(monitorcontrol.get_monitors())
            if not self.monitors:
                raise Exception("No compatible monitors found. Make sure DDC/CI is enabled in your monitor settings.")
            
            print(f"Found {len(self.monitors)} monitor(s)")
            
            # Get current brightness
            with self.monitors[0] as monitor:
                self.original_brightness = monitor.get_luminance()
                print(f"Current brightness: {self.original_brightness}")
                self.brightness_var.set(self.original_brightness)
                self.value_label.config(text=f"{self.original_brightness}%")

            self.update_thread = None

        except Exception as e:
            error_msg = f"Error initializing: {str(e)}\n\nPlease make sure:\n1. You're running as administrator\n2. DDC/CI is enabled in monitor settings\n3. Monitor supports DDC/CI"
            print(error_msg)
            messagebox.showerror("Error", error_msg)
            raise

    def adjust_brightness(self, delta):
        new_value = min(100, max(0, self.brightness_var.get() + delta))
        self.brightness_var.set(new_value)
        self.value_label.config(text=f"{new_value}%")  # Update display only

    def update_brightness(self, value):
        try:
            brightness = int(float(value))
            self.value_label.config(text=f"{brightness}%")
            
            # Start new update thread
            self.update_thread = threading.Thread(
                target=self.set_brightness,
                args=(brightness,)
            )
            self.update_thread.start()

        except Exception as e:
            error_msg = f"Error updating brightness: {str(e)}"
            print(error_msg)
            self.status_label.config(text=error_msg, foreground='#CF6679')

    def set_brightness(self, brightness):
        try:
            with self.monitors[0] as monitor:
                monitor.set_luminance(brightness)
            self.status_label.config(text="Updated successfully", foreground='#03DAC6')
            
        except Exception as e:
            error_msg = f"Error setting brightness: {str(e)}"
            print(error_msg)
            self.status_label.config(text=error_msg, foreground='#CF6679')

    def reset_brightness(self):
        """Reset brightness to original value"""
        try:
            self.brightness_var.set(self.original_brightness)
            self.update_brightness(self.original_brightness)
        except Exception as e:
            error_msg = f"Error resetting brightness: {str(e)}"
            print(error_msg)
            self.status_label.config(text=error_msg, foreground='#CF6679')

    def run(self):
        print("Starting application...")
        self.root.mainloop()

if __name__ == "__main__":
    print("Checking administrator privileges...")
    if not is_admin():
        print("Script needs to be run as administrator!")
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    print("Running with administrator privileges...")
    try:
        print("Starting brightness controller...")
        app = BrightnessController()
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        input("Press Enter to exit...") 