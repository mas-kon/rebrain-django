import psutil
import os
import sys
from psutil._common import bytes2human
import socket
import time
import logging
import json
import requests
from requests.exceptions import HTTPError

logging.basicConfig(filename='log_file.log',
                    encoding='utf-8',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.INFO)

http_headers = {'Content-Type': 'application/json; charset=utf-8'}


def log_write(log_message, log_level):
    if log_level == 'info':
        logging.info("%s", log_message)
    elif log_level == 'warn':
        logging.warning("%s", log_message)
    elif log_level == 'error':
        logging.error("%s", log_message)
    else:
        logging.critical('UNKNOWN ERROR')


def make_request(http_method, url, data, header):
    response = ''
    try:
        if http_method == 'get':
            response = requests.get(url, headers=header)
            response.raise_for_status()
        elif http_method == 'post':
            response = requests.post(url, data=data, headers=header)
            response.raise_for_status()
        elif http_method == 'put':
            response = requests.put(url, data=data, headers=header)
            response.raise_for_status()
        else:
            log_write(f'Wrong http request method.', 'error')
    except HTTPError as http_err:
        log_write(
            f"Server response: text- {response.text}, status code - {response.status_code}, reason - {response.reason}",
            'error')
        log_write(f'HTTP error occurred: {http_err}', 'error')
    except Exception as err:
        log_write(f'Other error occurred: {err}', 'error')
    else:
        return_value = {'data': response.text, 'status': response.status_code, 'reason': response.reason}
        return return_value


class PcClient:
    def __init__(self, pc_hostname):
        self.name = pc_hostname
        self.net_list = {}
        self.disk_list = {}
        self.cpu_info = {}
        self.load_avg = {}
        self.memory_info = {}
        self.hostname_info = {}

    def fill_disk_list(self):
        i = 0
        for part in psutil.disk_partitions(all=False):
            name_disk = 'disk' + str(i)
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            self.disk_list[name_disk] = {
                'device': part.device,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'fstype': part.fstype,
                'mountpoint': part.mountpoint
            }
            i += 1

        disk_l = []
        for key in self.disk_list:
            disk_l.append(self.disk_list[key])

        return disk_l

    def fill_network_list(self):
        af_map = {
            socket.AF_INET: 'IPv4',
            socket.AF_INET6: 'IPv6',
            psutil.AF_LINK: 'MAC',
        }

        duplex_map = {
            psutil.NIC_DUPLEX_FULL: "full",
            psutil.NIC_DUPLEX_HALF: "half",
            psutil.NIC_DUPLEX_UNKNOWN: "?",
        }

        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True)
        for nic, addrs in psutil.net_if_addrs().items():
            st = stats[nic]

            if st.isup:
                io = io_counters[nic]
                self.net_list[nic] = {
                    'net_adapter_device': nic,
                    'net_adapter_status': st.isup,
                    'net_adapter_mtu': st.mtu,
                    'net_adapter_speed': st.speed,
                    'net_adapter_duplex': duplex_map[st.duplex],
                    'net_adapter_bytes_send': io.bytes_sent,
                    'net_adapter_bytes_recv': io.bytes_recv,
                    'net_adapter_errs_in': io.errin,
                    'net_adapter_drops_in': io.dropin,
                    'net_adapter_errs_out': io.errout,
                    'net_adapter_drops_out': io.dropout,
                }
                for addr in addrs:
                    self.net_list[nic][af_map.get(addr.family, addr.family)] = addr.address

        net_l = []
        for key in self.net_list:
            net_l.append(self.net_list[key])

        return net_l

    def fill_cpu(self):
        self.cpu_info = {'cpu_cores': psutil.cpu_count(),
                         'cpu_physical_cores': psutil.cpu_count(logical=False),
                         'cpu_frequency_current': int(psutil.cpu_freq().current),
                         'cpu_frequency_max': int(psutil.cpu_freq().max)}
        return self.cpu_info

    def fill_load_average(self):
        self.load_avg = {'1min': psutil.getloadavg()[0], '5min': psutil.getloadavg()[1],
                         '15min': psutil.getloadavg()[2]}
        return self.load_avg

    def fill_memory(self):
        self.memory_info = {'memory_total': bytes2human(psutil.virtual_memory().total),
                            'memory_used': bytes2human(psutil.virtual_memory().used),
                            'memory_percent': int(psutil.virtual_memory().percent)}
        return self.memory_info

    def fill_hostinfo(self):
        try:
            descr = os.environ['DESC']
            self.hostname_info['description'] = descr
        except KeyError:
            os.environ['DESC'] = 'Description of ' + self.name
            self.hostname_info['description'] = os.environ['DESC']
        self.hostname_info['hostname'] = self.name
        # try:
        #     my_ip_addr = requests.get('http://eth0.me').text.replace('\n', '')
        # except requests.exceptions.ConnectionError:
        #     log_write('Error obtain external IP address.', 'error')
        #     my_ip_addr = '127.0.0.1'
        my_ip_addr = make_request('get', 'http://eth0.me', '', http_headers)
        if not my_ip_addr:
            self.hostname_info['external_ip'] = '127.0.0.1'
        else:
            self.hostname_info['external_ip'] = my_ip_addr['data'].replace('\n', '')
        return self.hostname_info

    def __call__(self):
        self.cpu_dict = self.fill_cpu()

        self.disk_dict = self.fill_disk_list()

        self.load_avg_dict = self.fill_load_average()

        self.memory_dict = self.fill_memory()

        self.network_dict = self.fill_network_list()

        self.hostname_dict = self.fill_hostinfo()

        # self.summary_info = {'hostinformation': self.hostname_dict,
        #                      'memory': self.memory_dict,
        #                      'cpu': self.cpu_dict,
        #                      'load_average': self.load_avg_dict,
        #                      'disk': self.disk_dict,
        #                      'network': self.network_dict}

        self.summary_info = {'description': self.hostname_dict['description'],
                             'name': self.hostname_dict['hostname'],
                             'ip_address': self.hostname_dict['external_ip'],
                             'memory_total': self.memory_dict['memory_total'],
                             'memory_used': self.memory_dict['memory_used'],
                             'memory_percent': self.memory_dict['memory_percent'],
                             'cpu_cores': self.cpu_dict['cpu_cores'],
                             'cpu_physical_cores': self.cpu_dict['cpu_physical_cores'],
                             'cpu_frequency_current': self.cpu_dict['cpu_frequency_current'],
                             'cpu_frequency_max': self.cpu_dict['cpu_frequency_max'],
                             'load_average_1min': self.load_avg_dict['1min'],
                             'load_average_5min': self.load_avg_dict['5min'],
                             'load_average_15min': self.load_avg_dict['15min'],
                             'client_is_active': True,
                             'disks': self.disk_dict,
                             'net_adapter': self.network_dict
                             }

        # print(self.cpu_dict)
        # print(self.hostname_dict)
        # print(self.network_dict)
        # print(self.load_avg_dict)
        # print(self.memory_dict)
        # print(self.disk_dict)
        # print(self.summary_info)
        return self.summary_info


