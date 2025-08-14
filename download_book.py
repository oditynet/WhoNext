import os
import time
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MassLib6Downloader:
    def __init__(self):
        self.download_dir = os.path.join(os.getcwd(), "downloaded_books")
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Настройка Firefox
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("browser.download.folderList", 2)
        firefox_options.set_preference("browser.download.dir", self.download_dir)
        firefox_options.set_preference("browser.download.useDownloadDir", True)
        firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
        
        # Указываем ваш путь к geckodriver
        service = Service(executable_path="/home/odity/bin/AI1/geckodriver")
        self.driver = webdriver.Firefox(service=service, options=firefox_options)
    
    def download_book(self, book_id):
        """Быстрое скачивание одной книги"""
        url = f"https://www.6lib.ru/download/komanduuhiy-frontom-{book_id}.txt"
        try:
            self.driver.get(url)
            
            # Быстрое ожидание и клик
            download_btn = WebDriverWait(self.driver, 1).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'dwn_txt')]"))
            )
            download_btn.click()
            print(f"Скачивание начато для ID: {book_id}")
            
            # Фиксированное ожидание 2 секунды
            #time.sleep(1)
            
        except Exception as e:
            print(f"Пропуск ID {book_id} (ошибка: {str(e)})")
    
    def download_range(self, start_id, end_id):
        """Скачивание диапазона ID"""
        print(f"Начало массового скачивания (ID {start_id}-{end_id})...")
        print("Для остановки нажмите Ctrl+C\n")
        
        for book_id in range(start_id, end_id + 1):
            self.download_book(book_id)
    
    def close(self):
        """Закрытие браузера"""
        self.driver.quit()

if __name__ == "__main__":
    downloader = MassLib6Downloader()
    
    try:
        # Запускаем скачивание с ID 24047 до 2000000
        downloader.download_range(51004, 2000000)
    except KeyboardInterrupt:
        print("\nСкачивание прервано пользователем")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")
    finally:
        downloader.close()
