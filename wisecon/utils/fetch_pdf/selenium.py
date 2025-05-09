import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse


__all__ = [
    "fetch_pdf_bytes_use_selenium"
]


def fetch_pdf_bytes_use_selenium(url: str, timeout: int = 10) -> bytes:
    """"""
    if os.getenv("WISECON_REPORT_DIR"):
        path = os.getenv("WISECON_REPORT_DIR")
    else:
        user_home = os.path.expanduser('~')
        path = os.path.join(user_home, "wisecon", "report")

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

    file_name = os.path.basename(urlparse(url).path)
    file_path = os.path.join(path, file_name)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            bytes_content = f.read()
        return bytes_content
    else:
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless=new")
        try:
            service = Service(executable_path=os.getenv("WISECON_CHROME_DRIVER_PATH"))
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            raise Exception(f"Failed to start ChromeDriver or WISECON_CHROME_DRIVER_PATH is not set: {e}")
        driver.get(url)

        sleep_time = 0
        while not os.path.exists(os.path.join(path, file_name)) and sleep_time < timeout:
            time.sleep(0.05)
            sleep_time += 0.05

        driver.quit()
        with open(file_path, "rb") as f:
            bytes_content = f.read()
        return bytes_content
