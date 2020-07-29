import subprocess
import sys
import os
import threading
import logging
import time
import re
import json

from typing import List, Text


log = logging.getLogger(__name__)


class HealthCheck:
    DEFAULT_CONF_PATH = ['./services.conf', '/etc/services.conf']

    def __init__(self, *args,  config=None, start_on_stop=True,  **kwargs):

        if config is None:
            self.config = self._get_default_config()
        else:
            self.config = config
        self.start_on_stop = start_on_stop

    def _get_default_config(self) -> Text:
        """Check the first available path for service config and returns it

        Returns
        -------
        Text
            return path of config
        """
        for pth in self.DEFAULT_CONF_PATH:
            if os.path.exists(os.path.abspath(pth)):
                return os.path.abspath(pth)

    def _parse_service_config(self) -> List:
        """get service name from each line of the config file and 
        returns it as a list

        Returns
        -------
        List
            List of services to be checked
        """

        with open(self.config) as fh:
            service_names = fh.readlines()

        service_names = filter(lambda x: x,  map(
            lambda x: x.replace('\n', ''), service_names))
        return service_names

    def run(self) -> None:
        """starts the healthcheck method for each service in seperate thread and 
        check for status 
        """
        services = self._parse_service_config()
        runnable_services = filter(lambda x: not x.startswith("#"), services)

        for service in runnable_services:
            threading.Thread(target=self.healthcheck,
                             name=f'{service}-status',
                             args=(service,),
                             daemon=False).start()

    def healthcheck(self, service):
        srv = Service(service)
        srv.status_humanized()
        if srv.status1 == 'active':
            log.info(
                f'{{ {srv.service} }} running with pid {srv.pid} and process: {srv.parent_app}')
        elif srv.status1 == 'inactive' or srv.status1 == 'failed':
            log.warning(f'{{ {srv.service} }} is not running')
            if self.start_on_stop:
                srv.restart()
                srv.status_humanized()
                log.info(
                    f'{{ {srv.service} }} running with pid {srv.pid} and process: {srv.parent_app}')
            else:
                log.critical(
                    f'{{ {srv.service} }} is stopped and is not restarted')


class Service:
    STATUS_EXP = r'^Active: (?P<status>\w+) \((?P<status2>.+?)\)(?: since (?P<started>.+?); (?P<started2>.*))?'
    PROCESS_EXP = r'(?P<pid>\d+) \((?P<parent>[\w-]+)\)'

    def __init__(self, service):
        self._status_result = None
        self.service = service
        self.pid = None
        self.parent_app = None
        self.status1 = None
        self.status2 = None

        self.started = None
        self.started_ago = None

        self.fullname = ""
        self.description = ""

        self.info = {}

    def _infer_type(self):
        raise NotImplementedError('to be implemented')


    @staticmethod
    def process_runner(cmd):
        process = subprocess.Popen(cmd, shell=True, stdin=None,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        result = process.communicate()
        return map(lambda x: x.decode().strip(), result)

    def restart(self):
        log.info(f'Restarting service {self.service}')

        cmd = f'systemctl restart {self.service}'
        out, err = self.process_runner(cmd)

        # log.info(f'{out} :: {err}')

    def start(self):
        log.info(f'Starting service {self.service}')

        cmd = f'systemctl start {self.service}'
        out, err = self.process_runner(cmd)

        # log.info(f'{out} :: {err}')

    def stop(self):
        log.info(f'Stopping service {self.service}')

        cmd = f'systemctl stop {self.service}'
        out, err = self.process_runner(cmd)

        # log.info(f'{out} :: {err}')

    def status(self):
        log.info(f'Checking service {{ {self.service} }} status')

        cmd = f'systemctl status {self.service}'
        out, err = self.process_runner(cmd)
        self._status_result = out
        self._status_err = err

    def status_humanized(self):
        # getting status from shell
        self.status()

        # checking for err
        if self._status_err:
            log.error(f'{self._status_err}')
            return

        # converting to list of lines
        res_list = list(
            map(lambda x: x.strip(), self._status_result.split('\n')))
        # log.info(json.dumps(res_list, indent=2, default=str))

        # checking first line for name and description
        first_line = res_list.pop(0)
        self.fullname, self.description = first_line.replace(
            '\u25cf ', '').split(' - ')

        # parsing remaining lines for other infos
        for line in res_list:
            if line.startswith('Active: '):
                r = re.findall(self.STATUS_EXP, line)
                log.debug(r)
                self.status1 = r[0][0]
                self.status2 = r[0][1]
                self.started = r[0][2]
                self.started_ago = r[0][3]
            elif line.startswith('Main PID:'):
                if self.status1 == 'active':
                    self.pid, self.parent_app = re.findall(
                        self.PROCESS_EXP, line.split(': ')[1])[0]

    def get_service_type(self):
        raise NotImplementedError('code not written')
