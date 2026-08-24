import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

from organizer import (
    preview_folder,
    organize_folder,
    undo_last,
    load_file_types,
    save_file_types,
    auto_organize_loop
)


# =================================================
# APP CONFIG
# =================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Smart File Organizer")
app.geometry("1100x720")
app.minsize(1000, 650)


# =================================================
# COLORS
# =================================================

BG = "#0B0F19"
SIDEBAR = "#111827"
CARD = "#151C2B"
CARD_HOVER = "#1B2436"
TEXT = "#F8FAFC"
MUTED = "#94A3B8"
ACCENT = "#3B82F6"
SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"


app.configure(fg_color=BG)


# =================================================
# VARIABLES
# =================================================

selected_folder = ""
preview_data = []

auto_thread = None
auto_stop_event = None
is_auto_running = False

moved_count = 0
error_count = 0


# =================================================
# GENERAL HELPERS
# =================================================

def update_status(text):
    status_label.configure(text=text)


def choose_folder():

    global selected_folder

    folder = filedialog.askdirectory(
        title="Select Folder"
    )

    if folder:

        selected_folder = folder

        folder_path_label.configure(
            text=selected_folder
        )

        update_status(
            "Folder selected. Ready to organize."
        )


# =================================================
# PREVIEW
# =================================================

