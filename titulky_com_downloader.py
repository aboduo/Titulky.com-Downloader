#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from urllib import request
from optparse import OptionParser, OptionGroup

# Globals
NAME = 'titulky_com_downloader'
PAGE = 'http://www.titulky.com'


def getLink(url, encoding):

    fd = request.urlopen(url)
    htmlSource = str(fd.read().decode(encoding))
    fd.close()

    pattern = r'''
            <a                               # Tag start
            [\s]+                            # Ignore white chars
            class="titulkydownloadajax"      # Find right html tag
            [\s]+
            href="(?P<addr>[^"]+)"[^>]*      # Find address in href (addr)
            >
            (?P<name>[^<]*)                  # Find name of movie (name)
            </a>                             # Tag end
           '''

    data = re.search(pattern, htmlSource, re.VERBOSE)

    if data:
        link = PAGE + '/' + data.group('addr')
        name = data.group('name')

        fd = request.urlopen(link)
        iframe = str(fd.read().decode(encoding))
        fd.close()

        #pattern = r'<a[\s]+[^h]+href="(?P<addr>[^"]+)"[^>]*>'
        pattern = r'''
                    <a                          # Tag start
                    [\s]+                       # Ignore white chars
                    [^h]+                       # Ignore all other atributes like id, class, etc.
                    href="(?P<addr>[^"]+)"      # Get address of titles
                    [^>]*                       # Ignore other atributes
                    >                           # Tag end
                   '''

        data = re.search(pattern, iframe, re.VERBOSE)

        if data:
            return (PAGE + data.group('addr'))
        else:
          #<img src="./captcha/captcha.php" />
            pattern = r'<img[\s]+src="./captcha/captcha.php"[\s]+/>'
            if re.search(pattern, iframe):
                print('You exhausted your daily limit of downloads')
            else:
                print('Cannot find data on page')


            sys.exit(1)

    else:
        print('Cannot find data on page')
        sys.exit(1)


def main():

    # Parsing Options & Args
    parser = OptionParser(description = '%prog Download subtitles from titulky.com',
                          usage = '%prog [options]',
                          epilog = 'Support: Otto Sabart (www.seberm.com / seberm@gmail.com)')

    options = OptionGroup(parser, "Program Options", "Options specific to titulky_com_downloader.")
    
    options.add_option('-l', '--link', dest='link', action='store_true', help='Prints download link on stdout')
    options.add_option('-e', '--encoding', dest='encoding', action='store', metavar='<encoding>', default='cp1250', help='Sets webpage encoding default [cp1250]')
    #options.add_option('-d', '--download', action='callback', callback=downloadTitles, help='Download subtitles')

    parser.add_option_group(options)

    (opt, args) = parser.parse_args()

    if args[0:]:
        # @todo Check the URL format
        url = args[0]
    else:
        # @todo In the future will be possible to read from stdin,
        #       Now it's an error
        print('You have to provide an URL address!')
        sys.exit(1)

    if opt.link:
            print(getLink(url, opt.encoding))




if __name__ == '__main__':
    main()