def main():
    host = socket.gethostname().split('.')[0]
    registration_id = 0
    log_write('Starting program', 'info')
    current_pc = PcClient(host)
    inf = current_pc()
    log_write(inf, 'info')

    while True:
        inf = current_pc()
        # print(json.dumps(inf, indent = 4, ensure_ascii=False))
        enc_json = json.JSONEncoder().encode(inf)
        server_url_add = 'http://127.0.0.1:8000/api/clients/add'
        server_url_update = 'http://127.0.0.1:8000/api/clients/' + str(registration_id)
        if registration_id == 0:
            req_add = make_request('post', server_url_add, enc_json, http_headers)
            if req_add:
                if req_add['reason'] == 'Created':
                    decrypt_json = json.JSONDecoder().decode(req_add['data'])
                    registration_id = decrypt_json['id']
                    log_write(
                        f"Connection to {server_url_add} for {inf['name']} with ID {registration_id} was successfully.",
                        'info')
            else:
                log_write(f"Can\'t add record for {inf['name']}. See above.", 'error')
                break
        else:
            req_update = make_request('put', server_url_update, enc_json, http_headers)
            if req_update:
                log_write(f"Update information about {inf['name']} ID {registration_id} was successfully.", 'info')
                if req_update['reason'] != 'OK':
                    log_write(
                        f"Can\'t update record for {inf['name']} with ID {registration_id}. Reason - {req_update['reason']}",
                        'error')
                    break
            else:
                log_write('Что-то пошло не так.', 'error')
                break

        time.sleep(30)


if __name__ == '__main__':
    sys.exit(main())
