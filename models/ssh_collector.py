import socket
from fabric import Connection
from invoke import CommandTimedOut
from paramiko import ssh_exception
from models.system_info import SystemInfo
from models.exceptions import HostCheckError

def get_os_info(conn: Connection, timeout: int = 3) -> tuple[str, str]:
    result = conn.run("hostnamectl", hide=True, timeout=timeout)

    hostname, kernel = "Неизвестно", "Неизвестно"

    if "Static hostname:" in result.stdout:
        hostname = result.stdout.split("Static hostname:")[1].splitlines()[0].strip()
    if "Kernel:" in result.stdout:
        kernel = result.stdout.split("Kernel:")[1].splitlines()[0].strip()

    return hostname, kernel

def get_printer_info(conn: Connection, timeout: int = 3) -> str:
    result = conn.run("lpstat -v", hide=True, encoding="utf-8", timeout=timeout)
    printers = []

    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue

        try:
            if 'usb://' in line:
                usb_info = line.split("://")[1].split("%")[0]
                printers.append(f"USB: {usb_info}")
            elif "socket://" in line:
                socket_info = line.split("://")[1].split("%")[0]
                printers.append(f"Socket: {socket_info}")
        except IndexError:
            printers.append(line)
    return "\n".join(printers) if printers else "Н/Д"


def get_cpu_temp(conn: Connection, timeout: int = 3) -> str:
    try:
        result = conn.run(
            """awk '{printf "%.1f\\n", $1/1000}' $(grep -l 'x86_pkg_temp' /sys/class/thermal/thermal_zone*/type 2>/dev/null | head -n1 | sed 's/type/temp/' || echo '/sys/class/thermal/thermal_zone0/temp')""",
            hide=True, timeout=timeout)
        cpu_temp = result.stdout.strip() + "°C"

        return cpu_temp
    except CommandTimedOut:
        cpu_temp = "Н/Д"
        return cpu_temp

def get_cpu_busy(conn: Connection, timeout: int = 3) -> str:
    try:
        result = conn.run("""vmstat 1 2 | tail -1 | awk '{print 100 - $15}'""", hide=True, timeout=timeout)
        cpu_busy = result.stdout.strip() + "%"

        return cpu_busy
    except CommandTimedOut:
        cpu_busy = "Н/Д"
        return cpu_busy


def gather_info(department: str, workplace_name: str, host: str, user: str, password: str, port=4220) -> SystemInfo:
    try:
        with Connection(host, user=user, port=port, connect_timeout=2, connect_kwargs={"password": password}) as conn:
            hostname, kernel = get_os_info(conn)
            return SystemInfo(
                department=department,
                workplace_name=workplace_name,
                host=host,
                hostname=hostname,
                kernel=kernel,
                printer=get_printer_info(conn),
                cpu_temp=get_cpu_temp(conn),
                cpu_busy=get_cpu_busy(conn)
            )
    except (TimeoutError, socket.timeout, socket.gaierror) as e:
        return SystemInfo(
            department=department,
            workplace_name=workplace_name,
            host=host,
            hostname="Н/Д",
            kernel="Н/Д",
            printer="Н/Д",
            cpu_temp="Н/Д",
            cpu_busy="Н/Д"
        )
    except ssh_exception.NoValidConnectionsError as e:
        raise HostCheckError(f"Не удалось подключиться к {host}:{port}. Проверьте порт") from e
    except ssh_exception.AuthenticationException as e:
        raise HostCheckError(f"Ошибка авторизации на {host}: неверный логин или пароль") from e
    except (ssh_exception.SSHException, OSError) as e:
        raise HostCheckError(f"Сетевая ошибка SSH при работе с {host}: {e}") from e
