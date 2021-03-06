import os
import sys


def get_vfat_mounts():
    vfats = []

    with open("/etc/mtab") as f:
        mtab = f.readlines()

    for mountline in mtab:
        mount_parts = mountline.split(" ")
        filesystem = mount_parts[2]
        if filesystem == "vfat":
            vfats.append(mount_parts[0])

    return vfats


def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def sudo(*cmd_args):
    try_list = ["gksudo", "kdesudo"]
    for sudo_cmd in try_list:
        sudo_path = which(sudo_cmd)
        if not sudo_path:
            continue

        for cmd in cmd_args:
            shell_command = "%s %s" % (sudo_path, cmd)
            os.system(shell_command)


def dialog(dialog_type, message):
    zenity = which("zenity")
    if dialog_type == "error":
        os.system("%s --error --text=\"%s\"" % (zenity, message))
    elif dialog_type == "info":
        os.system("%s --info --text=\"%s\"" % (zenity, message))
    else:
        print message


def sort_fats():
    fatsort_path = which("fatsort")
    if not fatsort_path:
        dialog("error", "This program uses fatsort. Please install 'fatsort'")
        sys.exit(1)

    vfats = get_vfat_mounts()
    if not vfats:
        dialog("error", "No vfat filesystems found in /etc/mtab")
        sys.exit()

    for dev in vfats:
        sudo("umount %s" % dev, "%s %s" % (fatsort_path, dev))

    dialog("info", "All okey, remove USB stick")

if __name__ == "__main__":
    sort_fats()