import time
from Crawler import login, get_html, crawl, get_page
from GUI import get_user_info
from Queue import Queue
from Report import report
import os
from axe_selenium_python import Axe

def main():
    username, password, elevance, suppress, continued = get_user_info()
    driver = login(username, password, elevance)

    # Output Directory
    # Check for existing output directories
    existing_output_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith(str(username) + "_output")]
    if existing_output_dirs:
        existing_output_dirs.sort(reverse=True)
        print(f"Found existing output directories: {existing_output_dirs}")
        output_dir = existing_output_dirs[0]
    else:
        output_dir = time.strftime("%Y_%m_%d__%H_%M_%S") + "_" + str(username) + "_output"

    # Load Queue and CompletedList
    queue = Queue(output_dir)

    if queue.isEmpty():
        print("Queue is empty. Starting from the homepage.")
        driver = get_page(driver)
        html = get_html(driver)
        accessibility_output = accessibility(driver, suppress) # Check accessibility of the page
        report(output_dir, driver, accessibility_output, driver.current_url, 0) # Generate report for the page
        links = crawl(html, elevance)
        for link in links:
            queue.enqueue(link)

    num = 0
    while not queue.isEmpty():
        if num > 5:
            driver.quit()
            driver = login(username, password, elevance)
            num = 0


        link, id_tracker = queue.dequeue()
        try:
            driver = get_page(driver, link=link)

            print("Crawling:", link)
            html = get_html(driver)

            if html is not None and "mobilehealthconsumer.com" in driver.current_url:
                print("Crawled:", driver.current_url)
                accessibility_output = accessibility(driver, suppress) # Check accessibility of the page
                report(output_dir, driver, accessibility_output, link, id_tracker) # Generate report for the page
                print("Accessibility report generated for:", driver.current_url)
                links = crawl(html, elevance)
                for link in links:
                    queue.enqueue(link)
                print("Queue Size:", queue.size())
                print("---------------" * 5)
                num += 1
        except Exception as e:
            print(f"An error occurred while crawling {link}:", e)
            print("---------------" * 5)
            continue


def accessibility(driver, suppress):
    axe = Axe(driver)
    axe.inject()  # Inject axe-core JavaScript into the page
    results = axe.run()

    """
    Suppress known issues
    "html-has-lang": {"enabled": False},
    "landmark-one-main": {"enabled": False},
    "region": {"enabled": False},
    "color-contrast": {"enabled": False},
    "page-has-heading-one": {"enabled": False}    
    """

    if suppress:
        # Suppress known issues
        new_violations = []
        for issue in results["violations"]:
            if issue["id"] in ["html-has-lang", "landmark-one-main", "region", "color-contrast", "page-has-heading-one"]:
               pass
            else:
                new_violations.append(issue)
        results["violations"] = new_violations

    return results

if "__main__" == __name__:
    main()

