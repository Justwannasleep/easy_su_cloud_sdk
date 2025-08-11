import platform
import subprocess
import uuid
import hashlib


def get_device_code():
    system = platform.system()
    info = ""

    try:
        if system == "Windows":
            # 获取硬盘序列号 (C盘)
            output = subprocess.check_output(
                "wmic diskdrive where index=0 get serialnumber", shell=True
            )
            info += output.decode().strip()

            # 获取主板序列号
            output = subprocess.check_output(
                "wmic baseboard get serialnumber", shell=True
            )
            info += output.decode().strip()

        elif system == "Linux":
            # 获取硬盘序列号
            output = subprocess.check_output(
                ["hdparm", "-i", "/dev/sda"], stderr=subprocess.DEVNULL
            )
            info += output.decode().split("SerialNo=")[-1].split()[0]

            # 获取主板序列号
            with open("/sys/class/dmi/id/board_serial") as f:
                info += f.read().strip()

        elif system == "Darwin":  # macOS
            # 获取硬盘序列号
            output = subprocess.check_output(["diskutil", "info", "/"], text=True)
            serial_line = [
                line for line in output.splitlines() if "Volume UUID" in line
            ][0]
            info += serial_line.split(":")[1].strip()

            # 获取硬件UUID
            output = subprocess.check_output(
                ["system_profiler", "SPHardwareDataType"], text=True
            )
            uuid_line = [line for line in output.splitlines() if "UUID" in line][0]
            info += uuid_line.split(":")[1].strip()
    except:
        pass  # 部分信息可能无法获取

    # 添加MAC地址作为后备
    mac = uuid.getnode()
    info += str(mac)

    # 添加操作系统信息
    info += platform.platform()

    # 生成哈希值作为设备编码
    return hashlib.sha256(info.encode()).hexdigest()
