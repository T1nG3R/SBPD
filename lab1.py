import win32event
import win32file
import win32con


# Функція для обробки переривань
import winioctlcon


def handle_disk_interrupts(disk, event):
    print(f"Access attempt to disk {disk} detected!")

    # Отримання статусу користувача (admin/user)
    user_status = get_user_status()

    # Визначення дозволів доступу в залежності від статусу користувача
    if user_status == "admin":
        access_rights = win32con.GENERIC_ALL
    elif user_status == "user":
        access_rights = win32con.GENERIC_READ | win32con.GENERIC_WRITE
    else:
        access_rights = 0  # Відмовити в доступі для невідомого статусу

    # Перевірка доступу до диску
    try:
        handle = win32file.CreateFile(
            disk,
            access_rights,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL,
            None
        )

        print(f"Access granted to disk {disk} for {user_status}")
        # Здійснення роботи з диском...

        win32file.CloseHandle(handle)
    except:
        print(f"Access denied to disk {disk} for {user_status}")


# Функція для отримання статусу користувача
def get_user_status():
    # Отримання статусу користувача (може бути реалізовано зчитуванням з бази даних або введенням з клавіатури)
    user_status = input("Enter user status (admin/user): ")
    return user_status


# Головна функція програми
def main():
    # Перехоплення переривань для диску A
    disk_A_interrupt = win32file.CreateFile(
        r"\\.\PhysicalDrive0",  # Приклад шляху до диску A
        win32con.FILE_ATTRIBUTE_READONLY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_OVERLAPPED,
        None
    )
    overlapped_A = win32file.OVERLAPPED()
    overlapped_A.hEvent = win32event.CreateEvent(None, 0, 0, None)
    win32file.DeviceIoControl(disk_A_interrupt, winioctlcon.FSCTL_ALLOW_EXTENDED_DASD_IO)
    win32file.ReadDirectoryChangesW(
        disk_A_interrupt,
        win32file.AllocateReadBuffer(4096),
        True,
        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_SIZE | win32con.FILE_NOTIFY_CHANGE_SECURITY,
        win32file.FILE_ALL_ACCESS,
        overlapped_A,
        handle_disk_interrupts,
    )

    # Перехоплення переривань для диску B
    disk_B_interrupt = win32file.CreateFile(
        r"\\.\PhysicalDrive1",  # Приклад шляху до диску B
        win32con.FILE_ATTRIBUTE_READONLY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL | win32con.FILE_FLAG_OVERLAPPED,
        None
    )
    overlapped_B = win32file.OVERLAPPED()
    overlapped_B.hEvent = win32event.CreateEvent(None, 0, 0, None)
    win32file.DeviceIoControl(disk_B_interrupt, winioctlcon.FSCTL_ALLOW_EXTENDED_DASD_IO, None, None, None)
    win32file.ReadDirectoryChangesW(
        disk_B_interrupt,
        win32file.AllocateReadBuffer(4096),
        True,
        win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_SIZE | win32con.FILE_NOTIFY_CHANGE_SECURITY,
        win32file.FILE_ALL_ACCESS,
        overlapped_B,
        handle_disk_interrupts,
    )

    # Очікування переривань
    while True:
        result_A = win32file.GetOverlappedResult(disk_A_interrupt, overlapped_A, True)
        result_B = win32file.GetOverlappedResult(disk_B_interrupt, overlapped_B, True)


# Виклик головної функції
if __name__ == '__main__':
    main()
