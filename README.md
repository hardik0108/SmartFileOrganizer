Smart File Organizer

A modern Python desktop application that automatically organizes files into categories based on their file extensions.

Smart File Organizer started as a simple Python file-organizing script and was developed into a practical desktop application with a professional GUI, preview mode, undo support, customizable JSON-based settings, logging, and optional automatic folder monitoring.

✨ Features

📁 Select any folder and organize its files

👀 Preview file movements before organizing

⚡ One-click manual organization

🤖 Optional Auto Organize for newly created files

↩️ Undo the last organization operation

🔧 Customize file-extension rules from Settings

📊 Progress bar and file statistics

🛡️ Duplicate filename protection

📦 Unknown file types are placed in Others

📝 Application logging

💾 Organization history for Undo

🌙 Dark/light mode

🖥️ Windows executable available through GitHub Releases

🗂️ Supported Categories

The default configuration includes:

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

File-extension rules can be customized from the application's Settings screen.

🖥️ Screenshots

Screenshots will be added here to demonstrate the application's dashboard, preview screen, and settings.

Recommended structure:

screenshots/
├── dashboard.png
├── preview.png
└── settings.png

Then add screenshots like:

![Smart File Organizer Dashboard](screenshots/dashboard.png)

🚀 Download

Windows

Download the latest release from:

GitHub Releases:
https://github.com/hardik0108/SmartFileOrganizer/releases

The release package contains:

SmartFileOrganizer.exe
settings.json

Keep settings.json in the same folder as SmartFileOrganizer.exe.

Always test the application on a test folder before organizing important files.

💻 Run from Source

Clone the repository:

git clone https://github.com/hardik0108/SmartFileOrganizer.git
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

Windows recommended for the packaged executable

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
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── .gitignore              # Git ignored files
└── SmartFileOrganizer.spec # PyInstaller build configuration

Generated files such as build/, dist/, app.log, and history.json are excluded from the Git repository.

⚙️ How It Works

The application separates the graphical interface from the file-organizing engine.

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
└── photo.jpg

After organization:

Downloads/
└── Images/
    └── photo.jpg

The application waits for a newly created file to finish changing before moving it.

↩️ Undo

After a manual organization, the application stores the source and destination paths of moved files.

Selecting Undo Last attempts to restore the files to their original locations.

🛡️ Safety

Smart File Organizer is designed to reduce common file-management problems:

Existing destination filenames are not overwritten.

Duplicate names are automatically renamed:
photo.jpg, photo(1).jpg, photo(2).jpg

Unknown extensions are placed in Others.

Preview mode lets users review planned moves before confirming.

Auto Organize can be stopped by the user.

File operations respect the permissions available to the current user.

Important: Always test the application on a test folder before organizing important personal or system folders.

🏗️ Build the Windows EXE

Install PyInstaller:

python -m pip install pyinstaller

Build the application:

python -m PyInstaller --clean --onefile --windowed --name SmartFileOrganizer app.py

The executable will be created at:

dist/SmartFileOrganizer.exe

Because the application uses an external settings.json configuration file, include settings.json with the released executable.

🐛 Known Limitations

The current release primarily targets Windows desktop usage.

File operations depend on available permissions.

Very large folders may take longer to process.

Auto Organize monitors the selected folder and does not recursively monitor every subfolder.

Users should avoid organizing system-critical folders.

The current release requires settings.json alongside the executable.

🔮 Future Improvements

Possible future versions may include:

Scheduled organization

More advanced file rules

File-size and date-based organization

Multiple watched folders

Improved recovery and rollback

Windows installer package

Additional operating-system support

More detailed activity history

Automatic application updates

🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

Reporting a bug

Open an issue.

Explain what happened.

Include the steps needed to reproduce it.

Include relevant error messages or screenshots.

Contributing code

Fork the repository.

Create a feature branch.

Make your changes.

Test the application.

Open a pull request.

📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.

👨‍💻 Author

Hardik Gondaliya

Built with Python as a practical desktop file-management application.

GitHub: https://github.com/hardik0108

⭐ If you find Smart File Organizer useful, consider starring the repository.