def show_preview():

    global preview_data

    if not selected_folder:

        messagebox.showwarning(
            "No Folder Selected",
            "Please select a folder first."
        )

        return

    try:

        preview_data = preview_folder(
            selected_folder
        )

        window = ctk.CTkToplevel(app)

        window.title("Organization Preview")
        window.geometry("850x600")
        window.configure(fg_color=BG)

        window.grab_set()

        title = ctk.CTkLabel(
            window,
            text="Organization Preview",
            font=("Segoe UI", 26, "bold"),
            text_color=TEXT
        )

        title.pack(
            pady=(25, 5)
        )

        subtitle = ctk.CTkLabel(
            window,
            text=f"{len(preview_data)} files found",
            font=("Segoe UI", 14),
            text_color=MUTED
        )

        subtitle.pack(
            pady=(0, 20)
        )

        scroll = ctk.CTkScrollableFrame(
            window,
            fg_color=CARD,
            corner_radius=15
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        if not preview_data:

            empty = ctk.CTkLabel(
                scroll,
                text="No files found in this folder.",
                font=("Segoe UI", 16),
                text_color=MUTED
            )

            empty.pack(
                pady=40
            )

        else:

            for item in preview_data:

                row = ctk.CTkFrame(
                    scroll,
                    fg_color=CARD_HOVER,
                    corner_radius=10
                )

                row.pack(
                    fill="x",
                    padx=8,
                    pady=5
                )

                file_label = ctk.CTkLabel(
                    row,
                    text=item["name"],
                    font=("Segoe UI", 13, "bold"),
                    text_color=TEXT,
                    anchor="w"
                )

                file_label.pack(
                    side="left",
                    padx=15,
                    pady=12
                )

                destination = ctk.CTkLabel(
                    row,
                    text=f"→ {item['destination']}",
                    font=("Segoe UI", 13),
                    text_color=ACCENT
                )

                destination.pack(
                    side="right",
                    padx=15
                )

        confirm = ctk.CTkButton(
            window,
            text="Confirm & Organize",
            width=220,
            height=45,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color="#2563EB",
            font=("Segoe UI", 14, "bold"),
            command=lambda: confirm_preview(window)
        )

        confirm.pack(
            pady=20
        )

    except Exception as e:

        messagebox.showerror(
            "Preview Error",
            str(e)
        )


def confirm_preview(window):

    window.destroy()

    start_organizing()


# =================================================
# ORGANIZE
# =================================================

def start_organizing():

    global moved_count
    global error_count

    if not selected_folder:

        messagebox.showwarning(
            "No Folder Selected",
            "Please select a folder first."
        )

        return

    if is_auto_running:

        messagebox.showwarning(
            "Auto Organize Active",
            "Stop Auto Organize first."
        )

        return

    start_button.configure(
        state="disabled"
    )

    preview_button.configure(
        state="disabled"
    )

    choose_button.configure(
        state="disabled"
    )

    progress_bar.set(0)

    progress_label.configure(
        text="Preparing..."
    )

    update_status(
        "Organizing your files..."
    )

    moved_count = 0
    error_count = 0

    thread = threading.Thread(
        target=organize_thread,
        daemon=True
    )

    thread.start()


def organize_thread():

    try:

        result = organize_folder(
            selected_folder,
            update_progress
        )

        app.after(
            0,
            organization_finished,
            result
        )

    except Exception as e:

        app.after(
            0,
            show_error,
            str(e)
        )


def update_progress(current, total):

    if total == 0:

        progress = 1

    else:

        progress = current / total

    app.after(
        0,
        lambda: progress_bar.set(progress)
    )

    app.after(
        0,
        lambda: progress_label.configure(
            text=f"{current} / {total} files"
        )
    )


def organization_finished(result):

    start_button.configure(
        state="normal"
    )

    preview_button.configure(
        state="normal"
    )

    choose_button.configure(
        state="normal"
    )

    progress_bar.set(1)

    moved = result.get(
        "moved",
        0
    )

    errors = result.get(
        "errors",
        0
    )

    total = result.get(
        "total",
        0
    )

    moved_value.configure(
        text=str(moved)
    )

    error_value.configure(
        text=str(errors)
    )

    total_value.configure(
        text=str(total)
    )

    progress_label.configure(
        text=f"{total} / {total} files"
    )

    update_status(
        "Organization completed successfully."
    )

    messagebox.showinfo(
        "Organization Complete",
        f"Total Files: {total}\n\n"
        f"Moved: {moved}\n"
        f"Errors: {errors}"
    )


def show_error(error):

    start_button.configure(
        state="normal"
    )

    preview_button.configure(
        state="normal"
    )

    choose_button.configure(
        state="normal"
    )

    update_status(
        "Something went wrong."
    )

    messagebox.showerror(
        "Error",
        error
    )


# =================================================
# UNDO
# =================================================

def undo():

    if is_auto_running:

        messagebox.showwarning(
            "Auto Organize Active",
            "Stop Auto Organize first."
        )

        return

    result = undo_last()

    if not result["success"]:

        messagebox.showinfo(
            "Undo",
            result["message"]
        )

        return

    restored = result.get(
        "restored",
        0
    )

    errors = result.get(
        "errors",
        0
    )

    update_status(
        "Last organization has been undone."
    )

    messagebox.showinfo(
        "Undo Complete",
        f"Files restored: {restored}\n"
        f"Errors: {errors}"
    )


# =================================================
# AUTO ORGANIZE
# =================================================

def toggle_auto():

    if auto_switch.get():

        start_auto()

    else:

        stop_auto()


def start_auto():

    global auto_stop_event
    global auto_thread
    global is_auto_running

    if not selected_folder:

        auto_switch.deselect()

        messagebox.showwarning(
            "No Folder Selected",
            "Please select a folder first."
        )

        return

    auto_stop_event = threading.Event()

    is_auto_running = True

    choose_button.configure(
        state="disabled"
    )

    start_button.configure(
        state="disabled"
    )

    preview_button.configure(
        state="disabled"
    )

    undo_button.configure(
        state="disabled"
    )

    stop_auto_button.configure(
        state="normal"
    )

    progress_bar.configure(
        mode="indeterminate"
    )

    progress_bar.start()

    update_status(
        "Auto Organize is watching the folder..."
    )

    auto_thread = threading.Thread(
        target=run_auto,
        daemon=True
    )

    auto_thread.start()


def run_auto():

    try:

        auto_organize_loop(
            selected_folder,
            auto_stop_event,
            auto_callback
        )

    except Exception as e:

        app.after(
            0,
            show_error,
            str(e)
        )


def auto_callback(
    filename,
    result
):

    app.after(
        0,
        lambda: update_status(
            f"Auto organized: {filename}"
        )
    )


def stop_auto():

    global is_auto_running

    if not is_auto_running:

        return

    if auto_stop_event:

        auto_stop_event.set()

    is_auto_running = False

    progress_bar.stop()

    progress_bar.configure(
        mode="determinate"
    )

    progress_bar.set(0)

    choose_button.configure(
        state="normal"
    )

    start_button.configure(
        state="normal"
    )

    preview_button.configure(
        state="normal"
    )

    undo_button.configure(
        state="normal"
    )

    stop_auto_button.configure(
        state="disabled"
    )

    auto_switch.deselect()

    update_status(
        "Auto Organize stopped."
    )


# =================================================
# SETTINGS
# =================================================

def open_settings():

    window = ctk.CTkToplevel(app)

    window.title("Settings")
    window.geometry("800x650")
    window.configure(fg_color=BG)

    window.grab_set()

    title = ctk.CTkLabel(
        window,
        text="File Organization Rules",
        font=("Segoe UI", 25, "bold"),
        text_color=TEXT
    )

    title.pack(
        pady=(25, 5)
    )

    subtitle = ctk.CTkLabel(
        window,
        text="Customize where each file type is stored.",
        font=("Segoe UI", 14),
        text_color=MUTED
    )

    subtitle.pack(
        pady=(0, 20)
    )

    scroll = ctk.CTkScrollableFrame(
        window,
        fg_color=CARD,
        corner_radius=15
    )

    scroll.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    entries = []

    file_types = load_file_types()

    for extension, folder in file_types.items():

        row = ctk.CTkFrame(
            scroll,
            fg_color=CARD_HOVER,
            corner_radius=8
        )

        row.pack(
            fill="x",
            padx=8,
            pady=4
        )

        extension_label = ctk.CTkLabel(
            row,
            text=extension,
            width=100,
            anchor="w",
            font=("Segoe UI", 13, "bold")
        )

        extension_label.pack(
            side="left",
            padx=15,
            pady=8
        )

        entry = ctk.CTkEntry(
            row,
            width=450
        )

        entry.insert(
            0,
            folder
        )

        entry.pack(
            side="left",
            padx=10
        )

        entries.append(
            (extension, entry)
        )

    def save():

        new_rules = {}

        for extension, entry in entries:

            destination = entry.get().strip()

            if destination:

                new_rules[
                    extension
                ] = destination

        if save_file_types(
            new_rules
        ):

            messagebox.showinfo(
                "Saved",
                "Settings saved successfully."
            )

            window.destroy()

        else:

            messagebox.showerror(
                "Error",
                "Could not save settings."
            )

    save_button = ctk.CTkButton(
        window,
        text="Save Changes",
        width=220,
        height=45,
        corner_radius=10,
        command=save
    )

    save_button.pack(
        pady=20
    )


# =================================================
# THEME
# =================================================

def toggle_theme():

    if theme_switch.get():

        ctk.set_appearance_mode("light")

    else:

        ctk.set_appearance_mode("dark")


# =================================================
# SIDEBAR
# =================================================

sidebar = ctk.CTkFrame(
    app,
    width=230,
    corner_radius=0,
    fg_color=SIDEBAR
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


logo = ctk.CTkLabel(
    sidebar,
    text="SMART\nORGANIZER",
    font=("Segoe UI", 25, "bold"),
    text_color=TEXT,
    justify="left"
)

logo.pack(
    anchor="w",
    padx=30,
    pady=(40, 50)
)


side_text = ctk.CTkLabel(
    sidebar,
    text="FILE MANAGEMENT",
    font=("Segoe UI", 11, "bold"),
    text_color=MUTED
)

side_text.pack(
    anchor="w",
    padx=30,
    pady=(0, 10)
)


# Sidebar buttons

def sidebar_button(text, command):

    button = ctk.CTkButton(
        sidebar,
        text=text,
        height=42,
        corner_radius=8,
        fg_color="transparent",
        hover_color=CARD_HOVER,
        text_color=TEXT,
        anchor="w",
        font=("Segoe UI", 14),
        command=command
    )

    button.pack(
        fill="x",
        padx=18,
        pady=4
    )

    return button


sidebar_button(
    "  Organize Files",
    choose_folder
)

sidebar_button(
    "  Preview Files",
    show_preview
)

sidebar_button(
    "  Undo Last",
    undo
)

sidebar_button(
    "  Settings",
    open_settings
)


# Bottom sidebar

sidebar_bottom = ctk.CTkFrame(
    sidebar,
    fg_color="transparent"
)

sidebar_bottom.pack(
    side="bottom",
    fill="x",
    padx=20,
    pady=25
)


theme_switch = ctk.CTkSwitch(
    sidebar_bottom,
    text="Light Mode",
    command=toggle_theme
)

theme_switch.pack(
    anchor="w"
)


version = ctk.CTkLabel(
    sidebar_bottom,
    text="Smart Organizer v1.0",
    font=("Segoe UI", 11),
    text_color=MUTED
)

version.pack(
    anchor="w",
    pady=(15, 0)
)


# =================================================
# MAIN CONTENT
# =================================================

main = ctk.CTkFrame(
    app,
    fg_color=BG,
    corner_radius=0
)

main.pack(
    side="left",
    fill="both",
    expand=True
)


# Header

header = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

header.pack(
    fill="x",
    padx=35,
    pady=(30, 10)
)


header_title = ctk.CTkLabel(
    header,
    text="File Organizer",
    font=("Segoe UI", 30, "bold"),
    text_color=TEXT
)

header_title.pack(
    side="left"
)


# =================================================
# FOLDER CARD
# =================================================

folder_card = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=15
)

folder_card.pack(
    fill="x",
    padx=35,
    pady=15
)


folder_title = ctk.CTkLabel(
    folder_card,
    text="Selected Folder",
    font=("Segoe UI", 14, "bold"),
    text_color=TEXT
)

folder_title.pack(
    anchor="w",
    padx=25,
    pady=(20, 5)
)


folder_path_label = ctk.CTkLabel(
    folder_card,
    text="No folder selected",
    font=("Segoe UI", 13),
    text_color=MUTED,
    anchor="w"
)

folder_path_label.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


choose_button = ctk.CTkButton(
    folder_card,
    text="Choose Folder",
    width=160,
    height=40,
    corner_radius=8,
    command=choose_folder
)

choose_button.pack(
    anchor="e",
    padx=25,
    pady=(0, 20)
)


# =================================================
# STATISTICS
# =================================================

stats = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

stats.pack(
    fill="x",
    padx=35,
    pady=10
)


def create_stat_card(
    parent,
    title,
    value,
    text_color
):

    card = ctk.CTkFrame(
        parent,
        fg_color=CARD,
        corner_radius=12
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=("Segoe UI", 12),
        text_color=MUTED
    )

    title_label.pack(
        anchor="w",
        padx=20,
        pady=(18, 3)
    )

    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=("Segoe UI", 25, "bold"),
        text_color=text_color
    )

    value_label.pack(
        anchor="w",
        padx=20,
        pady=(0, 18)
    )

    return value_label


