import requests


class SendlerOneCreate:


    #TODO написать что бы входящий поток был driver_page_source and driver.screen_shoot
    def send_html_and_screen(self, photo_file, page_file, msg):
        TOKEN = ''


        file_in = open(page_file, 'rb')
        open_files = {'document': file_in}

        file_phoro= open(photo_file, 'rb')
        open_files['photo'] = {'photo': file_phoro}

        open_files['caption'] = {'caption': msg}

        url_req = "https://api.telegram.org/bot" + TOKEN + "/sendDocument?chat_id=" + '331583382'

        response = requests.post(url_req, files=open_files)

        file_in.close()
        file_phoro.close()

        print(f"Отправил html в телеграм")


