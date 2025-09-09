import configparser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json, sys, ctypes
import os
from deep_translator import GoogleTranslator
import tkinter as tk

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.example.Dictionary")

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Resource not found: {full_path}")
    return full_path
WORDS_FOLDER = "words"

class TranslatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("English → Translator - By SouRav Bhattacharya")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
        self.sidebar_width = 250
        self.animation_speed = 20
        self.animation_delay = 10
        self.sidebar_open = False
        self.target_language_code = 'bn'

        try:
            root.iconbitmap(resource_path(r"icons/icon.ico"))

        except Exception as e:
            print("Icon load error:", e)
        self.data_dir = os.path.join(os.path.expanduser("~"), ".Dictionary")
        os.makedirs(self.data_dir, exist_ok=True)

        if sys.platform == "win32":

            try:
                ctypes.windll.kernel32.SetFileAttributesW(self.data_dir, 2)

            except:
                pass
        self.config_file = os.path.join(self.data_dir, "config.ini")
        self.style = ttk.Style(theme="darkly")
        self.main_paned = ttk.PanedWindow(root, orient=HORIZONTAL, bootstyle="dark", cursor="arrow")
        self.main_paned.pack(fill="both", expand=True)
        self.main_paned.bind("<B1-Motion>", self.prevent_drag)
        self.main_paned.bind("<ButtonRelease-1>", self.prevent_drag)
        self.sidebar = ttk.Frame(self.main_paned, width=200, style="Dark.TFrame", cursor="arrow")
        self.sidebar.pack_propagate(False)
        ttk.Label(self.sidebar, text="Select Language",font=('arial',15, 'bold'), style="Inverse.Dark.TLabel").pack(pady=10)
        self.red_frame = ttk.Frame(self.sidebar, height=850)
        self.red_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.lang_canvas = tk.Canvas(self.red_frame, bg=self.style.colors.dark, highlightthickness=0)
        self.lang_scrollbar = ttk.Scrollbar(self.red_frame, orient="vertical", command=self.lang_canvas.yview, bootstyle="round")
        self.lang_canvas.configure(yscrollcommand=self.lang_scrollbar.set)
        self.lang_scrollbar.pack(side="right", fill="y")
        self.lang_canvas.pack(side="left", fill="both", expand=True)
        self.languages_frame = ttk.Frame(self.lang_canvas)
        self.canvas_window = self.lang_canvas.create_window((0, 0), window=self.languages_frame, anchor="nw")

        def on_frame_configure(event):
            self.lang_canvas.configure(scrollregion=self.lang_canvas.bbox("all"))
        self.languages_frame.bind("<Configure>", on_frame_configure)

        def on_mouse_wheel(event):
            self.lang_canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        self.lang_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        
        self.language_codes = {
            "Afrikaans": "af",
            "Albanian": "sq",
            "Amharic": "am",
            "Arabic": "ar",
            "Armenian": "hy",
            "Assamese": "as",
            "Aymara": "ay",
            "Azerbaijani": "az",
            "Bambara": "bm",
            "Basque": "eu",
            "Belarusian": "be",
            "Bengali": "bn",
            "Bhojpuri": "bho",
            "Bosnian": "bs",
            "Bulgarian": "bg",
            "Catalan": "ca",
            "Cebuano": "ceb",
            "Chichewa": "ny",
            "Chinese (Simplified)": "zh-CN",
            "Chinese (Traditional)": "zh-TW",
            "Corsican": "co",
            "Croatian": "hr",
            "Czech": "cs",
            "Danish": "da",
            "Dhivehi": "dv",
            "Dogri": "doi",
            "Dutch": "nl",
            "English": "en",
            "Esperanto": "eo",
            "Estonian": "et",
            "Ewe": "ee",
            "Filipino": "tl",
            "Finnish": "fi",
            "French": "fr",
            "Frisian": "fy",
            "Galician": "gl",
            "Georgian": "ka",
            "German": "de",
            "Greek": "el",
            "Guarani": "gn",
            "Gujarati": "gu",
            "Haitian Creole": "ht",
            "Hausa": "ha",
            "Hawaiian": "haw",
            "Hebrew": "iw",
            "Hindi": "hi",
            "Hmong": "hmn",
            "Hungarian": "hu",
            "Icelandic": "is",
            "Igbo": "ig",
            "Ilocano": "ilo",
            "Indonesian": "id",
            "Irish": "ga",
            "Italian": "it",
            "Japanese": "ja",
            "Javanese": "jw",
            "Kannada": "kn",
            "Kazakh": "kk",
            "Khmer": "km",
            "Kinyarwanda": "rw",
            "Konkani": "gom",
            "Korean": "ko",
            "Krio": "kri",
            "Kurdish (Kurmanji)": "ku",
            "Kurdish (Sorani)": "ckb",
            "Kyrgyz": "ky",
            "Lao": "lo",
            "Latin": "la",
            "Latvian": "lv",
            "Lingala": "ln",
            "Lithuanian": "lt",
            "Luganda": "lg",
            "Luxembourgish": "lb",
            "Macedonian": "mk",
            "Maithili": "mai",
            "Malagasy": "mg",
            "Malay": "ms",
            "Malayalam": "ml",
            "Maltese": "mt",
            "Maori": "mi",
            "Marathi": "mr",
            "Meiteilon (Manipuri)": "mni-Mtei",
            "Mizo": "lus",
            "Mongolian": "mn",
            "Myanmar": "my",
            "Nepali": "ne",
            "Norwegian": "no",
            "Odia (Oriya)": "or",
            "Oromo": "om",
            "Pashto": "ps",
            "Persian": "fa",
            "Polish": "pl",
            "Portuguese": "pt",
            "Punjabi": "pa",
            "Quechua": "qu",
            "Romanian": "ro",
            "Russian": "ru",
            "Samoan": "sm",
            "Sanskrit": "sa",
            "Scots Gaelic": "gd",
            "Serbian": "sr",
            "Sesotho": "st",
            "Shona": "sn",
            "Sindhi": "sd",
            "Sinhala": "si",
            "Slovak": "sk",
            "Slovenian": "sl",
            "Somali": "so",
            "Spanish": "es",
            "Sundanese": "su",
            "Swahili": "sw",
            "Swedish": "sv",
            "Tajik": "tg",
            "Tamil": "ta",
            "Tatar": "tt",
            "Telugu": "te",
            "Thai": "th",
            "Tigrinya": "ti",
            "Tsonga": "ts",
            "Turkish": "tr",
            "Turkmen": "tk",
            "Twi": "ak",
            "Ukrainian": "uk",
            "Urdu": "ur",
            "Uyghur": "ug",
            "Uzbek": "uz",
            "Vietnamese": "vi",
            "Welsh": "cy",
            "Xhosa": "xh",
            "Yiddish": "yi",
            "Yoruba": "yo",
            "Zulu": "zu"
        }
        
        for lang in self.language_codes.keys():
            lbl = ttk.Label(
                self.languages_frame,
                text=lang,
                font=('Segoe UI', 13, 'bold'),
                anchor="w",
                style="Inverse.Dark.TLabel",
                cursor="hand2",
            )
            lbl.pack(fill="x", padx=5, pady=3, ipadx=10)
            lbl.bind("<Button-1>", lambda e, l=lang: self.set_target_language(l))
        self.content_frame = ttk.Frame(self.main_paned,)
        self.main_paned.add(self.sidebar)
        self.main_paned.add(self.content_frame)
        self.main_paned.sashpos(0, 0)
        self.open_sidebar()
        self.toggle_btn = ttk.Button(
            self.content_frame,
            text="☰",
            width=2,
            command=self.toggle_sidebar,
            bootstyle="dark",
            cursor="hand2"
        )
        self.toggle_btn.pack(side="top", anchor="nw", padx=2, pady=2)
        ttk.Label(self.content_frame, text="Enter English Text:", font=("Segoe UI", 25, "bold")).pack(pady=15)
        self.create_entry()
        ttk.Button(self.content_frame, text="Translate", command=self.translate_text, bootstyle=PRIMARY, cursor="hand2").pack(pady=15)
        self.translation_label = ttk.Label(self.content_frame, text="Bengali Translation:", font=("Segoe UI", 25, "bold"))
        self.translation_label.pack(pady=15)
        self.load_window_geometry()
        self.create_output()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_sidebar(self):

        if self.sidebar_open:
            self.close_sidebar()
        else:
            self.open_sidebar()

    def open_sidebar(self):
        pos = self.main_paned.sashpos(0)

        if pos < self.sidebar_width:
            new_pos = min(pos + self.animation_speed, self.sidebar_width)
            self.main_paned.sashpos(0, new_pos)
            self.root.after(self.animation_delay, self.open_sidebar)
        else:
            self.sidebar_open = True

    def close_sidebar(self):
        pos = self.main_paned.sashpos(0)

        if pos > 0:
            new_pos = max(pos - self.animation_speed, 0)
            self.main_paned.sashpos(0, new_pos)
            self.root.after(self.animation_delay, self.close_sidebar)
        else:
            self.sidebar_open = False
            self.toggle_btn.config(text="☰")

    def set_target_language(self, lang_name):
        code = self.language_codes.get(lang_name)

        if code:
            self.target_language_code = code
            self.translation_label.configure(text=f"{lang_name} Translation:")
            messagebox.showinfo("Language Selected", f"Target language set to {lang_name}")

    def prevent_drag(self, event=None):
        self.main_paned.sashpos(0, min(self.main_paned.sashpos(0), self.sidebar_width+1000))

    def create_entry(self):
        self.entry_container = ttk.Frame(self.content_frame, height=200)
        self.entry_container.pack(fill='x', side="top", expand=True, padx=20, pady=10)
        self.v_scroll = ttk.Scrollbar(self.entry_container, orient=VERTICAL, bootstyle="round")
        self.h_scroll = ttk.Scrollbar(self.entry_container, orient=HORIZONTAL, bootstyle="round")
        self.entry = ttk.Text(
            self.entry_container,
            width=50, height=5,
            font=("Segoe UI", 15),
            wrap='none',
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )
        self.entry.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns", columnspan=2)
        self.entry_container.grid_rowconfigure(0, weight=1)
        self.entry_container.grid_columnconfigure(0, weight=1)
        self.v_scroll.grid_remove()
        self.v_scroll.config(command=self.entry.yview)
        self.h_scroll.config(command=self.entry.xview)
        self.entry.tag_configure(
            "padding",
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=2,
            spacing3=2
        )
        self.entry.insert("1.0", "")
        self.entry.tag_add("padding", "1.0", "end")

        def apply_padding(event=None):
            self.entry.tag_add("padding", "1.0", "end")
        self.entry.bind("<<Modified>>", lambda e: (apply_padding(), self.entry.edit_modified(False)))
        self.words = []
        self.lb_index = -1
        self.listbox_up = False

        def keep_cursor_visible(event=None):
            self.entry.see("insert")
        self.entry.bind("<KeyRelease>", lambda e: (self.changed(e), keep_cursor_visible()))
        self.entry.bind("<Down>", self.move_down)
        self.entry.bind("<Up>", self.move_up)
        self.entry.bind("<Return>", self.enter_pressed)
        self.entry.bind("<Shift-Return>", self.new_line)
        self.entry.bind("<Configure>", lambda e: self.update_listbox_position())
        self.v_scroll.bind("<B1-Motion>", lambda e: self.update_listbox_position())
        self.h_scroll.bind("<B1-Motion>", lambda e: self.update_listbox_position())
        self.entry.bind("<MouseWheel>", lambda e: self.update_listbox_position())

        def handle_mousewheel(event):
            self.entry.yview_scroll(-1*(event.delta//120), "units")
            return "break"
        self.entry.bind("<MouseWheel>", handle_mousewheel)
        self.root.bind("<Button-1>", self.global_click)
        self.min_height = 5
        self.max_height = 4

    def global_click(self, event):

        if self.listbox_up:
            widget = event.widget

            if widget not in (self.lb, self.lb_frame, self.entry, self.v_scroll, self.h_scroll, self.scrollbar):
                self.lb_frame.destroy()
                self.listbox_up = False
                self.lb_index = -1

    def update_height(self):
        lines = int(self.entry.index('end-1c').split('.')[0])

        if lines > self.max_height:
            self.v_scroll.grid()
            new_height = self.max_height
        else:
            self.v_scroll.grid_remove()
            new_height = max(lines, self.min_height)
        self.entry.configure(height=new_height)
        text_content = self.entry.get("1.0", "end-1c").split("\n")
        max_line_length = max((len(line) for line in text_content), default=0)

        if max_line_length > self.entry['width']:
            self.h_scroll.grid(row=1, column=0, sticky="ew", columnspan=2)
        else:
            self.h_scroll.grid_remove()
        self.update_listbox_position()

    def create_output(self):
        self.output_frame = ttk.Frame(self.content_frame)
        self.output_frame.pack(fill=ttk.X, expand=True, padx=20, pady=10)
        self.output_frame.grid_rowconfigure(0, weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        self.output_text = ttk.Text(
            self.output_frame,
            height=5, width=20, state='disabled',
            font=("Segoe UI", 12),
            wrap='none'
        )
        self.output_v_scroll = ttk.Scrollbar(self.output_frame, orient=VERTICAL, command=self.output_text.yview, bootstyle="round")
        self.output_h_scroll = ttk.Scrollbar(self.output_frame, orient=HORIZONTAL, command=self.output_text.xview, bootstyle="round")
        self.output_text.config(yscrollcommand=self.output_v_scroll.set, xscrollcommand=self.output_h_scroll.set)
        self.output_text.grid(row=0, column=0, sticky="nsew")
        self.output_v_scroll.grid(row=0, column=1, sticky="ns")
        self.output_v_scroll.grid_remove()
        self.output_text.tag_configure(
            "padding",
            lmargin1=20,
            lmargin2=20,
            rmargin=20,
            spacing1=2,
            spacing3=2
        )
        self.output_text.insert("1.0", "")
        self.output_text.tag_add("padding", "1.0", "end")

        def apply_padding(event=None):
            self.output_text.tag_add("padding", "1.0", "end")
        self.output_text.bind("<<Modified>>", lambda e: (apply_padding(), self.output_text.edit_modified(False)))

        def handle_mousewheel(event):
            self.output_text.yview_scroll(-1*(event.delta//120), "units")
            return "break"
        self.output_text.bind("<MouseWheel>", handle_mousewheel)

    def enter_pressed(self, event=None):

        if self.listbox_up and self.lb_index >= 0:
            selected = self.lb.get(self.lb_index)
            self.replace_current_word(selected + " ")
            self.lb_frame.destroy()
            self.listbox_up = False
            self.lb_index = -1
            return "break"
        else:
            self.translate_text()
            return "break"

    def new_line(self, event=None):
        self.entry.insert(ttk.INSERT, "\n")
        self.update_height()
        return "break"

    def load_words(self, first_letter):
        file_path = resource_path(os.path.join(WORDS_FOLDER, f"{first_letter.lower()}.json"))

        if os.path.exists(file_path):

            with open(file_path, "r", encoding="utf-8") as f:
                self.words = json.load(f)
        else:
            self.words = []

    def get_current_word(self):
        text = self.entry.get("insert linestart", "insert")
        return text.split(" ")[-1]

    def replace_current_word(self, new_word):
        idx = "insert"
        line_start = self.entry.index(f"{idx} linestart")
        text = self.entry.get(line_start, idx)
        parts = text.split(" ")
        parts[-1] = new_word
        self.entry.delete(line_start, idx)
        self.entry.insert(line_start, " ".join(parts))

    def changed(self, event=None):
        self.update_height()
        typed = self.get_current_word()
        matches = []

        if typed:
            first_letter = typed[0].lower()
            self.load_words(first_letter)
            matches = [w for w in self.words if w.lower().startswith(typed.lower())]

        if matches:

            if not self.listbox_up or not hasattr(self, "lb_frame"):
                self.lb_frame = ttk.Frame(self.root)
                self.lb = tk.Listbox(self.lb_frame, width=20, height=6, cursor="hand2")
                self.lb.pack(side=tk.LEFT, fill=tk.BOTH)
                self.lb.bind("<<ListboxSelect>>", self.click_selection)
                self.scrollbar = ttk.Scrollbar(self.lb_frame, bootstyle="round")
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                self.lb.config(yscrollcommand=self.scrollbar.set)
                self.scrollbar.config(command=self.lb.yview)
                self.listbox_up = True
                self.lb_index = 0
            self.lb.delete(0, tk.END)
            for word in matches:
                self.lb.insert(tk.END, word)

            if self.lb_index < self.lb.size():
                self.lb.select_set(self.lb_index)
                self.lb.activate(self.lb_index)
                self.lb.see(self.lb_index)
            self.update_listbox_position()
        else:

            if self.listbox_up and hasattr(self, "lb_frame"):
                self.lb_frame.destroy()
                self.listbox_up = False
                self.lb_index = -1

    def update_listbox_position(self):

        if self.listbox_up and hasattr(self, "lb_frame"):
            bbox = self.entry.bbox("insert")

            if bbox:
                x, y, w, h = bbox
                self.abs_x = self.entry.winfo_rootx() + x
                self.abs_y = self.entry.winfo_rooty() + y + h

                if self.abs_x - self.root.winfo_rootx() < 445:
                    self.lb_frame.place(
                        x=self.abs_x - self.root.winfo_rootx(),
                        y=self.abs_y - self.root.winfo_rooty()
                    )
                else:
                    self.lb_frame.place(
                        x=self.abs_x - self.root.winfo_rootx() - self.lb_frame.winfo_width(),
                        y=self.abs_y - self.root.winfo_rooty()
                    )

    def move_down(self, event):

        if self.listbox_up:

            if self.lb_index < self.lb.size() - 1:
                self.lb_index += 1
                self.lb.select_clear(0, ttk.END)
                self.lb.select_set(self.lb_index)
                self.lb.activate(self.lb_index)
                self.lb.see(self.lb_index)
            return "break"

    def move_up(self, event):

        if self.listbox_up:

            if self.lb_index > 0:
                self.lb_index -= 1
                self.lb.select_clear(0, ttk.END)
                self.lb.select_set(self.lb_index)
                self.lb.activate(self.lb_index)
                self.lb.see(self.lb_index)
            return "break"

    def click_selection(self, event):

        if self.listbox_up:
            index = self.lb.curselection()

            if index:
                self.lb_index = index[0]
                selected = self.lb.get(self.lb_index)
                self.replace_current_word(selected)
                self.lb_frame.destroy()
                self.listbox_up = False
                self.lb_index = -1

    def translate_text(self):
        english_text = self.entry.get("1.0", ttk.END).strip()

        if not english_text:
            messagebox.showwarning("Input Error", "Please enter some text to translate!")
            return

        if len(english_text) > 5000:
            chunks = []
            for i in range(0, len(english_text), 5000):
                chunk = english_text[i:i+5000]

                if i+5000 < len(english_text):
                    last_period = chunk.rfind('.')
                    last_space = chunk.rfind(' ')

                    if last_period != -1 and last_period > len(chunk) - 100:
                        chunk = chunk[:last_period+1]
                        i = i - (5000 - last_period - 1)
                    elif last_space != -1:
                        chunk = chunk[:last_space]
                        i = i - (5000 - last_space)
                chunks.append(chunk)
        else:
            chunks = [english_text]

        try:
            translated_chunks = []
            for chunk in chunks:
                bengali_chunk = GoogleTranslator(source='en', target=self.target_language_code).translate(chunk)
                translated_chunks.append(bengali_chunk)
                self.root.update()
                self.root.after(100)
            bengali_text = ' '.join(translated_chunks)
            self.output_text.config(state='normal')
            self.output_text.delete(1.0, ttk.END)
            self.output_text.insert(ttk.END, bengali_text)
            lines = int(self.output_text.index('end-1c').split('.')[0])

            if lines > 6:
                self.output_v_scroll.grid()
            else:
                self.output_v_scroll.grid_remove()
            text_content = self.output_text.get("1.0", "end-1c").split("\n")
            max_line_length = max((len(line) for line in text_content), default=0)

            if max_line_length > int(self.output_text['width']):
                self.output_h_scroll.grid(row=1, column=0, sticky="ew", columnspan=2)
            else:
                self.output_h_scroll.grid_remove()
            self.output_text.update_idletasks()
            self.output_text.config(state='disabled')

        except Exception as e:
            messagebox.showerror("Translation Error", f"Error during translation: {str(e)}")

    def load_window_geometry(self):

        if os.path.exists(self.config_file):
            config = configparser.ConfigParser()
            config.read(self.config_file)

            if "Geometry" in config:
                geometry = config["Geometry"].get("size", "")
                state = config["Geometry"].get("state", "normal")

                if geometry:
                    self.root.geometry(geometry)
                    self.root.update_idletasks()
                    self.root.update()

                if state == "zoomed":
                    self.root.state("zoomed")
                elif state == "iconic":
                    self.root.iconify()

    def save_window_geometry(self):
        config = configparser.ConfigParser()
        config["Geometry"] = {
            "size": self.root.geometry(),
            "state": self.root.state()
        }

        with open(self.config_file, "w") as f:
            config.write(f)

    def on_close(self):
        self.save_window_geometry()
        root.destroy()
        os._exit(0)

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = TranslatorApp(root)
    root.mainloop()
