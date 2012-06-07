Scrapy for Google Places
========================

This doesn't work whatsoever. Well, that's a lie.  It actually works, for the first page.

However, for subsequent pages, it does not.

### Here's how you run it from the command line

First, set up the Email and Passwd with your google credentials.

Then:

`scrapy crawl google-login -o items.json -t json`