total_value = create_stat_card(
    stats,
    "FILES PROCESSED",
    "0",
    TEXT
)

moved_value = create_stat_card(
    stats,
    "FILES MOVED",
    "0",
    SUCCESS
)

error_value = create_stat_card(
    stats,
    "ERRORS",
    "0",
    DANGER
)


# =================================================
# ACTIONS
# =================================================

actions = ctk.CTkFrame(
    main,
    fg_color="transparent"
)

actions.pack(
    fill="x",
    padx=35,
    pady=15
)


preview_button = ctk.CTkButton(
    actions,
    text="Preview",
    width=145,
    height=45,
    corner_radius=9,
    fg_color=CARD,
    hover_color=CARD_HOVER,
    command=show_preview
)

preview_button.pack(
    side="left",
    padx=(0, 8)
)


start_button = ctk.CTkButton(
    actions,
    text="Start Organizing",
    width=175,
    height=45,
    corner_radius=9,
    fg_color=ACCENT,
    hover_color="#2563EB",
    font=("Segoe UI", 13, "bold"),
    command=start_organizing
)

start_button.pack(
    side="left",
    padx=8
)


undo_button = ctk.CTkButton(
    actions,
    text="Undo Last",
    width=145,
    height=45,
    corner_radius=9,
    fg_color=CARD,
    hover_color=CARD_HOVER,
    command=undo
)

