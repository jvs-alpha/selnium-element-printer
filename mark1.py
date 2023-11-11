from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# JavaScript code to capture the details of the clicked element
capture_element_details_script = """
function captureDetails(element) {
    if (!element) {
        console.log('Error: Clicked element is null or undefined.');
        return null;
    }

    // Get XPath
    function getPathTo(element) {
        if (!element || !element.parentNode)
            return '';

        var ix = 0;
        var siblings = element.parentNode.childNodes;

        for (var i = 0; i < siblings.length; i++) {
            var sibling = siblings[i];
            if (sibling === element)
                return getPathTo(element.parentNode) + '/' + element.tagName + '[' + (ix + 1) + ']';
            if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                ix++;
        }
        return '';
    }

    var details = {
        'xpath': getPathTo(element),
        'id': element.id,
        'name': element.name,
        'tag_name': element.tagName,
        'class_name': element.className,
        'link_text': element.innerText
    };

    return details;
}

document.addEventListener('click', function(e) {
    var clickedElement = e.target;
    var details = captureDetails(clickedElement);
    console.clear();  // Clear the console
    window.details = details;
    console.log('Details of the clicked element:', details);
});
"""

# Create a WebDriver instance (you need to have WebDriver installed)
driver = webdriver.Chrome()

# Open a webpage
url = "https://example.com"  # Replace with the URL of the webpage you want to use
driver.get(url)
waitdriver = WebDriverWait(driver, 10)

try:
    print("Please click on an element on the webpage.")

    # Execute the script to capture details of the clicked element
    driver.execute_script(capture_element_details_script)

    temp = dict()
    count = 1
    while True:
        # Keep the script running
        time.sleep(1)
        # logs = driver.get_log("browser")
        # if len(logs) != 0:
        #     print(logs)

        details = driver.execute_script("return window.details;")
        if details:
            if details == temp:
                continue
            with open("elements-clicked.md", "a") as f:
                f.write(f"{count}\n```json\n")
                f.write(f"{json.dumps(details, indent=2)}")
                f.write("\n```")
                f.write("\n")
                count += 1
                print(details)
            temp = details

finally:
    driver.quit()
