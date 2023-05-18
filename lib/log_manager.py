import csv
import json
import os
import requests
from datetime import datetime
from collections import defaultdict
from lib.constants import (
    API_ENDPOINT,
    KEYS_FOR_API,
    DEVICE_NAMES_API_TRACKING
)



class LogManager(object):
    def __init__(self, findmy_files, store_keys, timestamp_key, log_folder,
                 name_keys, name_separator, json_layer_separator, null_str,
                 date_format, no_date_folder):
        self._findmy_files = findmy_files
        self._store_keys = store_keys
        self._timestamp_key = timestamp_key
        self._log_folder = log_folder
        self._name_keys = name_keys
        self._name_separator = name_separator
        self._json_layer_separator = json_layer_separator
        self._null_str = null_str
        self._date_format = date_format
        self._no_date_folder = no_date_folder

        self._latest_log = {}
        self._log_cnt = defaultdict(int)

        self._keys = sorted(list(
            set(self._name_keys).union(set(self._store_keys))))

    def _process_item(self, item):
        item_dict = {}
        for key in self._keys:
            path = key.split(self._json_layer_separator)
            value = item
            for sub_key in path:
                if isinstance(value, dict) and sub_key in value:
                    value = value[sub_key]
                else:
                    value = self._null_str
                    break
            item_dict[key] = value
        return item_dict

    def _get_items_dict(self):
        items_dict = {}
        for file in self._findmy_files:
            try:
                with open(file, 'r') as f:
                    json_data = json.loads(f.read())
                for item in json_data:
                    item = self._process_item(item)
                    name = [item[key] if key in item else self._null_str
                            for key in self._name_keys]
                    name = self._name_separator.join(name)
                    if name in items_dict:
                        raise ValueError(f'{name} already exists!')
                    items_dict[name] = item
            except:
                pass
        if not items_dict:
            raise RuntimeError(f'No devices found. Please check if Full Disk '
                                'Access has been granted to Terminal.')
        return items_dict

    def _save_log(self, name, data):
        log_folder = self._log_folder
        if not self._no_date_folder:
            log_folder = os.path.join(
                log_folder, datetime.now().strftime(self._date_format))
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        path = os.path.join(log_folder, name + '.csv')

        if not os.path.exists(path):
            with open(path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(self._keys)

        with open(path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([data[k] for k in self._keys])

    def refresh_log(self):
        items_dict = self._get_items_dict()
        for name in items_dict:
            if (name not in self._latest_log or
                    self._latest_log[name] != items_dict[name]):
                self._save_log(name, items_dict[name])
                self._latest_log[name] = items_dict[name]
                self._log_cnt[name] += 1
                self.post_data_to_api(items_dict[name])

    def get_latest_log(self):
        return self._latest_log, self._log_cnt

    @staticmethod
    def post_data_to_api(data):
        filtered_data = dict(
            (key, value) for key, value in data.items() if
                             key in KEYS_FOR_API)
        if filtered_data.get('name') in DEVICE_NAMES_API_TRACKING:
            filtered_data['device_id'] = filtered_data.pop('id')
            filtered_data['batteryLevel'] = None if filtered_data.get(
                'batteryLevel') == 'NULL' else filtered_data.get('batteryLevel')
            get_response = requests.post(API_ENDPOINT, json=filtered_data)
            # print('Collecting data... (Use CTRL-C to stop it)')
            # print(get_response.status_code)
            # print(get_response.json())
