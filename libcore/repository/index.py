#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os

import requests
import json

from self import self

from libcore.config.config import Config
from libcore.exception.config_key_not_exist_exception import ConfigKeyNotExistException
from libcore.exception.indexer_init_failed_exception import IndexerInitFailedException
from libcore.exception.not_support_repository_indexer_exception import NotSupportRepositoryIndexerException
from libcore.until.string_util import StringUtil
from libcore.cache.cache import Cache
from libcore.exception.app_file_no_exist import AppFileNoExist


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
    # __repo_index = "C:\Users\Administrator\PycharmProjects\jergt\jergt-repo"
    __app = "/apps/"
    __versions = "/versions/"
    __version_json = ".json"

    # TODO Getter/Setter

    def get_publisher(self) -> list:
        return self.__publisher

    def set_publisher(self, publisher: str):
        self.__publisher = publisher

    # def set_publisher(self, repo_name: str = __app):
    # if repo_name is None:
    #     path = self.__repo_index + self.__app
    #     publisher = os.listdir(path)
    #     self.__publisher = publisher
    # else:
    #     try:
    #         path = self.__repo_index + repo_name
    #         publisher = os.listdir(path)
    #         self.__publisher = publisher
    #     except NotSupportRepositoryIndexerException as e:
    #         print(e)

    def get_version(self) -> str:
        # version = "version:{}".format(self.__version)
        # print(version)
        return self.__version

    def set_version(self, version: str):
        self.__version = version

    # def set_version(self, publisher: str):
    #     version = self.__index_html + self.__app + publisher + self.__index_json
    #     self.__version = version

    def get_os(self) -> str:
        return self.__os

    def set_os(self, os: str):
        self.__os = os

    # def set_os(self, publisher: str, version: str):
    #     self.__file = self.__index_html + self.__app + publisher + self.__versions + version + self.__version_json
    #     response = requests.get(self.__file)
    #     if response.status_code != 200:
    #         return None
    #     json_response = response.json()  # ????????????json?????????json?????????(?????????App?????????)
    #     index_os = json_response["os"]
    #     self.__os = index_os

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

    def set_file(self, filename: str | None):  # JDK????????????   ,file?????????????????????jdk-oracle-17.0.5-20221214-225037.zip
        path = Cache.init__system_type(self)
        file = path + filename + self.__index_json
        if StringUtil.is_empty(filename):
            raise AppFileNoExist
        if filename is None:
            file = "{index_html}/apps/{publisher}/versions/{version}{app_json}".format(index_html=self.__index_html,
                                                                                       publisher=self.__publisher,
                                                                                       version=self.__version,
                                                                                       app_json=self.__index_json)
            response = requests.get(file)
            if response.status_code != 200:
                return None
            json_response = response.json()
            file = json_response["file"]
            if StringUtil.is_empty(filename):
                return None
            self.__file = file  # ??????????????????filename???????????????????????????publisher???version
            # TODO ???????????????file?????????jdk??????????????????????????????????????????

        else:
            listfile = file.split("-", 3)
            publisher1 = listfile[1:2]
            _publisher = "".join(publisher1).strip()  # ????????????+????????????(?????????)

            version1 = listfile[2:3]
            _version = "".join(version1).strip()  # ?????????

            time_dist1 = listfile[3:4]
            _time_dist = ".".join(time_dist1)  # ???????????????

            time1 = _time_dist[0:1]
            _time = "".join(time1).strip()  # ??????????????????

            dist1 = _time_dist[1:2]
            _dist = "".join(dist1).strip()  # ????????????

            file = "{index_html}/apps/{publisher}/versions/{version}{app_json}".format(index_html=self.__index_html,
                                                                                       publisher=_publisher,
                                                                                       version=_version,
                                                                                       app_json=self.__index_json)
            response = requests.get(file)
            if response.status_code != 200:
                return None
            json_response = response.json()
            file = json_response["file"]
            if StringUtil.is_empty(filename):
                return None
            self.__file = file
            # TODO ???????????????file?????????jdk??????????????????????????????????????????

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
    ???????????? Github ??????????????????????????? Index ?????? ???JSON??????
    """
    __index_json = "/index.json"
    __mirror_url = ""

    def __init__(self, config: Config = None):
        """
         # TODO ?????????????????????????????????????????????
        :param config:
        """
        try:
            mirror = config.get("mirror")  # ?????????????????????
            # TODO ???????????? http://mirrors.jlab.io:9900 ???http://mirrors.jlab.io:9900/
            self.__mirror_url = mirror + self.__index_json
        except ConfigKeyNotExistException as e:
            raise IndexerInitFailedException("Can not read mirror from config file, because :{}".format(e))

    def get_version(self) -> str | None:
        response = requests.get(self.__mirror_url)  # ???????????????????????????response?????????
        if response.status_code != 200:
            return None
        json_response = response.json()  # ????????????json?????????json?????????(?????????App?????????)
        index_version = json_response["version"]  # ??????json???App?????????version??????
        if StringUtil.is_empty(index_version):
            return None
        return index_version.strip()

    def get_name(self) -> str:  # jdk-<??????>-<??????>-<??????-??????>.zip
        response = requests.get(self.__mirror_url)
        if response.status_code != 200:
            return ""
        json_response = response.json()
        index_name = json_response["name"]
        if StringUtil.is_empty(index_name):
            return ""
        return index_name.strip()

    def get_publisher(self) -> str | None:
        response = requests.get(self.__mirror_url)  # ???????????????????????????response?????????
        if response.status_code != 200:
            return None
        json_response = response.json()  # ????????????json?????????json?????????(?????????App?????????)
        index_publisher = json_response["publisher"]  # ??????json???App?????????publisher??????
        if StringUtil.is_empty(index_publisher):
            return None
        return index_publisher.strip()

    def get_update_time(self) -> str | None:
        response = requests.get(self.__mirror_url)  # ???????????????????????????response?????????
        if response.status_code != 200:
            return None
        json_response = response.json()  # ????????????json?????????json?????????(?????????App?????????)
        index_update_time = json_response["update-time"]  # ??????json???App?????????publisher??????
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
