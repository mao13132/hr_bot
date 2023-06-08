import asyncio

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from selenium.webdriver.common.keys import Keys

from browser.createbrowser import CreatBrowser

class HhScraper:
    def __init__(self, filter_dict):
        self.driver = filter_dict['driver']
        self.filter_dict = filter_dict
        self.count_auth = 3

    async def get_start_page(self):
        try:
            self.driver.get(self.filter_dict['url'])
        except Exception as es:
            print(f'Ошибка при заходе на главную {self.filter_dict["url"]} "{es}"')
            return False

        return True

    async def __check_load_start_page(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Сегодня')]")))
            return True
        except:
            print(f'Ошибка при загрузке стартовой страницы {self.filter_dict["url"]}')
            return False

    async def check_auth(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                      value="//*[contains(text(), 'Войти')]")

            return False

        except:

            return True

    async def click_to_in(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(text(), 'Войти')]").click()
        except Exception as es:

            print(f'Не могу кликнуть на вход "{es}"')
            return False

        return True

    async def __check_page_auth(self):
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'личный')]")))
            return True
        except:
            print(f'Ошибка при загрузке страницы авторизации {self.filter_dict["url"]}')
            return False

    async def __check_page_good_auth(self):

        try:
            error_aut = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), "
                                                                f"'Пожалуйста, попробуйте снова')]")

            if error_aut != []:
                print(f'Неправильные данные для входа {self.filter_dict["url"]}')
                return False
        except:
            pass

        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Счёт')]")))
            return True
        except:

            try:
                self.driver.find_elements(by=By.XPATH, value=f"//*[contains(text(), 'Пожалуйста, попробуйте снова')]")
                print(f'Неправильные данные для входа {self.filter_dict["url"]}')
                return False
            except:
                pass

            print(f'Ошибка при загрузке страницы после авторизации {self.filter_dict["url"]}')
            return False

    async def clear_login(self):
        try:
            test = self.driver.find_element(by=By.XPATH, value=f"//fieldset[contains(@class, 'input')]"
                                                               f"//input[@name='username']")
            self.driver.execute_script("arguments[0].setAttribute('value','')", test)

            test2 = self.driver.find_elements(by=By.XPATH, value=f"//*[contains(@data-qa, 'account-login-form')]"
                                                                 f"//input[@name='username']")
            self.driver.execute_script("arguments[0].setAttribute('value','')", test2[0])
        except:
            pass

    async def write_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//fieldset[contains(@class, 'input')]"
                                                        f"//input[@name='username']")\
                .send_keys(self.filter_dict['login'])

        except Exception as es:

            print(f'Не могу вписать логин {self.filter_dict["source"]} "{es}"')
            return False

        return True

    async def write_password(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//fieldset[contains(@class, 'input')]"
                                                        f"//input[contains(@data-qa"
                                                        f", 'password')]").send_keys(self.filter_dict['password'])

        except Exception as es:

            print(f'Не могу вписать пароль {self.filter_dict["source"]} "{es}"')
            return False

        return True

    async def click_aut_login(self):
        try:
            self.driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'account-login-actions')]"
                                                        f"/button").click()

        except Exception as es:

            print(f'Не могу кликнуть на кнопку войти по логину и паролю {self.filter_dict["source"]} "{es}"')
            return False

        return True

    async def job_autorize(self):

        await self.clear_login()

        response_write_login = await self.write_login()

        if not response_write_login:
            return False

        await asyncio.sleep(1)

        response_write_password = await self.write_password()

        if not response_write_password:
            return False

        await asyncio.sleep(1)

        response_click_login = await self.click_aut_login()

        if not response_click_login:
            return False

        await asyncio.sleep(1)

        response_good_aut = await self.__check_page_good_auth()

        if not response_good_aut:
            return False

        return True


    async def autorize_to_click(self):
        click_response = await self.click_to_in()
        if not click_response:
            return False

        check_load_page = await self.__check_page_auth()

        if not check_load_page:
            return False

        response_job_autorize = await self.job_autorize()

        if not response_job_autorize:
            return False

        return True

    async def loop_autorize(self):

        count = 0

        while True:

            if count > self.count_auth:
                return False

            self.driver.refresh()

            response_job_autorize = await self.job_autorize()

            if not response_job_autorize:
                count += 1
                continue

            return True

    async def module_aut(self):

        print(f'Не авторизован на {filter_dict["source"]} - авторизовываюсь')
        response_aut = await self.autorize_to_click()

        if not response_aut:
            response_loop_aut = await self.loop_autorize()
            if not response_loop_aut:
                print(f'Не смог авторизоваться - аварийно завершаюсь')
                return False

        return True

    async def start_scrap(self):
        to_start_page = await self.get_start_page()

        if not to_start_page:
            return False

        check_page = await self.__check_load_start_page()

        if not check_page:
            return False

        print(f'Успешно зашёл на {filter_dict["source"]}')

        response_auth = await self.check_auth()

        if not response_auth:
            response_aut = await self.module_aut()
            if not response_aut:
                return False

        print(f'Успешно авторизовался')
        print()



if __name__ == '__main__':

    stels = False
    browser_core = CreatBrowser('hhru', stels)

    filter_dict = {}
    filter_dict['source'] = 'hh.ru'
    filter_dict['url'] = 'https://hh.ru/employer'
    filter_dict['driver'] = browser_core.driver

    filter_dict['login'] = ''
    filter_dict['password'] = ''

    hh_scrap_core = HhScraper(filter_dict)

    response = asyncio.run(hh_scrap_core.start_scrap())
    print(response)
