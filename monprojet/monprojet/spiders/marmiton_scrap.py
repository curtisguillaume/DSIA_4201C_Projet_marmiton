import scrapy
from scrapy.http import Request

class MarmitonSpider(scrapy.Spider):
    name = 'marmit'
    allowed_domains = ['marmiton.org']
    start_urls = ['https://www.marmiton.org/recettes/index/categorie/aperitif-ou-buffet/']

    # Custom settings for this spider
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        # 'COOKIES_ENABLED': True,
        # 'ROBOTSTXT_OBEY': False,
        # 'AUTOTHROTTLE_ENABLED': True,
        # 'AUTOTHROTTLE_START_DELAY': 1,
        # 'AUTOTHROTTLE_MAX_DELAY': 10,
        # 'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        # 'AUTOTHROTTLE_DEBUG': True,
    }

    def parse(self, response):
        # Extraire les liens de recettes à partir de la page actuelle
        recettes = response.css("#content .mrtn-card__title a")
        
        for recette in recettes:
            lien = response.urljoin(recette.css("::attr(href)").get())
            yield Request(url=lien, callback=self.parse_recipe, meta={'lien': lien})
        
        # Extraire tous les liens de numéros de page
        page_links = response.css('nav.af-pagination a::attr(href)').extract()
        
        # Suivre tous les liens vers les pages suivantes, sauf la page actuelle (en évitant les duplications)
        for page_link in page_links:
            # Scrapy va suivre les liens vers les pages suivantes (par exemple, page 2, page 3, etc.)
            yield Request(url=response.urljoin(page_link), callback=self.parse)
    
    def parse_recipe(self, response):
        # Extraire le titre de la recette et la difficulté
        titre = response.css("div.main-title h1::text").get()
        difficulte = response.css(".recipe-primary__item .icon-difficulty + span::text").get()
        lien = response.meta['lien']
        note = response.css("span.recipe-header__rating-text::text").get()
        temps= response.css(".recipe-primary__item .icon-timer1 + span::text").get()
        prix = response.css(".recipe-primary__item .icon-price + span::text").get()

        yield {
            "lien": lien,
            "titre": titre,
            "difficulte": difficulte,
            "note": note,
            "temps": temps,
            "prix": prix

        }




