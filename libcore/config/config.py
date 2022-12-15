#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform  # 获取操作系统的信息
import getpass  # getuser返回登录用户名, getpass读取当前用户密码
import configparser  # 获取section 例如：[mysql]，然后还有key，value的内容

from libcore.exception.config_key_not_exist_exception import ConfigKeyNotExistException
from libcore.until.string_util import StringUtil
from libcore.exception.not_support_system_type_exception import NotSupportSystemTypeException
from libcore.exception.get_system_info_exception import GetSystemInfoException
from libcore.exception.config_file_parse_failed_exception import ConfigFileParseFailedException
from libcore.exception.key_value_not_in_range import KeyValueNotInRange

@staticmethod
class Config:
    """
    配置
    """


    __default_publisher_value = (
        'oracle',
        'aws'
    )

    __default_lang_value = (
        'en_US',
        'en_UK'
    )

    __default_mirror_value = (
        'ali',
        'tingshua'
    )

    __default_mirror = None
    __default_lang = "en_US"
    __default_publisher = "Oracle"

    __config = None

    __config_file_windows_tpl = "{system_root}\\Users\\{username}\\AppData\\Local\\jergt\\config\\.jergt-config.ini"
    __config_file_osx_tpl = "/Users/{username/.jergt/config/.jergt-config.ini}"
    __config_file_linux_tpl = "/home/{username}/.jergt/config/.jergt-config.ini"

    __config_file_windows = None
    __config_file_linux = None
    __config_file_osx = None

    __curr_system_type = None
    __curr_username = None
    __curr_windows_system_root = "C:"

    __allow_config_keys = (
        'publisher',
        'mirror',
        'lang'
    )

    def __init_system_info(self):
        """
        获取操作系统各种信息
        :return:
        """
        system_type = platform.system()  # 当前操作系统类型
        curr_username = getpass.getuser()  # 当前系统用户名

        if StringUtil.is_empty(curr_username):
            raise GetSystemInfoException("Failed to get current user name.")  # 获取当前用户名失败

        self.__curr_username = curr_username.strip()

        if system_type == "Darwin":
            self.__curr_system_type = "OSX"

        elif system_type == "Windows":  # Windows的默认环境路径
            system_root = os.getenv("SystemDrive", default="C:")
            if StringUtil.is_empty(system_root):
                raise GetSystemInfoException("Illegal system root path:{}".format(system_root))  # 系统路径不合理

            self.__curr_windows_system_root = system_root.strip()
        elif system_type == "Linux":
            self.__curr_system_type = "Linux"

        else:  # 无法识别的操作系统
            raise NotSupportSystemTypeException("Unrecognized operation system.")

    def __init_config_file_location(self):
        """
        初始化配置文件位置
        :param self:
        :return:
        """
        if self.__curr_system_type == "OSX":
            self.__config_file_osx = self.__config_file_osx_tpl.format(username=self.__curr_username)
        elif self.__curr_system_type == "Windows":
            self.__config_file_windows = self.__config_file_windows_tpl.format(
                system_root=self.__curr_windows_system_root, username=self.__curr_username)
        elif self.__curr_system_type == "Linux":
            self.__config_file_linux = self.__config_file_linux_tpl.format(username=self.__curr_username)
        else:
            pass

    def __load_config_file(self):
        """
        加载配置文件
        如果文件不存在，那么不加载（直接使用默认的）
        如果第一次保存配置的时候，文件不存在，直接创建。
        如果文件存在，加载，修改。
        :param self:
        :return:
        """

        if self.__curr_system_type == "OSX":
            self.__path = self.__config_file_osx
            return self.__path
        elif self.__curr_system_type == "Linux":
            self.__path = self.__config_file_linux
            return self.__path
        elif self.__curr_system_type == "Windows":
            self.__path = self.__config_file_windows
            return self.__path

        filename = self.__path

        if os.path.exists(filename):
            self.__config = configparser.ConfigParser()
            self.__config.read(filename, encoding="UTF-8")
            sections = self.__config.sections()  # sections获取配置文件（.jergt-config.ini）[]中的内容

            if "app" not in sections:
                raise ConfigFileParseFailedException(filename)

    def __init__(self):
        self.__val = None
        self.__path = None
        self.__init_system_info()
        self.__init_config_file_location()
        self.__load_config_file()

    def get(self, key: str) -> str:
        """
        获取配置项
        配置获取优先级： 当前环境变量 > 配置文件 > 默认值
        :param key: Key
        :return: Value
        """
        if StringUtil.is_empty(key):
            raise ConfigKeyNotExistException("{} is not in config file, because you key is Error".format(key))

        if key not in self.__allow_config_keys:
            raise ConfigKeyNotExistException("{} is not in config file.".format(key))

        key = key.strip()

        if self.__config is None:
            return self.__match_config_key(key=key)
        else:
            val = self.__config.get("app", key).strip()  # 获取用户在app中写入的key，获取到value
            # val = val.strip()   #集合到上一句了
            return self.__match_config_key(key=key) if StringUtil.is_empty(val) else val  # 就是下面的三元表达式
            # if StringUtil.is_empty(val):
            #     self.__match_config_key(key=key)
            # return val

    def __match_config_key(self, key: str) -> str:
        if key == "mirror":
            return self.__default_mirror
        elif key == "lang":
            return self.__default_lang
        elif key == "publisher":
            return self.__default_publisher  # 此处不需要else因为上面为不存在的key抛异常了

    def set(self, key: str, value: str) -> bool:  # 不想要bool
        """
        设置配置项
        :param key: Key
        :param value: Value
        :return:如果不存在这个配置项,那么返回 False
        """
        if self.__config.has_option("app", option=key):
            raise ConfigKeyNotExistException

        if key not in self.__allow_config_keys:
            self.__config.read("app", encoding="UTF-8")
            self.__config.set("app", "key", "value")
            self.__config.write(open("app", "w"))
        elif key in self.__allow_config_keys:
            if key == "publisher":
                if self.__config.get("app", key).strip() not in {"publisher对应的value"}:
                    raise KeyValueNotInRange
                else:
                    self.__config.read("app", encoding="UTF-8")
                    self.__config.set("app", "key", "value")
                    self.__config.write(open("app", "w"))
            elif key == "mirror":
                if self.__config.get("app", key).strip() not in {"mirror对应的value"}:
                    raise KeyValueNotInRange
                else:
                    self.__config.read("app", encoding="UTF-8")
                    self.__config.set("app", "key", "value")
                    self.__config.write(open("app", "w"))
            elif key == "lang":
                if self.__config.get("app", key).strip() not in {"lang对应的value"}:
                    raise KeyValueNotInRange

    def get_with_default(self, key: str, default: str):
        """
        获取配置项，如果这个配置项的值为空，那么返回 default
        配置获取优先级: 当前环境变量 > 配置文件 > 指定的默认值 > 默认值
        :param key:Key
        :return: Value
        :param default: 默认值
        :return: Value
        """

        self.__val = self.__config.get("app", key).strip()
        if self.__val is None:
            return default == self.__match_config_key


if __name__ == "__main__":
    pass


