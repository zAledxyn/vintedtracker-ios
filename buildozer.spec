[app]
title = VintedTracker
package.name = vintedtracker
package.domain = org.alex
version = 0.1

ios.codesign.allowed = 0

requirements = python3,kivy,kivymd,flask,pandas,plotly

orientation = portrait
fullscreen   = 1
ios.deployment_target = 17.0
source.include_exts = py,png,kv,csv,txt

[buildozer]
log_level = 2
