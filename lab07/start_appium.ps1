$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$env:JAVA_HOME = Join-Path $taskRoot '.tools\jdk'
$env:ANDROID_HOME = Join-Path $taskRoot '.tools\android-sdk'
$env:ANDROID_SDK_ROOT = $env:ANDROID_HOME
$env:APPIUM_HOME = Join-Path $taskRoot '.tools\appium-home'
& (Join-Path $taskRoot '.tools\appium\node_modules\.bin\appium.cmd') --address 127.0.0.1 --port 4723 --log-no-colors --log-timestamp --log (Join-Path $taskRoot 'lab07\results\appium-server.log')
