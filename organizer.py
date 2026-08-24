from pathlib import Path
import shutil
import json
import logging
import time
import sys

# -------------------------------------------------
# Application Directory
# -------------------------------------------------

if getattr(sys, "frozen", False):

    # Running as .exe
    APP_DIR = Path(sys.executable).resolve().parent

else:

    # Running as Python script
    APP_DIR = Path(__file__).resolve().parent


SETTINGS_FILE = APP_DIR / "settings.json"
HISTORY_FILE = APP_DIR / "history.json"
LOG_FILE = APP_DIR / "app.log"

# -------------------------------------------------
# Logging
# -------------------------------------------------

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SETTINGS_FILE = "settings.json"
HISTORY_FILE = "history.json"


# -------------------------------------------------
# Load Settings
# -------------------------------------------------

def load_file_types():

    try:

        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        return settings.get("file_types", {})

    except Exception as e:

        logging.error(
            f"Could not load settings: {e}"
        )

        return {}


# -------------------------------------------------
# Save Settings
# -------------------------------------------------

def save_file_types(file_types):

    try:

        with open(
            SETTINGS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                {"file_types": file_types},
                file,
                indent=4
            )

        logging.info("Settings updated")

        return True

    except Exception as e:

        logging.error(
            f"Could not save settings: {e}"
        )

        return False


# -------------------------------------------------
# Load History
# -------------------------------------------------

def load_history():

    try:

        if not Path(HISTORY_FILE).exists():
            return []

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception as e:

        logging.error(
            f"Could not load history: {e}"
        )

        return []


# -------------------------------------------------
# Save History
# -------------------------------------------------

def save_history(history):

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4
            )

    except Exception as e:

        logging.error(
            f"Could not save history: {e}"
        )


# -------------------------------------------------
# Get Destination
# -------------------------------------------------

def get_destination(item, file_types):

    extension = item.suffix.lower()

    return file_types.get(
        extension,
        "Others"
    )


# -------------------------------------------------
# Create Safe Destination
# -------------------------------------------------

def get_unique_destination(
    item,
    destination_folder
):

    destination_path = (
        destination_folder / item.name
    )

    counter = 1

    while destination_path.exists():

        new_name = (
            f"{item.stem}"
            f"({counter})"
            f"{item.suffix}"
        )

        destination_path = (
            destination_folder / new_name
        )

        counter += 1

    return destination_path


# -------------------------------------------------
# Preview Folder
# -------------------------------------------------

def preview_folder(path):

    folder = Path(path)

    if not folder.exists():
        raise FileNotFoundError(
            "Folder not found!"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            "Selected path is not a folder!"
        )

    file_types = load_file_types()

    preview = []

    for item in folder.iterdir():

        if not item.is_file():
            continue

        destination = get_destination(
            item,
            file_types
        )

        destination_folder = (
            folder / destination
        )

        destination_path = get_unique_destination(
            item,
            destination_folder
        )

        preview.append({
            "source": str(item),
            "name": item.name,
            "destination": destination,
            "target": str(destination_path)
        })

    return preview


# -------------------------------------------------
# Move One File
# -------------------------------------------------

def move_file(
    item,
    folder,
    file_types
):

    item = Path(item)
    folder = Path(folder)

    destination = get_destination(
        item,
        file_types
    )

    destination_folder = (
        folder / destination
    )

    destination_folder.mkdir(
        exist_ok=True,
        parents=True
    )

    destination_path = get_unique_destination(
        item,
        destination_folder
    )

    try:

        shutil.move(
            str(item),
            str(destination_path)
        )

        logging.info(
            f"Moved: {item.name} -> "
            f"{destination_path}"
        )

        return {
            "status": "moved",
            "source": str(item),
            "target": str(destination_path)
        }

    except Exception as e:

        logging.error(
            f"Error moving {item.name}: {e}"
        )

        return {
            "status": "error",
            "source": str(item),
            "target": "",
            "error": str(e)
        }


# -------------------------------------------------
# Organize Folder
# -------------------------------------------------

def organize_folder(
    path,
    progress_callback=None
):

    folder = Path(path)

    if not folder.exists():
        raise FileNotFoundError(
            "Folder not found!"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            "Selected path is not a folder!"
        )

    file_types = load_file_types()

    items = [
        item
        for item in folder.iterdir()
        if item.is_file()
    ]

    total = len(items)

    moved = 0
    errors = 0

    operations = []

    for index, item in enumerate(items, start=1):

        result = move_file(
            item,
            folder,
            file_types
        )

        if result["status"] == "moved":

            moved += 1

            operations.append({
                "source": result["source"],
                "target": result["target"]
            })

        else:

            errors += 1

        if progress_callback:

            progress_callback(
                index,
                total
            )

    # Save history only when something moved
    if operations:

        history = load_history()

        history.append({
            "folder": str(folder),
            "operations": operations
        })

        # Keep last 20 operations
        history = history[-20:]

        save_history(history)

    logging.info(
        f"Organization completed: "
        f"{moved} moved, {errors} errors"
    )

    return {
        "total": total,
        "moved": moved,
        "errors": errors,
        "operations": operations
    }


# -------------------------------------------------
# Undo Last Organization
# -------------------------------------------------

def undo_last():

    history = load_history()

    if not history:

        return {
            "success": False,
            "message": "Nothing to undo."
        }

    last_operation = history[-1]

    restored = 0
    errors = 0

    for operation in reversed(
        last_operation["operations"]
    ):

        source = Path(
            operation["source"]
        )

        target = Path(
            operation["target"]
        )

        try:

            if target.exists():

                source.parent.mkdir(
                    exist_ok=True,
                    parents=True
                )

                # If original filename now exists,
                # don't overwrite it.
                if source.exists():

                    source = get_unique_destination(
                        source,
                        source.parent
                    )

                shutil.move(
                    str(target),
                    str(source)
                )

                restored += 1

        except Exception as e:

            errors += 1

            logging.error(
                f"Undo error: {e}"
            )

    history.pop()

    save_history(history)

    logging.info(
        f"Undo completed: {restored} restored"
    )

    return {
        "success": True,
        "restored": restored,
        "errors": errors
    }


# -------------------------------------------------
# Check File Ready
# -------------------------------------------------

def wait_for_file(
    file_path,
    attempts=10
):

    file_path = Path(file_path)

    previous_size = -1

    for _ in range(attempts):

        if not file_path.exists():

            return False

        try:

            current_size = (
                file_path.stat().st_size
            )

            if current_size == previous_size:

                return True

            previous_size = current_size

        except OSError:

            pass

        time.sleep(1)

    return False


# -------------------------------------------------
# Auto Organize
# -------------------------------------------------

def auto_organize_loop(
    folder,
    stop_event,
    callback=None
):

    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    folder = Path(folder)

    file_types = load_file_types()

    class Handler(FileSystemEventHandler):

        def on_created(self, event):

            if event.is_directory:
                return

            file_path = Path(
                event.src_path
            )

            if not wait_for_file(file_path):
                return

            result = move_file(
                file_path,
                folder,
                file_types
            )

            if callback:

                callback(
                    file_path.name,
                    result["status"]
                )

    handler = Handler()

    observer = Observer()

    observer.schedule(
        handler,
        str(folder),
        recursive=False
    )

    observer.start()

    logging.info(
        f"Auto organize started: {folder}"
    )

    try:

        while not stop_event.is_set():

            time.sleep(0.5)

    finally:

        observer.stop()
        observer.join()

        logging.info(
            "Auto organize stopped"
        )