[app]
title = VintedTracker
package.name = vintedtracker
package.domain = org.alex
icon.filename = icon.png
source.dir = .          # <— hinzugefügt
version = 0.1           # <— hinzugefügt
source.include_exts = py,png,kv,csv,txt
requirements = python3,kivy,flask,pandas,plotly,customtkinter
orientation = portrait
fullscreen = 1
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.deployment_target = 13.0

[buildozer]
log_level = 2
