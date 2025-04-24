[app]
title = VintedTracker
package.name = vintedtracker
package.domain = org.alex
icon.filename = icon.png
source.dir = .
version = 0.1
source.include_exts = py,png,kv,csv,txt
requirements = python3,kivy,kivymd,flask,pandas,plotly
orientation = portrait
fullscreen = 1
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.deployment_target = 13.0
ios.codesign.allowed = False   # ← neu, wichtig!

[buildozer]
log_level = 2
