import customtkinter as ctk
import threading
import json
import os
from tkinter import filedialog
from backend import translate_text

# Modern color scheme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

APP_NAME = "🌍 Dev Translator Pro"
VERSION = "v2.0"

# Paths
USER_DATA_PATH = os.path.join(os.path.expanduser("~"), ".dev_translator")
CONFIG_FILE = os.path.join(USER_DATA_PATH, "config.json")
LANG_FILE = "languages.json"

if not os.path.exists(USER_DATA_PATH):
    os.makedirs(USER_DATA_PATH)

# Load languages from JSON
def load_languages():
    try:
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            langs = json.load(f)
            print(f"✅ Loaded {len(langs)} languages successfully!")
            return langs
    except Exception as e:
        print(f"❌ Error loading languages: {e}")
        print("⚠️ Using fallback languages (5 only)")
        return {
            "Auto Detect": "auto",
            "English": "en",
            "Arabic": "ar",
            "French": "fr",
            "Spanish": "es"
        }

LANGUAGES = load_languages()

# Load config
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"source": "Auto Detect", "target": "English", "last_text": "", "theme": "dark"}

# Save config
def save_config(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except:
        pass

# Main App
app = ctk.CTk()
app.title(APP_NAME)
app.geometry("1200x750")
app.minsize(1000, 650)

# Configure grid
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)

# ==================== HEADER ====================
header_frame = ctk.CTkFrame(app, fg_color=("#3b8ed0", "#1f6aa5"), corner_radius=0)
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

title_label = ctk.CTkLabel(
    header_frame, 
    text=APP_NAME, 
    font=ctk.CTkFont(size=32, weight="bold"),
    text_color="white"
)
title_label.pack(pady=20)

version_label = ctk.CTkLabel(
    header_frame,
    text=VERSION + f" | {len(LANGUAGES)} Languages Supported",
    font=ctk.CTkFont(size=12),
    text_color=("#e0e0e0", "#b0b0b0")
)
version_label.pack(pady=(0, 15))

# ==================== LANGUAGE SELECTOR ====================
lang_frame = ctk.CTkFrame(app, fg_color="transparent")
lang_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=30, sticky="ew")
lang_frame.grid_columnconfigure((0, 1, 2), weight=1)

source_var = ctk.StringVar()
target_var = ctk.StringVar()

# From Language
from_label = ctk.CTkLabel(lang_frame, text="📥 From", font=ctk.CTkFont(size=14, weight="bold"))
from_label.grid(row=0, column=0, pady=(0, 5))

source_menu = ctk.CTkOptionMenu(
    lang_frame,
    values=list(LANGUAGES.keys()),
    variable=source_var,
    font=ctk.CTkFont(size=14),
    dropdown_font=ctk.CTkFont(size=12),
    width=300,
    height=40,
    corner_radius=10
)
source_menu.grid(row=1, column=0, padx=10, sticky="ew")

# Swap Button
def swap_languages():
    src = source_var.get()
    tgt = target_var.get()
    if src != "Auto Detect":
        source_var.set(tgt)
        target_var.set(src)
        # Swap text boxes
        input_text = input_box.get("1.0", "end").strip()
        output_text = output_box.get("1.0", "end").strip()
        input_box.delete("1.0", "end")
        output_box.delete("1.0", "end")
        input_box.insert("1.0", output_text)
        output_box.insert("1.0", input_text)

swap_btn = ctk.CTkButton(
    lang_frame,
    text="⇄",
    command=swap_languages,
    font=ctk.CTkFont(size=24, weight="bold"),
    width=60,
    height=40,
    corner_radius=10,
    fg_color=("#2b7a9e", "#1f5a7a"),
    hover_color=("#236280", "#1a4960")
)
swap_btn.grid(row=1, column=1, padx=5)

# To Language
to_label = ctk.CTkLabel(lang_frame, text="📤 To", font=ctk.CTkFont(size=14, weight="bold"))
to_label.grid(row=0, column=2, pady=(0, 5))

target_menu = ctk.CTkOptionMenu(
    lang_frame,
    values=list(LANGUAGES.keys()),
    variable=target_var,
    font=ctk.CTkFont(size=14),
    dropdown_font=ctk.CTkFont(size=12),
    width=300,
    height=40,
    corner_radius=10
)
target_menu.grid(row=1, column=2, padx=10, sticky="ew")

# ==================== TEXT BOXES ====================
text_frame = ctk.CTkFrame(app, fg_color="transparent")
text_frame.grid(row=2, column=0, columnspan=2, padx=30, pady=(0, 20), sticky="nsew")
text_frame.grid_columnconfigure((0, 1), weight=1)
text_frame.grid_rowconfigure(0, weight=1)

# Input Box
input_container = ctk.CTkFrame(text_frame)
input_container.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
input_container.grid_rowconfigure(1, weight=1)
input_container.grid_columnconfigure(0, weight=1)

