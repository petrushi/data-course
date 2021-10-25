SPIDER_MODULES = ['leroyparser.spiders']
NEWSPIDER_MODULE = 'leroyparser.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'NOTSET'  #INFO ERROR
LOG_FILE = 'log.txt'
IMAGES_STORE = 'images'
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8
ITEM_PIPELINES = {
   'leroyparser.pipeline.DataBasePipeline': 1,
   'leroyparser.pipeline.LeroyPhotosPipeline': 1,
}
