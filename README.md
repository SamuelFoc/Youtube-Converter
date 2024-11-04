# 🎶 YouTube MP3 Downloader Web App 🎶

This app provides a simple web interface to download YouTube videos as MP3 files! With a few clicks, you can add multiple YouTube URLs, manage your download list, and save all your favorite songs in one place.

## 🚀 Features

- 📝 Add YouTube URLs to create a playlist.
- ❌ Remove single videos or clear the entire playlist.
- ⏬ Download all videos as MP3 files in a single ZIP file.
- 🧹 Automatic cleanup of old files every 30 seconds to keep your downloads directory clean.
- 🌐 Automatically opens your default browser at `localhost:5000` when you run the app.

## 📦 Installation and Setup

### Prerequisites

- Python 3.12 installed with `pip` (ensure it’s added to your PATH).
- Install the required dependencies by running:
  ```bash
  pip install flask requests pytubefix
  ```

### How to Build the Standalone Executable

To create a standalone executable for this app, you can use **PyInstaller**. First, install PyInstaller:

```bash
pip install pyinstaller
```

Then, run the following command to bundle the app into a single executable file. This command includes all the necessary files and dependencies for the app to run as a standalone:

```bash
pyinstaller --onefile --add-data "templates/index.html;templates" --add-data "downloads;downloads" --hidden-import pyexpat --hidden-import pkg_resources.py2_warn --paths "C:\Python312\DLLs" --paths "C:\Python312\Lib\site-packages" app.py
```

### Explanation of PyInstaller Command

- `--onefile`: Packages the app into a single executable file.
- `--add-data "templates/index.html;templates"`: Includes the `index.html` template file.
- `--add-data "downloads;downloads"`: Creates a `downloads` directory for storing MP3 files.
- `--hidden-import pyexpat --hidden-import pkg_resources.py2_warn`: Ensures necessary dependencies are included.
- `--paths`: Specifies paths to Python DLLs and site packages.

After running this command, you'll find the executable (`app.exe`) in the `dist` folder.

## 📝 How to Use the App

1. **Run the App**: Double-click `app.exe` (or run `python app.py` if running directly in Python).
2. **Open the App**: Your default web browser will automatically open to `http://localhost:5000`.
3. **Add URLs**: Paste YouTube video URLs in the input field and click **Pridať Video** to add them to your download list.
4. **Manage URLs**:
   - **Delete** individual videos using the delete button next to each entry.
   - **Clear All** to remove all entries from the list.
5. **Download All**:
   - Click **Stiahnuť Všetky Piesne** to download all videos as MP3 files.
   - Wait for the download to finish, and you'll be prompted to download a ZIP file containing all MP3s.
6. **Automatic Cleanup**: The app automatically deletes downloaded files older than 1 minute to save space.

## ⚙️ Troubleshooting

If you encounter any issues:

- Ensure all required libraries are installed (`flask`, `requests`, `pytubefix`).
- Run the app as `python app.py` in development mode for debugging.

## 📄 License

This project is licensed under the MIT License. Enjoy your music! 🎵
