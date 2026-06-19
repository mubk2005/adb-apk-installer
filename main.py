import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import threading

class ADBInstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB APK Installer")
        self.root.geometry("700x600")
        
        # Variable to store APK file path
        self.apk_path_var = tk.StringVar()
        
        # Check ADB availability
        self.adb_path = self.check_adb()
        
        # Create GUI widgets
        self.create_widgets()
        
        # Show ADB status
        if self.adb_path:
            self.log_message(f"✓ ADB found: {self.adb_path}")
        else:
            self.log_message("✗ ADB not found! Please install ADB first.")
            self.log_message("  Run: sudo apt install adb")
        
    def check_adb(self):
        """Check if adb is available on the system"""
        try:
            # Check if adb is in PATH
            result = subprocess.run(["which", "adb"], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            
            # Check common locations
            common_paths = [
                "/usr/bin/adb",
                "/usr/local/bin/adb",
                "/usr/lib/android-sdk/platform-tools/adb"
            ]
            
            for path in common_paths:
                if os.path.exists(path):
                    return path
                    
            return None
        except:
            return None
        
    def run_adb_command(self, command):
        """Execute an ADB command"""
        if not self.adb_path:
            return "Error: ADB not found!"
        
        # Replace 'adb' with full path if needed
        if command[0] == "adb":
            command[0] = self.adb_path
            
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error executing command: {e}"
            
    def create_widgets(self):
        # Title Label
        title_label = tk.Label(self.root, text="ADB APK Installer", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame for device connection
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=5)
        
        self.connection_status_label = tk.Label(connection_frame, text="Device Status: Unknown", fg="orange")
        self.connection_status_label.pack(side=tk.LEFT, padx=5)
        
        btn_test_connection = tk.Button(connection_frame, text="Test Connection", command=self.test_connection, bg="blue", fg="white")
        btn_test_connection.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator1 = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN)
        separator1.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame for file selection
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        
        lbl_path = tk.Label(file_frame, text="APK File Path:")
        lbl_path.pack(side=tk.LEFT)
        
        entry_path = tk.Entry(file_frame, textvariable=self.apk_path_var, width=40)
        entry_path.pack(side=tk.LEFT, padx=5)
        
        btn_browse = tk.Button(file_frame, text="Browse", command=self.browse_apk)
        btn_browse.pack(side=tk.LEFT)
        
        # Separator
        separator2 = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN)
        separator2.pack(fill=tk.X, padx=5, pady=5)
        
        # Installation options frame
        options_frame = tk.LabelFrame(self.root, text="Installation Options", padx=10, pady=10)
        options_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Checkbox for bypass low target SDK
        self.bypass_sdk_var = tk.BooleanVar(value=True)
        chk_bypass_sdk = tk.Checkbutton(
            options_frame, 
            text="Bypass Low Target SDK Block (for old apps)", 
            variable=self.bypass_sdk_var,
            font=("Arial", 9)
        )
        chk_bypass_sdk.pack(anchor=tk.W)
        
        # Checkbox for test packages
        self.allow_test_var = tk.BooleanVar(value=False)
        chk_allow_test = tk.Checkbutton(
            options_frame, 
            text="Allow Test Packages (-t)", 
            variable=self.allow_test_var,
            font=("Arial", 9)
        )
        chk_allow_test.pack(anchor=tk.W)
        
        # Checkbox for grant permissions
        self.grant_perms_var = tk.BooleanVar(value=False)
        chk_grant_perms = tk.Checkbutton(
            options_frame, 
            text="Grant All Permissions (-g)", 
            variable=self.grant_perms_var,
            font=("Arial", 9)
        )
        chk_grant_perms.pack(anchor=tk.W)
        
        # Frame for install buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        btn_install = tk.Button(button_frame, text="Install APK", command=self.start_install, bg="green", fg="white", width=15)
        btn_install.pack(side=tk.LEFT, padx=5)
        
        btn_install_downgrade = tk.Button(button_frame, text="Install (Downgrade)", command=lambda: self.start_install(allow_downgrade=True), bg="orange", fg="white", width=20)
        btn_install_downgrade.pack(side=tk.LEFT, padx=5)
        
        # Separator
        separator3 = tk.Frame(self.root, height=2, bd=1, relief=tk.SUNKEN)
        separator3.pack(fill=tk.X, padx=5, pady=5)
        
        # Output area
        output_label = tk.Label(self.root, text="Output Log:")
        output_label.pack(anchor=tk.W, padx=10)
        
        self.output_text = scrolledtext.ScrolledText(self.root, height=12, state='disabled')
        self.output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
    def browse_apk(self):
        """Open file dialog to select APK file"""
        filename = filedialog.askopenfilename(title="Select APK File", filetypes=[("APK files", "*.apk")])
        if filename:
            self.apk_path_var.set(filename)
            
    def log_message(self, message):
        """Add message to output area"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.output_text.config(state='disabled')
        self.root.update_idletasks()
        
    def check_device(self):
        """Check if a device is connected"""
        output = self.run_adb_command(["adb", "devices"])
        lines = output.strip().split('\n')
        
        if len(lines) < 2:
            return False, "No output from adb devices"
            
        device_found = False
        for line in lines[1:]:
            if line.strip() and "\tdevice" in line:
                device_found = True
                break
                
        if device_found:
            return True, "Device connected successfully"
        else:
            return False, "No device found. Please enable USB Debugging"
            
    def test_connection(self):
        """Test device connection and show result"""
        self.log_message("=" * 50)
        self.log_message("Testing device connection...")
        
        if not self.adb_path:
            self.log_message("✗ ADB not found! Please install ADB first.")
            self.log_message("  Run: sudo apt install adb")
            return
        
        is_connected, message = self.check_device()
        
        if is_connected:
            self.connection_status_label.config(text="Device Status: Connected ✓", fg="green")
            self.log_message("✓ " + message)
            # Get more device info
            device_info = self.run_adb_command(["adb", "shell", "getprop", "ro.product.model"])
            if device_info.strip():
                self.log_message(f"Device Model: {device_info.strip()}")
            android_version = self.run_adb_command(["adb", "shell", "getprop", "ro.build.version.release"])
            if android_version.strip():
                self.log_message(f"Android Version: {android_version.strip()}")
        else:
            self.connection_status_label.config(text="Device Status: Not Connected ✗", fg="red")
            self.log_message("✗ " + message)
            self.log_message("Troubleshooting tips:")
            self.log_message("1. Enable USB Debugging on your phone")
            self.log_message("2. Connect via USB cable")
            self.log_message("3. Accept the permission prompt on your phone")
            
        self.log_message("=" * 50)
        
    def install_apk(self, apk_path, allow_downgrade=False):
        """Install APK on device with various options"""
        if not os.path.exists(apk_path):
            return "APK file not found!"
        
        if not self.adb_path:
            return "ADB not found!"
            
        # Build command with options
        command = ["adb", "install"]
        
        # Add options based on parameters
        if allow_downgrade:
            command.append("-d")
            
        # Add -r for replace
        command.append("-r")
        
        # Check if bypass low target SDK is selected
        if self.bypass_sdk_var.get():
            command.append("--bypass-low-target-sdk-block")
            
        # Check if allow test packages is selected
        if self.allow_test_var.get():
            command.append("-t")
            
        # Check if grant permissions is selected
        if self.grant_perms_var.get():
            command.append("-g")
            
        command.append(apk_path)
        
        self.log_message(f"Command: {' '.join(command)}")
        
        return self.run_adb_command(command)
        
    def start_install(self, allow_downgrade=False):
        """Start installation in a separate thread"""
        thread = threading.Thread(target=self.perform_install, args=(allow_downgrade,))
        thread.daemon = True
        thread.start()
        
    def perform_install(self, allow_downgrade=False):
        """Perform the actual installation process"""
        self.log_message("=" * 50)
        self.log_message("Starting installation process...")
        
        if not self.adb_path:
            self.log_message("✗ Error: ADB not found!")
            messagebox.showerror("ADB Error", "ADB not found!\nPlease install ADB first:\nsudo apt install adb")
            return
        
        # Check device connection first
        is_connected, msg = self.check_device()
        if not is_connected:
            self.log_message(f"✗ Error: {msg}")
            self.connection_status_label.config(text="Device Status: Not Connected ✗", fg="red")
            messagebox.showerror("Connection Error", "No device connected!\nPlease connect your device and test connection first.")
            return
            
        self.log_message("✓ Device connected")
        self.connection_status_label.config(text="Device Status: Connected ✓", fg="green")
        
        # Check if APK file is selected
        apk_path = self.apk_path_var.get()
        if not apk_path:
            self.log_message("✗ Error: Please select an APK file")
            messagebox.showerror("Error", "Please select an APK file first.")
            return
            
        self.log_message(f"APK file: {os.path.basename(apk_path)}")
        
        if allow_downgrade:
            self.log_message("Installing with downgrade option (-d)...")
        else:
            self.log_message("Installing with replace option (-r)...")
            
        if self.bypass_sdk_var.get():
            self.log_message("Bypass low target SDK block enabled")
            
        if self.allow_test_var.get():
            self.log_message("Allow test packages enabled")
            
        if self.grant_perms_var.get():
            self.log_message("Grant all permissions enabled")
            
        self.log_message("Installing...")
        result = self.install_apk(apk_path, allow_downgrade)
        
        self.log_message("--- Installation Output ---")
        self.log_message(result)
        self.log_message("---------------------------")
        
        if "Success" in result:
            self.log_message("✓ Installation completed successfully!")
            messagebox.showinfo("Success", "APK installed successfully!")
        elif "INSTALL_FAILED_ALREADY_EXISTS" in result:
            self.log_message("⚠ App already exists. Try using 'Install (Downgrade)' button for older versions.")
            messagebox.showwarning("Already Exists", "App already installed.\nUse 'Install (Downgrade)' for older versions.")
        elif "INSTALL_FAILED_VERSION_DOWNGRADE" in result:
            self.log_message("⚠ Version downgrade detected. Use 'Install (Downgrade)' button.")
            messagebox.showwarning("Version Error", "Version downgrade detected.\nUse 'Install (Downgrade)' button.")
        elif "INSTALL_FAILED_DEPRECATED_SDK_VERSION" in result:
            self.log_message("⚠ SDK version is too old for this Android version.")
            self.log_message("💡 Make sure 'Bypass Low Target SDK Block' option is checked.")
            messagebox.showerror("SDK Error", "The app is too old for this Android version.\nPlease make sure 'Bypass Low Target SDK Block' is checked.")
        else:
            self.log_message("✗ Installation failed.")
            messagebox.showerror("Installation Failed", "Installation was not successful.\nPlease check the output log for details.")
            
        self.log_message("=" * 50)

def main():
    root = tk.Tk()
    app = ADBInstallerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
