import logging
from hcheck import HealthCheck

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s]  %(levelname)8s  line: %(lineno)3s  > %(message)s  ",
                    filename='/var/log/pyhealthcheck.log')

try:
    h = HealthCheck()
    h.run()
except:
    log.exception('Error in healthcheck')
