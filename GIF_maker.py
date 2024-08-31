import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Initialize global images list
images = []

# Function to open images
def open_images():
    filenames = filedialog.askopenfilenames(initialdir=os.path.expanduser("~"),
                                            title="Select Files",
                                            filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png"), ("all files", "*.*")))
    if filenames:
        for filename in filenames:
            img = Image.open(filename)
            img_resized = img.resize((100, 100))  # Adjusted size for the labels
            images.append(img_resized)
            display_image(img_resized, len(images) - 1)

# Function to display images in labels
def display_image(img, index):
    img_photo = ImageTk.PhotoImage(img)

    if index < 6:  # Display up to 6 images
        img_labels[index].config(image=img_photo, width=100, height=100, bg="#ffffff", relief="solid", borderwidth=2)
        img_labels[index].image = img_photo  # Keep reference to avoid garbage collection

# Function to create GIF from images
def create_gif(images, gif_path):
    if len(images) < 2:
        messagebox.showerror("ValueError", "At least 2 images are needed.")
        return None

    try:
        images[0].save(
            gif_path,
            save_all=True,
            append_images=images[1:],
            duration=200,
            loop=0
        )
        print(f"GIF saved to: {gif_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save GIF: {e}")
        return None

    return gif_path

# Function to generate GIF and display it
def generate_gif():
    gif_path = filedialog.asksaveasfilename(defaultextension=".gif",
                                           filetypes=[("GIF files", "*.gif")],
                                           initialfile="costumes.gif",
                                           title="Save GIF as")
    if gif_path:
        gif_path = create_gif(images, gif_path)
        if gif_path:
            gif_lab = Image.open(gif_path)
            tk_gif_image = ImageTk.PhotoImage(gif_lab)
            gif_label.config(image=tk_gif_image, relief="solid", borderwidth=2)
            gif_label.image = tk_gif_image  # Keep reference to avoid garbage collection
            messagebox.showinfo("Success", "Your GIF is ready and saved in the chosen location.")

# Function to create a rounded button with hover effect
def create_rounded_button(master, text, command, color, text_color, font_size):
    def on_enter(event):
        button.itemconfig(rect, fill="#357a38")
        button.itemconfig(text_item, fill="white")

    def on_leave(event):
        button.itemconfig(rect, fill=color)
        button.itemconfig(text_item, fill=text_color)

    button = tk.Canvas(master, width=150, height=40, bg=master.cget("bg"), bd=0, highlightthickness=0, relief="flat")
    rect = button.create_rectangle(0, 0, 150, 40, fill=color, outline="")
    text_item = button.create_text(75, 20, text=text, fill=text_color, font=("Segoe UI", font_size, "bold"))
    button.bind("<Button-1>", lambda e: command())
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    return button

# Main application window
root = tk.Tk()
root.title("zrainerzz.com")
root.iconbitmap("logo_zrainerzz_ico.ico")

# Set window size to be slightly smaller than the screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width - 100  # Adjust as needed
window_height = screen_height - 100  # Adjust as needed
root.geometry(f"{window_width}x{window_height}")

# Configure window
root.configure(bg="#f0f0f0")

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
button_frame.pack(side=tk.TOP, fill=tk.X)

# Frame for images with improved padding and layout
image_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
image_frame.pack(side=tk.TOP, pady=20, expand=True)

# Frame for GIF
gif_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)
gif_frame.pack(side=tk.TOP, pady=20, expand=True)

# Image labels with improved spacing
img_labels = [tk.Label(image_frame, bg="#f0f0f0", width=100, height=100) for _ in range(6)]
for i, label in enumerate(img_labels):
    label.grid(row=i // 3, column=i % 3, padx=20, pady=20)

# GIF label with improved size
gif_label = tk.Label(gif_frame, bg="#f0f0f0", width=300, height=300)
gif_label.pack(pady=10)

# Rounded buttons
open_images_button = create_rounded_button(button_frame, "Open Images", open_images, "#4CAF50", "white", 12)
open_images_button.pack(side=tk.LEFT, padx=10)

generate_gif_button = create_rounded_button(button_frame, "Generate GIF", generate_gif, "#f44336", "white", 12)
generate_gif_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
