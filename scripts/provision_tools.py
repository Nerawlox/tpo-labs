"""Download isolated official development tools under .tools (not committed)."""
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / ".tools"
TOOLS.mkdir(exist_ok=True)


def download(url, target):
    target = Path(target)
    if target.exists():
        return target
    response = requests.get(url, stream=True, timeout=180)
    response.raise_for_status()
    temporary = target.with_suffix(target.suffix + ".part")
    with temporary.open("wb") as stream:
        for chunk in response.iter_content(1024 * 1024):
            stream.write(chunk)
    temporary.replace(target)
    print(f"Downloaded {target.name}: {target.stat().st_size // 1024**2} MB", flush=True)
    return target


def jdk():
    destination = TOOLS / "jdk"
    if (destination / "bin" / "java.exe").exists():
        return destination
    info = requests.get("https://api.adoptium.net/v3/assets/latest/21/hotspot", params={"architecture":"x64","image_type":"jdk","os":"windows","vendor":"eclipse"}, timeout=60)
    info.raise_for_status()
    archive = download(info.json()[0]["binary"]["package"]["link"], TOOLS / "jdk.zip")
    with zipfile.ZipFile(archive) as file:
        base = file.namelist()[0].split('/')[0]
        file.extractall(TOOLS / "jdk-unpack")
    shutil.move(str(TOOLS / "jdk-unpack" / base), destination)
    return destination


def android_tools():
    sdk = TOOLS / "android-sdk"
    destination = sdk / "cmdline-tools" / "latest"
    if (destination / "bin" / "sdkmanager.bat").exists():
        return sdk
    response = requests.get("https://dl.google.com/android/repository/repository2-1.xml", timeout=90)
    response.raise_for_status()
    tree = ET.fromstring(response.content)
    package = next(p for p in tree.findall("remotePackage") if p.attrib.get("path") == "cmdline-tools;latest")
    url = next(a.find("complete/url").text for a in package.findall("archives/archive") if a.findtext("host-os") == "windows")
    archive = download("https://dl.google.com/android/repository/" + url, TOOLS / "android-tools.zip")
    with zipfile.ZipFile(archive) as file:
        file.extractall(TOOLS / "android-tools-unpack")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(TOOLS / "android-tools-unpack" / "cmdline-tools"), destination)
    return sdk


def k6():
    destination = TOOLS / "k6"
    if list(destination.glob("**/k6.exe")):
        return
    release = requests.get("https://github.com/grafana/k6/releases/latest", timeout=60)
    release.raise_for_status()
    version = release.url.rstrip('/').split('/')[-1]
    url = f"https://github.com/grafana/k6/releases/download/{version}/k6-{version}-windows-amd64.zip"
    archive = download(url, TOOLS / "k6.zip")
    with zipfile.ZipFile(archive) as file:
        file.extractall(destination)
    print("k6 ready", flush=True)


def postman():
    destination = TOOLS / "postman"
    if (destination / "postman-cli.exe").exists():
        return
    archive = download("https://dl-cli.pstmn.io/download/latest/win64", TOOLS / "postman.zip")
    with zipfile.ZipFile(archive) as file:
        file.extractall(destination)
    print("Postman CLI ready", flush=True)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        tasks = [pool.submit(fn) for fn in (jdk, android_tools, k6, postman)]
        values = [task.result() for task in tasks]
    java, sdk = values[:2]
    environment = os.environ | {"JAVA_HOME":str(java), "ANDROID_HOME":str(sdk), "ANDROID_SDK_ROOT":str(sdk)}
    manager = sdk / "cmdline-tools/latest/bin/android.exe"
    packages = ["platform-tools", "platforms/android-35", "build-tools/35.0.0", "emulator", "system-images/android-30/google_apis/x86_64"]
    print("Installing Android SDK packages", flush=True)
    for package in packages:
        with (TOOLS / ("sdk-" + package.replace('/', '-') + ".log")).open("w",encoding="utf-8") as log:
            run = subprocess.run([str(manager), f"--sdk={sdk}", "sdk", "install", package], env=environment, stdout=log, stderr=subprocess.STDOUT)
        print(f"{package}: exit {run.returncode}", flush=True)
        run.check_returncode()
    for required in ["platforms/android-35/android.jar", "build-tools/35.0.0/aapt2.exe", "system-images/android-30/google_apis/x86_64/system.img"]:
        if not (sdk / required).exists():
            raise RuntimeError(f"Missing SDK file: {required}")
