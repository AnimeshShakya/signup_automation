import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import random
import string
import re

def random_email():
    return "user" + ''.join(random.choices(string.digits, k=6)) + "@example.com"

def random_phone():
    return "98" + ''.join(random.choices(string.digits, k=8))

# ----------- CONFIG -----------
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
BRAVE_PATH = "/usr/bin/brave-browser"
REGISTER_URL = "https://authorized-partner.netlify.app/register"

# ----------- TEST DATA -----------
data = {
    "set_up_your_account": {
        "first_name": "Animesh",
        "last_name": "Shakya",
        "email": random_email(),
        "phone": random_phone(),
        "password": "Animesh@123",
        "confirm_password": "Animesh@123"
    },
    "agency_details": {
        "agency_name": "Animesh Travels",
        "role_in_agency": "Owner",
        "email": "shakyaanimesh858@gmail.com",
        "website": "www.animeshtravels.com",
        "address": "Kathmandu",
        "region_of_operation": "Nepal"
    },
    "professional_experience": {
        "years_of_experience": "5",
        "number_of_students_recruited_annually": "50",
        "focus_areas": "Undergraduate admission to Canada",
        "success_metrics": "90",
        "services_provided": "Career Counseling"
    },
    "verification_and_preferences": {
        "business_registration_number": "NP-CRO-45995",
        "preferred_countries": "Australia",
        "preferred_institution_types": "Universities",
        "certification_details": "ICEF Certified educational agent"
    }
}

# ----------- CREATE DRIVER -----------
def create_brave_driver():
    service = Service(CHROMEDRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.binary_location = BRAVE_PATH
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=service, options=options)

def select_nepal_from_dropdown(driver, wait):
    """Handle the Nepal selection from dropdown with improved logic"""
    print("🔄 Selecting region of operation...")
    
    time.sleep(3)
    
    dropdown_found = False
    
    dropdown_selectors = [
        "//button[contains(.,'Select Your Region of Operation')]",
        "//button[contains(@class, 'select')]",
        "//div[contains(text(),'Select Your Region of Operation')]/ancestor::button",
        "//button[@role='combobox']",
        "//button[contains(@class,'justify-between')]",
        "//button[contains(@id, 'region') or contains(@name, 'region')]"
    ]
    
    for selector in dropdown_selectors:
        try:
            dropdown_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            if dropdown_btn.is_displayed() and dropdown_btn.is_enabled():
                print(f"✅ Found dropdown with selector: {selector}")
                driver.execute_script("arguments[0].click();", dropdown_btn)
                dropdown_found = True
                break
        except:
            continue
    
    if not dropdown_found:
        print("❌ Could not find dropdown button")
        driver.save_screenshot("dropdown_not_found.png")
        return False
    
    time.sleep(2)
    
    nepal_selected = False
    
    try:
        nepal_options = driver.find_elements(By.XPATH, "//span[contains(text(),'Nepal')] | //div[contains(text(),'Nepal')] | //li[contains(text(),'Nepal')]")
        print(f"Found {len(nepal_options)} Nepal options")
        
        for option in nepal_options:
            if option.is_displayed():
                print("✅ Clicking on visible Nepal option")
                driver.execute_script("arguments[0].click();", option)
                nepal_selected = True
                break
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    if not nepal_selected:
        try:
            print("Trying keyboard navigation...")
            from selenium.webdriver.common.keys import Keys
            
            dropdown_btn.send_keys("Nepal")
            time.sleep(1)
            dropdown_btn.send_keys(Keys.ENTER)
            nepal_selected = True
            print("✅ Nepal selected via keyboard")
        except Exception as e:
            print(f"Keyboard method failed: {e}")
    
    if not nepal_selected:
        try:
            search_inputs = driver.find_elements(By.XPATH, "//input[@placeholder='Search...'] | //input[contains(@placeholder, 'search')]")
            if search_inputs:
                search_input = search_inputs[0]
                search_input.clear()
                search_input.send_keys("Nepal")
                time.sleep(2)
                
                nepal_options = driver.find_elements(By.XPATH, "//span[contains(text(),'Nepal')] | //div[contains(text(),'Nepal')]")
                for option in nepal_options:
                    if option.is_displayed():
                        driver.execute_script("arguments[0].click();", option)
                        nepal_selected = True
                        print("✅ Nepal selected via search")
                        break
        except Exception as e:
            print(f"Search method failed: {e}")
    
    if nepal_selected:
        time.sleep(2)
        
        try:
            time.sleep(1)
            
            updated_dropdown = driver.find_element(By.XPATH, "//button[contains(.,'Nepal')]")
            print("✅ Nepal selection verified!")
            return True
        except:
            try:
                next_button = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]")
                if next_button.is_enabled():
                    print("✅ Next button is enabled - selection likely successful")
                    return True
            except:
                print("⚠️ Could not verify selection, but proceeding anyway")
                return True
    else:
        print("❌ Failed to select Nepal")
        driver.save_screenshot("nepal_selection_failed.png")
        return False

