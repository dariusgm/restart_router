import json
import os
from time import sleep

import falcon
import pychrome


class Restart:
    def onContent(self, **kwargs) -> None:
        if self.current_page == 'login':
            print("Logging in")
            # set Password
            self.tab.Runtime.evaluate(expression=self.__set_password(self.router_password), returnByValue=False,
                                      awaitPromise=False)
            sleep(1)

            # trigger login
            self.tab.Runtime.evaluate(expression=self.__trigger_login(), returnByValue=False, awaitPromise=False)

            sleep(1)

            self.current_page = 'restart'
            return
        elif self.current_page == 'restart':
            print("Restarting")
            # Visit restart page
            self.tab.Page.navigate(url="http://{}/?status_restart&mid=StatusRestart".format(self.router_ip))

            sleep(1)
            # trigger restart popup
            self.tab.Runtime.evaluate(expression=self.__trigger_restart_popup(), returnByValue=False, awaitPromise=False)
            sleep(1)

            self.current_page = 'restarting'
            self.tab.Runtime.evaluate(expression=self._trigger_restart(), returnByValue=False, awaitPromise=False)
            return

    def execute(self):
        self.browser = pychrome.Browser(url=self.chromium_url)

        self.tab = self.browser.new_tab()
        self.tab.start()
        self.tab.Page.enable()
        self.tab.Runtime.enable()

        # Install Callback
        self.tab.Page.domContentEventFired = self.onContent

        # get on router
        self.tab.Page.navigate(url="http://{}".format(self.router_ip), _timeout=15)

        # Wait here very long, as the callback will do the real work
        self.tab.wait(15)

        # closing everything
        self.tab.stop()
        self.browser.close_tab(self.tab)

    def __init__(self, router_ip, router_password, chromium_url):
        self.router_ip = router_ip
        self.router_password = router_password
        self.current_page = 'login'
        self.chromium_url = chromium_url
        self.browser = None
        self.tab = None

    def __set_password(self, router_password: str) -> str:
        return "document.getElementById('Password').value = \"{}\"".format(router_password)

    def __trigger_login(self):
        return "document.getElementById('LoginBtn').click()"

    def __trigger_restart_popup(self):
        return "document.getElementById('PAGE_RESTART_RESTART').click()"

    def _trigger_restart(self):
        return "document.getElementById('PAGE_RESTART_POPUP_APPLY').click()"


class RestartRouterResponse:
    def on_get(self, req, resp):
        """Handles GET requests"""
        try:
            router_ip = os.environ.get('IP', '192.168.0.1')
            router_password = os.environ.get('PASSWORD')

            # using localhost for non-docker development
            chromium_url = os.environ.get('CHROMIUM_URL', '127.0.0.1:9200')

            restart = Restart(router_ip, router_password, chromium_url)
            restart.execute()

            resp.body = json.dumps(dict(finished=True))
        except Exception as e:
            resp.body = json.dumps(dict(error=e))


api = falcon.API()
api.add_route('/restart', RestartRouterResponse())
