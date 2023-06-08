import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from browser.createbrowser import CreatBrowser

class HhScraper:
    def __init__(self, driver, filter_dict):
        self.driver = driver
        self.filter_dict = filter_dict

    async def get_start_page(self):
        try:
            self.driver.get(self.filter_dict['url'])
        except Exception as es:
            print(f'Ошибка при заходе на главную "{es}"')
            return False

        return True

    async def __check_load_start_page(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Найти')]")))
            return True
        except:
            print(f'Ошибка при загрузке стартовой страницы страницы')
            return False

    async def start_scrap(self):
        to_start_page = await self.get_start_page()

        if not to_start_page:
            return False

        check_page = await self.__check_load_start_page()



if __name__ == '__main__':

    stels = False
    browser_core = CreatBrowser('hhru', stels)

    filter_dict = {}
    filter_dict['url'] = 'https://hh.ru/'

    hh_scrap_core = HhScraper(browser_core.driver, filter_dict)

    response = asyncio.run(hh_scrap_core.start_scrap())
    print(response)
