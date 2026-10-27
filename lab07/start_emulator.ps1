$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$env:JAVA_HOME = Join-Path $taskRoot '.tools\jdk'
$env:ANDROID_HOME = Join-Path $taskRoot '.tools\android-sdk'
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:ANDROID_AVD_HOME = Join-Path $taskRoot '.tools\avd'
$taskEmulator = Join-Path $env:ANDROID_HOME 'emulator\emulator.exe'
Start-Process -FilePath $taskEmulator -ArgumentList @('-avd','TrainingPhone','-port','5554','-no-window','-no-boot-anim','-no-snapshot','-gpu','swiftshader','-memory','2048','-cores','2','-no-audio','-no-metrics') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $taskRoot '.tools\emulator-output.log') -RedirectStandardError (Join-Path $taskRoot '.tools\emulator-error.log')
Write-Output 'Emulator started; inspect adb devices and sys.boot_completed.'
