# Scrapy-tripadvisor-reviews
Using scrapy to scrape tripadvisor in order to get users' reviews.

The code in this repository was used to scrape and gather data from tripadvisor about some brazilian cities attractions. The data were used to train a sentiment analysis classifier used in https://github.com/igorbpf/Twitter-Sentiment (https://twisentiment.herokuapp.com/). 

# Usage
In the project's root folder type:

scrapy crawl tripadvisor -o tripadvisor_reviews.csv

the reviews will be stored in a csv file named tripadvisor_reviews
