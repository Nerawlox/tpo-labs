"""Build a small native APK with Android SDK tools; no Gradle dependency."""
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "lab07"
TOOLS = ROOT / ".tools"
JDK = Path(os.environ.get("JAVA_HOME", str(TOOLS / "jdk")))
SDK = Path(os.environ.get("ANDROID_HOME", str(TOOLS / "android-sdk")))
BUILD = LAB / "build"
OUTPUT = LAB / "artifacts"
ENV = os.environ | {"JAVA_HOME":str(JDK)}


def run(command, cwd=None):
    result = subprocess.run([str(x) for x in command], cwd=cwd or LAB, env=ENV, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(result.stdout, end="")
    print(result.stderr, end="")
    result.check_returncode()


if __name__ == "__main__":
    BUILD.mkdir(exist_ok=True)
    OUTPUT.mkdir(exist_ok=True)
    classes = BUILD / "classes"; classes.mkdir(exist_ok=True)
    dex = BUILD / "dex"; dex.mkdir(exist_ok=True)
    sdk_tools = SDK / "build-tools/35.0.0"
    android_jar = SDK / "platforms/android-35/android.jar"
    sources = list((LAB / "src").rglob("*.java"))
    run([JDK/"bin/javac.exe","-encoding","UTF-8","-source","8","-target","8","-bootclasspath",android_jar,"-d",classes,*sources])
    run([JDK/"bin/jar.exe","cf",BUILD/"classes.jar","-C",classes,"."])
    run([sdk_tools/"d8.bat","--lib",android_jar,"--output",dex,BUILD/"classes.jar"])
    unsigned = BUILD / "unsigned.apk"
    run([sdk_tools/"aapt2.exe","link","--manifest",LAB/"AndroidManifest.xml","-I",android_jar,"-o",unsigned])
    with zipfile.ZipFile(unsigned,"a") as package:
        package.write(dex/"classes.dex","classes.dex")
    aligned = BUILD / "aligned.apk"
    run([sdk_tools/"zipalign.exe","-f","4",unsigned,aligned])
    keystore = TOOLS / "android-debug.keystore"
    if not keystore.exists():
        run([JDK/"bin/keytool.exe","-genkeypair","-keystore",keystore,"-storepass","android","-keypass","android","-alias","androiddebugkey","-keyalg","RSA","-keysize","2048","-validity","10000","-dname","CN=Android Debug,O=Android,C=US"])
    apk = OUTPUT / "study-notes.apk"
    run([sdk_tools/"apksigner.bat","sign","--ks",keystore,"--ks-pass","pass:android","--key-pass","pass:android","--out",apk,aligned])
    run([sdk_tools/"apksigner.bat","verify","--verbose",apk])
    print(f"APK: {apk}")
