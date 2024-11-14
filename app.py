import logging
import os
import threading
import time

import cv2
from fuzzywuzzy import fuzz
import keyboard
import pytesseract
import yt_dlp


# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"your_path_to_tesseract.exe"

# Event to control stopping the capture
stop_event = threading.Event()

def get_live_stream_url(youtube_url):
    """
    Retrieve the direct streaming URL for the specified YouTube live stream.

    Args:
        youtube_url (str): The URL of the YouTube live stream.

    Returns:
        str: The direct stream URL.
    """
    ydl_opts = {
        'format': 'bestvideo',
        'quiet': True,
        'force-ipv4': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        return info['url']

def contains_target_text(image, target_text):
    """
    Check if the target text is present in the given image using OCR and fuzzy matching.

    Args:
        image (np.array): The image to analyze.
        target_text (str): The text to search for.

    Returns:
        tuple: A tuple (bool, str) indicating if the target text was found and the detected text.
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    logging.debug(f"Detected text: {text}")  # Debugging output
    similarity_score = fuzz.partial_ratio(target_text.lower(), text.lower())
    return similarity_score >= MATCH_THRESHOLD, text

def capture_screenshots_with_ocr(stream_url, target_text):
    """
    Capture screenshots from the live stream at specified intervals, and save screenshots
    that contain the target text.

    Args:
        stream_url (str): The direct URL to the live stream.
        target_text (str): The text to search for in screenshots.
    """
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Cannot open video stream.")
        return

    # Create a directory for saving screenshots
    if not os.path.exists("SKD"):
        os.makedirs("SKD")

    shot_count = 0
    last_detected_text = ""
    last_capture_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Cannot read frame. Retrying in 1 second...")
            time.sleep(1)
            continue

        current_time = time.time()

        # Capture frame if interval has passed
        if (current_time - last_capture_time) >= CAPTURE_INTERVAL:
            print("Frame read successfully.")
            is_match, current_detected_text = contains_target_text(frame, target_text)
            print(current_detected_text)
            last_capture_time = current_time

            # Save screenshot if the target text is detected and differs from the last detected text
            if is_match and current_detected_text != last_detected_text:
                filename = os.path.join("SKD", f"screenshot_{shot_count + 1}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Captured and saved {filename} containing the target text.")
                shot_count += 1
                last_detected_text = current_detected_text
            else:
                logging.debug(f"Screenshot {shot_count + 1} does not contain the target text or is the same as last.")

        # Check for stop signal
        if stop_event.is_set():
            print("Stopping capture...")
            break

    cap.release()
    cv2.destroyAllWindows()

def listen_for_stop():
    """
    Listen for the 'ctrl+s' key combination to stop the screenshot capture.
    """
    keyboard.wait('ctrl+s')
    stop_event.set()

def start_capture(stream_url, target_text):
    """
    Start capturing screenshots in a separate thread.

    Args:
        stream_url (str): The direct URL to the live stream.
        target_text (str): The text to search for in screenshots.
    """
    capture_screenshots_with_ocr(stream_url, target_text)

if __name__ == "__main__":
    # Change data here
    YOUTUBE_URL = 'YOUR_YOUTUBE_LIVESTREAM_URL'  # YouTube live stream URL
    TARGET_TEXT = "YOUR_TARGET_NAME_TO_SEARCH"  # Target text to search for in screenshots
    CAPTURE_INTERVAL = 3  # Interval in seconds for capturing screenshots
    MATCH_THRESHOLD = 80  # Threshold for fuzzy text matching

    # Initialize loggings
    logging.basicConfig(level=logging.DEBUG)

    # Get the live stream URL
    stream_link = get_live_stream_url(YOUTUBE_URL)
    if stream_link:
        # Start the screenshot capture in a separate thread
        capture_thread = threading.Thread(target=start_capture, args=(stream_link, TARGET_TEXT))
        capture_thread.start()

        # Start listening for the stop signal
        listen_for_stop()
