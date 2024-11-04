from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from pytubefix import YouTube
from pytubefix.cli import on_progress
import requests
import os
import zipfile
import threading
import time
from datetime import datetime, timedelta
import sys
import tempfile
import webbrowser

# Modify paths for PyInstaller packaging
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    # Use a writable temporary directory for downloads
    output_dir = os.path.join(tempfile.gettempdir(), "downloads")
else:
    template_folder = 'templates'
    output_dir = './downloads'

app = Flask(__name__, template_folder=template_folder)
app.secret_key = os.urandom(24)  # Secret key for session

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

# Session initialization
def init_session():
    if 'url_list' not in session:
        session['url_list'] = []
    if 'url_titles' not in session:
        session['url_titles'] = []

# Download status variables
download_status = {
    "completed": False
}

# Schedule cleanup
def schedule_cleanup():
    while True:
        now = datetime.now()
        for root, _, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Delete files older than 1 minute
                if os.path.isfile(file_path) and now - datetime.fromtimestamp(os.path.getctime(file_path)) > timedelta(minutes=1):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
        time.sleep(30)  # Run cleanup every 30 seconds

# Start the cleanup scheduler in a separate thread
threading.Thread(target=schedule_cleanup, daemon=True).start()

@app.route("/", methods=["GET", "POST"])
def index():
    init_session()
    if request.method == "POST":
        new_url = request.form.get("url")
        if new_url:
            try:
                yt = YouTube(new_url)
                title = yt.title
                session['url_list'].append(new_url)
                session['url_titles'].append(title[:50])  # Save first 50 chars of title
                session.modified = True
            except Exception as e:
                print(f"Error retrieving title: {e}")
        return redirect(url_for("index"))
    return render_template("index.html", urls=session.get('url_titles', []))

@app.route("/delete/<int:url_index>", methods=["POST"])
def delete_url(url_index):
    init_session()
    if 0 <= url_index < len(session['url_list']):
        session['url_list'].pop(url_index)
        session['url_titles'].pop(url_index)
        session.modified = True
    return redirect(url_for("index"))

@app.route("/delete_all", methods=["POST"])
def delete_all():
    init_session()
    # Clear the current URL list and titles
    session['url_list'] = []
    session['url_titles'] = []
    session.modified = True
    return redirect(url_for("index"))

@app.route("/download_all", methods=["POST"])
def download_all():
    init_session()
    url_list = session.get('url_list', [])
    downloaded_files = []  # To store paths of files downloaded in this session

    def download_videos():
        download_status["completed"] = False
        for url in url_list:
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    yt = YouTube(url)
                    ys = yt.streams.get_audio_only()
                    file_path = ys.download(output_path=output_dir, filename=f"{yt.title}.mp3")
                    downloaded_files.append(file_path)  # Add this file to our session list
                else:
                    print(f"Failed to access {url}: Status code {response.status_code}")
            except Exception as e:
                print(f"Failed to download {url}: {e}")
        
        # Create a zip file only with downloaded files from this session
        zip_path = os.path.join(output_dir, "all_downloads.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file_path in downloaded_files:
                if os.path.isfile(file_path) and file_path.endswith(".mp3"):
                    zipf.write(file_path, arcname=os.path.basename(file_path))
        
        download_status["completed"] = True  # Mark download as completed

    threading.Thread(target=download_videos).start()
    return jsonify({"status": "Download started"})  # Keep page open

@app.route("/progress", methods=["GET"])
def progress():
    return jsonify(download_status)

@app.route("/download_zip", methods=["GET"])
def download_zip():
    zip_path = os.path.join(output_dir, "all_downloads.zip")
    return send_file(zip_path, as_attachment=True, download_name="all_downloads.zip")

if __name__ == "__main__":
    # Start Flask server and open the default web browser to localhost:5000
    threading.Timer(1.25, lambda: webbrowser.open("http://localhost:5000")).start()
    app.run(debug=True)
    app.run(debug=True)
