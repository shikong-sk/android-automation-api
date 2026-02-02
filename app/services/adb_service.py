"""
ADB 服务模块

提供基于 adbutils 的 ADB 命令操作，包括：
- 获取已安装应用列表
- 安装/卸载应用
- 推送/拉取文件
- 执行 shell 命令
- 获取设备属性
"""

import base64
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from adbutils import AdbClient, AdbDevice


@dataclass
class AppInfo:
    """
    应用信息数据类

    Attributes:
        package_name: 应用包名
        version_name: 版本名称
        version_code: 版本号
        first_install_time: 首次安装时间
        last_update_time: 最后更新时间
    """

    package_name: str
    version_name: Optional[str] = None
    version_code: Optional[int] = None
    first_install_time: Optional[str] = None
    last_update_time: Optional[str] = None


class AdbService:
    """
    ADB 服务类

    提供基于 adbutils 的 ADB 命令操作。
    与 DeviceManager 配合使用，通过设备序列号连接设备。

    Attributes:
        _client: AdbClient 实例
        _device: AdbDevice 实例
    """

    def __init__(self, device_serial: Optional[str] = None):
        """
        初始化 ADB 服务

        Args:
            device_serial: 设备序列号。如果为 None，则使用第一个可用设备。
        """
        self._client = AdbClient(host="127.0.0.1", port=5037)
        if device_serial:
            self._device = self._client.device(device_serial)
        else:
            devices = self._client.device_list()
            if not devices:
                raise RuntimeError("No ADB devices found")
            self._device = devices[0]

    @property
    def device(self) -> AdbDevice:
        """获取 ADB 设备对象"""
        return self._device

    @property
    def serial(self) -> str:
        """获取设备序列号"""
        serial = self._device.serial
        return serial if serial else ""

    def list_packages(self, filter_type: Optional[str] = None) -> List[str]:
        """
        获取已安装应用包名列表

        Args:
            filter_type: 过滤类型，可选值：
                - None: 所有应用
                - "third_party" 或 "3": 第三方应用
                - "system" 或 "s": 系统应用

        Returns:
            List[str]: 应用包名列表
        """
        if filter_type in ("third_party", "3"):
            # 第三方应用
            output = self._device.shell("pm list packages -3")
        elif filter_type in ("system", "s"):
            # 系统应用
            output = self._device.shell("pm list packages -s")
        else:
            # 所有应用
            output = self._device.shell("pm list packages")

        packages = []
        for line in output.strip().split("\n"):
            if line.startswith("package:"):
                packages.append(line[8:])
        return sorted(packages)

    def get_package_info(self, package_name: str) -> Optional[Dict[str, Any]]:
        """
        获取应用详细信息

        Args:
            package_name: 应用包名

        Returns:
            Dict: 应用信息字典，包含版本、安装时间等
        """
        try:
            output = self._device.shell(f"dumpsys package {package_name}")
            info = {
                "package_name": package_name,
                "version_name": None,
                "version_code": None,
                "first_install_time": None,
                "last_update_time": None,
                "target_sdk": None,
                "min_sdk": None,
            }

            for line in output.split("\n"):
                line = line.strip()
                if line.startswith("versionName="):
                    info["version_name"] = line.split("=", 1)[1]
                elif line.startswith("versionCode="):
                    # versionCode=123 minSdk=21 targetSdk=33
                    parts = line.split(" ")
                    for part in parts:
                        if part.startswith("versionCode="):
                            try:
                                info["version_code"] = int(part.split("=")[1])
                            except ValueError:
                                pass
                        elif part.startswith("minSdk="):
                            try:
                                info["min_sdk"] = int(part.split("=")[1])
                            except ValueError:
                                pass
                        elif part.startswith("targetSdk="):
                            try:
                                info["target_sdk"] = int(part.split("=")[1])
                            except ValueError:
                                pass
                elif line.startswith("firstInstallTime="):
                    info["first_install_time"] = line.split("=", 1)[1]
                elif line.startswith("lastUpdateTime="):
                    info["last_update_time"] = line.split("=", 1)[1]

            return info
        except Exception:
            return None

    def get_all_packages_info(self, filter_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取所有应用的详细信息

        Args:
            filter_type: 过滤类型，同 list_packages

        Returns:
            List[Dict]: 应用信息列表
        """
        packages = self.list_packages(filter_type)
        result = []
        for pkg in packages:
            info = self.get_package_info(pkg)
            if info:
                result.append(info)
        return result

    def install_apk(
        self, apk_path: str, reinstall: bool = False, grant_permissions: bool = True
    ) -> bool:
        """
        安装 APK 文件

        Args:
            apk_path: APK 文件路径（本地路径）
            reinstall: 是否重新安装（保留数据）
            grant_permissions: 是否自动授予所有权限

        Returns:
            bool: 安装是否成功
        """
        try:
            # adbutils install 方法参数
            self._device.install(apk_path)
            return True
        except Exception:
            return False

    def uninstall_package(self, package_name: str, keep_data: bool = False) -> bool:
        """
        卸载应用

        Args:
            package_name: 应用包名
            keep_data: 是否保留应用数据

        Returns:
            bool: 卸载是否成功
        """
        try:
            if keep_data:
                self._device.shell(f"pm uninstall -k {package_name}")
            else:
                self._device.uninstall(package_name)
            return True
        except Exception:
            return False

    def shell(self, command: str) -> str:
        """
        执行 shell 命令

        Args:
            command: 要执行的 shell 命令

        Returns:
            str: 命令输出
        """
        return self._device.shell(command)

    def get_prop(self, prop_name: str) -> str:
        """
        获取设备属性

        Args:
            prop_name: 属性名称

        Returns:
            str: 属性值
        """
        value = self._device.prop.get(prop_name)
        return value if value else ""

    def get_device_info(self) -> Dict[str, Any]:
        """
        获取设备详细信息

        Returns:
            Dict: 设备信息字典
        """
        return {
            "serial": self.serial,
            "model": self.get_prop("ro.product.model"),
            "brand": self.get_prop("ro.product.brand"),
            "manufacturer": self.get_prop("ro.product.manufacturer"),
            "device": self.get_prop("ro.product.device"),
            "android_version": self.get_prop("ro.build.version.release"),
            "sdk_version": self.get_prop("ro.build.version.sdk"),
            "build_id": self.get_prop("ro.build.id"),
        }

    def push_file(self, local_path: str, remote_path: str) -> bool:
        """
        推送文件到设备

        Args:
            local_path: 本地文件路径
            remote_path: 设备上的目标路径

        Returns:
            bool: 是否成功
        """
        try:
            self._device.sync.push(local_path, remote_path)
            return True
        except Exception:
            return False

    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """
        从设备拉取文件

        Args:
            remote_path: 设备上的文件路径
            local_path: 本地目标路径

        Returns:
            bool: 是否成功
        """
        try:
            self._device.sync.pull(remote_path, local_path)
            return True
        except Exception:
            return False

    def get_battery_info(self) -> Dict[str, Any]:
        """
        获取电池信息

        Returns:
            Dict: 电池信息字典
        """
        output = self._device.shell("dumpsys battery")
        info = {}
        for line in output.split("\n"):
            line = line.strip()
            if ": " in line:
                key, value = line.split(": ", 1)
                key = key.strip().lower().replace(" ", "_")
                # 尝试转换为数字
                try:
                    if value.lower() in ("true", "false"):
                        info[key] = value.lower() == "true"
                    else:
                        info[key] = int(value)
                except ValueError:
                    info[key] = value
        return info

    def get_screen_resolution(self) -> Dict[str, int]:
        """
        获取屏幕分辨率

        Returns:
            Dict: 包含 width 和 height 的字典
        """
        output = self._device.shell("wm size")
        # Physical size: 1080x2400
        for line in output.split("\n"):
            if "Physical size:" in line:
                size = line.split(":")[1].strip()
                width, height = size.split("x")
                return {"width": int(width), "height": int(height)}
        return {"width": 0, "height": 0}

    def get_screen_density(self) -> int:
        """
        获取屏幕密度

        Returns:
            int: 屏幕密度 (dpi)
        """
        output = self._device.shell("wm density")
        # Physical density: 420
        for line in output.split("\n"):
            if "Physical density:" in line:
                return int(line.split(":")[1].strip())
        return 0

    def take_screenshot(self, local_path: str) -> bool:
        """
        截取屏幕截图

        Args:
            local_path: 保存截图的本地路径

        Returns:
            bool: 是否成功
        """
        try:
            # 先截图到设备临时目录
            remote_path = "/sdcard/screenshot_temp.png"
            self._device.shell(f"screencap -p {remote_path}")
            # 拉取到本地
            self._device.sync.pull(remote_path, local_path)
            # 删除设备上的临时文件
            self._device.shell(f"rm {remote_path}")
            return True
        except Exception:
            return False

    def take_screenshot_base64(self) -> Dict[str, Any]:
        """
        截取屏幕截图并返回 base64 编码

        Returns:
            Dict: 包含 base64 图片数据和屏幕尺寸
                - image: base64 编码的图片数据 (data:image/png;base64,...)
                - width: 屏幕宽度
                - height: 屏幕高度
        """
        try:
            # 使用 screencap -p 直接获取 PNG 数据
            # encoding=None 返回原始字节数据
            png_data = self._device.shell("screencap -p", encoding=None)
            
            # 转换为 base64
            base64_data = base64.b64encode(png_data).decode("utf-8")
            
            # 获取屏幕尺寸
            resolution = self.get_screen_resolution()
            
            return {
                "image": f"data:image/png;base64,{base64_data}",
                "width": resolution.get("width", 0),
                "height": resolution.get("height", 0),
            }
        except Exception as e:
            return {"error": str(e), "image": None, "width": 0, "height": 0}

    def reboot(self, mode: Optional[str] = None) -> bool:
        """
        重启设备

        Args:
            mode: 重启模式，可选值：
                - None: 正常重启
                - "recovery": 重启到 recovery 模式
                - "bootloader": 重启到 bootloader 模式

        Returns:
            bool: 命令是否发送成功
        """
        try:
            if mode:
                self._device.shell(f"reboot {mode}")
            else:
                self._device.shell("reboot")
            return True
        except Exception:
            return False
