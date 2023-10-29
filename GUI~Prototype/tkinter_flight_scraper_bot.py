from time import sleep, strftime
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart



class Flight_Bot:

    
    def __init__(self):
        print('initiating the bot...')
        
        self.YOUR_HOTMAIL_EMAIL = # string
        self.YOURPASSWORD = # string
        self.YOUR_OTHER_EMAIL = # string
        YOUR_CHROME_DRIVER_PATH = # string
        chromedriver_path = YOUR_CHROME_DRIVER_PATH + '/chromedriver_win32/chromedriver.exe'
        global driver
        driver = webdriver.Chrome(executable_path=chromedriver_path) # This will open the Chrome window
        sleep(2)
        
    
    # Load more results to maximize the scraping
    def load_more(self):
        try:
            more_results = '//a[@class = "moreButton"]'
            driver.find_element_by_xpath(more_results).click()
            # Printing these notes during the program helps me quickly check what it is doing
            print('sleeping.....')
            sleep(randint(45,60))
        except:
            pass
    
    def page_scrape(self):
        """This function takes care of the scraping part"""
        sleep(5)
        xp_sections = '//*[@class="section duration"]'
        sections = driver.find_elements_by_xpath(xp_sections)
        sections_list = [value.text for value in sections]
        section_a_list = sections_list[::2] # This is to separate the two flights
        section_b_list = sections_list[1::2] # This is to separate the two flights
        
        # if you run into a reCaptcha, you might want to do something about it
        # you will know there's a problem if the lists above are empty
        # this if statement lets you exit the bot or do something else
        # you can add a sleep here, to let you solve the captcha and continue scraping
        # i'm using a SystemExit because i want to test everything from the start
        if section_a_list == []:
            raise SystemExit
        
        # I'll use the letter A for the outbound flight and B for the inbound
        a_duration = []
        a_section_names = []
        for n in section_a_list:
            # Separate the time from the cities
            a_section_names.append(''.join(n.split()[2:5]))
            a_duration.append(''.join(n.split()[0:2]))
        b_duration = []
        b_section_names = []
        for n in section_b_list:
            # Separate the time from the cities
            b_section_names.append(''.join(n.split()[2:5]))
            b_duration.append(''.join(n.split()[0:2]))
    
        xp_dates = '//div[@class="section date"]'
        dates = driver.find_elements_by_xpath(xp_dates)
        dates_list = [value.text for value in dates]
        a_date_list = dates_list[::2]
        b_date_list = dates_list[1::2]
        # Separating the weekday from the day
        a_day = [value.split()[0] for value in a_date_list]
        a_weekday = [value.split()[1] for value in a_date_list]
        b_day = [value.split()[0] for value in b_date_list]
        b_weekday = [value.split()[1] for value in b_date_list]
        print(b_weekday)
        
        # getting the prices
        xp_prices = '//a[@class="booking-link"]/span[@class="price option-text"]'
        prices = driver.find_elements_by_xpath(xp_prices)
        prices_list = [price.text.replace('$','') for price in prices if price.text != '']
        prices_list = list(map(int, prices_list))
        print(prices_list)
    
        # the stops are a big list with one leg on the even index and second leg on odd index
        xp_stops = '//div[@class="section stops"]/div[1]'
        stops = driver.find_elements_by_xpath(xp_stops)
        stops_list = [stop.text[0].replace('n','0') for stop in stops]
        a_stop_list = stops_list[::2]
        b_stop_list = stops_list[1::2]
    
        xp_stops_cities = '//div[@class="section stops"]/div[2]'
        stops_cities = driver.find_elements_by_xpath(xp_stops_cities)
        stops_cities_list = [stop.text for stop in stops_cities]
        a_stop_name_list = stops_cities_list[::2]
        b_stop_name_list = stops_cities_list[1::2]
        
        # this part gets me the airline company and the departure and arrival times, for both legs
        xp_schedule = '//div[@class="section times"]'
        schedules = driver.find_elements_by_xpath(xp_schedule)
        hours_list = []
        carrier_list = []
        for schedule in schedules:
            hours_list.append(schedule.text.split('\n')[0])
            carrier_list.append(schedule.text.split('\n')[1])
        # split the hours and carriers, between a and b legs
        a_hours = hours_list[::2]
        a_carrier = carrier_list[::2]
        b_hours = hours_list[1::2]
        b_carrier = carrier_list[1::2]
    
        
        cols = (['Out Day', 'Out Time', 'Out Weekday', 'Out Airline', 'Out Cities', 'Out Duration', 'Out Stops', 'Out Stop Cities',
                'Return Day', 'Return Time', 'Return Weekday', 'Return Airline', 'Return Cities', 'Return Duration', 'Return Stops', 'Return Stop Cities',
                'Price'])
    
        flights_df = pd.DataFrame({'Out Day': a_day,
                                   'Out Weekday': a_weekday,
                                   'Out Duration': a_duration,
                                   'Out Cities': a_section_names,
                                   'Return Day': b_day,
                                   'Return Weekday': b_weekday,
                                   'Return Duration': b_duration,
                                   'Return Cities': b_section_names,
                                   'Out Stops': a_stop_list,
                                   'Out Stop Cities': a_stop_name_list,
                                   'Return Stops': b_stop_list,
                                   'Return Stop Cities': b_stop_name_list,
                                   'Out Time': a_hours,
                                   'Out Airline': a_carrier,
                                   'Return Time': b_hours,
                                   'Return Airline': b_carrier,                           
                                   'Price': prices_list})[cols]
        
        flights_df['timestamp'] = strftime("%Y%m%d-%H%M") # so we can know when it was scraped
        return flights_df
    
    
    def start_kayak(self, city_from, city_to, date_start, date_end):
        """City codes - it's the IATA codes!
        Date format -  YYYY-MM-DD"""
    
        kayak = ('https://www.kayak.com/flights/' + city_from + '-' + city_to +
                 '/' + date_start + '-flexible/' + date_end + '-flexible?sort=bestflight_a')
        driver.get(kayak)
        sleep(randint(15,20))
        
        # sometimes a popup shows up, so we can use a try statement to check it and close
        try:
            xp_popup_close = '//button[contains(@id,"dialog-close") and contains(@class,"Button-No-Standard-Style close ")]'
            driver.find_elements_by_xpath(xp_popup_close)[5].click()
        except Exception as e:
            pass
        sleep(randint(15,25))
        print('loading more.....')
        
    #     Flight_Bot.load_more(self)
        
        print('starting first scrape.....')
        df_flights_best = Flight_Bot.page_scrape(self)
        df_flights_best['sort'] = 'best'
        sleep(randint(18,25))
        df_flights_best.to_csv('testing_best.csv')
        
        try:
            # Let's also get the lowest prices from the matrix on top
            matrix = driver.find_elements_by_xpath('//*[contains(@id,"FlexMatrixCell")]')
            matrix_prices = [price.text.replace('$','') for price in matrix]
            matrix_prices = list(map(int, matrix_prices))
            matrix_min = min(matrix_prices)
            matrix_avg = sum(matrix_prices)/len(matrix_prices)
        except Exception as e:
            driver.find_elements_by_xpath('//button[contains(@class,"heading withBorder Button-No-Standard-Style")]')[1].click()
            # Let's also get the lowest prices from the matrix on top
            matrix = driver.find_elements_by_xpath('//*[contains(@id,"FlexMatrixCell")]')
            matrix_prices = [price.text.replace('$','') for price in matrix]
            matrix_prices = list(map(int, matrix_prices))
            matrix_min = min(matrix_prices)
            matrix_avg = sum(matrix_prices)/len(matrix_prices)
            pass            
            
        
        print('switching to cheapest results.....')
        cheap_results = '//a[@data-code = "price"]'
        driver.find_element_by_xpath(cheap_results).click()
        sleep(randint(60,90))
        print('loading more.....')
        
    #     Flight_Bot.load_more(self)
        
        print('starting second scrape.....')
        df_flights_cheap = Flight_Bot.page_scrape(self)
        df_flights_cheap['sort'] = 'cheap'
        sleep(randint(60,80))
        
        print('switching to quickest results.....')
        quick_results = '//a[@data-code = "duration"]'
        driver.find_element_by_xpath(quick_results).click()  
        sleep(randint(60,90))
        print('loading more.....')
        
    #     Flight_Bot.load_more(self)
        
        print('starting third scrape.....')
        df_flights_fast = Flight_Bot.page_scrape(self)
        df_flights_fast['sort'] = 'fast'
        sleep(randint(60,80))
        
        # saving a new dataframe as an excel file. the name is custom made to your cities and dates
        final_df = df_flights_cheap.append(df_flights_best).append(df_flights_fast)
        final_df.to_excel('search_backups//{}_flights_{}-{}_from_{}_to_{}.xlsx'.format(strftime("%Y%m%d-%H%M"),
                                                                                       city_from, city_to, 
                                                                                       date_start, date_end), index=False)
        print('saved df.....')
        
        # We can keep track of what they predict and how it actually turns out!
        xp_loading = '//div[contains(@id,"advice")]'
        loading = driver.find_element_by_xpath(xp_loading).text
        xp_prediction = '//span[@class="info-text"]'
        prediction = driver.find_element_by_xpath(xp_prediction).text
        print(loading+'\n'+prediction)
        
        # sometimes we get this string in the loading variable, which will conflict with the email we send later
        # just change it to "Not Sure" if it happens
        weird = '¯\\_(ツ)_/¯'
        if loading == weird:
            loading = 'Not sure'
        
        username = self.YOUR_HOTMAIL_EMAIL
        password = self.YOURPASSWORD
    
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        msg = ('Subject: Flight Scraper\n\n\
    Cheapest Flight: {}\nAverage Price: {}\n\nRecommendation: {}\n\nEnd of message'.format(matrix_min, matrix_avg, (loading+'\n'+prediction)))
        message = MIMEMultipart()
        message['From'] = self.YOUR_HOTMAIL_EMAIL
        message['to'] = self.YOUR_OTHER_EMAIL
        server.sendmail(self.YOUR_HOTMAIL_EMAIL, self.YOUR_OTHER_EMAIL, msg)
        print('sent email.....')
