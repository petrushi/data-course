SPIDER_MODULES = ['leroyparser.spiders']
NEWSPIDER_MODULE = 'leroyparser.spiders'
USER_AGENT = 'Mozilla/5.0'
ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'ERROR'
LOG_FILE = 'log.txt'
IMAGES_STORE = 'images'
CONCURRENT_REQUESTS = 32
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16
ITEM_PIPELINES = {
   'leroyparser.pipeline.DataBasePipeline': 1,
   'leroyparser.pipeline.LeroyPhotosPipeline': 1,
}
