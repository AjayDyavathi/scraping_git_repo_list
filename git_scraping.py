from bs4 import BeautifulSoup
import requests
import csv

file = open('git_repo.csv', 'w')
writer = csv.writer(file)
writer.writerows([['Name', 'Description', 'Stars', 'Language', 'Updated on']])

search_term = 'CVE 2018'
formatted_search_term = search_term.replace(' ', '+')
link = f'https://github.com/search?q={formatted_search_term}&type=Repositories'
try:
    while True:
        try:
            page = requests.get(link).text
            soup = BeautifulSoup(page, 'lxml')
            raw_repo_list = soup.find(class_='repo-list')

        except AttributeError as e:
            print('Connection closed, waiting for 20 seconds')
            time.sleep(20)
            continue

        print('Scraping from ', link, '-> git_repo.csv')
        repos = raw_repo_list.find_all(class_='repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source')
        for repo in repos:
            formatted_repo_list = []

            name = repo.find(class_='f4 text-normal').text
            formatted_repo_list.append(name)

            desc = repo.find(class_='mb-1')
            description = desc.text.strip() if desc else 'No description'
            formatted_repo_list.append(description)

            star = repo.find(class_='muted-link')
            star_num = star.text.strip() if star else 'No stars'
            formatted_repo_list.append(star_num)

            lang = repo.find(itemprop='programmingLanguage')
            language = lang.text.strip() if lang else 'Not mentioned'
            formatted_repo_list.append(language)

            dt = repo.find('relative-time')
            updated_on = dt.text.strip() if dt else 'Not mentioned'
            formatted_repo_list.append(updated_on)

            writer.writerows([formatted_repo_list])

            sub_link = soup.find('a', class_='next_page')
            link = 'https://github.com' + sub_link['href'] if sub_link else None
            if link == None:
                break

except Exception as e:
    print(str(e))

finally:
    file.close()
