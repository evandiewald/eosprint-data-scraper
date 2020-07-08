# eosprint-data-scraper
A crude-but-effective automated data scraper for EOSPRINT 2.x build preparation files. Use with caution during beta stage.
Questions? Please open an issue and/or submit a pull request. 

> :no_entry: **This software has not yet been rigorously tested!** Always double-check results!

![Conversion Cover](/images/conversion-cover.png)

## Overview
EOS build preparation files can only be exported in a binary format (OPENJZ) that does not allow users to parse them for relevant exposure parameters and machine settings. Typically, this critical information must be entered by hand into a spreadsheet, making for a tedious process. `eosprint-data-scraper` is a simple framework for automating the data scraping process and exporting it as a CSV file. At its core, the software is an implementation of a specified set of procedures using two Python libraries: [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/index.html) and [Tesseract Optical Character Recognition (OCR)](https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/). Essentially, the script moves your mouse automatically around the EOSPRINT window, allowing it to take screenshots of relevant sections and to parse them for the relevant information. In the end, the data is exported into two CSV files, for exposure settings (which can vary in part-wise fashion, such as laser power, scan speed, and hatch spacing) and machine settings (build-level parameters like preheat temperature and differential pressure), respectively. 

![Data scraper in action](/images/eosprint-scraper-demo.gif)

## Usage
> :warning: As of this writing, EOSPRINT 2.x only supports Windows OS (7/10).

1. Clone the repository:

`$ git clone https://github.com/evandiewald/eosprint-data-scraper.git`

2. I highly recommend installing dependencies and running the code within a [virtual environment](https://docs.python.org/3/library/venv.html). Once activated, install `requirements.txt` via `pip`: 

`(venv) ~\eosprint-data-scraper > pip install -r requirements.txt`

3. Install Tesseract OCR: 
* [Windows 32bit/64bit](https://github.com/UB-Mannheim/tesseract/wiki)
* ~~[Linux/macOS](https://github.com/tesseract-ocr/tesseract/wiki#installation)~~

4. Initialize `eosprint-data-scraper.py`:
* Assuming you are using Windows, you will have to point `pytesseract` to the tesseract executable that you just installed, which by default is in your Program Files directory. You'll most likely have to change this line:
```python
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'
```
* You also need to specify which parameter sets to scrape. Usually, EOSPRINT gives a few "locked" parameter sets that you can't delete or view. In the example below, there are three of these (and they are zero-indexed), so `param_start = 3`. I have 6 relevant PV's, so `param_end = param_end + 6`. 

![Exposure parameter indexing](/images/parameter-setup-annotated.png)

In its current form, the code does not support scrolling through more parameters than can be displayed in the window, but this should be an easy change to make in a future commit.

5. Run the code.
The code was tested on a 1920x1080 display, but it *should* work on any **16:9** monitor (the higher the resolution, the more accurate it will be). When you run the code, there is a 5-second delay to give you time to open up EOSPRINT (make sure it is full-screen). Once EOSPRINT is up, **do NOT touch your mouse/keyboard**. You should start to see your cursor move around the screen. The whole process should take a couple minutes, but you will know it's complete when this popup message appears:

![Popup notification](/images/scraping-complete.PNG)

## Exported Data Format

The exporting format is a point of further development (please feel free to submit a pull request if you have more refined solutions!), but at this point we automatically make two separate CSV files: `process_settings.csv` & `exposure_parameters.csv`. **I cannot stress this enough: this is meant to be a time-saving piece of software, but the tesseract code does make some mistakes. Be sure to double-check the values in the spreadsheets.**

The format of `exposure_parameters.csv` is the following:

![exposure parameters](/images/exposure-settings-csv.PNG)

For each parameter set, there are rows corresponding to the different exposure patterns (in this case, "hatch", "infill", "upskin", "downskin", "contour" (x2), & "edge").
