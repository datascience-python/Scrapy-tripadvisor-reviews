#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from myscraps.items import ReviewItem
from scrapy import Request

class TripAdvisorReview(scrapy.Spider):
    name = "tripadvisor"
    # Cities: Recife, Porto Alegre, Salvador, Brasilia, Fortaleza, Curitiba, Belo Horizonte, Vitoria, Florianopolis, Natal, Goiania.
    start_urls = ["https://www.tripadvisor.com.br/Attractions-g304560-Activities-Recife_State_of_Pernambuco.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303546-Activities-Porto_Alegre_State_of_Rio_Grande_do_Sul.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303272-Activities-Salvador_State_of_Bahia.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303322-Activities-Brasilia_Federal_District.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303293-Activities-Fortaleza_State_of_Ceara.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303441-Activities-Curitiba_State_of_Parana.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303374-Activities-Belo_Horizonte_State_of_Minas_Gerais.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303320-Activities-Vitoria_State_of_Espirito_Santo.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303576-Activities-Florianopolis_State_of_Santa_Catarina.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303518-Activities-Natal_State_of_Rio_Grande_do_Norte.html",\
                    "https://www.tripadvisor.com.br/Attractions-g303324-Activities-Goiania_State_of_Goias.html"]

    def parse(self, response):
        urls = []
        for href in response.xpath('//div[@class="property_title"]/a/@href').extract():
            url = response.urljoin(href)
            if url not in urls:
                urls.append(url)

                yield scrapy.Request(url, callback=self.parse_page)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            print url
            yield scrapy.Request(url, self.parse)

    def parse_page(self, response):

        review_page = response.xpath('//div[@class="wrap"]/div/a/@href').extract()

        if review_page:
            for i in range(len(review_page)):
                url = response.urljoin(review_page[i])
                yield scrapy.Request(url, self.parse_review)

        next_page = response.xpath('//div[@class="unified pagination "]/a/@href').extract()
        if next_page:
            url = response.urljoin(next_page[-1])
            yield scrapy.Request(url, self.parse_page)



    def parse_review(self, response):

        item = ReviewItem()

        contents = response.xpath('//div[@class="entry"]/p').extract()
        content = contents[0].encode("utf-8")

        ratings = response.xpath('//span[@class="rate sprite-rating_s rating_s"]/img/@alt').extract()
        rating = ratings[0][0]


        item['rating'] = rating
        item['review'] = content
        yield item