input_label = ctk.CTkLabel(
    input_container,
    text="✍️ Enter Text",
    font=ctk.CTkFont(size=14, weight="bold")
)
input_label.grid(row=0, column=0, pady=(5, 5), sticky="w", padx=10)

input_box = ctk.CTkTextbox(
    input_container,
    font=ctk.CTkFont(size=16),
    corner_radius=10,
    border_width=2,
    border_color=("#3b8ed0", "#1f6aa5"),
    wrap="word"
)
input_box.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")

# Character count
char_count_label = ctk.CTkLabel(
    input_container,
    text="0 characters",
    font=ctk.CTkFont(size=11),
    text_color=("gray50", "gray60")
)
char_count_label.grid(row=2, column=0, pady=(0, 5), sticky="e", padx=10)

def update_char_count(*args):
    text = input_box.get("1.0", "end").strip()
    count = len(text)
    char_count_label.configure(text=f"{count} characters")

input_box.bind("<<Modified>>", lambda e: (update_char_count(), input_box.edit_modified(False)))

# Output Box
output_container = ctk.CTkFrame(text_frame)
output_container.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
output_container.grid_rowconfigure(1, weight=1)
output_container.grid_columnconfigure(0, weight=1)

output_label = ctk.CTkLabel(
    output_container,
    text="📝 Translation",
    font=ctk.CTkFont(size=14, weight="bold")
)
output_label.grid(row=0, column=0, pady=(5, 5), sticky="w", padx=10)

output_box = ctk.CTkTextbox(
    output_container,
    font=ctk.CTkFont(size=16),
    corner_radius=10,
    border_width=2,
    border_color=("#28a745", "#1e7a35"),
    wrap="word"
)
output_box.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="nsew")

# Copy button
def copy_translation():
    text = output_box.get("1.0", "end").strip()
    if text:
        app.clipboard_clear()
        app.clipboard_append(text)
        status_label.configure(text="✅ Copied to clipboard!", text_color=("#28a745", "#1e7a35"))
        app.after(2000, lambda: status_label.configure(text="Ready to translate", text_color=("gray20", "gray80")))

copy_btn = ctk.CTkButton(
    output_container,
    text="📋 Copy",
    command=copy_translation,
    width=80,
    height=28,
    corner_radius=8,
    font=ctk.CTkFont(size=12)
)
copy_btn.grid(row=2, column=0, pady=(0, 5), sticky="e", padx=10)

# ==================== CONTROLS ====================
controls = ctk.CTkFrame(app, fg_color="transparent")
controls.grid(row=3, column=0, columnspan=2, pady=(0, 20), padx=30, sticky="ew")
controls.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

# Status Label
status_label = ctk.CTkLabel(
    controls,
    text="Ready to translate",
    font=ctk.CTkFont(size=13),
    text_color=("gray20", "gray80")
)
status_label.grid(row=0, column=0, columnspan=5, pady=(0, 10))

# Translation function
def do_translate():
    text = input_box.get("1.0", "end").strip()
    if not text:
        status_label.configure(text="❌ Please enter text to translate", text_color=("#dc3545", "#a02530"))
        return

    translate_btn.configure(state="disabled", text="Translating...")
    status_label.configure(text="🔄 Translating... Please wait", text_color=("#ffc107", "#cc9a06"))
    output_box.delete("1.0", "end")

    def worker():
        src = LANGUAGES.get(source_var.get(), "auto")
        tgt = LANGUAGES.get(target_var.get(), "en")
        result = translate_text(text, src, tgt)
        app.after(0, lambda: finish(result))

    threading.Thread(target=worker, daemon=True).start()

def finish(result):
    output_box.delete("1.0", "end")
    output_box.insert("1.0", result)
    status_label.configure(text="✅ Translation complete!", text_color=("#28a745", "#1e7a35"))
    translate_btn.configure(state="normal", text="🌍 Translate")

# Theme toggle
def toggle_mode():
    current = ctk.get_appearance_mode()
    new_mode = "light" if current == "Dark" else "dark"
    ctk.set_appearance_mode(new_mode)
    config = load_config()
    config["theme"] = new_mode
    save_config(config)

