import tkinter as tk
from tkinter import font, scrolledtext
from PIL import Image, ImageTk
import ctypes
import sys
from datetime import datetime

class EtchItApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ETCH-IT")
        
        # --- Fullscreen & Resize Settings ---
        self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # ==========================================
        # 1. HEX CODE COLOR CONFIGURATION
        # ==========================================
        self.colors = {
            "root_bg": "#000000",
            "sidebar_bg": "#FFFFFF",
            "main_content_bg": "#F5F5F5",
            "sidebar_text": "#6D6B6B",
            "nav_hover": "#F0F0F0",
            "accent_red": "#9a1e1a",
            "btn_hover_red": "#880505",
            "f1_grad_start": "#b81d1d",
            "f1_grad_end": "#f04135",
            "f2_grad_start": "#f68519",
            "f2_grad_end": "#ffe439",
            "f2_hover_start": "#e0740d",
            "f2_hover_end": "#f0d320",
            "f3_grad_start": "#1a73e8",
            "f3_grad_end": "#6fb1fc",
            "f3_hover_start": "#155db1",
            "f3_hover_end": "#63a0e6",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "btn_text_white": "#FFFFFF",
            "console_bg": "#FFFFFF"
        }

        # ==========================================
        # 2. PANEL CONFIGURATIONS
        # ==========================================
        self.frame2_btn_cfg = {
            "width": 440, "height": 400, "pos_x": 90, "pos_y": 600,
            "corner_radius": 15, "text": "View Gerber", "text_color": "#FFFFFF",
            "font": ("Arial", 25, "bold"), "icon_path": "upload.png",
            "icon_size": (35, 35), "spacing": 15
        }

        self.frame3_btn_cfg = {
            "width": 440, "height": 400, "pos_x": 550, "pos_y": 600,
            "corner_radius": 15, "text": "Etch-IT!", "text_color": "#FFFFFF",
            "font": ("Arial", 25, "bold"), "icon_path": "cnc.png",
            "icon_size": (35, 35), "spacing": 15
        }

        # Status / Debug Panel Config
        self.status_cfg = {
            "width": 380, "height": 840, "pos_x": 1020, "pos_y": 160,
            "corner_radius": 20
        }

        # ==========================================
        # 3. NEW: STANDALONE ICON CONFIGURATION
        # ==========================================
        self.right_standalone_cfg = {
            "path": "doodle.png",        # Change to your desired icon file
            "size": (420, 1100),       # Change size (width, height)
            "pos_x": 1400,            # Change horizontal position
            "pos_y": 1              # Change vertical position
        }

        self.cfg = {
            "sidebar_rel_width": 0.065, "header_logo_size": (70, 70),
            "nav_icon_size": (30, 30), "button_padding_x": 20,
            "nav_font_size": 10, "corner_radius": 15 
        }
        
        self.frame1_icon_path = "circuit.png" 
        self.frame1_icon_size = (390, 390)    
        self.frame1_icon_pos = (680, 180)    

        self.apply_dark_title_bar(self.root)
        self.root.configure(bg=self.colors["root_bg"])
        self.load_assets()

        # --- Layout Setup ---
        self.sidebar = tk.Frame(self.root, bg=self.colors["sidebar_bg"])
        self.sidebar.place(relx=0, rely=0, relwidth=self.cfg["sidebar_rel_width"], relheight=1)

        self.main_content = tk.Frame(self.root, bg=self.colors["main_content_bg"])
        self.main_content.place(relx=self.cfg["sidebar_rel_width"], rely=0, 
                                relwidth=1-self.cfg["sidebar_rel_width"], relheight=1)

        # --- HOMEPAGE ELEMENTS ---
        self.home_elements = []
        self.anim_x, self.anim_y = 90, 60
        self.welcome_label = tk.Label(self.main_content, text="", bg=self.colors["main_content_bg"], 
                                      fg=self.colors["accent_red"], font=("Arial", 20, "bold"))
        self.welcome_label.place(x=self.anim_x, y=self.anim_y)
        self.home_elements.append(self.welcome_label)
        
        self.subtitle_label = tk.Label(self.main_content, text="PCB Etching and Drilling Device for Chemical-Free Fabrication", 
                                      bg=self.colors["main_content_bg"], fg=self.colors["text_secondary"], font=("Arial", 16))
        self.subtitle_label.place(x=90, y=95)
        self.home_elements.append(self.subtitle_label)

        # --- FRAME 1 ---
        self.center_frame_x, self.center_frame_y = 90, 160
        self.center_frame_w, self.center_frame_h = 900, 410
        self.mid_canvas = tk.Canvas(self.main_content, bg=self.colors["main_content_bg"], highlightthickness=0)
        self.mid_canvas.place(x=self.center_frame_x, y=self.center_frame_y, width=self.center_frame_w, height=self.center_frame_h)
        self.home_elements.append(self.mid_canvas)
        self.draw_f1_content()

        # --- FRAME 2 ---
        f2 = self.frame2_btn_cfg
        self.mid_canvas2 = tk.Canvas(self.main_content, bg=self.colors["main_content_bg"], 
                                     width=f2["width"], height=f2["height"], highlightthickness=0, cursor="hand2")
        self.mid_canvas2.place(x=f2["pos_x"], y=f2["pos_y"])
        self.home_elements.append(self.mid_canvas2)
        self.draw_f2_button()

        # --- FRAME 3 ---
        f3 = self.frame3_btn_cfg
        self.mid_canvas3 = tk.Canvas(self.main_content, bg=self.colors["main_content_bg"], 
                                     width=f3["width"], height=f3["height"], highlightthickness=0, cursor="hand2")
        self.mid_canvas3.place(x=f3["pos_x"], y=f3["pos_y"])
        self.home_elements.append(self.mid_canvas3)
        self.draw_f3_button()

        # --- STATUS CONSOLE ---
        self.setup_status_console()

        # --- PLACING THE NEW STANDALONE ICON ---
        if hasattr(self, 'right_standalone_img'):
            self.standalone_icon_label = tk.Label(self.main_content, image=self.right_standalone_img, 
                                                 bg=self.colors["main_content_bg"])
            self.standalone_icon_label.place(x=self.right_standalone_cfg["pos_x"], 
                                            y=self.right_standalone_cfg["pos_y"])
            self.home_elements.append(self.standalone_icon_label)

        # --- HOVER BINDINGS ---
        self.mid_canvas2.bind("<Enter>", lambda e: self.draw_f2_button(hover=True))
        self.mid_canvas2.bind("<Leave>", lambda e: self.draw_f2_button(hover=False))
        self.mid_canvas3.bind("<Enter>", lambda e: self.draw_f3_button(hover=True))
        self.mid_canvas3.bind("<Leave>", lambda e: self.draw_f3_button(hover=False))

        # Sidebar & Animation
        self.setup_header("logo2.png")
        self.home_btn = self.create_nav_item("Home", self.home_icon_img, pack_side="top")
        self.exit_btn = self.create_nav_item("Exit", self.exit_icon_img, pack_side="bottom")
        self.hide_btn = self.create_nav_item("Hide", self.hide_icon_img, pack_side="bottom")
        self.phrases = ["Welcome to ETCH-IT!", "Interprets Gerber Files", "Generates G-codes!"]
        self.current_phrase_index = 0
        self.typewriter_effect(0)
        self.root.after(100, self.sync_sidebar_buttons)

        # Initial Log
        self.log_message("System Initialized...")
        self.log_message("Ready for Gerber input.")

    def setup_status_console(self):
        s = self.status_cfg
        self.console_canvas = tk.Canvas(self.main_content, bg=self.colors["main_content_bg"], 
                                        width=s["width"], height=s["height"], highlightthickness=0)
        self.console_canvas.place(x=s["pos_x"], y=s["pos_y"])
        self.home_elements.append(self.console_canvas)
        self.draw_rounded_rect(self.console_canvas, 0, 0, s["width"], s["height"], s["corner_radius"], color=self.colors["console_bg"])
        self.console_canvas.create_text(20, 30, text="SYSTEM LOGS", fill=self.colors["accent_red"], font=("Arial", 14, "bold"), anchor="w")
        self.console_canvas.create_line(20, 50, s["width"]-20, 50, fill="#EEEEEE")
        self.log_widget = tk.Text(self.main_content, bg=self.colors["console_bg"], fg=self.colors["text_primary"],
                                  font=("Consolas", 10), borderwidth=0, highlightthickness=0, state='disabled')
        self.log_widget.place(x=s["pos_x"]+15, y=s["pos_y"]+60, width=s["width"]-30, height=s["height"]-80)

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_widget.config(state='normal')
        self.log_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_widget.see(tk.END)
        self.log_widget.config(state='disabled')

    def handle_click(self, name):
        self.log_message(f"Navigation: {name} clicked.")
        if name == "Exit": self.root.destroy()
        elif name == "Hide": self.root.iconify()

    def draw_f1_content(self):
        self.mid_canvas.delete("all")
        self.draw_rounded_rect(self.mid_canvas, 0, 0, self.center_frame_w, self.center_frame_h, 20, 
                                gradient=(self.colors["f1_grad_start"], self.colors["f1_grad_end"]))
        self.mid_canvas.create_text(70, 110, text="Generate G-Code", fill="#FFFFFF", font=("Arial", 30, "bold"), anchor="w")
        self.mid_canvas.create_text(72, 150, text="Upload Gerber and Drill File", fill="#FFFFFF", font=("Arial", 14), anchor="w")
        if hasattr(self, 'frame1_right_icon'):
            self.mid_canvas.create_image(self.frame1_icon_pos[0], self.frame1_icon_pos[1] + 20, image=self.frame1_right_icon)
        
        self.start_btn_canvas = tk.Canvas(self.mid_canvas, bg=self.colors["f1_grad_start"], width=220, height=50, highlightthickness=0, cursor="hand2")
        self.start_btn_canvas.place(x=130, y=240)
        
        def on_gen_click(e):
            self.log_message("Starting G-Code Generation...")
            self.log_message("Analyzing Gerber layers...")
            self.root.after(1000, lambda: self.log_message("SUCCESS: G-Code generated."))

        def draw_gen_btn(color):
            self.draw_rounded_rect(self.start_btn_canvas, 0, 0, 220, 50, 10, color=color)
            self.start_btn_canvas.create_text(110, 25, text="GENERATE!", fill=self.colors["btn_text_white"], font=("Arial", 10, "bold"))
        
        draw_gen_btn("#424242")
        self.start_btn_canvas.bind("<Enter>", lambda e: draw_gen_btn("#5a5a5a"))
        self.start_btn_canvas.bind("<Leave>", lambda e: draw_gen_btn("#424242"))
        self.start_btn_canvas.bind("<Button-1>", on_gen_click)

    def draw_f2_button(self, hover=False):
        self.mid_canvas2.delete("all")
        f2 = self.frame2_btn_cfg
        c1 = self.colors["f2_hover_start"] if hover else self.colors["f2_grad_start"]
        c2 = self.colors["f2_hover_end"] if hover else self.colors["f2_grad_end"]
        self.draw_rounded_rect(self.mid_canvas2, 0, 0, f2["width"], f2["height"], f2["corner_radius"], gradient=(c1, c2))
        text_font = font.Font(family=f2["font"][0], size=f2["font"][1], weight=f2["font"][2])
        total_w = f2["icon_size"][0] + f2["spacing"] + text_font.measure(f2["text"])
        start_x = (f2["width"] - total_w) / 2
        if hasattr(self, 'f2_icon_img'):
            self.mid_canvas2.create_image(start_x + (f2["icon_size"][0]/2), f2["height"]/2, image=self.f2_icon_img)
        self.mid_canvas2.create_text(start_x + f2["icon_size"][0] + f2["spacing"], f2["height"]/2, text=f2["text"], fill=f2["text_color"], font=f2["font"], anchor="w")
        self.mid_canvas2.bind("<Button-1>", lambda e: self.log_message("Opening Gerber Viewer..."))

    def draw_f3_button(self, hover=False):
        self.mid_canvas3.delete("all")
        f3 = self.frame3_btn_cfg
        c1 = self.colors["f3_hover_start"] if hover else self.colors["f3_grad_start"]
        c2 = self.colors["f3_hover_end"] if hover else self.colors["f3_grad_end"]
        self.draw_rounded_rect(self.mid_canvas3, 0, 0, f3["width"], f3["height"], f3["corner_radius"], gradient=(c1, c2))
        text_font = font.Font(family=f3["font"][0], size=f3["font"][1], weight=f3["font"][2])
        total_w = f3["icon_size"][0] + f3["spacing"] + text_font.measure(f3["text"])
        start_x = (f3["width"] - total_w) / 2
        if hasattr(self, 'f3_icon_img'):
            self.mid_canvas3.create_image(start_x + (f3["icon_size"][0]/2), f3["height"]/2, image=self.f3_icon_img)
        self.mid_canvas3.create_text(start_x + f3["icon_size"][0] + f3["spacing"], f3["height"]/2, text=f3["text"], fill=f3["text_color"], font=f3["font"], anchor="w")
        self.mid_canvas3.bind("<Button-1>", lambda e: self.log_message("Etching process sequence started."))

    def load_assets(self):
        try:
            self.home_icon_img = ImageTk.PhotoImage(Image.open("home.png").resize(self.cfg["nav_icon_size"], Image.Resampling.LANCZOS))
            self.exit_icon_img = ImageTk.PhotoImage(Image.open("logo3.png").resize(self.cfg["nav_icon_size"], Image.Resampling.LANCZOS))
            self.hide_icon_img = ImageTk.PhotoImage(Image.open("logo4.png").resize(self.cfg["nav_icon_size"], Image.Resampling.LANCZOS))
            f1_icon = Image.open(self.frame1_icon_path).resize(self.frame1_icon_size, Image.Resampling.LANCZOS)
            self.frame1_right_icon = ImageTk.PhotoImage(f1_icon)
            f2_icon = Image.open(self.frame2_btn_cfg["icon_path"]).resize(self.frame2_btn_cfg["icon_size"], Image.Resampling.LANCZOS)
            self.f2_icon_img = ImageTk.PhotoImage(f2_icon)
            f3_icon = Image.open(self.frame3_btn_cfg["icon_path"]).resize(self.frame3_btn_cfg["icon_size"], Image.Resampling.LANCZOS)
            self.f3_icon_img = ImageTk.PhotoImage(f3_icon)
            
            # Load the new standalone icon
            standalone_img = Image.open(self.right_standalone_cfg["path"]).resize(self.right_standalone_cfg["size"], Image.Resampling.LANCZOS)
            self.right_standalone_img = ImageTk.PhotoImage(standalone_img)
            
        except Exception as e: print(f"Asset Error: {e}")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def draw_rounded_rect(self, canvas, x, y, w, h, r, color=None, gradient=None):
        canvas.delete("shape")
        if gradient:
            start_rgb, end_rgb = self.hex_to_rgb(gradient[0]), self.hex_to_rgb(gradient[1])
            for i in range(int(w)):
                curr_rgb = tuple(int(start_rgb[j] + (end_rgb[j] - start_rgb[j]) * (i / w)) for j in range(3))
                curr_hex = self.rgb_to_hex(curr_rgb)
                canvas.create_line(x + i, y + r, x + i, y + h - r, fill=curr_hex, tags="shape")
                if i >= r and i <= w - r:
                    canvas.create_line(x + i, y, x + i, y + r, fill=curr_hex, tags="shape")
                    canvas.create_line(x + i, y + h - r, x + i, y + h, fill=curr_hex, tags="shape")
            canvas.create_oval(x, y, x+r*2, y+r*2, fill=gradient[0], outline=gradient[0], tags="shape")
            canvas.create_oval(x+w-r*2, y, x+w, y+r*2, fill=gradient[1], outline=gradient[1], tags="shape")
            canvas.create_oval(x, y+h-r*2, x+r*2, y+h, fill=gradient[0], outline=gradient[0], tags="shape")
            canvas.create_oval(x+w-r*2, y+h-r*2, x+w, y+h, fill=gradient[1], outline=gradient[1], tags="shape")
        else:
            canvas.create_oval(x, y, x+r*2, y+r*2, fill=color, outline=color, tags="shape")
            canvas.create_oval(x+w-r*2, y, x+w, y+r*2, fill=color, outline=color, tags="shape")
            canvas.create_oval(x, y+h-r*2, x+r*2, y+h, fill=color, outline=color, tags="shape")
            canvas.create_oval(x+w-r*2, y+h-r*2, x+w, y+h, fill=color, outline=color, tags="shape")
            canvas.create_rectangle(x+r, y, x+w-r, y+h, fill=color, outline=color, tags="shape")
            canvas.create_rectangle(x, y+r, x+w, y+h-r, fill=color, outline=color, tags="shape")
        canvas.tag_lower("shape")

    def create_nav_item(self, text, icon, pack_side="top"):
        canvas = tk.Canvas(self.sidebar, bg=self.colors["sidebar_bg"], highlightthickness=0, cursor="hand2")
        canvas.pack(side=pack_side, padx=self.cfg["button_padding_x"], pady=(10, 20 if text == "Exit" else 0))
        canvas.bind("<Enter>", lambda e: self.draw_btn(canvas, self.colors["nav_hover"], text, icon))
        canvas.bind("<Leave>", lambda e: self.draw_btn(canvas, self.colors["sidebar_bg"], text, icon))
        canvas.bind("<Button-1>", lambda e: self.handle_click(text))
        return {"canvas": canvas, "text": text, "icon": icon}

    def draw_btn(self, canvas, color, text, icon):
        canvas.delete("all")
        canvas.update_idletasks()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w < 5: return
        self.draw_rounded_rect(canvas, 0, 0, w, h, self.cfg["corner_radius"], color=color)
        if icon: canvas.create_image(w/2, h/2 - 10, image=icon)
        canvas.create_text(w/2, h/2 + (18 if icon else 0), text=text, fill=self.colors["sidebar_text"], font=("Arial", self.cfg["nav_font_size"], "bold"))

    def setup_header(self, logo_path):
        try:
            img = Image.open(logo_path).resize(self.cfg["header_logo_size"], Image.Resampling.LANCZOS)
            self.side_logo_img = ImageTk.PhotoImage(img)
            tk.Label(self.sidebar, image=self.side_logo_img, bg=self.colors["sidebar_bg"]).pack(pady=(40, 5)) 
            tk.Label(self.sidebar, text="ETCH-IT", bg=self.colors["sidebar_bg"], fg=self.colors["sidebar_text"], font=("Arial", 11, "bold")).pack(pady=(0, 30))
        except: pass

    def typewriter_effect(self, char_index):
        phrase = self.phrases[self.current_phrase_index]
        if char_index <= len(phrase):
            self.welcome_label.config(text=phrase[:char_index])
            self.root.after(100, lambda: self.typewriter_effect(char_index + 1))
        else: self.root.after(500, lambda: self.jump_animation(0, 2))

    def jump_animation(self, jump_count, total_jumps):
        if jump_count < total_jumps:
            self.welcome_label.place(x=self.anim_x, y=self.anim_y - 15)
            self.root.after(150, lambda: self.welcome_label.place(x=self.anim_x, y=self.anim_y))
            self.root.after(300, lambda: self.jump_animation(jump_count + 1, total_jumps))
        else: self.root.after(1500, self.next_phrase)

    def next_phrase(self):
        self.current_phrase_index = (self.current_phrase_index + 1) % len(self.phrases)
        self.welcome_label.config(text="")
        self.typewriter_effect(0)

    def sync_sidebar_buttons(self, event=None):
        self.sidebar.update_idletasks()
        sidebar_w = self.sidebar.winfo_width()
        new_size = sidebar_w - (self.cfg["button_padding_x"] * 2)
        if new_size > 20:
            for btn in [self.home_btn, self.exit_btn, self.hide_btn]:
                btn["canvas"].config(width=new_size, height=new_size)
                self.root.after(10, lambda b=btn: self.draw_btn(b["canvas"], self.colors["sidebar_bg"], b["text"], b["icon"]))

    def apply_dark_title_bar(self, window):
        try:
            window.update()
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(ctypes.c_int(2)), 4)
        except: pass 


if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Hide the window initially so it doesn't show a white box
    root.withdraw() 
    
    app = EtchItApp(root)
    
    # 2. Force the window to calculate its size and position
    root.update_idletasks()
    
    # 3. Bring the window forward once it's ready
    root.deiconify()
    
    root.mainloop()