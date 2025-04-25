[app]
title = VintedTracker
package.name = vintedtracker
package.domain = org.alex
source.dir = .
version = 0.1
requirements = python3,kivy,kivymd,flask==2.2.3,click==8.1.3,pandas,numpy,plotly,customtkinter,tkhtmlview
orientation = portrait
fullscreen = 1
ios.codesign.allowed = false   # 0 oder false, beides gilt

[ios]
kivy_ios_url = https://github.com/kivy/kivy-ios
deployment_target = 13.0
codesign.allowed = false     # unsigniert für TrollStore

[buildozer]
log_level = 2
