import requests, json, re
from bs4 import BeautifulSoup as BS

url = "https://www.healthline.com/nutrition/50-super-healthy-foods"

def get_html():
    r = requests.get(url)
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(r.text)

def get_data():
    with open('index.html', encoding='utf-8') as file:
        html = file.read()

    soup = BS(html, 'lxml')

    parts_of_name = soup.find(class_='article-body css-d2znx6 undefined').find_all('div', class_='css-0')

    data = []

    for part in parts_of_name:

        for title in part.find_all('h3'):
            if title.text[0].isnumeric() and title.text[1] != '–' and title.text[2] != '–':

                description = title.find_next().text
                to_replace = re.findall(r" \([0-9]{2}\)", description) + \
                             re.findall(r" \([0-9]\)", description) + \
                             re.findall(r" \([0-9]{2}, [0-9]{2}\)", description) # to remove links in hooks

                for item in to_replace:
                    description = description.replace(item, '') # to replace digits in hooks

                data.append(
                    {
                        'name_of_food': title.text[3:].strip(),
                        'description_of_food': description
                    }
                )

        for title in part.find_all('h2'):
            if title.text[0].isnumeric() and title.text[1] != '–' and title.text[2] != '–':

                description = title.find_next_sibling().text
                to_replace = re.findall(r" \([0-9]{2}\)", description) + \
                             re.findall(r" \([0-9]\)", description) + \
                             re.findall(r" \([0-9]{2}, [0-9]{2}\)", description) # to remove links in hooks

                for item in to_replace:
                    description = description.replace(item, '') # to replace digits in hooks

                data.append(
                    {
                        'name_of_food': title.text[3:].strip(),
                        'description_of_food': description
                    }
                )

    with open('foods.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def main():
    get_html()
    get_data()

if __name__ == '__main__':
    main()