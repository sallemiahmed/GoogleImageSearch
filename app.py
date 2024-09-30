import os
import requests
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image
from io import BytesIO
import threading
import configparser

CONFIG_FILE = 'api.cfg'

# Function to search images on Google using the Custom Search API
def google_image_search(api_key, search_engine_id, query, num_results, start_index=1, color_type=None, dominant_color=None, size=None, img_type=None):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': search_engine_id,
        'key': api_key,
        'searchType': 'image',
        'num': num_results,
        'start': start_index
    }
    
    # Add optional filters
    if color_type:
        params['imgColorType'] = color_type
    if dominant_color:
        params['imgDominantColor'] = dominant_color
    if size:
        params['imgSize'] = size
    if img_type:
        params['imgType'] = img_type

    response = requests.get(url, params=params)
    return response.json().get('items', [])

# Function to download and save images
def download_image(url, output_dir, image_name, log_widget):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        file_path = os.path.join(output_dir, f"{image_name}.jpg")
        img.save(file_path)
        log_widget.insert(END, f"Downloaded: {file_path}\n")
        log_widget.yview(END)
    except Exception as e:
        log_widget.insert(END, f"Failed to download {url}: {e}\n")
        log_widget.yview(END)

# Function to handle the search process in a separate thread
def start_search(api_key, search_engine_id, query, num_images, color_type, dominant_color, size, img_type, log_widget, output_dir):
    def search():
        total_images_downloaded = 0
        start_index = 1
        downloaded_urls = set()

        log_widget.insert(END, "Starting image search...\n")
        log_widget.yview(END)

        while total_images_downloaded < num_images:
            batch_size = min(num_images - total_images_downloaded, 10)
            image_results = google_image_search(api_key, search_engine_id, query, batch_size, start_index, color_type, dominant_color, size, img_type)
            
            if not image_results:
                log_widget.insert(END, "No more images found.\n")
                log_widget.yview(END)
                break

            for i, item in enumerate(image_results, start=total_images_downloaded + 1):
                url = item.get('link')
                if url and url not in downloaded_urls:
                    download_image(url, output_dir, f"{query}_{i}", log_widget)
                    downloaded_urls.add(url)
                    total_images_downloaded += 1
                    if total_images_downloaded >= num_images:
                        break

            start_index += batch_size
    
    # Run the search process in a separate thread
    threading.Thread(target=search).start()

# Function to browse for an output directory
def browse_directory(entry):
    folder_selected = filedialog.askdirectory()
    entry.delete(0, END)
    entry.insert(0, folder_selected)

# Function to save API settings to the config file
def save_config(api_key, search_engine_id):
    config = configparser.ConfigParser()
    config['API'] = {
        'API_KEY': api_key,
        'SEARCH_ENGINE_ID': search_engine_id
    }
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Function to load API settings from the config file
def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        return config['API'].get('API_KEY'), config['API'].get('SEARCH_ENGINE_ID')
    return "", ""

# GUI setup
def create_gui():
    root = Tk()
    root.title("Google Image Search")
    root.geometry("500x600")

    # Load API Key and Search Engine ID from config if available
    saved_api_key, saved_search_engine_id = load_config()

    # API Key and Search Engine ID
    Label(root, text="API Key:").grid(row=0, column=0, sticky=W)
    api_key_entry = Entry(root, width=40)
    api_key_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
    api_key_entry.insert(0, saved_api_key)

    Label(root, text="Search Engine ID:").grid(row=1, column=0, sticky=W)
    search_engine_id_entry = Entry(root, width=40)
    search_engine_id_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
    search_engine_id_entry.insert(0, saved_search_engine_id)

    # Save Config Button (now placed at the top-right corner)
    Button(root, text="Save API Config", command=lambda: save_config(api_key_entry.get(), search_engine_id_entry.get())).grid(row=0, column=3, rowspan=2, padx=5, pady=5)

    # Query and Number of Results
    Label(root, text="Keyword:").grid(row=2, column=0, sticky=W)
    query_entry = Entry(root, width=40)
    query_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)

    Label(root, text="Number of Results:").grid(row=3, column=0, sticky=W)
    num_images_entry = Entry(root, width=10)
    num_images_entry.grid(row=3, column=1, padx=5, pady=5)

    # Image Options
    Label(root, text="Image Color Type:").grid(row=4, column=0, sticky=W)
    color_type_var = StringVar()
    color_type_options = ["", "color", "gray", "mono", "trans"]
    color_type_menu = ttk.Combobox(root, textvariable=color_type_var, values=color_type_options)
    color_type_menu.grid(row=4, column=1, padx=5, pady=5)

    Label(root, text="Dominant Color:").grid(row=5, column=0, sticky=W)
    dominant_color_var = StringVar()
    dominant_color_options = ["", "black", "blue", "brown", "gray", "green", "orange", "pink", "purple", "red", "teal", "white", "yellow"]
    dominant_color_menu = ttk.Combobox(root, textvariable=dominant_color_var, values=dominant_color_options)
    dominant_color_menu.grid(row=5, column=1, padx=5, pady=5)

    Label(root, text="Image Size:").grid(row=6, column=0, sticky=W)
    size_var = StringVar()
    size_options = ["", "huge", "icon", "large", "medium", "small", "xlarge", "xxlarge"]
    size_menu = ttk.Combobox(root, textvariable=size_var, values=size_options)
    size_menu.grid(row=6, column=1, padx=5, pady=5)

    Label(root, text="Image Type:").grid(row=7, column=0, sticky=W)
    type_var = StringVar()
    type_options = ["", "clipart", "face", "lineart", "stock", "photo", "animated"]
    type_menu = ttk.Combobox(root, textvariable=type_var, values=type_options)
    type_menu.grid(row=7, column=1, padx=5, pady=5)

    # Output Directory
    Label(root, text="Output Directory:").grid(row=8, column=0, sticky=W)
    output_dir_entry = Entry(root, width=40)
    output_dir_entry.grid(row=8, column=1, columnspan=2, padx=5, pady=5)
    Button(root, text="Browse", command=lambda: browse_directory(output_dir_entry)).grid(row=8, column=3, padx=5, pady=5)

    # Log Box
    log_text = Text(root, height=10, width=60)
    log_text.grid(row=9, column=0, columnspan=4, padx=5, pady=5)

    # Start Button
    def on_start():
        api_key = api_key_entry.get()
        search_engine_id = search_engine_id_entry.get()
        query = query_entry.get()
        num_images = int(num_images_entry.get())
        color_type = color_type_var.get()
        dominant_color = dominant_color_var.get()
        size = size_var.get()
        img_type = type_var.get()
        output_dir = output_dir_entry.get()

        if api_key and search_engine_id and query and num_images > 0:
            start_search(api_key, search_engine_id, query, num_images, color_type, dominant_color, size, img_type, log_text, output_dir)
        else:
            log_text.insert(END, "Please fill in all required fields.\n")
            log_text.yview(END)

    Button(root, text="Start Search", command=on_start).grid(row=10, column=0, columnspan=4, padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
