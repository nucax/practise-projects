@echo off
setlocal

rem Prompt for all face entries (press Enter to use the example default shown)
set /p LOOK_R="ui.faces.look_r (default: ( ⚆_⚆) ): "
if "%LOOK_R%"=="" set LOOK_R=( ⚆_⚆)
set /p LOOK_L="ui.faces.look_l (default: (☉_☉ ) ): "
if "%LOOK_L%"=="" set LOOK_L=(☉_☉ )
set /p LOOK_R_HAPPY="ui.faces.look_r_happy (default: ( ◕‿◕) ): "
if "%LOOK_R_HAPPY%"=="" set LOOK_R_HAPPY=( ◕‿◕)
set /p LOOK_L_HAPPY="ui.faces.look_l_happy (default: (◕‿◕ ) ): "
if "%LOOK_L_HAPPY%"=="" set LOOK_L_HAPPY=(◕‿◕ )
set /p SLEEP="ui.faces.sleep (default: (⇀‿‿↼) ): "
if "%SLEEP%"=="" set SLEEP=(⇀‿‿↼)
set /p SLEEP2="ui.faces.sleep2 (default: (≖‿‿≖) ): "
if "%SLEEP2%"=="" set SLEEP2=(≖‿‿≖)
set /p AWAKE="ui.faces.awake (default: (◕‿‿◕) ): "
if "%AWAKE%"=="" set AWAKE=(◕‿‿◕)
set /p BORED="ui.faces.bored (default: (-__-) ): "
if "%BORED%"=="" set BORED=(-__-)
set /p INTENSE="ui.faces.intense (default: (°▃▃°) ): "
if "%INTENSE%"=="" set INTENSE=(°▃▃°)
set /p COOL="ui.faces.cool (default: (⌐■_■) ): "
if "%COOL%"=="" set COOL=(⌐■_■)
set /p HAPPY="ui.faces.happy (default: (•‿‿•) ): "
if "%HAPPY%"=="" set HAPPY=(•‿‿•)
set /p EXCITED="ui.faces.excited (default: (ᵔ◡◡ᵔ) ): "
if "%EXCITED%"=="" set EXCITED=(ᵔ◡◡ᵔ)
set /p GRATEFUL="ui.faces.grateful (default: (^‿‿^) ): "
if "%GRATEFUL%"=="" set GRATEFUL=(^‿‿^)
set /p MOTIVATED="ui.faces.motivated (default: (☼‿‿☼) ): "
if "%MOTIVATED%"=="" set MOTIVATED=(☼‿‿☼)
set /p DEMOTIVATED="ui.faces.demotivated (default: (≖__≖) ): "
if "%DEMOTIVATED%"=="" set DEMOTIVATED=(≖__≖)
set /p SMART="ui.faces.smart (default: (✜‿‿✜) ): "
if "%SMART%"=="" set SMART=(✜‿‿✜)
set /p LONELY="ui.faces.lonely (default: (ب__ب) ): "
if "%LONELY%"=="" set LONELY=(ب__ب)
set /p SAD="ui.faces.sad (default: (╥☁╥ ) ): "
if "%SAD%"=="" set SAD=(╥☁╥ )
set /p ANGRY="ui.faces.angry (default: (-_-') ): "
if "%ANGRY%"=="" set ANGRY=(-_-')
set /p FRIEND="ui.faces.friend (default: (♥‿‿♥) ): "
if "%FRIEND%"=="" set FRIEND=(♥‿‿♥)
set /p BROKEN="ui.faces.broken (default: (☓‿‿☓) ): "
if "%BROKEN%"=="" set BROKEN=(☓‿‿☓)
set /p DEBUG="ui.faces.debug (default: (#__#) ): "
if "%DEBUG%"=="" set DEBUG=(#__#)
set /p UPLOAD="ui.faces.upload (default: (1__0) ): "
if "%UPLOAD%"=="" set UPLOAD=(1__0)
set /p UPLOAD1="ui.faces.upload1 (default: (1__1) ): "
if "%UPLOAD1%"=="" set UPLOAD1=(1__1)
set /p UPLOAD2="ui.faces.upload2 (default: (0__1) ): "
if "%UPLOAD2%"=="" set UPLOAD2=(0__1)

rem Now call PowerShell to write a full config.toml using a here-string.
rem The batch variables are available in PowerShell via $env:VAR_NAME

powershell -NoProfile -Command ^
"$content = @'
main.name = \"Pwnagotchi\"
main.lang = \"en\"
main.whitelist = [
    \"My-Network\",
    \"Another\"
]
main.confd = \"/etc/pwnagotchi/conf.d/\"
main.custom_plugin_repos = [
    \"https://github.com/tisboyo/pwnagotchi-pisugar2-plugin/archive/master.zip\",
    \"https://github.com/nullm0ose/pwnagotchi-plugin-pisugar3/archive/master.zip\",
    \"https://github.com/Sniffleupagus/pwnagotchi_plugins/archive/master.zip\",
    \"https://github.com/NeonLightning/pwny/archive/master.zip\"
]

main.custom_plugins = \"/usr/local/share/pwnagotchi/custom-plugins/\"

main.plugins.auto-update.enabled = true
main.plugins.auto-update.install = true
main.plugins.auto-update.interval = 1

main.plugins.bt-tether.enabled = true

main.plugins.bt-tether.devices.ios-phone.enabled = true
main.plugins.bt-tether.devices.ios-phone.search_order = 2
main.plugins.bt-tether.devices.ios-phone.mac = \"ch:an:ge:me:me:me\"
main.plugins.bt-tether.devices.ios-phone.ip = \"172.20.10.6\"
main.plugins.bt-tether.devices.ios-phone.netmask = 24
main.plugins.bt-tether.devices.ios-phone.interval = 5
main.plugins.bt-tether.devices.ios-phone.scantime = 20
main.plugins.bt-tether.devices.ios-phone.max_tries = 0
main.plugins.bt-tether.devices.ios-phone.share_internet = true
main.plugins.bt-tether.devices.ios-phone.priority = 999

main.plugins.fix_services.enabled = true

main.plugins.gdrivesync.enabled = false
main.plugins.gdrivesync.backupfiles = ['']
main.plugins.gdrivesync.backup_folder = \"PwnagotchiBackups\"
main.plugin.gdrivesync.interval = 1

main.plugins.gpio_buttons.enabled = false

main.plugins.gps.enabled = false
main.plugins.gps.speed = 19200
main.plugins.gps.device = \"/dev/ttyUSB0\" # for GPSD: \"localhost:2947\"

main.plugins.grid.enabled = true
main.plugins.grid.report = true

main.plugins.logtail.enabled = false
main.plugins.logtail.max-lines = 10000

main.plugins.memtemp.enabled = false
main.plugins.memtemp.scale = \"celsius\"
main.plugins.memtemp.orientation = \"horizontal\"

main.plugins.net-pos.enabled = false
main.plugins.net-pos.api_key = \"test\"

main.plugins.onlinehashcrack.enabled = false
main.plugins.onlinehashcrack.email = \"\"
main.plugins.onlinehashcrack.dashboard = \"\"
main.plugins.onlinehashcrack.single_files = false

main.plugins.pisugar2.enabled = false
main.plugins.pisugar2.shutdown = 5
main.plugins.pisugar2.sync_rtc_on_boot = false

main.plugins.session-stats.enabled = true
main.plugins.session-stats.save_directory = \"/var/tmp/pwnagotchi/sessions/\"

main.plugins.ups_hat_c.enabled = false
main.plugins.ups_hat_c.label_on = true  # show BAT label or just percentage
main.plugins.ups_hat_c.shutdown = 5  # battery percent at which the device will turn off
main.plugins.ups_hat_c.bat_x_coord = 140
main.plugins.ups_hat_c.bat_y_coord = 0

main.plugins.ups_lite.enabled = false
main.plugins.ups_lite.shutdown = 2

main.plugins.webcfg.enabled = true

main.plugins.webgpsmap.enabled = false

main.plugins.wigle.enabled = false
main.plugins.wigle.api_key = \"\"
main.plugins.wigle.donate = false

main.plugins.wpa-sec.enabled = false
main.plugins.wpa-sec.api_key = \"\"
main.plugins.wpa-sec.api_url = \"https://wpa-sec.stanev.org\"
main.plugins.wpa-sec.download_results = false

main.iface = \"wlan0mon\"
main.mon_start_cmd = \"/usr/bin/monstart\"
main.mon_stop_cmd = \"/usr/bin/monstop\"
main.mon_max_blind_epochs = 50
main.no_restart = false

main.log.path = \"/etc/pwnagotchi/log/pwnagotchi.log\"
main.log.rotation.enabled = true
main.log.rotation.size = \"10M\"

ai.enabled = true
ai.path = \"/root/brain.nn\"
ai.laziness = 0.1
ai.epochs_per_episode = 50

ai.params.gamma = 0.99
ai.params.n_steps = 1
ai.params.vf_coef = 0.25
ai.params.ent_coef = 0.01
ai.params.max_grad_norm = 0.5
ai.params.learning_rate = 0.001
ai.params.verbose = 1

personality.advertise = true
personality.deauth = true
personality.associate = true
personality.channels = []
personality.min_rssi = -200
personality.ap_ttl = 120
personality.sta_ttl = 300
personality.recon_time = 30
personality.max_inactive_scale = 2
personality.recon_inactive_multiplier = 2
personality.hop_recon_time = 10
personality.min_recon_time = 5
personality.max_interactions = 3
personality.max_misses_for_recon = 5
personality.excited_num_epochs = 10
personality.bored_num_epochs = 15
personality.sad_num_epochs = 25
personality.bond_encounters_factor = 20000
personality.throttle_a = 0.4
personality.throttle_d = 0.9

personality.clear_on_exit = true # clear display when shutting down cleanly

ui.invert = true # false = black background, true = white background

ui.fps = 1
ui.font.name = \"DejaVuSansMono\" # for japanese: fonts-japanese-gothic
ui.font.size_offset = 0 # will be added to the font size

ui.faces.look_r = \"__LOOK_R__\"
ui.faces.look_l = \"__LOOK_L__\"
ui.faces.look_r_happy = \"__LOOK_R_HAPPY__\"
ui.faces.look_l_happy = \"__LOOK_L_HAPPY__\"
ui.faces.sleep = \"__SLEEP__\"
ui.faces.sleep2 = \"__SLEEP2__\"
ui.faces.awake = \"__AWAKE__\"
ui.faces.bored = \"__BORED__\"
ui.faces.intense = \"__INTENSE__\"
ui.faces.cool = \"__COOL__\"
ui.faces.happy = \"__HAPPY__\"
ui.faces.excited = \"__EXCITED__\"
ui.faces.grateful = \"__GRATEFUL__\"
ui.faces.motivated = \"__MOTIVATED__\"
ui.faces.demotivated = \"__DEMOTIVATED__\"
ui.faces.smart = \"__SMART__\"
ui.faces.lonely = \"__LONELY__\"
ui.faces.sad = \"__SAD__\"
ui.faces.angry = \"__ANGRY__\"
ui.faces.friend = \"__FRIEND__\"
ui.faces.broken = \"__BROKEN__\"
ui.faces.debug = \"__DEBUG__\"
ui.faces.upload = \"__UPLOAD__\"
ui.faces.upload1 = \"__UPLOAD1__\"
ui.faces.upload2 = \"__UPLOAD2__\"
ui.faces.png = false
ui.faces.position_x = 0
ui.faces.position_y = 34

ui.web.enabled = true
ui.web.address = \"::\" # listening on both ipv4 and ipv6 - switch to 0.0.0.0 to listen on just ipv4
ui.web.username = \"rpi\"
ui.web.password = \"raspberry\"
ui.web.origin = \"\"
ui.web.port = 8080
ui.web.on_frame = \"\"

ui.display.enabled = true
ui.display.rotation = 0
ui.display.type = \"waveshare_3\"

bettercap.handshakes = \"/root/handshakes\"
bettercap.silence = [
    \"ble.device.new\",
    \"ble.device.lost\",
    \"ble.device.disconnected\",
    \"ble.device.connected\",
    \"ble.device.service.discovered\",
    \"ble.device.characteristic.discovered\",
    \"wifi.client.new\",
    \"wifi.client.lost\",
    \"wifi.client.probe\",
    \"wifi.ap.new\",
    \"wifi.ap.lost\",
    \"mod.started\"
]


fs.memory.enabled = true
fs.memory.mounts.log.enabled = true
fs.memory.mounts.log.mount = \"/etc/pwnagotchi/log/\"
fs.memory.mounts.log.size = \"50M\"
fs.memory.mounts.log.sync = 60
fs.memory.mounts.log.zram = true
fs.memory.mounts.log.rsync = true

fs.memory.mounts.data.enabled = true
fs.memory.mounts.data.mount = \"/var/tmp/pwnagotchi\"
fs.memory.mounts.data.size = \"50M\"
fs.memory.mounts.data.sync = 3600
fs.memory.mounts.data.zram = true
fs.memory.mounts.data.rsync = true
'@

# Replace placeholders with values from environment variables set by the batch file
$content = $content -replace '__LOOK_R__', [System.Text.RegularExpressions.Regex]::Escape($env:LOOK_R)
$content = $content -replace '__LOOK_L__', [System.Text.RegularExpressions.Regex]::Escape($env:LOOK_L)
$content = $content -replace '__LOOK_R_HAPPY__', [System.Text.RegularExpressions.Regex]::Escape($env:LOOK_R_HAPPY)
$content = $content -replace '__LOOK_L_HAPPY__', [System.Text.RegularExpressions.Regex]::Escape($env:LOOK_L_HAPPY)
$content = $content -replace '__SLEEP__', [System.Text.RegularExpressions.Regex]::Escape($env:SLEEP)
$content = $content -replace '__SLEEP2__', [System.Text.RegularExpressions.Regex]::Escape($env:SLEEP2)
$content = $content -replace '__AWAKE__', [System.Text.RegularExpressions.Regex]::Escape($env:AWAKE)
$content = $content -replace '__BORED__', [System.Text.RegularExpressions.Regex]::Escape($env:BORED)
$content = $content -replace '__INTENSE__', [System.Text.RegularExpressions.Regex]::Escape($env:INTENSE)
$content = $content -replace '__COOL__', [System.Text.RegularExpressions.Regex]::Escape($env:COOL)
$content = $content -replace '__HAPPY__', [System.Text.RegularExpressions.Regex]::Escape($env:HAPPY)
$content = $content -replace '__EXCITED__', [System.Text.RegularExpressions.Regex]::Escape($env:EXCITED)
$content = $content -replace '__GRATEFUL__', [System.Text.RegularExpressions.Regex]::Escape($env:GRATEFUL)
$content = $content -replace '__MOTIVATED__', [System.Text.RegularExpressions.Regex]::Escape($env:MOTIVATED)
$content = $content -replace '__DEMOTIVATED__', [System.Text.RegularExpressions.Regex]::Escape($env:DEMOTIVATED)
$content = $content -replace '__SMART__', [System.Text.RegularExpressions.Regex]::Escape($env:SMART)
$content = $content -replace '__LONELY__', [System.Text.RegularExpressions.Regex]::Escape($env:LONELY)
$content = $content -replace '__SAD__', [System.Text.RegularExpressions.Regex]::Escape($env:SAD)
$content = $content -replace '__ANGRY__', [System.Text.RegularExpressions.Regex]::Escape($env:ANGRY)
$content = $content -replace '__FRIEND__', [System.Text.RegularExpressions.Regex]::Escape($env:FRIEND)
$content = $content -replace '__BROKEN__', [System.Text.RegularExpressions.Regex]::Escape($env:BROKEN)
$content = $content -replace '__DEBUG__', [System.Text.RegularExpressions.Regex]::Escape($env:DEBUG)
$content = $content -replace '__UPLOAD__', [System.Text.RegularExpressions.Regex]::Escape($env:UPLOAD)
$content = $content -replace '__UPLOAD1__', [System.Text.RegularExpressions.Regex]::Escape($env:UPLOAD1)
$content = $content -replace '__UPLOAD2__', [System.Text.RegularExpressions.Regex]::Escape($env:UPLOAD2)

# Save as config.toml (overwrites if exists)
Set-Content -Path '.\config.toml' -Value $content -Encoding UTF8

Write-Output 'config.toml written to the current folder.'
" 

echo Done. config.toml created in this folder.
pause
endlocal
