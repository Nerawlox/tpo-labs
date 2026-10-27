"""Create a project-local Android 11 AVD using the installed system image."""
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/".tools"
AVD=TOOLS/"avd/TrainingPhone.avd"
AVD.mkdir(parents=True,exist_ok=True)
(AVD.parent/"TrainingPhone.ini").write_text(f"avd.ini.encoding=UTF-8\npath={AVD}\ntarget=android-30\n",encoding="utf-8")
settings={
    "AvdId":"TrainingPhone", "avd.ini.displayname":"Training Phone (Android 11)",
    "abi.type":"x86_64", "hw.cpu.arch":"x86_64", "hw.cpu.ncore":"2",
    "hw.ramSize":"2048", "hw.lcd.width":"1080", "hw.lcd.height":"1920", "hw.lcd.density":"420",
    "hw.device.name":"pixel_2", "hw.device.manufacturer":"Google", "hw.keyboard":"yes",
    "hw.mainKeys":"no", "hw.gpu.enabled":"yes", "hw.gpu.mode":"swiftshader",
    "hw.audioInput":"yes", "hw.audioOutput":"yes", "hw.gsmModem":"yes",
    "hw.accelerometer":"yes", "hw.sensors.orientation":"yes", "hw.battery":"yes",
    "disk.dataPartition.size":"2G", "image.sysdir.1":"system-images/android-30/google_apis/x86_64/",
    "tag.id":"google_apis", "tag.display":"Google APIs", "PlayStore.enabled":"false",
    "showDeviceFrame":"no", "fastboot.forceColdBoot":"yes", "vm.heapSize":"256",
}
(AVD/"config.ini").write_text("\n".join(f"{k}={v}" for k,v in settings.items())+"\n",encoding="utf-8")
print(f"AVD prepared: {AVD}")
