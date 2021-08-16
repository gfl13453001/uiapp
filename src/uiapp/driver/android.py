#!/usr/bin/env python
#-*- coding:utf-8 -*-

# authors:guanfl
# 2021/8/5



import os
import subprocess
import time


class _InitBase(object):

    def __init__(self,devices,driver="main"):
        self.device = devices
        self.dump_file = '/sdcard/uiapp.xml'
        self.DIR = r"D:\ui"
        try:
            os.mkdir(self.DIR)
        except:
            pass
        self.pull_file =  self.DIR
        get_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base = os.path.join(get_dir, 'common/key/adb.exe').replace("\\", "/")
        self.adb_path = base if driver == "main" else driver



    def setup(self):

        self._dump_ui()
        time.sleep(1)
        self._pull_file()
        self._keypackage_install()

        # return _InitBase.setup

    def _dump_ui(self) :
        file = os.path.join(self.DIR,'uiapp.xml')
        shell = None
        if self.device is None:
            shell = f"{self.adb_path}  shell uiautomator dump {self.dump_file}"
        else:
            shell = f"{self.adb_path} -s {self.device} shell uiautomator dump {self.dump_file}"

        subprocess.Popen(shell)


    def _pull_file(self):
        """
        拉取ui
        :return:
        """
        shell = None
        if self.device is None:
            shell = f"{self.adb_path} pull {self.dump_file} {self.pull_file}"
        else:
            shell = f'{self.adb_path} -s {self.device} pull {self.dump_file} {self.pull_file}'

        return subprocess.Popen(shell)


    def dump_init(self):
        """
        拉取当前ui元素
        :return:
        """

    def _keypackage_install(self):
        """
        初始化安装虚拟键盘、解决中文输入
        :return:
        """
        get_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xt = os.path.join(get_dir,'common/key/ADBKeyboard.apk').replace("\\",'/')
        x_shell = None
        k_shell = None

        if self.device is None:
            x_shell = f"{self.adb_path}  install  -r {xt}"
            k_shell = f"{self.adb_path}  shell ime set com.android.adbkeyboard/.AdbIME"

        else:
            x_shell = f"{self.adb_path} -s {self.device} install  -r {xt}"
            k_shell = f"{self.adb_path} -s {self.device} shell ime set com.android.adbkeyboard/.AdbIME"

        x = subprocess.Popen(x_shell, stdout=subprocess.PIPE).communicate()[0]

        # 设置默认输入法
        k = subprocess.Popen(k_shell, stdout=subprocess.PIPE).communicate()[0]


        return _InitBase



