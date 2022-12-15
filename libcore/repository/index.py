#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

import requests
import json

from self import self

from libcore.config.config import Config
from libcore.exception.config_key_not_exist_exception import ConfigKeyNotExistException
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.until.string_util import StringUtil
from libcore.cache.cache import Cache


class App:
    __publisher = None
    __version = None
    __os = None
    __arch = None
    __dist = None
    __checksum_algo = None
    __checksum_content = None
    __file = None
    __path = None

    __index_json = "/index.json"
    __index_html = "http://192.168.3.20:9900"
    __app = "/apps/"
    __versions = "/versions/"
    __version_json = ".json"

    # TODO Getter/Setter

    def get_publisher(self) -> str:
        return self.__publisher

    def set_publisher(self, repo_name: str = __app):
        if repo_name is None:
            publisher = self.__index_html + self.__app
            self.__publisher = publisher
        else:
            publisher = self.__index_html + repo_name
            self.__publisher = publisher

    def get_version(self) -> str:
        return self.__version

    def set_version(self, publisher: str):
        version = self.__index_html + self.__app + publisher + self.__index_json
        self.__version = version

    def get_os(self) -> str:
        return self.__os

    def set_os(self, publisher: str, version: str):
        self.__file = self.__index_html + self.__app + publisher + self.__versions + version + self.__version_json
        response = requests.get(self.__file)
        if response.status_code != 200:
            return None
        json_response = response.json()  # 请求获取json，返回json的内容(也就是App的内容)
        index_os = json_response["os"]
        self.__os = index_os

    def get_arch(self) -> str:
        return self.__arch

    def set_arch(self, arch: str):
        self.__arch = arch

    def get_dist(self) -> str:
        return self.__dist

    def set_dist(self, dist: str):
        self.__dist = dist

    def get_checksum_algo(self) -> str:
        return self.__checksum_algo

    def set_checksum_algo(self, checksum_algo: str):
        self.__checksum_algo = checksum_algo

    def get_checksum_content(self) -> str:
        return self.__checksum_content

    def set_checksum_content(self, checksum_content: str):
        self.__checksum_content = checksum_content

    def get_file(self) -> str:
        return self.__file

    def set_file(self, file: str = None):  # JDK下载地址   ,file是文件名例如：jdk-oracle-17.0.5-20221214-225037.zip
        pass
        # path = Cache.init__system_type(self)
        # file = path + filename + self.__index_json
        # if StringUtil.is_empty(file):
        #     raise
        #
        # if file is None:
        #     file = "{app_html}/apps/{publisher}/versions/{version}{app_json}".format(app_html=self.__index_html,
        #                                                                              publisher=self.__publisher,
        #                                                                              version=self.__version,
        #                                                                              app_json=self.__app_json)
        #     response = requests.get(file)
        #     if response.status_code != 200:
        #         return None
        #     json_response = response.json()
        #     file = json_response["file"]
        #     if StringUtil.is_empty(file):
        #         return None
        #     self.__file = file
        #     if
        #     file.split("-", 3)

    def __init__(self):
        self.__index_json = None
        self.__index_html = None
        self.json_file = None
        self.__publisher = None
        self.__version = None
        self.__os = None
        self.__arch = None
        self.__dist = None
        self.__checksum_algo = None
        self.__checksum_content = None
        self.__file = None


class Index:
    """
    用于访问 Github 存储库或者镜像源的 Index 文件 （JSON）。
    """
    __index_json = "/index.json"
    __mirror_url = ""

    def __init__(self, config: Config = None):
        """
         # TODO 根据环境变量配置文件读取镜像源
        :param config:
        """
        try:
            mirror = config.get("mirror")  # 获取的文件路径
            # TODO 处理兼容 http://mirrors.jlab.io:9900 和http://mirrors.jlab.io:9900/
            self.__mirror_url = mirror + self.__index_json
        except ConfigKeyNotExistException as e:
            raise IndexerInitFailedException("Can not read mirror from config file, because :{}".format(e))

    def get_version(self) -> str | None:
        response = requests.get(self.__mirror_url)  # 请求该路径的信息，response是回应
        if response.status_code != 200:
            return None
        json_response = response.json()  # 请求获取json，返回json的内容(也就是App的内容)
        index_version = json_response["version"]  # 获取json（App）中的version内容
        if StringUtil.is_empty(index_version):
            return None
        return index_version.strip()

    def get_name(self) -> str:  # jdk-<版本>-<厂商>-<日期-时间>.zip
        response = requests.get(self.__mirror_url)
        if response.status_code != 200:
            return ""
        json_response = response.json()
        index_name = json_response["name"]
        if StringUtil.is_empty(index_name):
            return ""
        return index_name.strip()

    def get_publisher(self) -> str | None:
        response = requests.get(self.__mirror_url)  # 请求该路径的信息，response是回应
        if response.status_code != 200:
            return None
        json_response = response.json()  # 请求获取json，返回json的内容(也就是App的内容)
        index_publisher = json_response["publisher"]  # 获取json（App）中的publisher内容
        if StringUtil.is_empty(index_publisher):
            return None
        return index_publisher.strip()

    def get_update_time(self) -> str | None:
        response = requests.get(self.__mirror_url)  # 请求该路径的信息，response是回应
        if response.status_code != 200:
            return None
        json_response = response.json()  # 请求获取json，返回json的内容(也就是App的内容)
        index_update_time = json_response["update-time"]  # 获取json（App）中的publisher内容
        if StringUtil.is_empty(index_update_time):
            return None
        return index_update_time.strip()

    def get_app_versions_by_publisher(self, publisher: str) -> list:
        app = "/apps/"
        version_url = self.__mirror_url + app + publisher
        version_list = os.listdir(version_url)
        return version_list

    def get_app(self, publisher: str, version: str):
        pass


if __name__ == "__main__":
    pass
