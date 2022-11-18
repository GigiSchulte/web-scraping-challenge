#imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#scrape all function
def scrape_all():
    #splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    

    browser.quit()

#scrape the mars news page


#scrape through the featured image page


#scrape through the facts page


#scrape through the hemispheres pages


#set up as a flask app
if __name__=="__main__":
    print(scrape_all())