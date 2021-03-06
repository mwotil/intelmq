# -*- coding: utf-8 -*-
import json
import logging
import sys

from intelmq.lib.bot import CollectorBot
from intelmq.lib.message import Report

try:
    from sdk.blueliv_api import BluelivAPI
except ImportError:
    BluelivAPI = None


class BluelivCrimeserverCollectorBot(CollectorBot):
    def init(self):
        if BluelivAPI is None:
            self.logger.error('Could not import BluelivAPI. Please install it.')
            self.stop()

    def init(self):
        if BluelivAPI is None:
            self.logger.error('Could not import sdk.blueliv_api.BluelivAPI. Please install it.')
            self.stop()

    def process(self):
        self.logger.info("Downloading report through API")
        http_proxy = getattr(self.parameters, 'http_proxy', None)
        https_proxy = getattr(self.parameters, 'http_ssl_proxy', None)
        proxy = None
        if http_proxy and https_proxy:
            proxy = {'http': http_proxy,
                     'https': https_proxy}
        api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                         token=self.parameters.api_key,
                         log_level=logging.INFO,
                         proxy=proxy)

        response = api.crime_servers.online()
        self.logger.info("Report downloaded.")

        report = Report()
        report.add("raw", json.dumps([item for item in response.items]))
        self.send_message(report)


if __name__ == "__main__":
    bot = BluelivCrimeserverCollectorBot(sys.argv[1])
    bot.start()
