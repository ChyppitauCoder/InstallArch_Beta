import os
import json
import time
import sys
import string

settings = {
    "main": "",
    "boot": "",
    "fs": "",
    "de": "",
    "dm": "",
    "soft": "",
    "user": "",
    "passwd_user": "",
    "passwd_root": "",
    "timezone": "",
    "locale": ""
}

setting_file = 'users_data.json'

with open(setting_file, 'w') as file:
    json.dump(settings, file)    

def load_users_data():
    if os.path.exists(setting_file):
        with open(setting_file, "r", encoding="utf-8") as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                print("An error occured! Trying to init empty array.")
                return {}
    else:
        return {}

def save_users_data():
    os.system(f"touch {setting_file}")
    with open(setting_file, '+w') as f:
        file.write(f"{settings}")

def install_just():
    get_guide = input("Get install guide(all commands) or allow to this installer make it without your copy-pasting?[Y/n]")
    if get_guide == "Y" or get_guide == "y":
        print(f'Here is your commands:\n\n\npacman -Syu; mkfs.fat -F32 {settings["boot"]} && mkfs.{settings["fs"]} {settings["main"]}; mount {settings["main"]} /mnt && mount {settings["boot"]} /mnt/boot --mkdir; pacstrap /mnt base base-devel linux linux-firmware linux-headers sudo nano vim neovim bash-completion grub efibootmgr git {settings["de"]} {settings["dm"]} {settings["soft"]} micro os-prober ntfs-3g networkmanager xorg wayland tff-ubuntu tff-jetbrains-mono-nerd && genfstab /mnt >> /mnt/etc/fstab && arch-chroot /mnt; useradd -m -g users -G wheel -s /bin/bash {settings["user"]} && usermod -a -G sudo {settings["user"]}; echo "{settings["user"]}:{settings["passwd_user"]}" | chpasswd; echo "root:{settings["passwd_root"]}" | chpasswd; ln -sf /usr/share/zoneinfo/{settings["timezone"]} /etc/localtime; git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si && cd -;')
        if settings["locale"] != "":
            print(f'echo "{settings["locale"]}.UTF-8 UTF-8" > /etc/locale.gen && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && echo "{settings["locale"]}.UTF-8 UTF-8" > /etc/locale.conf && locale-gen;')
        else:
            print(f'echo "en_US.UTF-8 UTF-8" > /etc/locale.gen;')
        print(r'echo -e "[multilib]\nInclude = /etc/pacman.d/mirrorlist";')
        if settings["dm"] != "":
            print(f"systemctl enable {settings["dm"]};")
        print(f"systemctl enable networkmanager; grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot/efi --removable && grub-mkconfig -o /boot/grub/grub.cfg; pacman -Syu; exit && umount -R /mnt && echo system was installed.; reboot now;")
    else:
        try:
            global settings
            os.system("pacman -Syu")
            os.system(f"mkfs.fat -F32 {settings["boot"]}")
            os.system(f"mkfs.{settings["fs"]} {settings["main"]}")
            os.system(f"mount {settings["main"]} /mnt")
            os.system(f"mount {settings["boot"]} /mnt/boot --mkdir")
            os.system(f"pacstrap /mnt base base-devel linux linux-firmware linux-headers sudo nano vim neovim bash-completion grub efibootmgr git {settings["de"]} {settings["dm"]} {settings["soft"]} micro os-prober ntfs-3g networkmanager xorg wayland tff-ubuntu tff-jetbrains-mono-nerd")
            os.system(f"genfstab -U /mnt >> /mnt/etc/fstab")
            os.system(f"arch-chroot /mnt")
            os.system(f"useradd -m -g users -G wheel -s /bin/bash {settings["user"]}")
            os.system(f"usermod -a -G sudo {settings["user"]}")
            os.system(f'echo "{settings["user"]}:{settings["passwd_user"]}" | chpasswd')
            os.system(f'echo "root:{settings["passwd_root"]}" | chpasswd')
            os.system(f"ln -sf /usr/share/zoneinfo/{settings["timezone"]} /etc/localtime")
            os.system(f"git clone https://aur.archlinux.org/yay.git")
            os.system(f"cd yay")
            os.system(f"makepkg -si")
            os.system(f"cd -")

            with open("/etc/locale.gen", "+w") as file:
                file.write("en_US.UTF-8 UTF-8")

                if settings["locale"] != "":
                    file.write(f"{settings["locale"]}.UTF-8 UTF-8")
                os.system("locale-gen")
            
            if settings["locale"] != "":
                with open("/etc/locale.conf", "+w") as file:
                    file.write(f"{settings["locale"]}.UTF-8")  
                    os.system("locale-gen")
            
            with open("/etc/pacman.conf", "+w") as file:
                file.write("[multilib]\nInclude = /etc/pacman.d/mirrorlist")

            if settings["dm"] != "":
                os.system(f"systemctl enable {settings["dm"]}")

            try:
                os.system(f"systemctl enable networkmanager")
            except Exception:
                print ("Can't enable networkmanager. Try make it yourself past installation.")

            os.system(f"grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot/efi --removable")
            os.system(f"grub-mkconfig -o /boot/grub/grub.cfg")
            os.system("pacman -Syu")
            os.system("exit")
            os.system(f"umount -R /mnt")

            print("System was installed! Welcome to Arch Linux! Recomendated actions: change system in bios from old to new.")
            contin = input("Reboot now?[Y/n]")
            if contin == "Y" or contin == "y":
                os.system("reboot") 
            else:
                print ("continue your post installation")

        except Exception as e:
            print (f"An error occured! {e}. You need to continue installation yourself.")

            input("Press any key to exit...")
            sys.exit()

