from selenium import webdriver
from time import sleep
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


class PageLoader:
    def __init__(self):
        sleep(7)
        self.options = webdriver.ChromeOptions()

        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        user_agent_rotator = UserAgent(
            software_names=software_names,
            operating_systems=operating_systems,
            limit=100,
        )
        user_agent = user_agent_rotator.get_random_user_agent()

        self.options.add_argument(f"user-agent={user_agent}")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("w3c", True)
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        sleep(5)

    def load_page(self, url):
        self.driver = webdriver.Remote(
            "http://selenium:4444/wd/hub", options=self.options
        )
        self.driver.get(url=url)
        sleep(7)
        html = self.driver.page_source
        self.driver.quit()
        return html
