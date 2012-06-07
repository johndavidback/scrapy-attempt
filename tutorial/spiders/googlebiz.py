__author__ = 'john.back'

from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import FormRequest, Request
from scrapy.selector import HtmlXPathSelector
from tutorial.items import GoogleItem

# This is the class that does work.
class LoginSpider(BaseSpider):
    name = 'google-login'

    # Need to put some details here.
    start_urls = ['']

    def parse(self, response):
        """
        This overrides the builtin function parse() and forces us to login
        to the google service.
        """
        return [FormRequest.from_response(response,
                formdata={'Email': 'need email', 'Passwd': 'need password'},
                callback = self.after_login)]

    def after_login(self, response):
        """
        This is the callback from the login function and does the
        actual parsing
        """

        print 'STARTING AFTER LOGIN'

        print response

        # Display the body in the console
        # print response.body

        # Create an xpath selector
        hxs = HtmlXPathSelector(response)

        # Container for item objects
        items = []
        all_next_links = []

        # Get all of the links to the next pages
        links = hxs.select('//a[contains(@href, "/local/add/analytics?storeid=")]')

        # Go through all of the links on the analytics page
        for l in links:

            # Create a new google item
            item = GoogleItem()

            # Assign the values
            item['link'] = l.select('@href').extract()
            item['value'] = l.select('text()').extract()
            item['next_link'] = ''

            if item['value']:
                try:
                    pass
                except:
                    pass

            # print u'%s : %s' % (item['link'], item['value'])

            items.append(item)

        # This plucks the 'Next >>' links from the site
        next_links = hxs.select('//a[contains(text(), "Next")]')
        the_next_link = None
        for n in next_links:
            item = GoogleItem()

            item['link'] = n.select('@href').extract()
            item['value'] = n.select('text()').extract()
            item['next_link'] = n.select('@href').extract()

            the_next_link = u'http://google.com%s' % item['next_link'][0]

            # print u'going to next link %s' % item['next_link']

            items.append(item)

        return items


        # Let's get the next link
        if the_next_link:
            print 'Going to the next link %s' % the_next_link
            next_items = [Request(the_next_link, callback=self.parse)]
        else:
            return []

        return items + next_items


    def parse_next_link(self, response):

        print 'THIS IS THE RESPONSE'
        print response


# This is the class that does not work
class GoogleSpider(CrawlSpider):
    name = 'google-spider'
    allowed_domains = ['google.com']
    logged_in = False

    start_urls = [
        ''
    ]

    rules = (

        Rule(SgmlLinkExtractor(allow=('/local/add/businessCenter?page=', )), callback='parse_items'),
    )


#    def init_request(self):
#        """
#        This is called initially
#        """
#        return self.login()

    def login(self, response):
        """
        This is where I am stuck.  Obviously response is not defined.
        """
        return [FormRequest.from_response(response,
            formdata={'Email': '', 'Passwd': ''},
            callback = self.after_login)]


    def after_login(self):
        """
        Required for the crawler to start crawling
        """
        self.initialized()


    def parse_items(self, response):

        if not self.logged_in:
            login(response)


        print response.body

        hxs = HtmlXPathSelector(response)

        items = []
        # Get all of the links to the next pages
        links = hxs.select('//a[contains(@href, "/local/add/analytics?storeid=")]')

        for l in links:
            item = GoogleItem()

            item['link'] = l.select('@href').extract()
            item['value'] = l.select('text()').extract()
            item['next_link'] = ''

            items.append(item)

        next_links = hxs.select('//a[contains(text(), "Next")]')
        for n in next_links:
            item = GoogleItem()

            item['link'] = n.select('@href').extract()
            item['value'] = n.select('text()').extract()
            item['next_link'] = n.select('@href').extract()

            items.append(item)

        return items