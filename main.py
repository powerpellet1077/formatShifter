import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import os
import datetime


file_types = Image.registered_extensions()
readable_file_types = [ext for ext, fmt in file_types.items() if fmt in Image.OPEN]
writable_file_types = [ext for ext, fmt in file_types.items() if fmt in Image.SAVE]
root = tk.Tk()
root.geometry("350x200")
root.title("FormatShifter")
root.iconphoto(False, tk.PhotoImage(file='icon.png'))
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
            # messagebox.showerror(title="FormatShifter", message=f"Unsupported format: {output_format}, this image cannot be converted to the selected format")
            # return
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
