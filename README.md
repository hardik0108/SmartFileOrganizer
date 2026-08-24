Smart File Organizer

A modern desktop application built with Python that automatically organizes files into categories based on their file extensions.

Smart File Organizer started as a simple Python file-organizing script and was developed into a complete desktop application with a professional GUI, preview mode, undo support, JSON-based settings, logging, and optional automatic folder monitoring.

✨ Features

📁 Select any folder and organize its files

👀 Preview where files will be moved before organizing

⚡ One-click manual organization

🤖 Optional Auto Organize mode for newly created files

↩️ Undo the last organization operation

🔧 Customize file-extension rules through the Settings UI

📊 Progress bar and file statistics

🛡️ Duplicate filename protection

📦 Unknown file types are placed in Others

📝 Application logging with app.log

💾 Organization history for Undo

🌙 Dark/light mode

🖥️ Standalone Windows .exe available through releases

🗂️ Supported Categories

The default configuration includes categories such as:

Documents

Images

Music

Videos

Archives

Development

Installers

Design

Fonts

Others

File-extension rules can be customized from the application's Settings.

🖥️ Screenshots

Add your application screenshots here.

Example:

screenshots/
├── dashboard.png
├── preview.png
└── settings.png

Then add them to this section:

![Smart File Organizer](screenshots/dashboard.png)

🚀 Download and Run

Option 1 — Windows EXE

Download the latest SmartFileOrganizer.exe from the project's GitHub Releases.

Place settings.json in the same directory as the executable if your release package includes it separately.

Option 2 — Run from Source

Clone the repository:

git clone https://github.com/hardik0108/file-organizer
cd SmartFileOrganizer

Create a virtual environment:

python -m venv .venv

Activate it on Windows PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

📦 Requirements

Python 3.10+

Windows recommended for the packaged .exe

Python dependencies:

CustomTkinter

Watchdog

PyInstaller (only required for building the executable)

Install them with:

pip install -r requirements.txt

🏗️ Project Structure

SmartFileOrganizer/
│
├── app.py                  # Graphical user interface
├── organizer.py            # File organization engine
├── settings.json           # File-extension configuration
├── requirements.txt        # Python dependencies
├── history.json            # Organization history
├── app.log                 # Application log
├── SmartFileOrganizer.spec # PyInstaller build configuration
│
├── build/                  # PyInstaller build files
└── dist/                   # Generated executable
    └── SmartFileOrganizer.exe

⚙️ How It Works

The application separates the user interface from the file-organizing logic.

User
  ↓
CustomTkinter GUI
  ↓
Preview / Organize / Auto Organize
  ↓
organizer.py
  ↓
Read rules from settings.json
  ↓
Detect file extension
  ↓
Choose destination category
  ↓
Handle duplicate filename
  ↓
Move file
  ↓
Save log/history

🔧 Custom File Rules

File rules are stored in settings.json.

Example:

{
    "file_types": {
        ".pdf": "Documents",
        ".jpg": "Images",
        ".mp3": "Music",
        ".py": "Development/Python Files"
    }
}

You can also modify these rules through the application's Settings screen.

🤖 Auto Organize

Auto Organize is optional.

When enabled, the application watches the selected folder for new files.

For example:

Downloads/
    photo.jpg

After detection:

Downloads/
    Images/
        photo.jpg

The application waits for a newly created file to finish changing before moving it.

↩️ Undo

After a manual organization, the application stores the source and destination paths of moved files.

Selecting Undo Last attempts to restore the files to their original locations.

🛡️ Safety

Smart File Organizer is designed to avoid common file-management problems:

Existing destination filenames are not overwritten.

Duplicate names are automatically renamed, for example:
photo.jpg, photo(1).jpg, photo(2).jpg

Unknown extensions are placed in Others.

Preview mode lets users review planned moves before confirming.

Auto Organize can be stopped by the user.

Always test the application on a test folder before organizing important personal folders.

🏗️ Build the Windows EXE

Install PyInstaller:

python -m pip install pyinstaller

Build:

python -m PyInstaller --clean --onefile --windowed --name SmartFileOrganizer app.py

The executable will be created in:

dist/SmartFileOrganizer.exe

For the current JSON-based configuration, include settings.json with the released application.

🐛 Known Limitations

The current release targets desktop usage, especially Windows.

File operations depend on the permissions available to the user.

Very large folders may take longer to process.

Auto Organize watches the selected folder and does not recursively monitor every subfolder.

Users should avoid organizing system-critical folders.

🔮 Future Improvements

Possible future versions may include:

Scheduled organization

More advanced file rules

File-size/date-based organization

Multiple watched folders

Better recovery and rollback

Installer package

Additional operating-system support

More detailed activity history

🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

If you find a bug:

Open an issue.

Explain what happened.

Include the steps needed to reproduce it.

Include relevant error messages or screenshots.

If you want to contribute code:

Fork the repository.

Create a feature branch.

Make your changes.

Test the application.

Open a pull request.

📄 License

Choose and add a license before publishing the project publicly.

For example, if you decide to use the MIT License, add a LICENSE file containing the MIT License terms.

👨‍💻 Author

Hardik Gondaliya

Built as a Python project to turn a file-organizing script into a practical desktop application.

⭐ If you find Smart File Organizer useful, consider starring the repository.