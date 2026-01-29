import uiautomator2 as u2
from IPython import embed

d = u2.connect()


def main():
    print("设备信息:", d.info)
    print("准备进入 IPython 交互式调试...")
    print("可用方法:")
    print("  - d.xxx() : uiautomator2 所有方法")
    print("  - Ctrl+D  : 退出交互模式继续执行")
    print("  - exit()  : 完全退出")
    print("-" * 40)
    embed()


if __name__ == "__main__":
    main()
