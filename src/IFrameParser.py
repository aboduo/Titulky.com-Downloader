from logging import debug, info, error, warning, exception
from datetime import datetime

from threading import Thread

titlesLinks = []

class IFrameParser(Thread):

    def __init__(self, opener, url, name, encoding, lock):
        self.__opener = opener
        self.__url = url
        self.__name = name
        self.__encoding = encoding
        self.__lock = lock

        Thread.__init__(self)


    def run(self):
        debug('[%s]: Running new IFrameParser thread (%s)' % (self.__name, self.__url))
         
        try:
            fd = self.__opener.open(self.__url)
            iframe = str(fd.read().decode(self.__encoding))
        except urllib.error.URLError as e:
            error('[%s]: URL error: %s' % (self.__name, e.reason))
        except IOError:
            error('[%s]: IO Error - thread exiting' % self.__name)
            fd.close()
            sys.exit(1)

        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        debug('[%s]: Parsing iframe ...' % self.__name)

        data = re.search(pattern, iframe, re.VERBOSE)

        if data:
            debug('[%s]: Found link: %s' % (self.__name, PAGE + data.group('addr')))
            self.lock.acquire()
            titlesLinks.append({'name' : self.__name, 'url' : PAGE + data.group('addr'), 'wait' : datetime.now().hour})
            self.lock.release()
        else:
            debug('[%s]: No links found' % self.__name)
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                warning('[%s]: You exhausted your free daily limit of downloads - it\'s necessary to re-type captcha code' % self.__name)
            else:
                info('[%s]: Cannot find data on page' % self.__name)
