import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import os
import datetime
import base64

file_types = Image.registered_extensions()
readable_file_types = [ext for ext, fmt in file_types.items() if fmt in Image.OPEN]
writable_file_types = [ext for ext, fmt in file_types.items() if fmt in Image.SAVE]
icon64 = "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"
root = tk.Tk()
root.geometry("350x200")
root.title("FormatShifter")
icon = tk.PhotoImage(data=base64.b64decode(icon64))
root.iconphoto(False, icon)
root.configure(background="#001d2b")
root.resizable(False, False)
image = None
file_path = None




def openFile():
    global image, file_path
    try:
        file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select a File",
            filetypes=(("Image Files", "*." + ";*".join(readable_file_types)), ("All Files", "*.*"))
        )
        if file_path:
            image = Image.open(file_path)
            openButton.config(text=str(os.path.basename(file_path)))
    except:
        threading.Thread(target=lambda: messagebox.showerror(title="FormatShifter", message="Please select a valid file type")).start()


def saveFile():
    global image
    if image:
        output_format = cvtDropdown.get().upper().replace(".", "")
        if not output_format:
            messagebox.showwarning(title="FormatShifter", message="Please select an output format.")
            return


        format_mapping = {
            'JPG': 'JPEG',
            'TIF': 'TIFF'}

        if output_format in format_mapping:
            output_format = format_mapping[output_format]

        if output_format in ['JPEG', 'BMP'] and image.mode not in ['RGB', 'L']:
            image = image.convert('RGB')
        elif output_format == 'GIF' and image.mode != 'P':
            image = image.convert('P')
        elif output_format == 'TIFF' and image.mode not in ['RGB', 'RGBA', 'L']:
            image = image.convert('RGBA')

        file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.' + output_format.lower()
        save_path = filedialog.asksaveasfilename(
            initialdir=".",
            title="Save As",
            defaultextension="." + output_format.lower(),
            filetypes=[("Image Files", "*." + output_format.lower())]
        )

        if save_path:
            try:
                image.save(save_path, format=output_format)
                messagebox.showinfo(title="FormatShifter", message="File converted successfully!")
            except Exception as e:
                messagebox.showerror(title="FormatShifter", message="Error during conversion: " + str(e))

    else:
        messagebox.showwarning(title="FormatShifter", message="No image loaded. Please open an image first.")

title = tk.Label(root, font=("Terminal", 25), text="FormatShifter")
title.configure(background="#001d2b", foreground="white")
title.pack()
subTitle = tk.Label(root, font=("Terminal", 10), text="Created by Logan Hair")
subTitle.configure(background="#001d2b", foreground="white")
subTitle.pack(fill=tk.BOTH, padx=0, pady=0)
openButton = tk.Button(root, command=openFile, text="Open file", font=("Terminal", 10))
openButton.configure(background="#001d2b", foreground="white")
openButton.pack(pady=5)
cvtToLabel = tk.Label(root, text="Convert to:", font=("Terminal", 15))
cvtToLabel.configure(background="#001d2b", foreground="white")
cvtToLabel.pack()
cvtDropdown = ttk.Combobox(root, values=writable_file_types)
cvtDropdown.configure(background="#001d2b", foreground="white")
cvtDropdown.pack(pady=5)
convertButton = tk.Button(root, command=saveFile, text="Convert!", font=("Terminal", 20))
convertButton.configure(background="#001d2b", foreground="white")
convertButton.pack(pady=5)
root.mainloop()
