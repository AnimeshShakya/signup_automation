## 📁 Project Contents
- `automation_script.py` – Main automation script
- `README.md` – Setup and usage instructions
- `test_report.pdf` – Sample test run report
- `demo_video.mp4` – demo video of script execution


# Environment/setup
#
#
#
# Selenium Automation Setup Guide

This README will guide you through setting up and running the Selenium automation script for registering on the authorized partner website.

## Prerequisites

Before running the script, ensure you have the following installed on your system:

### System Requirements
- **Python**: Version 3.7 or higher
- **Brave Browser**: Must be installed on your system
- **ChromeDriver**: Compatible with your Chrome/Brave version

##  Installation Steps

### 1. Install Python Dependencies

First, create a virtual environment (recommended):

```bash
python3 -m venv selenium_env
source selenium_env/bin/activate

# On Windows:
selenium_env\Scripts\activate
```

Install required Python packages:

```bash
pip install selenium requests
```

### 2. Install Brave Browser

#### Ubuntu/Debian:
```bash
sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-releases.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg arch=amd64] https://brave-browser-apt-releases.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
sudo apt update
sudo apt install brave-browser
```

#### Windows:
Download and install from the [official Brave website](https://brave.com/download/)

### 3. Install ChromeDriver

#### Option A: Using webdriver-manager (Recommended)
```bash
pip install webdriver-manager
```

Then modify the script to use automatic driver management (see Configuration section).

#### Option B: Manual Installation

1. Check your Brave/Chrome version:
   ```bash
   brave-browser --version
   # or
   google-chrome --version
   ```

2. Download the corresponding ChromeDriver from [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)

3. Extract and place ChromeDriver:
   ```bash
   # Linux/macOS
   sudo mv chromedriver /usr/local/bin/
   sudo chmod +x /usr/local/bin/chromedriver
   
   # Windows: Place chromedriver.exe in your PATH or project directory
   ```

## ⚙️ Configuration

### 1. Update File Paths

Edit the script to match your system paths:

```python
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver" 
BRAVE_PATH = "/usr/bin/brave-browser"         

# For Windows, paths might be:
# CHROMEDRIVER_PATH = "C:\\path\\to\\chromedriver.exe"
# BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
```

### 2. Alternative: Use webdriver-manager

For automatic driver management, replace the `create_brave_driver()` function:

```python
from webdriver_manager.chrome import ChromeDriverManager
```

### 3. Prepare Required Documents

Create a folder with the following documents (update paths in the script):

```
Documents/
├── sample1.pdf
├── sample2.pdf
```

Update the file paths in the script:
```python
# Update these paths to your actual document locations
file_inputs[0].send_keys("/path/to/your/sample1.pdf")
file_inputs[1].send_keys("/path/to/your/sample2.pdf")
```

### 4. Customize Registration Data

Modify the `data` dictionary in the script with your information:

##  How to run the script
#
#
#
#
### Basic Execution

1. Navigate to the script directory:
   ```bash
   cd /path/to/your/script
   ```

2. Activate virtual environment (if using):
   ```bash
   source selenium_env/bin/activate  # Linux/macOS
   # or
   selenium_env\Scripts\activate     # Windows
   ```

3. Run the script:
   ```bash
   python automation_script.py
   ```

# Any test data or accounts used
#
#
#
# credentials.json file contains test data

## 🔧 Common Issues and Solutions

### Issue 1: ChromeDriver Version Mismatch
**Error**: `SessionNotCreatedException: This version of ChromeDriver only supports Chrome version X`

**Solution**: 
- Update ChromeDriver to match your Brave/Chrome version
- Or use webdriver-manager for automatic version management

### Issue 2: Brave Browser Not Found
**Error**: `WebDriverException: unknown error: cannot find Chrome binary`

**Solution**: 
- Verify Brave installation path
- Update `BRAVE_PATH` in the script
- Common paths:
  - Linux: `/usr/bin/brave-browser`
  - macOS: `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`
  - Windows: `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`

### Issue 3: Permission Denied (Linux/macOS)
**Error**: `Permission denied: '/usr/local/bin/chromedriver'`

**Solution**:
```bash
sudo chmod +x /usr/local/bin/chromedriver
```

### Issue 4: Element Not Found
**Error**: `NoSuchElementException` or `TimeoutException`

**Solution**: 
- The website structure may have changed
- Check the element selectors in the script
- Increase wait times if needed
- Run in visible mode to debug

### Issue 5: File Upload Issues
**Error**: Files not uploading correctly

**Solution**:
- Ensure file paths are absolute, not relative
- Check file permissions
- Verify files exist at specified locations

## Script Features

- **Automatic Email Generation**: Uses Mail.tm API for temporary emails
- **Smart Element Detection**: Multiple fallback selectors for robust automation
- **Error Handling**: Comprehensive error handling and logging
- **Screenshot Capture**: Saves screenshots on errors for debugging
- **Retry Logic**: Automatic retries for critical operations

## Important Notes

1. **Rate Limiting**: The script includes delays to avoid overwhelming the server
2. **Legal Compliance**: Ensure you have permission to automate the target website
3. **Maintenance**: Website changes may require script updates
4. **Security**: Never commit credentials or sensitive data to version control