class Devices(_InitBase):
    def __init__(self,devices,driver="main"):
        """
        usage: wm [subcommand] [options]
            wm size [reset|WxH|WdpxHdp]
            wm density [reset|DENSITY]
            wm overscan [reset|LEFT,TOP,RIGHT,BOTTOM]
            wm scaling [off|auto]
            wm screen-capture [userId] [true|false]
            wm size: return or override display size.
                 width and height in pixels unless suffixed with 'dp'.
            wm density: override display density.
            wm overscan: set overscan area for display.
            wm scaling: set display scaling mode.
            wm screen-capture: enable/disable screen capture.
            wm dismiss-keyguard: dismiss the keyguard, prompting the user for auth if necessary.
        :return:
        """
        super(Devices, self).__init__(devices,driver=driver)


    def size(self):
        """
        设备尺寸大小
        :return:
        """
        get_content = None

        if self.device is None:
            size_shell = f"{self.adb_path}  shell wm size"
        else:
            size_shell = f"{self.adb_path} -s {self.device} shell wm size"

        xt = subprocess.Popen(size_shell, stdout=subprocess.PIPE, shell=True)
        get_content = xt.stdout.read().decode()

        xts = get_content.replace("\r\n","")
        get_window_size = [x.replace(" ","").split("x") for x in xts.split(":")]
        return int(get_window_size[-1][0]),int(get_window_size[-1][1])

    def set_size(self,x,y):
        """
        修改设备分辨率
        :return:
        """
        size_shell = None

        if self.device is None:
            size_shell = f"{self.adb_path}  shell wm size {x}x{y}"
        else:
            size_shell = f"{self.adb_path} -s {self.device} shell wm size {x}x{y}"

        xt = subprocess.Popen(size_shell, stdout=subprocess.PIPE, shell=True)
        get_content = xt.stdout.read().decode()

        xts = get_content.replace("\r\n","")



    def screen(self,path,name):
        size_shell = None
        file = "screenshot.png"

        if self.device is None:

            size_shell = f"{self.adb_path}  shell  /system/bin/screencap -p /sdcard/{file}"
            pull = f"{self.adb_path}    pull /sdcard/{file} {path}"
            re = os.rename(rf"{path}\{file}",rf"{path}\{name}")
        else:
            size_shell = f"{self.adb_path} -s {self.device} shell /system/bin/screencap -p /sdcard/screenshot.png"
            pull = f"{self.adb_path}    pull /sdcard/screenshot.png {path}"

        xt = subprocess.Popen(size_shell, stdout=subprocess.PIPE, shell=True)
        xx = subprocess.Popen(pull, stdout=subprocess.PIPE, shell=True)
        get_content = xt.stdout.read().decode()

        xts = get_content.replace("\r\n", "")



    def reset_size(self):
        """
        还原设备分辨率
        :return:
        """
        get_content = None

        if self.device is None:
            size_shell = f"{self.adb_path}  shell wm size reset"
        else:
            size_shell = f"{self.adb_path} -s {self.device} shell wm size reset"

        xt = subprocess.Popen(size_shell, stdout=subprocess.PIPE, shell=True)
        get_content = xt.stdout.read().decode()

        xts = get_content.replace("\r\n","")


    @property
    def inputmethod(self):
        adb_path = self.adb_path
        device = self.device
        class Settings:

            def set_default(self):
                """
                设置系统默认的输入法 安卓 AOSP
                :return:
                """
                k_shell = None
                if device is None:
                    k_shell = f"{adb_path} shell ime set com.android.inputmethod.latin/.LatinIME"
                else:
                    k_shell = f"{adb_path} -s {device} shell ime set com.android.inputmethod.latin/.LatinIME"

                return subprocess.Popen(k_shell, stdout=subprocess.PIPE).communicate()[0]

            def set(self,packagename):
                """
                设置指定的输入法
                :return:
                """
                k_shell = None
                if device is None:
                    k_shell = f"{adb_path} shell ime set {packagename}"
                else:
                    k_shell = f"{adb_path} -s {device} shell ime set {packagename}"

                return subprocess.Popen(k_shell, stdout=subprocess.PIPE).communicate()[0]

            def get(self):
                """
                获取系统安装的输入法
                :return:
                """
                k_shell = None
                if device is None:
                    k_shell = f"{adb_path} shell ime list -s"
                else:
                    k_shell = f"{adb_path} -s {device} shell ime set ime list -s"

                info_list =  subprocess.Popen(k_shell, stdout=subprocess.PIPE).communicate()[0]
                xl = info_list.decode()
                obj_ime = xl.replace("\n","").split("\r")
                return obj_ime[:-1]

            def get_setting_default(self):
                """
                获取系统默认输入法
                :return:
                """
                k_shell = None
                if device is None:
                    k_shell = f"{adb_path} shell settings get secure default_input_method"
                else:
                    k_shell = f"{adb_path} -s {device} shell settings get secure default_input_method"

                info_list =  subprocess.Popen(k_shell, stdout=subprocess.PIPE).communicate()[0]
                xl = info_list.decode()
                obj_ime = xl.replace("\n","").split("\r")
                return obj_ime[:-1]

        return Settings()

    @property
    def date(self):
        device = self.device
        driver = self.adb_path

        class at:
            """
            星期几
            月
            日期
            时间
            时间区域
            年
            """

            def get_date(self):
                if device is None:
                    get_content = None

                    size_shell = f"{driver}  shell date"
                else:
                    size_shell = f"{driver} -s {device} date"

                xt = subprocess.Popen(size_shell, stdout=subprocess.PIPE, shell=True)
                get_content = xt.stdout.read().decode()
                xp = get_content.replace("\r\n","").split(" ")
                return xp

        return at()





