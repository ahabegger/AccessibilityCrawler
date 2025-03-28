import csv
import os
import re


def report(directory, driver, accessibility_output, link, id_tracker):
    # Organize Data
    url = driver.current_url
    title = driver.title

    project_dir = create_project_directory(directory)
    screenshot_path = create_screenshot(driver, id_tracker, project_dir)

    # Accessibility Output
    timestamp = accessibility_output["timestamp"]
    passes = accessibility_output["passes"]
    number_passes = len(passes)
    violations = accessibility_output["violations"]
    number_violations = len(violations)
    incomplete = accessibility_output["incomplete"]
    number_incomplete = len(incomplete)

    # Score Calculation
    total = number_passes + number_violations + number_incomplete
    score = (number_passes / total) * 100 + 0.5 * (number_incomplete / total) * 100
    print(f"Accessibility Score: {score} | Passes: {number_passes} | Violations: {number_violations} | Incomplete: {number_incomplete}")

    # Write the accessibility output to a CSV file
    page_access_path = os.path.join(project_dir, 'accessibility_report_by_page.csv')
    if not os.path.exists(page_access_path):
        with open(page_access_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["ID", "URL", "Title", "Score", "Link", "Screenshot Path", "Timestamp", "Number of Passes", "Number of Violations", "Number of Incomplete", "Violations", "Incomplete"]
            writer.writerow(header)

    with open(page_access_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        cols = [id_tracker, url, title, score, link, screenshot_path, timestamp, number_passes, number_violations, number_incomplete, violations, incomplete]
        new_cols = [ascii_encode(col) for col in cols]
        writer.writerow(new_cols)

    # Write the violations to a CSV file
    issue_access_path = os.path.join(project_dir, 'accessibility_report_by_issue.csv')
    if not os.path.exists(issue_access_path):
        with open(issue_access_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ["ID", "URL", "Title", "Link", "Screenshot Path", "Timestamp", "Violation ID", "Impact", "Help", "Help URL", "JSON Data"]
            writer.writerow(header)

    with open(issue_access_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        for violation in violations:
            cols = [id_tracker, url, title, link, screenshot_path, timestamp, violation["id"], violation["impact"], violation["help"], violation["helpUrl"], violation["nodes"]]
            new_cols = [ascii_encode(col) for col in cols]
            writer.writerow(new_cols)


def create_screenshot(driver, id_tracker, project_dir):
    title = driver.title

    try:
        # Create a full path for the Screenshots directory
        screenshots_dir = os.path.join(project_dir, "Screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        # Save screenshot with sanitized filename
        safe_filename = sanitize_filename(f"{title}-{id_tracker}")
        screenshot_path = os.path.join(screenshots_dir, f"{safe_filename}.png")
        driver.save_screenshot(screenshot_path)

        print(f"Screenshot saved to: {screenshot_path}")
        screenshot_path = sanitize_filename(f"{title}-{id_tracker}.png")
    except Exception as e:
        print(f"An error occurred while saving the screenshot: {e}")
        screenshot_path = ''

    return screenshot_path

def create_project_directory(directory):
    try:
        # Create a full path for the Project directory
        project_dir = os.getcwd()
        project_dir = os.path.join(project_dir, directory)
        os.makedirs(project_dir, exist_ok=True)
    except Exception as e:
        print(f"An error occurred while saving the Project directory: {e}")
        project_dir = ''

    return project_dir


def clear_reports():
    if os.path.exists('accessibility_report_by_page.csv'):
        os.remove('accessibility_report_by_page.csv')
    if os.path.exists('accessibility_report_by_issue.csv'):
        os.remove('accessibility_report_by_issue.csv')
    if os.path.exists('Screenshots'):
        for file in os.listdir('Screenshots'):
            os.remove(f'Screenshots/{file}')

def sanitize_filename(filename):
    # Remove invalid filename characters and limit length
    return re.sub(r'[<>:"/\\|?*]', '_', filename)[:200]

def ascii_encode(data):
    if isinstance(data, str):
        # Remove or replace non-ASCII characters
        return ''.join(char for char in str(data) if ord(char) < 128)
    elif isinstance(data, (list, dict)):
        # Convert complex objects to string and encode
        return ascii_encode(str(data))
    return data

if __name__ == "__main__":
    clear_reports()