import os
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)


class ChessComParser:
    def __init__(self):
        self.session = requests.Session()

    def get_soup(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Проверка на ошибки
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logging.error(f"Ошибка при загрузке страницы: {e}")
            return None

    def get_all_titled_tuesday_links(self, chess_com_url):
        soup = self.get_soup(chess_com_url)
        if soup:
            all_links = soup.find_all('a', class_='tournaments-live-name', href=True)
            return {link['href'] for link in all_links}
        else:
            return set()

    def get_next_page_link(self, chess_com_url):
        soup = self.get_soup(chess_com_url)
        if soup:
            next_link = soup.find('link', rel='next')
            if next_link:
                return next_link.get('href')
        return None

    def get_titled_tuesday_csv_link(self, titled_tuesday_link):
        soup = self.get_soup(titled_tuesday_link)
        if soup:
            csv_link_element = soup.find('a', {'aria-label': 'Скачать партии'})
            if csv_link_element:
                return csv_link_element['href']
            else:
                logging.error("Ссылка на скачивание CSV не найдена на странице.")
        else:
            logging.error(f"Не удалось загрузить страницу: {titled_tuesday_link}")

    def get_csv_file(self, csv_url, save_folder):
        try:
            # Проверяем существование папки и создаем ее, если она не существует
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            parsed_url = urlparse(csv_url)
            filename = os.path.basename(parsed_url.path)
            save_path = os.path.join(save_folder, filename)

            response = self.session.get(csv_url)
            response.raise_for_status()  # Проверка на ошибки

            with open(save_path, 'wb') as file:
                file.write(response.content)
            logging.info(f"Файл успешно загружен по адресу: {save_path}")
            return save_path
        except (requests.RequestException, IOError) as e:
            logging.error(f"Произошла ошибка при загрузке файла: {str(e)}")
            return None
