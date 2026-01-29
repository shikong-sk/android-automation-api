from test_connect_phone import connect_phone


def main():
    d = connect_phone()
    d.press("home")
    d.app_start("com.lphtsccft")


if __name__ == "__main__":
    main()
