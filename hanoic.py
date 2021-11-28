import csv
import urllib.request
from bs4 import BeautifulSoup
from time import sleep
from traceback import print_exc

def crawl_single_product(url, rv):
    # with open("html", "r") as f:
        # soup = BeautifulSoup(f.read(), 'html.parser')
    try:
        with urllib.request.urlopen(url) as site:
            soup = BeautifulSoup(site.read().decode("utf8"), 'html.parser')
            # with open("html", "w") as f:
            # f.write(soup.prettify())
            _ = {}
            _['Name'] = soup.find("div", class_="product_detail-title") \
                         .find("h1").string.strip()
            _['Producer'] = soup.find("ul", attrs={"class": "list-unstyled"}) \
                             .contents[5].find('span', attrs={'itemprop': 'name'}).string.strip()
            summary = soup.find("div", class_="product-summary-item").find("ul")
            for child in summary.find_all("li"):
                data = [x.strip() for x in child.string.split(':')]
                if data[0] == 'Ổ cứng':
                    data[0] = 'DISK'
                elif data[0] == 'VGA':
                    data[0] = 'GPU'
                elif data[0] == 'Màn hình':
                    data[0] = 'DISPLAY'
                _[data[0]] = data[1]
                price = soup.find("div", attrs={"id": "product-info-price"})
                _['New Price'] = price.find("strong", class_="giakm").string.strip()
                price = price.find("strong", class_="giany")
                _['Old Price'] = price.string.strip() if price else None
                rv.append(_)
        return True
    except:
        print_exc()
        return False

def crawl_product_list():
    res = []
    with open('Crawl_Search_HN_CPT.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        index = -1
        line_count = 0
        f, t = 1, 100
        for row in csv_reader:
            index += 1
            if index < 1 or index < f or index > t:
                continue
            print(index, row[1])
            line_count += 1
            if not crawl_single_product(row[1], res):
                break
            sleep(0.5)
        print(f'Processed {line_count} lines.')

    with open('out.csv', 'w', encoding='utf-8', newline='') as file:
        fieldnames = ['Name', 'Producer', 'CPU', 'RAM', 'DISK', 'GPU', 'DISPLAY', 'Old Price', 'New Price']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for _ in res:
            row = {}
            for field in fieldnames:
                row[field] = _.get(field, None)
            writer.writerow(row)
            print(row)

if __name__=='__main__':
    crawl_product_list()
    
    