class _AdbActivity(_InitBase):

    def __init__(self,devices,driver="main"):
        super(_AdbActivity, self).__init__(devices,driver=driver)


    def port(self,port=8066):
        """
        修改ip
        :param port:
        :return:
        """
        self.install_shell = None
        if self.device is None:
            self.install_shell = f"{self.adb_path}  tcpip -{port}"
        else:
            self.install_shell = f"{self.adb_path} -s {self.device} tcpip {port}"

        return subprocess.Popen(self.install_shell).communicate()[0]

    def version(self):
        self.version_shell = None
        if self.device is None:
            self.version_shell = f"{self.adb_path}  shell getprop ro.build.version.release"
        else:
            self.version_shell = f"{self.adb_path} -s {self.device} shell getprop ro.build.version.release"

        vr = subprocess.Popen(self.version_shell,stdout=subprocess.PIPE)
        vr_text = vr.stdout.read().decode()
        return vr_text



    def install(self,app_path):
        """
        -l ：锁定应用程序
        -t ：允许测试包
        :param app_path:
        :return:
        """
        adb_path = self.adb_path
        device = self.device
        class meta:
            def __init__(self):
                self.install_shell = None

            def r(self):
                """
                强制安装
                :return:
                """
                if app_path is None:
                    self.install_shell = f"{adb_path}  install -r {app_path}"

                else:
                    self.install_shell = f"{adb_path} -s {device} install -r {app_path}"


                return subprocess.Popen(self.install_shell).communicate()[0]

            def t(self):
                """
                运行安装测试包
                :return:
                """
                if app_path is None:
                    self.install_shell = f"{adb_path}  install -t {app_path}"

                else:
                    self.install_shell = f"{adb_path} -s {device} install -t {app_path}"


                return subprocess.Popen(self.install_shell).communicate()[0]

            def d(self):
                """
                d ：允许降级覆盖安装
                :return:
                """
                if app_path is None:
                    self.install_shell = f"{adb_path}  install -d {app_path}"

                else:
                    self.install_shell = f"{adb_path} -s {device} install -d {app_path}"


                return subprocess.Popen(self.install_shell).communicate()[0]

            def p(self):
                """
                -p ：部分应用安装
                :return:
                """
                if app_path is None:
                    self.install_shell = f"{adb_path}  install -p {app_path}"

                else:
                    self.install_shell = f"{adb_path} -s {device} install -p {app_path}"


                return subprocess.Popen(self.install_shell).communicate()[0]

            def g(self):
                """
                -g ：为应用程序授予所有运行时的权限

                :return:
                """
                if app_path is None:
                    self.install_shell = f"{adb_path}  install -g {app_path}"

                else:
                    self.install_shell = f"{adb_path} -s {device} install -g {app_path}"


                return subprocess.Popen(self.install_shell).communicate()[0]

        return meta()



    def uninstall(self,app_package,parameters=None):
        """
        :param app_path:
        :return:
        """
        x = "uninstall"
        if parameters is None:
            return subprocess.Popen(rf"{self.adb_path}  {x}  {app_package}").communicate()[0]
        else:
            return subprocess.Popen(rf"{self.adb_path}  {x} {parameters} {app_package}").communicate()[0]


    def _connect(self,ip):
        x = f"{self.adb_path} connect {ip}"
        return subprocess.Popen(x).communicate()[0]

    def disconnect(self):
        """
        端口设备连接
        :param ip:
        :return:
        """
        x = "disconnect"
        return subprocess.Popen(rf"{self.adb_path} {x} {self.device}").communicate()[0]

    def select(self):
        x = f"{self.adb_path}  devices"
        xt = subprocess.Popen(x, stdout=subprocess.PIPE, shell=True)
        kt = xt.stdout.read().decode()

        list_stdout = kt.split('\n')

        devices = []
        for x in list_stdout:
            for y in x.split(" "):
                if y not in ["List","of","devices","attached\r",'\r']:
                    devices.append(y.replace("\r", "").split('\t'))

        index_top = devices[0]

        return index_top


    def _package_info(self):
        get_package_shell = None
        if self.device is None:
            get_package_shell = f"{self.adb_path} shell dumpsys window w  findstr name="
        else:
            get_package_shell = f"{self.adb_path} -s {self.device} shell dumpsys window w  findstr name="

        xt = subprocess.Popen(get_package_shell, stdout=subprocess.PIPE,shell=True)
        kt = xt.stdout.read().decode("utf-8")
        list_txt = kt.split('\n')
        packages_list = []
        for x in list_txt:
            xp = x.replace(" ", '').replace("\r","")
            cp = xp.split("=")
            if cp[0] == "mSurface":
                for pack in cp:
                    if pack.startswith("com") or pack.endswith("Activity"):
                        packages_list.append(pack.replace(")","").split("/"))


        return packages_list[0]



    def for_wait(self):
        """
        进行重新重启adb连接
        :return:
        """
        for_wait_shell = None
        if self.device is None:
            for_wait_shell = f"{self.adb_path} wait-for-device"
        else:
            for_wait_shell = f"{self.adb_path}  -s {self.device} wait-for-device"
        subprocess.Popen(for_wait_shell)
        return _AdbActivity.for_wait


    def start_server(self):
        """
        开启adb服务
        :return:
        """
        start_server = None
        if self.device is None:
            start_server = f"{self.adb_path}  start-server"
        else:
            start_server = f"{self.adb_path}  -s {self.device} start-server"
        subprocess.Popen(start_server)
        return _AdbActivity.start_server

    def kill_server(self):
        """
        关闭adb服务
        :return:
        """
        kill_server = None
        if self.device is None:

            kill_server = f"{self.adb_path}  kill-server"
        else:
            kill_server = f"{self.adb_path} -s {self.device} kill-server"
        subprocess.Popen(kill_server)

        return _AdbActivity.kill

    def reboot(self):
        """
        关闭adb服务
        :return:
        """
        reboot = None
        if self.device is None:
            reboot = f"{self.adb_path}  reboot"
        else:
            reboot = f"{self.adb_path}  -s {self.device} reboot"
        return subprocess.Popen(reboot)




    def call(self,tel):
        """
        拨打电话
        :param tel:
        :return:
        """


