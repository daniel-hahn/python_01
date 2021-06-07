'''
@author dan

not finished...

this program takes an ebay product url and max. bidding price as input
and automatically bids higher during the last second using an HTTP GET request

this is just a fun project and not meant to be actually used, 
as it would be rather unfair :)
'''

import requests
import time
from bs4 import BeautifulSoup
import re


class Bidding:
    
    def __init__(self, ebay_prduct_url, max_bid):

        self._ebay_prduct_url = ebay_prduct_url
        a = max_bid.replace(",", ".")
        self._max_bid = float(a)

        # get() request
        response = requests.get(self._ebay_prduct_url)

        # store the webpage contents
        self._webpage = response.content

        # check status sode (optional)
        # print(response.status_code)

        # create a BeautifulSoup object out of the webpage content
        self._soup = BeautifulSoup(self._webpage, "html.parser")

        # new bid margin
        self._margin = float("1.00") # in euro

        # last bid 
        self._last_bid = 0.0
    
    def bid(self):

        # get current price
        # update soup!
        current_price = self.soup.find(id='prcIsum_bidPrice')
        current_price = current_price.replace(",", ".")
        current_price = float(current_price)

        bid_price = current_price + self.margin
        bid_price = str(bid_price)
        bid_price = bid_price.replace(".", ",")

        # get bid item
        # bid = soup.find(id='MaxBidId')

        # get bid url
        #bid_url_1 = self.soup.find(id='bidBtn_btn').href

        # takes left offer
        bid_url_2 = self.soup.find(id='placeBidSec_btn_1').data-fallback
        
        # make GET request 
        x = bid_url_2.split('&')
        http_request = x[0] + "&" + x[1] + "&" + x[2] + "&" +  "maxbid=" + bid_price + "&" + x[4] + "&" + x[5] + "&"  + x[6] + "&"  + x[7]

        # send request
        print(http_request)
        #x = requests.get(http_request)

        # update last bid
        self._last_bid = bid_price
        
    def checkTime(self):

        # update soup!
        time_left = self._soup.find(id='vi-cdown_timeLeft')
        print(time_left.string)
        time_left = re.sub('[^0-9]','', str(time_left))
        return int(time_left)

    def haveHighestBid(self):
        
        # update soup!
        current_price = self._soup.find(id='prcIsum_bidPrice')
        current_price = current_price.string.replace(",", ".")
        current_price = re.sub('[^.0-9]','', str(current_price))
        current_price = float(current_price)

        if current_price == self._last_bid :
            return True
        else :
            return False

    def higherThanMaxBid(self):
        
        # update soup!
        current_price = self._soup.find(id='prcIsum_bidPrice')
        current_price = current_price.string.replace(",", ".")
        current_price = re.sub('[^.0-9]','', str(current_price))
        current_price = float(current_price)
        
        if current_price <= self._max_bid - self._margin:
            return False
        else :
            return True 


if __name__ == "__main__": 

    print("Welcome to auto bidding") 

    # get url input         
    url = input('Please enter the product url: ')
    print('Ok!')

    # get max bid input
    m_bid = input('Please enter your max bid [eg. 12,50]: ')
    print('Ok!')

    # create instance
    b = Bidding(url, m_bid)

    while True:

        # check if you have highest bid
        if b.haveHighestBid() == False:  
            
            # check if bid is higher than your max bid
            if b.higherThanMaxBid() == False:

                # check time left
                if b.checkTime() < 2:
                # bid if time is running out
                    b.bid()

                else :
                    time.sleep(1) # in sec
            
            else :
                break
        
        else :
            time.sleep(1) # in sec

       

        # get time left
        