undo_button.pack(
    side="left",
    padx=8
)


# =================================================
# AUTO ORGANIZE CARD
# =================================================

auto_card = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=12
)

auto_card.pack(
    fill="x",
    padx=35,
    pady=10
)


auto_info = ctk.CTkFrame(
    auto_card,
    fg_color="transparent"
)

auto_info.pack(
    side="left",
    padx=20,
    pady=15
)


auto_title = ctk.CTkLabel(
    auto_info,
    text="Auto Organize",
    font=("Segoe UI", 14, "bold"),
    text_color=TEXT
)

auto_title.pack(
    anchor="w"
)


auto_description = ctk.CTkLabel(
    auto_info,
    text="Automatically organize new files",
    font=("Segoe UI", 12),
    text_color=MUTED
)

auto_description.pack(
    anchor="w"
)


auto_switch = ctk.CTkSwitch(
    auto_card,
    text="",
    command=toggle_auto
)

auto_switch.pack(
    side="right",
    padx=25
)


stop_auto_button = ctk.CTkButton(
    auto_card,
    text="Stop",
    width=80,
    height=35,
    corner_radius=8,
    fg_color=DANGER,
    hover_color="#DC2626",
    command=stop_auto,
    state="disabled"
)

stop_auto_button.pack(
    side="right",
    padx=5
)


