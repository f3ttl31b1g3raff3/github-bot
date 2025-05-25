from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from dotenv import load_dotenv
import codecs

# Load environment variables
load_dotenv()


def decode_hex_password(hex_password):
    """
    Decode a hexadecimal encoded password back to ASCII
    """
    try:
        return codecs.decode(hex_password.strip(), "hex").decode("ascii")
    except Exception as e:
        raise ValueError(f"Failed to decode hex password: {str(e)}")


class GitHubBot:
    def __init__(self):
        # Initialize Chrome WebDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, username=None, password=None):
        """
        Login to GitHub using provided credentials or environment variables
        """
        try:
            # Use environment variables if no credentials provided
            username = username or os.getenv("GITHUB_USERNAME")
            hex_password = password or os.getenv("GITHUB_PASSWORD")

            if not username or not hex_password:
                raise ValueError(
                    "GitHub credentials not provided and not found in environment variables"
                )

            # Decode the hex password
            password = decode_hex_password(hex_password)

            # Navigate to GitHub login page
            self.driver.get("https://github.com/login")

            # Wait for and find username field
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "login_field"))
            )
            username_field.send_keys(username)

            # Find password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            # Find and click login button
            login_button = self.driver.find_element(By.NAME, "commit")
            login_button.click()

            # Wait for successful login (checking for avatar button presence)
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.Button-label"))
            )
            print("Successfully logged in to GitHub!")
            return True

        except Exception as e:
            print(f"Error during login: {str(e)}")
            return False

        finally:
            self.driver.quit()


if __name__ == "__main__":
    bot = GitHubBot()
    bot.login()  # Will use environment variables for credentials
