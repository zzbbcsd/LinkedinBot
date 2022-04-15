import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
chrome_path ='your own chrome path'
driver = webdriver.Chrome(executable_path=chrome_path)
driver.get('https://www.linkedin.com/jobs/search/?f_AL=true&f_E=2%2C3') 

sign_in = driver.find_element_by_link_text("Sign in")
sign_in.click()

email = driver.find_element_by_name('session_key')
email.send_keys('username')
password = driver.find_element_by_name('session_password')
password.send_keys('userpassword')
password.send_keys(Keys.ENTER) #enter key

# find all jobs in the visible pages

all_jobs_on_this_page = driver.find_elements_by_class_name(
        "job-card-container__metadata-wrapper")

keep_going = True
pages = 0
while keep_going:
    if pages >= 10:
        keep_going = False
    page = driver.find_element_by_class_name(
        "artdeco-pagination__indicator--number")
    pages += 1
    for job in all_jobs_on_this_page:
        job.click()

        # skip the complicated ones
        try:
            apply_button = driver.find_element_by_css_selector(".jobs-s-apply button")
            apply_button.click()



            submit_button = driver.find_element_by_css_selector("footer button")

            # If the submit_button is a "Next" button, then this is a multi-step application, so skip.
            if submit_button.get_attribute("data-control-name") == "continue_unify":
                close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
                close_button.click()

                discard_button = driver.find_elements_by_class_name("artdeco-modal__confirm-dialog-btn")[1]
                discard_button.click()
                print("Complex application, skipped.")
                continue
            else:
                submit_button.click()

            # Once application completed, close the pop-up window.

            close_button = driver.find_element_by_class_name("artdeco-modal__dismiss")
            close_button.click()

            # If already applied to job or job is no longer accepting applications, then skip.
        except NoSuchElementException:
            print("No application button, skipped.")
            continue
    page.click()

print(pages)
driver.quit()