class AppPackAge(_InitBase):

    def __init__(self,devices,driver="main"):
        super(AppPackAge, self).__init__(devices,driver=driver)


    def current_package_info(self):
        """
        获取当前启动的app包的信息
        :return:
        """
        if self.device is None:
            p1 = subprocess.Popen([f"{self.adb_path}", "shell", "dumpsys", "window"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["findstr", "mCurrentFocus"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            output = p2.communicate()[0]
        else:
            p1 = subprocess.Popen([f"{self.adb_path}", "-s",f"{self.device}","shell", "dumpsys", "window"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["findstr", "mCurrentFocus"], stdin=p1.stdout, stdout=subprocess.PIPE)
            p1.stdout.close()
            output = p2.communicate()[0]
        xi = output.decode().replace("\r\n","").replace("}","").split(" ")
        return tuple(xi[-1].split("/"))

    def activity(self):
        """
        获取app activity
        :param packagename:
        :return:
        """
        return self.current_package_info()[-1]

    def get_package(self):
        """
        :return:
        """
        return self.current_package_info()[0]

    def get_packages(self):
        """
        获取安装包package
        :return:
        """
        get_package_shell = None
        if self.device is None:
            get_package_shell = f"{self.adb_path} shell pm list packages"
        else:
            get_package_shell = f"{self.adb_path} -s {self.device} shell pm list packages"

        xt = subprocess.Popen(get_package_shell, stdout=subprocess.PIPE, shell=True)
        kt = xt.stdout.read().decode()
        xname = kt.split('\n')
        package_list = []
        for x in xname:
            package_list.append(x.replace("\r",""))
        return package_list

    def run(self,package,activity):
        """
        启动app
        :param package:
        :param activity:
        :return:
        """
        run_shell = None
        if self.device is None:
            # run_shell = f"{self.adb_path} shell am start -W  {package}/{activity}"
            run_shell = f"{self.adb_path} shell am start -n  {package}/{activity}"
        else:
            run_shell = f"{self.adb_path} -s {self.device} shell am start -n  {package}/{activity}"

        xt = subprocess.Popen(run_shell, stdout=subprocess.PIPE,shell=True)
        kt = xt.stdout.read().decode("utf-8")
        print(run_shell)
        xt.kill()
        return AppPackAge.run

    def close(self,package):
        """
        关闭启动的应用
        :param package:
        :return:
        """
        close_shell = None
        if self.device is None:
            close_shell = f"{self.adb_path} shell am force-stop {package}"
        else:
            close_shell = f"{self.adb_path} -s {self.device} shell am force-stop {package}"
        xt = subprocess.Popen(close_shell, stdout=subprocess.PIPE,shell=True)
        kt = xt.stdout.read().decode("utf-8")
        xt.kill()

    def package_path(self):
        package_path_shell = None
        if self.device is None:
            package_path_shell = f"{self.adb_path}  shell pm list packages -f"
        else:
            package_path_shell = f"{self.adb_path} -s {self.device} shell pm list packages -f"
        xt = subprocess.Popen(package_path_shell, stdout=subprocess.PIPE, shell=True)
        kt = xt.stdout.read().decode("utf-8")
        xt.kill()

