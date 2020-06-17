# -*- coding:utf-8 -*-
import os
import time
import random
import yaml


def load_config(filename):
    with open(filename, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as e:
            print(e)
            raise

    return config


if __name__ == "__main__":
    ''''''
    from pprint import pprint

    res = load_config('test-acc.yaml')
    pprint(res)
