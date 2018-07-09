import scrapy


class HospitalsSpider(scrapy.Spider):
    name = "hospitals"

    def start_requests(self):
        urls = [
            'https://texashealthemergencyroom.com/locations'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'hospital-%s.html' % page
        # get all the content with <section class="metro_location">
        divs = response.xpath('//section[@class="metro_location"]')
        for item in divs: 
            name, address, city, state, zipcode = "", "", "", "", ""
            # for each <section class="metro_location">
            # get the text inside <h4></h4> from <div class="metro_info">
            # since name is separated with two lines, so we need to concatenate them
            for name_text in item.xpath('.//div[@class="metro_info"]//h4/text()'): 
                name += name_text.extract() + " " 
            # get the text inside <p></p> from <div class="address">
            for line_num, addr_text in enumerate(item.xpath('.//div[@class="address"]//p/text()')):
                if line_num == 0:
                    address = addr_text.extract() # 1105 North Central Expy
                elif line_num == 1:
                    addr_str = addr_text.extract() # Allen, TX 75013
                    addr_lst = addr_str.split(',')
                    city = addr_lst[0]
                    state = addr_lst[1].split()[0]
                    zipcode = addr_lst[1].split()[1]
            # use strip() to remove all leading and trailing white space
            yield {
                'name' : name.strip(),
                'address' : address.strip(),
                'city' : city.strip(),
                'state' : state.strip(),
                'zipcode' : zipcode.strip()
            }