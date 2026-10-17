-- desktop-style window switcher begin
hl.bind("ALT + Tab", hl.dsp.global("desktop-style:window-next"))
hl.bind("ALT + SHIFT + Tab", hl.dsp.global("desktop-style:window-previous"))
hl.bind("Alt_L", hl.dsp.global("desktop-style:window-accept"), { release = true, ignore_mods = true, non_consuming = true })
hl.bind("Alt_R", hl.dsp.global("desktop-style:window-accept"), { release = true, ignore_mods = true, non_consuming = true })
-- desktop-style window switcher end
