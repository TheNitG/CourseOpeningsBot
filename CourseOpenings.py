# Import necessary packages
import os
# Web browser packages
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
'''HAVE A QUEUE FOR EACH THREAD SO MORE PEOPLE CAN CHECK COURSES EACH TIME'''


# Function to find the products and their respective prices from the search term taking in a CRN as an argument
def is_course_open(crn, driver):
    # Get the page
    driver.get(url)
    # Find the CRN element to edit
    course_number = driver.find_element_by_name('crn')
    # Edit the CRN element
    course_number.send_keys(str(crn))
    # Find the term dropdown to interact with
    select_term = Select(driver.find_element_by_name('TERMYEAR'))
    # Select the Spring 2021 (term of interest for add/drop right now) option
    select_term.select_by_visible_text('Spring 2022')
    # Find the course availability dropdown to interact with
    select_open = Select(driver.find_element_by_name('open_only'))
    # Select the only open sections option
    select_open.select_by_visible_text('ONLY OPEN Sections')
    # Emulate the enter keypress to submit the form
    course_number.send_keys(Keys.ENTER)
    # Determine if the course is open and return True if so, else return False
    return 'NO SECTIONS FOUND FOR THIS INQUIRY' not in driver.page_source


# Check if the course is valid
def is_valid_course(driver):
    # Find the CRN element to edit
    course_number = driver.find_element_by_name('crn')
    select_open = Select(driver.find_element_by_name('open_only'))
    # Select the only open sections option
    select_open.select_by_visible_text('ALL Sections (FULL and OPEN)')
    # Emulate the enter keypress to submit the form
    course_number.send_keys(Keys.ENTER)
    # Determine if the course exists and return True if so, else return False
    return 'NO SECTIONS FOUND FOR THIS INQUIRY' not in driver.page_source


# Method to keep checking if a class is open
async def show_course_status(message, crn):
    # Make the web-driver
    driver = make_driver()
    # # Add the web-driver to the list of web-drivers
    # drivers.append(driver)
    # Get the boolean value for if the course is open or not
    status_value = is_course_open(crn, driver)
    # Check if the course actually exists
    if status_value or is_valid_course(driver):
        result = ''
        # Display OPEN if open
        if status_value:
            result = f'CRN: {crn} is OPEN <@{message.author.id}>'
            await message.channel.send(result)
        else:
            result = f'CRN: {crn} is CLOSED'
            await message.channel.send(result)
        # # Attempts variable used to keep track of how many times tried (to show it is still running and retrying)
        # attempt = 1
        # # While the course is closed, keep retrying
        # while not status_value:
        #     # Updates the user with the current status with the number of attempts and OPEN or CLOSED
        #     for x in range(interval):
        #         await message.channel.send(f'{crn}: is CLOSED (Attempt {attempt}), Retrying in {interval - x}s')
        #         # To make it wait interval amount of seconds
        #         sleep(1)
        #     # Increment the number of attempts
        #     attempt += 1
        #     # Checks if the course is open now
        #     status_value = is_course_open(crn, driver)
        # await message.channel.send(f'CRN: {crn} is OPEN')
        # Close and quit the web-driver
        driver.close()
        driver.quit()
        return result
    # Close and quit the web-driver
    driver.close()
    driver.quit()
    result = f'{crn} is not a valid CRN'
    # If the program reaches this point, the CRN isn't valid
    await message.channel.send(result)
    return result


# Make the driver by attempting to use different chrome.exe paths and throw a WebDriverException if unsuccessful
def make_driver():
    # Define the browser type and configure options to work
    options = webdriver.ChromeOptions()
    # Make it so browser runs in background
    options.add_argument('headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    # Path to the chromedriver included in this repository
    chrome_driver_binary = "./chromedriver"
    # Create the driver object which will be None until the try-except is executed
    try:
        # Path to the chrome executable (change if needed to your chrome.exe path)
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        # Attempt to create the driver with the necessary configurations
        driver_attempt = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
        # Return if successful
        return driver_attempt
    except:
        try:
            # Path to the chrome executable (change if needed to your chrome.exe path)
            options.binary_location = r"\Program Files\Google\Chrome\Application\chrome.exe"
            # Attempt to create the driver with the necessary configurations
            driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
            # Return if successful
            return driver_attempt
        except WebDriverException:
            try:
                # Try another common path
                options.binary_location = r"\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                # Attempt to create the driver with the necessary configurations
                driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
                # Return if successful
                return driver_attempt
            except WebDriverException:
                try:
                    # Try another common path
                    options.binary_location = r"\Users\%UserName%\AppData\Local\Google\Chrome\Application\chrome.exe"
                    # Attempt to create the driver with the necessary configurations
                    driver_attempt = webdriver.Chrome(chrome_driver_binary, options=options)
                    # Return if successful
                    return driver_attempt
                except WebDriverException:
                    # Throw a WebDriverException
                    raise WebDriverException('Please go into CourseOpenings.py and enter the path of your chrome.exe file')


# # Run the show_course_status method as a thread
# async def thread_course_status(message, crn):
#     # Create the thread
#     current_thread = Thread(target=show_course_status, args=(message, crn,))
#     # Make thread close when program closes
#     current_thread.daemon = True
#     # Start the thread
#     current_thread.start()


# # Method that properly closes the webdriver, window, and the program
# def close_all():
#     # Close and quit all web-drivers
#     for driver in drivers:
#         try:
#             driver.close()
#         except:
#             pass
#         driver.quit()


# # Create a list to store all web-drivers
# drivers = []
# Declare the URL of the Timetable
url = 'https://apps.es.vt.edu/ssb/HZSKVTSC.P_DispRequest'
