# YouTube Live Stream Screenshot & OCR Tool

This project captures screenshots from a YouTube live stream, performs OCR on each screenshot, and saves images containing specific target text. This tool is particularly useful for live-streamed events where it’s hard to monitor specific participants without constant attention.

## Background

I developed this tool to help family, friends, and colleagues who participate in the SKD CPNS selection test. Results for this test are often live-streamed on YouTube, where viewers can watch the progress of each participant and see rankings against others. However, it's challenging to monitor streams during working hours, and it can be time-consuming to find specific participants in a large group.

This tool automates the process by taking periodic screenshots of the stream, scanning for the target text (like a participant’s name), and saving relevant screenshots to a folder. Users can check the results at their convenience, without needing to constantly monitor the stream.

## Features

- Captures screenshots from a YouTube live stream at regular intervals.
- Uses Tesseract OCR with fuzzy matching to identify specific target text in screenshots.
- Saves relevant screenshots containing the target text in a local folder.
- Allows users to stop the capture process with a simple keyboard shortcut (`Ctrl+S`).

## Requirements

- **Python 3.x**
- **Tesseract OCR** (Make sure to install Tesseract and update the binary path in the code)
- **OpenCV**: `cv2`
- **yt-dlp**: For extracting direct video stream links from YouTube
- **fuzzywuzzy**: For fuzzy string matching
- **keyboard**: For detecting keyboard shortcuts

Install the required packages:
```bash
pip install opencv-python yt-dlp fuzzywuzzy[speedup] keyboard pytesseract
```

## Setup

1. **Install Tesseract OCR**: Download and install Tesseract OCR. Update the path to the Tesseract executable in the code:
```python
pytesseract.pytesseract.tesseract_cmd = r"your_path_to_tesseract.exe"
```

2. **Run the Script**: Open a terminal and run the script:
```bash
python app.py
```

3. **Stopping the Script**: To stop the capture process, press Ctrl+S.

## Usage

1. **Specify the YouTube Live Stream URL**: Replace the `YOUTUBE_URL` variable in the code with the URL of the desired YouTube live stream.

2. **Specify the Target Text**: Set the `TARGET_TEXT` variable to the text you want to search for in the live stream (e.g., a participant’s name).

3. **Run the Script**: The program will capture screenshots every few seconds and check for the target text in each image. If the text is detected, the screenshot is saved to the SKD folder in the current directory.

## Code Overview

- **`get_live_stream_url`**: Extracts the direct stream URL from YouTube using yt-dlp.
- **`contains_target_text`**: Uses Tesseract OCR to read text in a screenshot, performing fuzzy matching to check if it contains the target text.
- **`capture_screenshots_with_ocr`**: Captures screenshots at set intervals, runs OCR on each screenshot, and saves the image if the target text is detected.
- **`listen_for_stop`**: Monitors for the `Ctrl+S` key press to stop the capture process.

## Example Use Case

The tool is useful for tracking specific participants during live-streamed tests, competitions, or other events without needing to constantly monitor the screen. Screenshots with relevant information are saved, allowing users to view them at a later time.

## License
This project is open-source and available under the MIT License.

## Notes
- Ensure Tesseract OCR is installed and properly configured.
- Adjust `CAPTURE_INTERVAL` as needed for desired screenshot frequency.
