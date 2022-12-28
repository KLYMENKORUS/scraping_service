import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent


__all__ = ('get_work_ua', 'get_dou_ua', 'djinni_co')

browser = UserAgent()

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': browser.google
}


def get_work_ua(url, city=None, language=None):

    response = requests.get(url=url, headers=headers)

    jobs = []
    errors = []
    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            main_div = [f"https://www.work.ua{link.find_next('a').get('href')}" for link in
                        soup.find_all('div', class_='card-hover')]

            count_vl = 0
            for link_job in main_div:
                reg = requests.get(url=link_job, headers=headers)
                bs = BeautifulSoup(reg.text, 'lxml')

                content_job = bs.find_all('div', class_='card wordwrap')

                if content_job:
                    for job in content_job:
                        try:
                            title = job.find_next('h1', id='h1-name').get_text(strip=True)
                        except:
                            title = 'No name vacancy'
                        try:
                            description = job.find_next('div', id='job-description').get_text(strip=True)
                        except:
                            description = 'It not description vacancy'
                        try:
                            company = job.find_next('p', class_='text-indent text-muted add-top-sm').\
                                find_next('a').find('b').get_text(strip=True)
                        except:
                            company = 'No name company'

                        jobs.append({
                                'title': title,
                                'url': link_job,
                                'company': company,
                                'description': description,
                                'city_id': city,
                                'language_id': language
                            })

                        count_vl += 1
                        print(f'Vacancy # {count_vl}/{len(main_div)}')
                else:
                    errors.append({
                        'url': url,
                        'title': 'Div does not exists',
                    })
        else:
            errors.append({
                    'url': url,
                    'title': 'Page do not response',
            })

    return jobs, errors


def get_dou_ua(url, city=None, language=None):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("disable-dev-shm-usage")
    # driver = webdriver.Chrome(
    #     executable_path='chromedriver.exe',
    #     options=options
    # )
    driver = webdriver.Chrome(
        chrome_options=options, executable_path=ChromeDriverManager().install()
    )
    jobs = []
    errors = []
    if url:
        try:
            driver.get(url=url)
            time.sleep(5)
            try:
                button = driver.find_element(By.XPATH, '//*[@id="vacancyListId"]/div/a')
                button.click()
                time.sleep(5)
            except Exception:
                pass

            soup = BeautifulSoup(driver.page_source, 'lxml')
            list_vacancy = soup.find_all('li', class_='l-vacancy')

            if list_vacancy:
                count_vl = 0
                for content in list_vacancy:
                    try:
                        title = content.find('a', class_='vt').text.strip().replace('\xa0', ' ')
                    except:
                        title = 'No name vacancy'
                    try:
                        href = content.find('a', class_='vt').get('href')
                    except:
                        href = 'Oops no job link'
                    try:
                        company = content.find('a', class_='company').text.strip()
                    except:
                        company = 'No name company'
                    try:
                        description = content.find('div', class_='sh-info').text.strip().replace('\xa0', ' ')
                    except:
                        description = 'It not description vacancy'

                    jobs.append({
                        'title': title,
                        'url': href,
                        'company': company,
                        'description': description,
                        'city_id': city,
                        'language_id': language
                    })
                    count_vl += 1
                    print(f'Vacancies # {count_vl}/{len(list_vacancy)}')
            else:
                errors.append({
                    'url': url,
                    'title': 'Li does not exists'
                })

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    return jobs, errors


def djinni_co(url, city=None, language=None):
    response = requests.get(url=url, headers=headers)

    jobs = []
    errors = []
    if url:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            page_count = int(soup.find('ul', class_='pagination').find_all('a', class_='page-link')[-2].text)

            for page in range(1, page_count + 1):
                url_1 = f'{url}&page={page}'
                response = requests.get(url=url_1, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                li_lst = soup.find('ul', class_='list-jobs').find_all('li', class_='list-jobs__item')

                if li_lst:
                    for li in li_lst:
                        try:
                            title = li.find_next('div', class_='list-jobs__title').find('a').get_text(strip=True)
                        except:
                            title = 'No name vacancy'
                        try:
                            href = "https://djinni.co" \
                                   f"{li.find_next('div', class_='list-jobs__title').find('a').get('href')}"
                        except:
                            href = 'Oops no job link'
                        try:
                            description = li.find_next('div', class_='list-jobs__description').find('p').\
                                get_text(strip=True)
                        except:
                            description = 'It not description vacancy'
                        try:
                            company = li.find_next('div', class_='list-jobs__details__info').find('a').\
                                get_text(strip=True)
                        except:
                            company = 'No name company'

                        jobs.append({
                            'title': title,
                            'url': href,
                            'company': company,
                            'description': description,
                            'city_id': city,
                            'language_id': language
                        })

                    print(f'Page # {page}/{page_count}')
                else:
                    errors.append({
                        'url': url,
                        'title': 'Li does not exists'
                    })

        else:
            errors.append({
                'url': url,
                'title': 'Page do not response'
            })

    return jobs, errors

