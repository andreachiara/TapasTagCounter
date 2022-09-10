from operator import ge
from unittest import result
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

titles_map = {'title' : 'link'}
queer_num = 0
tot_num = 0
filename = 'result_2.tsv'
title_re = re.compile("(?<=Read).*?(?=\| Tapas Web Comics)")




class LinkscrawlItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    attr = scrapy.Field()

class someSpider(CrawlSpider):
  global filename
  with open(filename, 'a') as f:
    f.write('title\tqueer?\tyes/all\t%\ttags\turl\n')
  name = 'linkscrawl'
  item = []

  allowed_domains = ['tapas.io']
  start_urls = ['https://tapas.io/comics?b=ALL&g=0&f=NONE&s=DATE&pageNumber=135&pageSize=20&since=&']

  rules = (Rule (LinkExtractor(allow=(r'tapas.io\/series\/'), deny=('account')), callback="parse_obj", follow=True),
  )

  def parse_obj(self,response):
    global queer_num
    global tot_num
    global filename
    global title_re
    if (response.url[-5:] == '/info'):
      #print(response.status)
      #item = LinkscrawlItem()
      #item["link"] = str(response.url)+":"+str(response.status)
      res_stat = response.status
      status = response.url
      item = response.url
      print(res_stat)
      title_raw = str(response.xpath('//title/text()').get())
      title = ""
      title_allmatch = title_re.search(title_raw)
      if (title_allmatch is None):
        return
      title = title_allmatch.group(0)
      #title = title_raw
      #titles_map.update({str(title) : str(response.url)})
      t_pad = ""

      tot_num += 1
      #tags = str(response.css('info-detail__row'))
      #tags = response.xpath('//a[@class="genre-btn js-fb-tracking"]/a/text()').get()
      tags = response.css('.tags__item *::text').getall()
      genres = response.css('.genre-btn *::text').getall()

      alltags = ""
      allgenres = ""

      for i in range (len(title), 70):
        t_pad += " "

      for tag in tags:
        alltags += tag + ','
      
      for genre in genres:
        alltags += genre + ','

      is_queer = False
      queer_str = "No"
      tags_lower = str(alltags).lower()
      acc_tags = re.compile("queer|bl|gl|yaoi|yuri|boys love|boyslove|boys_love|girls_love|girls love|girlslove|shounenai|shounen ai|shonen ai|shonenai|shonen_ai|shounen_ai|shōnen_ai|shōnen ai|shoujo_ai|shoujo ai|shojo ai|shojoai|shoujoai|shōjoai|shōjo ai|shōjo_ai|girls love|lgbt|lgbtq|lgbtq+|lgbtqai|lgbtqai+|lgbtqia|lgbtqia+|lgbtqa|lgbtqa+|intersexual|intersequality|intersex|asexual|asexuality|pansexual|pansexuality|aromantic|lesbian|gay|bisexual|bisexuality|trans|transgender|nonbinary|enby|ftm|mtf|genderfluid|genderqueer|crossdress|crossdressing|transmasc|transfemme|transfeminine|transmasculine|sexual orientation|gender identity|homosexuality|hrt")
      if (acc_tags.search(tags_lower)):
        is_queer = True
        queer_str = "YESSSSS"
        queer_num += 1

      with open(filename, 'a') as f:
        f.write(str(title) + '\t' + queer_str + '\t' + str(queer_num) + '/' + str (tot_num) + '\t' + str((queer_num/tot_num)*100) + '\t"' + tags_lower + '"\t"' + str(response.url) + '"\n')
      self.log('Saved file %s' % filename)