# Save function
def save_translation():
    text = output_box.get("1.0", "end").strip()
    if not text:
        status_label.configure(text="❌ Nothing to save", text_color=("#dc3545", "#a02530"))
        return
    try:
        file_path = filedialog.asksaveasfilename(
            title="Save Translation",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            status_label.configure(
                text=f"✅ Saved: {os.path.basename(file_path)}", 
                text_color=("#28a745", "#1e7a35")
            )
    except Exception as e:
        status_label.configure(text=f"❌ Error: {str(e)}", text_color=("#dc3545", "#a02530"))

# Clear function
def clear_all():
    input_box.delete("1.0", "end")
    output_box.delete("1.0", "end")
    status_label.configure(text="🗑️ Cleared all", text_color=("gray20", "gray80"))
    char_count_label.configure(text="0 characters")

# Buttons with modern design
translate_btn = ctk.CTkButton(
    controls,
    text="🌍 Translate",
    command=do_translate,
    font=ctk.CTkFont(size=16, weight="bold"),
    height=45,
    corner_radius=10,
    fg_color=("#3b8ed0", "#1f6aa5"),
    hover_color=("#2b7a9e", "#1a5580")
)
translate_btn.grid(row=1, column=0, padx=8, sticky="ew")

clear_btn = ctk.CTkButton(
    controls,
    text="🗑️ Clear",
    command=clear_all,
    font=ctk.CTkFont(size=14),
    height=45,
    corner_radius=10,
    fg_color=("#6c757d", "#495057"),
    hover_color=("#5a6268", "#3a3f44")
)
clear_btn.grid(row=1, column=1, padx=8, sticky="ew")

mode_btn = ctk.CTkButton(
    controls,
    text="🌓 Theme",
    command=toggle_mode,
    font=ctk.CTkFont(size=14),
    height=45,
    corner_radius=10,
    fg_color=("#6f42c1", "#5a32a3"),
    hover_color=("#5a32a3", "#4a2885")
)
mode_btn.grid(row=1, column=2, padx=8, sticky="ew")

save_btn = ctk.CTkButton(
    controls,
    text="💾 Save",
    command=save_translation,
    font=ctk.CTkFont(size=14),
    height=45,
    corner_radius=10,
    fg_color=("#28a745", "#1e7a35"),
    hover_color=("#218838", "#19692b")
)
save_btn.grid(row=1, column=3, padx=8, sticky="ew")

# About button
def show_about():
    about_window = ctk.CTkToplevel(app)
    about_window.title("About")
    about_window.geometry("400x300")
    about_window.resizable(False, False)
    
    ctk.CTkLabel(
        about_window,
        text="🌍 Dev Translator Pro",
        font=ctk.CTkFont(size=24, weight="bold")
    ).pack(pady=20)
    
    ctk.CTkLabel(
        about_window,
        text=VERSION,
        font=ctk.CTkFont(size=14)
    ).pack(pady=5)
    
    ctk.CTkLabel(
        about_window,
        text=f"Powerful translation app\n{len(LANGUAGES)} Languages supported\nPowered by Google Translate",
        font=ctk.CTkFont(size=13),
        justify="center"
    ).pack(pady=20)
    
    ctk.CTkLabel(
        about_window,
        text="Made with ❤️ using Python & CustomTkinter",
        font=ctk.CTkFont(size=11),
        text_color="gray"
    ).pack(pady=10)
    
    ctk.CTkButton(
        about_window,
        text="Close",
        command=about_window.destroy,
        width=100
    ).pack(pady=20)

about_btn = ctk.CTkButton(
    controls,
    text="ℹ️ About",
    command=show_about,
    font=ctk.CTkFont(size=14),
    height=45,
    corner_radius=10,
    fg_color=("#17a2b8", "#117a8b"),
    hover_color=("#138496", "#0e6674")
)
about_btn.grid(row=1, column=4, padx=8, sticky="ew")

# ==================== FOOTER ====================
footer = ctk.CTkLabel(
    app,
    text="Tip: Press Ctrl+Enter to translate quickly",
    font=ctk.CTkFont(size=11),
    text_color=("gray40", "gray60")
)
footer.grid(row=4, column=0, columnspan=2, pady=(0, 10))

# ==================== LOAD CONFIG ====================
config = load_config()
source_var.set(config.get("source", "Auto Detect"))
target_var.set(config.get("target", "English"))
input_box.insert("1.0", config.get("last_text", ""))
if config.get("theme"):
    ctk.set_appearance_mode(config["theme"])

# ==================== SAVE ON CLOSE ====================
def on_closing():
    save_config({
        "source": source_var.get(),
        "target": target_var.get(),
        "last_text": input_box.get("1.0", "end").strip(),
        "theme": ctk.get_appearance_mode().lower()
    })
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

# ==================== KEYBOARD SHORTCUTS ====================
def on_ctrl_enter(event):
    do_translate()

def on_ctrl_l(event):
    clear_all()

def on_ctrl_s(event):
    save_translation()

app.bind('<Control-Return>', on_ctrl_enter)
app.bind('<Control-l>', on_ctrl_l)
app.bind('<Control-s>', on_ctrl_s)

# ==================== RUN ====================
print("=" * 70)
print(f"🌍 Dev Translator Pro {VERSION}")
print(f"✅ {len(LANGUAGES)} Languages Loaded Successfully!")
print("=" * 70)
app.mainloop()