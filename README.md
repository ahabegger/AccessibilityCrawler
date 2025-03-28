# Accessibility Crawler

An automated tool for crawling websites and generating accessibility reports using axe-core and Selenium.

## Features

- Automated accessibility testing using axe-core
- Web crawling capabilities to navigate through sites
- Suppression of common/known accessibility issues
- Support for sites requiring authentication
- Special handling for Elevance client sites
- Resumable testing sessions
- Report generation for accessibility violations

## Requirements

- Python 3.6+
- Chrome or Firefox browser

## Installation

1. Download GitBash or Git for Windows from [git-scm.com](https://git-scm.com/downloads) if you don't have it installed.
   - For Linux/Mac users, ensure you have `git` installed via your package manager.
2. Clone this repository to your local machine [github.docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository):
   ```
    git clone https://github.com/ahabegger/AccessibilityCrawler.git
   ```
3. Navigate to the cloned directory:
   ```
   cd AccessibilityCrawler
   ```
4. Create a virtual environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```
5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the accessibility checker while in the cloned directory:

```
python AccessibilityChecker.py
```

This will:
1. Open a GUI to enter credentials
2. Log in to the target website
3. Crawl through available pages
4. Generate accessibility reports in an output directory

## Configuration Options

- **Continue Session**: Resume from a previous crawl session
- **Elevance Client**: Enable special handling for Elevance sites
- **Suppress Known Issues**: Filter out common accessibility issues

## Output

Reports are saved in timestamped directories with the format:
`YYYY_MM_DD__HH_MM_SS_username_output/`


## Dependencies

- `selenium`: For web automation
- `axe-selenium-python`: For accessibility testing
- `tkinter`: For GUI elements
- `requests`: For HTTP requests
- `beautifulsoup4`: For HTML parsing
- `webdriver-manager`: For managing WebDriver binaries

## Security

This project is secure for public distribution for several reasons:

- **No hardcoded credentials**: The application uses a GUI for credential input rather than storing any passwords or API keys in the codebase.
- **Limited to authorized access**: The crawler only accesses content that an authenticated user would normally be able to view.
- **MHC data protection**: All Mobile Health Consumer data remains protected behind authentication. The tool simply automates actions a manual tester would perform.
- **Local report storage**: All reports and screenshots are stored locally on the user's device, not uploaded to any external servers.
- **Trusted dependencies**: All dependencies are widely-used, trusted open-source libraries with regular security updates.
- **No sensitive data extraction**: The tool focuses solely on accessibility testing and doesn't extract or store user/patient information.
- **Sanitized outputs**: Report generation includes data sanitization to prevent security issues in output files.

Using this tool requires valid credentials for any protected system, ensuring that only authorized users can perform accessibility testing on secured environments.