def set_settings():
    os.system("clear")
    command_line = ""

    while command_line != "quit":
        global settings
        prin = 'Welcome to guide! Follow these commands to install arch using this installer:\n"cfdisk" - open cfdisk.\n"lsblk" - show you disk partitions.\n"main": select main partition and program mount him.\n"boot": select the boot partition.\n"fs" - choose file system.\n"de": select desktop enviroment.\n"dm" - choose your desktop manager.\n"soft" - choose soft you want.\n"nvidia" - install nvidia driver.\n"user": choose your username.\n"timezone" - choose your timezone.\n"locale" - enter your second locale. Will be keyboard and system locale (X11 only).\n"pu": choose user password.\n"pr": choose root password.\n"install" - install.\n"quit": abort installation.\n"save": save your settings, if you want install arch later.\n"load" - load your saved settings.\n"conf" - show your current configuration.\n"clear": clear screen\n\n'
        command_line = input(f'Welcome to most minimalist arch installer! Guide: \n\n\n{prin}')

        if command_line == "cfdisk":
            os.system("lsblk")
            
            disk = input("Enter your disk: (example: /dev/sda)")
            if "/dev/" not in disk:
                disk = "/dev/" + disk

            os.system(f"cfdisk {disk}")
        elif command_line == "lsblk":
            os.system("lsblk")
            contin = input("Press any key to continue")
        elif command_line == "main":
            partition = input("enter your main partition (example: /dev/sda1): ")
            if "/dev/" not in partition:
                partition = "/dev/" + partition
            if string.digits not in partition:
                num = input("Enter the number of partition: ")
                partition = partition + num

            settings["main"] = f"{partition}"
            save_users_data()
        elif command_line == "boot":
            partition = input("enter your main partition (example: /dev/sda2): ")
            if "/dev/" not in partition:
                partition = "/dev/" + partition
            if string.digits not in partition:
                num = input("Enter the number of partition: ")
                partition = partition + num

            settings["boot"] = f"{partition}"
            save_users_data()
        elif command_line == "fs":
            fs = input("Enter your wish file system (Example: ext4) (Example: btrfs): ")

            settings["fs"] = fs
            save_users_data()
        elif command_line == "de":
            de = input("Choose your Desktop Enviroment\n[1] KDE\n[2] Gnome\n[3] Cinnamon\n[4] LXQT\n[5] Xfce4\n[6] LXDE\n[7] Hyprland\n[8] i3\nDon't found your default?\n[9] Install basic system without DE\n\n")
            if de == "1":
                settings["de"] = "plasma"
            elif de == "2":
                settings["de"] = "gnome"
            elif de == "3":
                settings["de"] = "cinnamon"
            elif de == "4":
                settings["de"] = "lxqt"
            elif de == "5":
                settings["de"] = "xfce4"
            elif de == "6":
                settings["de"] = "lxde"
            elif de == "7":
                settings["de"] = "hyprland"
            elif de == "8":
                settings["de"] = "i3"
            elif de == "9":
                settings["de"] = ""
            else:
                print("Unknow option. You are back to main menu")
                contin = input("Press any key to continue")

            save_users_data()
        elif command_line == "dm":
            dm = input("Choose your Desktop Manager\n[1] SDDM\n[2] GDM\n[3] LXDM\n[4] LightDM\nDon't found your default?\n[5] Install system without DM (requires set up dm yourself)\n")
            if dm == "1":
                settings["dm"] = "sddm"
            elif dm == "2":
                settings["dm"] = "gdm"
            elif dm == "3":
                settings["dm"] = "lxdm"
            elif dm == "4":
                settings["dm"] = "lightdm"
            elif dm == "5":
                settings["dm"] = ""
            else:
                print("Unknow option. You are back to main menu")
                contin = input("Press any key to continue")

            save_users_data()
        elif command_line == "soft":
            soft = input("Enter soft you want (if you want to more than one other soft, separate him with a space): ")

            settings["soft"] = soft
            save_users_data()
        elif command_line == "nvidia":
            settings["soft"] += " nvidia"
            input("Done")

            save_users_data()
        elif command_line == "user":
            user = input("Enter username: ")

            settings["user"] = user
            save_users_data()
        elif command_line == "timezone":
            timezone = input("Enter your timezone (example: Europe/Moscow): ")

            settings["timezone"] = timezone
            save_users_data()
        elif command_line == "locale":
            locale = input("Enter your locale (Example: ru_RU) (Example: en_US): ")

            settings["locale"] = locale
            save_users_data()
        elif command_line == "pu":
            passwd = input("Enter password: ")
            time.sleep(4)
            passwd2 = input("Retype password: ")
            if passwd2 != passwd:
                print("Error! Passwords don't equals!")
                contin = input("Press any key to continue")
            else:
                settings["passwd_user"] = passwd
                save_users_data()
        elif command_line == "pr":
            passwd = input("Enter password: ")
            time.sleep(4)
            passwd2 = input("Retype password: ")
            if passwd2 != passwd:
                print("Error! Passwords don't equals!")
                contin = input("Press any key to continue")
            else:
                settings["passwd_root"] = passwd
                save_users_data()
        elif command_line == "install":
            contin = input(f"Are you sure want to continue with config: {str(settings)}?")
            if contin == "Y" or contin == "y":
                install_just()
            else:
                input("Press any key to back in main menu")
        elif command_line == "save":
            save_users_data()
            time.sleep(2)
            print ("Done!")
        elif command_line == "load":
            load_users_data()
            time.sleep(2)
            print ("Done!")
        elif command_line == "conf":
            with open(setting_file, "r") as file:
                print (file.read())
                input("Press any key to back in main menu")
        elif command_line == "clear":
            os.system("clear")
        elif command_line != "quit":
            input("Unknow command. Press any key to try again")

set_settings()
