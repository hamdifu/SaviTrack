import bs4
import smtplib
import requests
import json

class ScrapeData:

    def myntra(self,soup):
        goal = soup.select("script")[1].string
        # print(goal)
        match = json.loads(goal,strict=False)
        price = float(match['offers']['price'])
        name = match['name']
        print(f'Price : {price}\nName : {name}')
        return (price,name)

    def amazon(self,soup):
        price = float(soup.find(name="span", class_="a-price-whole").getText())
        name = soup.find(name='span', id='productTitle').getText().strip(' ')
        print(f'Price : {price}\nName : {name}')
        return (price,name)

    def hnm(self,soup):
        goal = soup.select("script")[11].string
        # print(json.loads(goal))
        data = json.loads(goal)
        price = float(data['offers'][0]['price'])
        name = data['name']
        print(f'Price : {price}\nName : {name}')
        return (price,name)

    # def zara(soup):
    #     price = float(soup.find(name='span',class_='money-amount__main').getText())
    #     name = soup.find(name='h1',class_='product-detail-info__header-name').getText()
    #     print(f'Price : {price}\nName : {name}')

    def nykaa(self,soup):
        price = float(soup.find(class_='css-1jczs19',name='span').getText().replace('₹',''))
        name = soup.find(class_='css-1gc4x7i',name='h1').getText()
        print(f'Price : {price}\nName : {name}')
        return (price,name)

    def urbanic(soup):
        pass

    def start(self,url):
        header = {
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        }
        response = requests.get(url=url, headers=header)
        response.raise_for_status()
        data = response.text
        soup = bs4.BeautifulSoup(data,"html.parser")
        # print(soup.prettify())
        name = url.split('/')[2]
        price = 0
        print(name)
        if name == 'www.amazon.in':
            price = self.amazon(soup)
        elif name == 'www.myntra.com':
            price = self.myntra(soup)
        elif name == 'www2.hm.com':
            price = self.hnm(soup)
        elif name == 'www.nykaa.com':
            price = self.nykaa(soup)

        return price

    def check_price(self, price, budget, url,to_email):
        if price <= budget:
            self.send_mail(price, url,to_email)


    def send_mail(self,price,url,email):
        user = 'preposterous.logic@gmail.com'
        password = 'dngomwitkppcdewz'
        # connection = smtplib.SMTP("smtp.gmail.com")
        with smtplib.SMTP("smtp.gmail.com",587) as connection:
            connection.starttls()  # to secure connection
            connection.login(user=user, password=password)
            connection.sendmail(from_addr=user, to_addrs=email,
                                msg=f'Subject:Price Drop!!\n\nFinally price dropped to Rs{price} for the product {url}!')
            # connection.close() #we don't have to write this line because of the with statement

url = 'https://www.myntra.com/swimwear/speedo/speedo-black-solid-bodysuit-8fs2760001/6674281/buy'
s1 = ScrapeData()
price = s1.start(url)[0]
to_email = 'suchismita.mishra8@gmail.com'
s1.check_price(price,1800,url,to_email)

# suchismita.mishra8@gmail.com