# ----------- MAIN AUTOMATION -----------
def main():
    email, password = create_mailtm_account()
    token = get_mailtm_token(email, password)

    data["set_up_your_account"]["email"] = email

    driver = create_brave_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get(REGISTER_URL)
        wait.until(EC.presence_of_element_located((By.ID, "remember")))
        checkbox = driver.find_element(By.ID, "remember")
        checkbox.click()        
        driver.find_element(By.XPATH, "//button[contains(text(),'Continue')]").click()

        # -------- STEP 1: Set up account --------
        wait.until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys(data["set_up_your_account"]["first_name"])
        driver.find_element(By.NAME, "lastName").send_keys(data["set_up_your_account"]["last_name"])
        driver.find_element(By.NAME, "email").send_keys(data["set_up_your_account"]["email"])
        driver.find_element(By.NAME, "phoneNumber").send_keys(data["set_up_your_account"]["phone"])
        driver.find_element(By.NAME, "password").send_keys(data["set_up_your_account"]["password"])
        driver.find_element(By.NAME, "confirmPassword").send_keys(data["set_up_your_account"]["confirm_password"])
        driver.find_element(By.XPATH, "//button[contains(text(),'Next')]").click()

        main_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)

        print("✅ Signup form submitted successfully!")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-input-otp='true'][maxlength='6']")))

        code = get_verification_code(token)
        if code:
            driver.find_element(By.CSS_SELECTOR, "input[data-input-otp='true'][maxlength='6']").send_keys(code)
            driver.find_element(By.XPATH, "//button[contains(text(),'Verify Code')]").click()
            print("✅ Email verified and signup completed!")
        else:
            print("❌ Verification code not found in email.")
            return
            
        # -------- STEP 2: Agency Details --------
        print("🔄 Starting Step 2: Agency Details")
        wait.until(EC.presence_of_element_located((By.NAME, "agency_name"))).send_keys(data["agency_details"]["agency_name"])
        
        try:
            role_dropdown = driver.find_element(By.NAME, "role_in_agency")
            if role_dropdown.tag_name == "select":
                Select(role_dropdown).select_by_visible_text(data["agency_details"]["role_in_agency"])
            else:
                role_dropdown.send_keys(data["agency_details"]["role_in_agency"])
        except Exception as e:
            print(f"Role selection issue: {e}")
            driver.find_element(By.NAME, "role_in_agency").send_keys(data["agency_details"]["role_in_agency"])
        
        driver.find_element(By.NAME, "agency_email").send_keys(data["agency_details"]["email"])
        driver.find_element(By.NAME, "agency_website").send_keys(data["agency_details"]["website"])
        driver.find_element(By.NAME, "agency_address").send_keys(data["agency_details"]["address"])
        
        max_retries = 2
        for attempt in range(max_retries + 1):
            print(f"Attempt {attempt + 1} to select Nepal...")
            if select_nepal_from_dropdown(driver, wait):
                break
            elif attempt < max_retries:
                print("Retrying Nepal selection...")
                time.sleep(2)
            else:
                print("❌ All attempts to select Nepal failed. Stopping automation.")
                return
        
        try:
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", next_button)
            print("✅ Proceeding to Step 3 - Professional Experience")
        except Exception as e:
            print(f"❌ Could not click Next button: {e}")
            driver.save_screenshot("next_button_error.png")
            return

        # -------- STEP 3: Professional Experience --------
        print("🔄 Starting Step 3: Professional Experience")
        try:
            experience_dropdown_selectors = [
                "//button[contains(.,'Select Your Experience Level')]",
                "//button[contains(@role, 'combobox') and contains(.,'Experience')]",
                "//button[contains(@class,'justify-between') and contains(.,'Experience')]"
            ]
            dropdown_found = False
            for selector in experience_dropdown_selectors:
                try:
                    experience_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    driver.execute_script("arguments[0].click();", experience_dropdown)
                    dropdown_found = True
                    print(f"✅ Found experience dropdown with selector: {selector}")
                    break
                except Exception:
                    continue
            if not dropdown_found:
                print("❌ Could not find experience dropdown")
                driver.save_screenshot("experience_dropdown_not_found.png")
                return

            time.sleep(2)

            experience_options = driver.find_elements(By.XPATH, "//span[contains(text(),'5 years')] | //div[contains(text(),'5 years')] | //li[contains(text(),'5 years')]")
            for option in experience_options:
                if option.is_displayed():
                    print("✅ Clicking on visible '5 years' option")
                    driver.execute_script("arguments[0].click();", option)
                    break
            else:
                print("❌ Could not find '5 years' option")
                driver.save_screenshot("experience_option_not_found.png")
                return

            students_input = wait.until(EC.presence_of_element_located((By.NAME, "number_of_students_recruited_annually")))
            students_input.clear()
            students_input.send_keys(data["professional_experience"]["number_of_students_recruited_annually"])
            print("✅ Entered number of students")
            
            focus_input = wait.until(EC.presence_of_element_located((By.NAME, "focus_area")))
            focus_input.clear()
            focus_input.send_keys(data["professional_experience"]["focus_areas"])
            print("✅ Entered focus areas")
            
            success_input = wait.until(EC.presence_of_element_located((By.NAME, "success_metrics")))
            success_input.clear()
            success_input.send_keys(data["professional_experience"]["success_metrics"])
            print("✅ Entered success metrics")
            
            print("Selecting services provided...")
            try:
                checkbox = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Career Counseling')]/preceding-sibling::button[@role='checkbox'] | //button[@role='checkbox' and @aria-describedby and contains(@aria-describedby, 'form-item-description')]"))
                )
                if checkbox.get_attribute("aria-checked") != "true":
                    driver.execute_script("arguments[0].click();", checkbox)
                    print("✅ Career Counseling checkbox selected!")
                else:
                    print("✅ Career Counseling checkbox already selected")
            except Exception as e:
                print(f"❌ Could not select Career Counseling: {e}")
            
            next_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            print("✅ Step 3 completed successfully!")
            
        except Exception as e:
            print(f"❌ Step 3 failed: {e}")
            driver.save_screenshot("step3_error.png")
            return

        # -------- STEP 4: Verification and Preferences --------
        print("🔄 Starting Step 4: Verification and Preferences")
        try:
            print("Entering business registration number...")
            business_registration_input = wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//input[contains(@placeholder, 'Enter your registration number')] | " +
                "//input[contains(@name, 'business')] | " +
                "//input[contains(@id, 'business')]"
            )))
            business_registration_input.clear()
            business_registration_input.send_keys(data["verification_and_preferences"]["business_registration_number"])
            print("✅ Business registration number entered")

            print("Selecting preferred institution types...")
            try:
                checkboxes = driver.find_elements(By.XPATH, "//button[@role='checkbox']")
                for checkbox in checkboxes:
                    parent = checkbox.find_element(By.XPATH, "..")
                    if "Universities" in parent.text:
                        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                        time.sleep(0.5)
                        if checkbox.get_attribute("aria-checked") != "true":
                            driver.execute_script("arguments[0].click();", checkbox)
                            print("✅ Universities checkbox selected")
                        else:
                            print("✅ Universities checkbox already selected")
                        break
                else:
                    print("❌ Universities checkbox not found in checkboxes list")
            except Exception as e:
                print(f"❌ Could not select Universities checkbox: {e}")
                driver.save_screenshot("universities_checkbox_error.png")

            print("Selecting preferred country Australia...")
            try:
                country_dropdown = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@role='combobox' and contains(@id,'form-item')]"))
                )
                driver.execute_script("arguments[0].click();", country_dropdown)
                time.sleep(1)
                australia_option = wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'cursor-pointer') and .//span[text()='Australia']]"))
                )
                driver.execute_script("arguments[0].click();", australia_option)
                print("✅ Australia selected as preferred country")
            except Exception as e:
                print(f"❌ Could not select preferred country Australia: {e}")

            print("Entering certification details...")
            try:
                certification_input = wait.until(EC.presence_of_element_located((
                    By.XPATH,
                    "//input[contains(@placeholder, 'Certification Details')] | " +
                    "//textarea[contains(@placeholder, 'Certification Details')] | " +
                    "//input[contains(@name, 'certification')] | " +
                    "//textarea[contains(@name, 'certification')]"
                )))
                certification_input.clear()
                certification_input.send_keys(data["verification_and_preferences"]["certification_details"])
                print("✅ Certification details entered")
            except Exception as e:
                print(f"❌ Could not enter certification details: {e}")

            print("Handling file uploads...")
            try:
                file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                
                if file_inputs:
                    print(f"Found {len(file_inputs)} file upload inputs")
                else:
                    print("No file upload inputs found")
            except Exception as e:
                print(f"⚠️ File upload handling skipped: {e}")

            print("Uploading CV and cover letter...")
            try:
                file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                if len(file_inputs) >= 2:
                    file_inputs[0].send_keys("/home/animesh/Documents/python/signup_automation/Animesh Shakya CV Backend Development.pdf")
                    print("✅ CV uploaded")
                    file_inputs[1].send_keys("/home/animesh/Documents/python/signup_automation/Cover_Letter_Animesh.pdf")
                    print("✅ Cover letter uploaded")
                else:
                    print("❌ Not enough file inputs found for CV and cover letter.")
            except Exception as e:
                print(f"❌ File upload failed: {e}")

            print("Uploading business document...")
            try:
                file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
                if file_inputs:
                    file_inputs[0].send_keys("/home/animesh/Documents/python/Animesh Shakya CV")
                    print("✅ Business document uploaded")
                else:
                    print("❌ No file input found. The upload may require manual interaction or a different automation approach.")
            except Exception as e:
                print(f"❌ File upload failed: {e}")

            print("Submitting the form...")
            submit_button = wait.until(EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(text(),'Submit')] | " +
                "//button[@type='submit']"
            )))
            driver.execute_script("arguments[0].click();", submit_button)
            print("✅ Step 4 completed successfully!")

            time.sleep(3)
            
            try:
                success_indicator = driver.find_element(By.XPATH, 
                    "//h1[contains(text(),'Success')] | " +
                    "//div[contains(text(),'successful')] | " +
                    "//h2[contains(text(),'Thank you')]"
                )
                print("🎉 Registration completed successfully!")
            except:
                print("✅ Form submitted successfully!")

        except Exception as e:
            print(f"❌ Step 4 failed: {e}")
            driver.save_screenshot("step4_error.png")
            return
    finally:
        driver.quit()

def create_mailtm_account():
    domain_resp = requests.get("https://api.mail.tm/domains")
    domain = domain_resp.json()["hydra:member"][0]["domain"]
    username = "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"{username}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    acc_resp = requests.post("https://api.mail.tm/accounts", json={
        "address": email,
        "password": password
    })
    acc_resp.raise_for_status()
    return email, password

def get_mailtm_token(email, password):
    token_resp = requests.post("https://api.mail.tm/token", json={
        "address": email,
        "password": password
    })
    token_resp.raise_for_status()
    return token_resp.json()["token"]

def get_verification_code(token, wait_time=30):
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(wait_time // 2): 
        msg_resp = requests.get("https://api.mail.tm/messages", headers=headers)
        msgs = msg_resp.json()["hydra:member"]
        if msgs:
            msg_id = msgs[0]["id"]
            msg_detail = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
            match = re.search(r"\b\d{4,8}\b", msg_detail["text"])
            if match:
                return match.group(0)
        time.sleep(2)  
    return None

if __name__ == "__main__":
    main()