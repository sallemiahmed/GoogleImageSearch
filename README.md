
# Google Image Search Downloader

This is a Python GUI application that allows users to search and download images using the Google Custom Search API. The application allows users to input search parameters such as image type, color, size, and more. It also provides an option to save the API Key and Search Engine ID for future searches.

## Features

- Search and download images from Google Custom Search API.
- Refine your search by image color, dominant color, size, and type.
- Save API keys for future use.
- Responsive and user-friendly GUI with real-time logging during search.

## How to Use

### 1. Download the Precompiled Windows Executable:

You can download the precompiled Windows executable directly from the [Releases](https://github.com/your-username/GoogleImageSearch/releases) section. Once downloaded, simply run the `.exe` file, no need to install Python or other dependencies.

### 2. Running the Application

1. Enter your **API Key** and **Search Engine ID** (You can get these from the Google Cloud Console).
2. Input the **search keyword** (e.g., `Adel Imam`).
3. Specify the **number of results** you wish to retrieve.
4. Choose additional search filters such as:
   - **Image Color Type**: color, gray, mono, transparent.
   - **Dominant Color**: black, blue, brown, gray, green, orange, pink, purple, red, teal, white, yellow.
   - **Image Size**: icon, small, medium, large, xlarge, xxlarge, huge.
   - **Image Type**: clipart, face, lineart, stock, photo, animated.
5. Select the **output directory** where the images will be saved.
6. Click the **Start Search** button to begin downloading images.
7. Use the **Save API Config** button to save your API Key and Search Engine ID to a configuration file (`api.cfg`) for future use.

## Screenshots

Below are some screenshots of the GUI:

![GUI Example](link-to-screenshot.png)

## Compiling the Application on Windows

If you'd like to compile the application yourself, follow the instructions below:

### Prerequisites

Before compiling the application on Windows, ensure that you have the following installed:

1. **Python**: Download and install Python from [here](https://www.python.org/downloads/). Ensure that you add Python to your system’s PATH during installation.
   
2. **PyInstaller**: This is the tool used to compile Python scripts into standalone executables. You can install it by running the following command in your terminal:

   ```bash
   pip install pyinstaller
   ```

### Compilation Steps

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/GoogleImageSearch.git
   cd GoogleImageSearch
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Run `PyInstaller` to create the standalone executable:

   ```bash
   pyinstaller --onefile --windowed app.py
   ```

4. Once the compilation is complete, you can find the `app.exe` inside the `dist` folder. You can now distribute this `.exe` file or run it on any Windows machine without needing Python installed.

### Additional PyInstaller Options

If you want to customize the `.exe` file (e.g., adding an icon), you can use the following options with `PyInstaller`:

```bash
pyinstaller --onefile --windowed --icon=youricon.ico app.py
```

- **`--onefile`**: Packages everything into a single executable file.
- **`--windowed`**: Runs the application in windowed mode without showing the console.
- **`--icon`**: Adds an icon to the executable.

## Saving and Loading API Configurations

The application allows you to save your **API Key** and **Search Engine ID** in a configuration file (`api.cfg`). If this file is present, the application will load these values automatically the next time it is started.

### How to Save the API Config

1. Enter the API Key and Search Engine ID in the respective fields.
2. Click the **Save API Config** button. This will save the values to a file called `api.cfg` in the current directory.

### How to Load the API Config

When the application starts, it checks if the `api.cfg` file exists. If found, it loads the API Key and Search Engine ID into the respective fields automatically.

## Troubleshooting

### Common Issues

1. **Error: Unable to Identify Image File**
   - Some websites may block direct access to image files. These images will not be downloaded. In the logs, you will see messages indicating that some image files could not be downloaded or identified.

2. **Frozen GUI During Search**
   - If the GUI seems frozen while performing a search, don’t worry. The search is running in the background, and the results will be displayed in the log window as soon as the search completes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
