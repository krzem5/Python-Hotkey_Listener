import hotkey



hotkey.init()
hotkey.register("ctrl+alt+shift+J",lambda:(print("Hotkey!"),False)[1])
hotkey.loop()
