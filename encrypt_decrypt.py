import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

class EncryptionApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.example.EncryptionApp")
        self.key = None
        self.selected_file = None

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("File Encryption with AES-256")
        window.set_default_size(600, 400)

        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        main_box.set_margin_start(20)
        main_box.set_margin_end(20)

        # File selection
        file_button = Gtk.Button(label="Select File")
        file_button.connect("clicked", self.on_file_button_clicked)
        main_box.append(file_button)

        self.file_label = Gtk.Label(label="No file selected")
        main_box.append(self.file_label)

        # Key input
        key_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.key_entry = Gtk.Entry()
        self.key_entry.set_placeholder_text("Enter 32-byte key (hex) or generate one")
        key_box.append(self.key_entry)

        generate_key_button = Gtk.Button(label="Generate Key")
        generate_key_button.connect("clicked", self.on_generate_key_clicked)
        key_box.append(generate_key_button)
        main_box.append(key_box)

        # Encrypt/Decrypt buttons
        encrypt_button = Gtk.Button(label="Encrypt File")
        encrypt_button.connect("clicked", self.on_encrypt_clicked)
        main_box.append(encrypt_button)

        decrypt_button = Gtk.Button(label="Decrypt File")
        decrypt_button.connect("clicked", self.on_decrypt_clicked)
        main_box.append(decrypt_button)

        # Status label
        self.status_label = Gtk.Label(label="")
        main_box.append(self.status_label)

        window.set_child(main_box)
        window.present()

    def on_file_button_clicked(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Select a File",
            action=Gtk.FileChooserAction.OPEN,
            transient_for=button.get_root(),
            modal=True
        )
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Select", Gtk.ResponseType.OK)
        dialog.connect("response", self.on_file_dialog_response)
        dialog.show()

    def on_file_dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.selected_file = dialog.get_file().get_path()
            self.file_label.set_text(f"Selected: {self.selected_file}")
        dialog.destroy()

    def on_generate_key_clicked(self, button):
        self.key = get_random_bytes(32)  # 256-bit key
        self.key_entry.set_text(self.key.hex())
        self.status_label.set_text("New key generated")

    def on_encrypt_clicked(self, button):
        if not self.selected_file:
            self.status_label.set_text("Error: No file selected")
            return
        if not self.key:
            try:
                self.key = bytes.fromhex(self.key_entry.get_text())
                if len(self.key) != 32:
                    raise ValueError
            except ValueError:
                self.status_label.set_text("Error: Invalid 32-byte key (use hex or generate one)")
                return

        output_file = self.selected_file + ".enc"
        try:
            encrypt_file(self.key, self.selected_file, output_file)
            self.status_label.set_text(f"Encrypted file created: {output_file}")
        except Exception as e:
            self.status_label.set_text(f"Error: {str(e)}")

    def on_decrypt_clicked(self, button):
        if not self.selected_file:
            self.status_label.set_text("Error: No file selected")
            return
        if not self.key:
            try:
                self.key = bytes.fromhex(self.key_entry.get_text())
                if len(self.key) != 32:
                    raise ValueError
            except ValueError:
                self.status_label.set_text("Error: Invalid 32-byte key (use hex or generate one)")
                return

        output_file = self.selected_file + ".decrypted"
        try:
            decrypt_file(self.key, self.selected_file, output_file)
            self.status_label.set_text(f"Decrypted file created: {output_file}")
        except Exception as e:
            self.status_label.set_text(f"Error: {str(e)}")

def encrypt_file(key, input_file, output_file):
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    with open(input_file, 'rb') as f:
        data = f.read()
    padding_length = 16 - (len(data) % 16)
    data += bytes([padding_length] * padding_length)
    ciphertext = cipher.encrypt(data)
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)

def decrypt_file(key, input_file, output_file):
    with open(input_file, 'rb') as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ciphertext)
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    with open(output_file, 'wb') as f:
        f.write(plaintext)

def main():
    app = EncryptionApp()
    app.run()

if __name__ == "__main__":
    main()
