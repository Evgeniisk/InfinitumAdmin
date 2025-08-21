from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from AuthenticationApp.models import CustomUser, Invite
from selenium.webdriver.support.ui import Select
import time
import os
import subprocess
import shutil

#The class defines one class for testing this applications basic functionality and security as if it is in a production environment such as whether the user is able to authentication in the app use it etc
class FullUserFlowTest(StaticLiveServerTestCase):
    def setUp(self):
        self.selenium = WebDriver() #Initialoses the selenium driver (I use firefox)
        self.selenium.implicitly_wait(10)
        url = self.live_server_url #URL of Django's live server for testing
        current_dir = os.path.dirname(__file__) #Current file directory
        env_path = os.path.join(os.path.dirname(__file__), '../../../frontend/.env.production') #Path to the front end production environment url
        #This writes Djangos live server url for testing to the front end .env.production file
        with open(env_path, "w") as file:
            file.write(f"VITE_API_URL={url}")
        #This finds the npm executable on the system which is npm.cmd for windows because I developed this app on windows
        npm_cmd = shutil.which("npm") or shutil.which("npm.cmd")
        #This is the path to the front end directory
        frontend_dir = os.path.abspath(os.path.join(current_dir, "../../../frontend"))
        print(frontend_dir) #for debugging
        #This runs npm run build to build the frontend for production 
        subprocess.run([npm_cmd, "run", "build"], cwd=frontend_dir, check=True)
    #This shuts the testing environment down and quits the selenium browser instance after testing is complete
    def tearDown(self):
        self.selenium.quit()
    #the function for testing the function of the web app as specified at the beginning of this document
    def test_full_auth_flow(self):
        email = "testuser@example.com"
        password = "StrongPass123!"
        self.selenium.get(f"{self.live_server_url}")
        self.selenium.find_element(By.ID, "Login").click()
        self.selenium.find_element(By.ID, "landing_page").click()
        self.selenium.find_element(By.ID, "Register").click()
        self.selenium.find_element(By.ID, "Security_info").click()
        self.selenium.find_element(By.ID, "Login/Signup").click()
        self.selenium.find_element(By.ID, "SignUp").click()

        self.selenium.find_element(By.NAME, "first_name").send_keys("Test")
        self.selenium.find_element(By.NAME, "last_name").send_keys("User")
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "workplace_name").send_keys("Test LTD")
        self.selenium.find_element(By.NAME, "workplace_address_line_1").send_keys("Test 1")
        self.selenium.find_element(By.NAME, "workplace_address_line_2").send_keys("Test 2")
        self.selenium.find_element(By.NAME, "workplace_address_city").send_keys("London")
        self.selenium.find_element(By.NAME, "workplace_address_Zip").send_keys("Test")
        country_select_element = self.selenium.find_element(By.NAME, "workplace_address_Country")
        country_select = Select(country_select_element)
        country_select.select_by_visible_text("United Kingdom")
        self.selenium.find_element(By.NAME, "password").send_keys(password)
        submit_button = self.selenium.find_element(By.ID, "signup-submit")
        #Selenium scrolls the page until the submit button is visible
        self.selenium.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_button) #arguments[0] is the submit button to be visible
        time.sleep(0.3)
        submit_button.click()


        self.assertTrue(CustomUser.objects.filter(email=email).exists())
        user = CustomUser.objects.get(email=email)
        self.assertFalse(user.email_confirmed)
        #confirmation_url = f"{self.live_server_url}/EmailConfirmationPage/"
        #self.selenium.get(confirmation_url)
        confirmation_code_input = self.selenium.find_element(By.ID, "ConfirmationCodeInput")
        confirmation_code = user.email_confirmation_code
        confirmation_code_input.send_keys(f"{confirmation_code}")
        submit_button = self.selenium.find_element(By.ID, "submit-button")
        submit_button.click()
        user.refresh_from_db()
        self.assertTrue(user.email_confirmed)

        self.selenium.get(f"{self.live_server_url}/LoginPage/")
        user = CustomUser.objects.get(email=email)
        if user.is_locked == True:
            user.is_locked = False
            user.failed_login_attempts = 0
            user.unlock_account_token = None
            user.unlock_account_token_created_at = None
            user.unlock_account_token_expires_at = None
            user.save()
        user.refresh_from_db()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys("Random")
        self.selenium.find_element(By.ID, "login-submit").click()
        user.refresh_from_db()
        print(user.is_locked)
        self.assertTrue(user.is_locked)
        token = user.unlock_account_token
        self.selenium.get(f"{self.live_server_url}/AccountUnlocked?token={token}")
        print(f"{self.live_server_url}/AccountUnlocked?token={token}")
        self.selenium.find_element(By.ID, "login").click()
        self.selenium.find_element(By.ID, "reset_password").click()
        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.ID, "Reset_password").click()
        user.refresh_from_db()
        token = user.reset_password_token
        self.selenium.get(f"{self.live_server_url}/ResetPasswordPage?token={token}")
        password = "NewStrongPassword123"
        self.selenium.find_element(By.NAME, "password").send_keys(password)
        self.selenium.find_element(By.NAME, "password2").send_keys(password)
        self.selenium.find_element(By.ID, "submit-button").click()

        self.selenium.find_element(By.NAME, "email").send_keys(email)
        self.selenium.find_element(By.NAME, "password").send_keys(password)
        self.selenium.find_element(By.ID, "login-submit").click()
        user.refresh_from_db()

        wait = WebDriverWait(self.selenium, 5)
        element = wait.until(EC.presence_of_element_located((By.ID, "app")))
        assert element is not None, "Element with ID 'app' was not found."
        wait.until(lambda driver: driver.execute_script("return document.getElementById('app').children.length > 0"))
        #Very importat to do by link text because of vue rendering issues.
        #client_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Clients")))
        #client_button.click()
        wait = WebDriverWait(self.selenium, 20)
        #Very importat to do by link text because of vue rendering issues.
        clients_button = wait.until(EC.element_to_be_clickable((By.ID, "Clients")))
        clients_button.click()
        jobs_button = wait.until(EC.element_to_be_clickable((By.ID, "Jobs")))
        jobs_button.click()
        templates_button = wait.until(EC.element_to_be_clickable((By.ID, "Templates")))
        templates_button.click()
        individual_button = wait.until(EC.element_to_be_clickable((By.ID, "IndividualTemplates")))
        individual_button.click()
        time.sleep(2)
        company_button = wait.until(EC.element_to_be_clickable((By.ID, "CompanyTemplates")))
        company_button.click()
        time.sleep(2)
        Jobs_button = wait.until(EC.element_to_be_clickable((By.ID, "Jobs")))
        Jobs_button.click()
        time.sleep(2)
        settings_button = wait.until(EC.element_to_be_clickable((By.ID, "SettingsButton")))
        self.assertIn("/app/", self.selenium.current_url)
        settings_button.click()
        time.sleep(2)
        self.selenium.find_element(By.ID, "InviteUser").click()
        First_name = "Eugene"
        Last_name = "Korostelev"
        Email2 = "example2@gmail.com"
        Position = "Developer"
        WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable((By.ID, "InputFname")))
        self.selenium.find_element(By.ID, "InputFname").send_keys(First_name)
        self.selenium.find_element(By.ID, "InputLname").send_keys(Last_name)
        self.selenium.find_element(By.ID, "InputEmail").send_keys(Email2)
        self.selenium.find_element(By.ID, "InputPosition").send_keys(Position)
        self.selenium.find_element(By.ID, "submitbutton").click()
        WebDriverWait(self.selenium, 10).until(EC.invisibility_of_element_located((By.ID, "InviteUserModal")))
        self.selenium.find_element(By.ID, "closecanvasbutton").click()
        WebDriverWait(self.selenium, 10).until(EC.invisibility_of_element_located((By.ID, "offcanvasTop")))
        self.selenium.find_element(By.ID, "LogoutButton").click()
        WebDriverWait(self.selenium, 10).until(EC.element_to_be_clickable((By.ID, "LogOutConfirm")))
        self.selenium.find_element(By.ID, "LogOutConfirm").click()
        time.sleep(1)
        self.assertTrue(Invite.objects.filter(email=Email2).exists())
        invite = Invite.objects.get(email=Email2)
        self.selenium.get(f"{self.live_server_url}/UserRegistrationPage/?token={invite.token}")
        password2 = "ANotherSOmepassword"
        self.selenium.find_element(By.NAME, "first_name").send_keys(First_name)
        self.selenium.find_element(By.NAME, "last_name").send_keys(Last_name)
        self.selenium.find_element(By.NAME, "email").send_keys(Email2)
        self.selenium.find_element(By.NAME, "password").send_keys(password2)
        self.selenium.find_element(By.ID, "Submit").click()
        confirmation_code_input = self.selenium.find_element(By.ID, "ConfirmationCodeInput")
        user = CustomUser.objects.get(email=Email2)
        confirmation_code = user.email_confirmation_code
        confirmation_code_input.send_keys(f"{confirmation_code}")
        submit_button = self.selenium.find_element(By.ID, "submit-button")
        time.sleep(2)
        submit_button.click()
        time.sleep(2)
        user.refresh_from_db()
        self.assertTrue(user.email_confirmed)
        self.selenium.find_element(By.NAME, "email").send_keys(Email2)
        self.selenium.find_element(By.NAME, "password").send_keys(password2)
        self.selenium.find_element(By.ID, "login-submit").click()
        clients_button = wait.until(EC.element_to_be_clickable((By.ID, "Clients")))
        clients_button.click()
        time.sleep(2)
        settings_button = wait.until(EC.element_to_be_clickable((By.ID, "SettingsButton")))
        settings_button.click()
        time.sleep(2)