# =================================================
# PROGRESS
# =================================================

progress_card = ctk.CTkFrame(
    main,
    fg_color=CARD,
    corner_radius=12
)

progress_card.pack(
    fill="x",
    padx=35,
    pady=10
)


progress_title = ctk.CTkLabel(
    progress_card,
    text="Activity",
    font=("Segoe UI", 14, "bold"),
    text_color=TEXT
)

progress_title.pack(
    anchor="w",
    padx=20,
    pady=(15, 5)
)


progress_bar = ctk.CTkProgressBar(
    progress_card,
    width=600,
    height=12,
    corner_radius=10
)

progress_bar.pack(
    fill="x",
    padx=20,
    pady=10
)

progress_bar.set(0)


progress_label = ctk.CTkLabel(
    progress_card,
    text="0 / 0 files",
    font=("Segoe UI", 11),
    text_color=MUTED
)

progress_label.pack(
    anchor="e",
    padx=20,
    pady=(0, 15)
)


# =================================================
# STATUS BAR
# =================================================

status_label = ctk.CTkLabel(
    main,
    text="Ready",
    font=("Segoe UI", 12),
    text_color=MUTED
)

status_label.pack(
    anchor="w",
    padx=40,
    pady=5
)


# =================================================
# CLOSE
# =================================================

def close_app():

    global auto_stop_event

    if auto_stop_event:

        auto_stop_event.set()

    app.destroy()


app.protocol(
    "WM_DELETE_WINDOW",
    close_app
)


# =================================================
# START
# =================================================

app.mainloop()