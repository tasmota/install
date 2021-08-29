These files are needed for flashing Tasmota32s2 with esptool.py to an ESP32-S2.

esptool.py --chip esp32s2 --baud 115200 --before default_reset --after hard_reset write_flash -z --flash_mode dout --flash_freq 40m --flash_size detect 0x1000 bootloader_dout_40m.bin 0x8000 partitions.bin 0xe000 boot_app0.bin 0x10000 tasmota32s2.bin
