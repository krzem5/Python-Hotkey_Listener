import ctypes
import ctypes.wintypes
import traceback
import atexit



WM_KEYDOWN=0x0100
WM_SYSKEYDOWN=0x0104
WH_KEYBOARD_LL=13
VK_PACKET=0xe7
LLKHF_INJECTED=0x10
LLKHF_ALTDOWN=0x20
PM_REMOVE=1



ctypes.wintypes.ULONG_PTR=ctypes.POINTER(ctypes.wintypes.DWORD)
ctypes.wintypes.LRESULT=ctypes.c_int
ctypes.wintypes.LowLevelKeyboardProc=ctypes.WINFUNCTYPE(ctypes.c_int,ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.wintypes.KBDLLHOOKSTRUCT=type("KBDLLHOOKSTRUCT",(ctypes.Structure,),{"_fields_":[("vk_code",ctypes.wintypes.DWORD),("scan_code",ctypes.wintypes.DWORD),("flags",ctypes.wintypes.DWORD),("time",ctypes.c_int),("dwExtraInfo",ctypes.wintypes.ULONG_PTR)]})
ctypes.windll.kernel32.GetModuleHandleW.argtypes=(ctypes.wintypes.LPCWSTR,)
ctypes.windll.kernel32.GetModuleHandleW.restype=ctypes.wintypes.HMODULE
ctypes.windll.user32.CallNextHookEx.argtypes=(ctypes.POINTER(ctypes.wintypes.HHOOK),ctypes.c_int,ctypes.wintypes.WPARAM,ctypes.wintypes.LPARAM)
ctypes.windll.user32.CallNextHookEx.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.DispatchMessageW.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.DispatchMessageW.restype=ctypes.wintypes.LRESULT
ctypes.windll.user32.PeekMessageW.argtypes=(ctypes.wintypes.LPMSG,ctypes.wintypes.HWND,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint)
ctypes.windll.user32.PeekMessageW.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.SetWindowsHookExW.argtypes=(ctypes.c_int,ctypes.wintypes.LowLevelKeyboardProc,ctypes.wintypes.HINSTANCE,ctypes.wintypes.DWORD)
ctypes.windll.user32.SetWindowsHookExW.restype=ctypes.wintypes.HHOOK
ctypes.windll.user32.TranslateMessage.argtypes=(ctypes.wintypes.LPMSG,)
ctypes.windll.user32.TranslateMessage.restype=ctypes.wintypes.BOOL
ctypes.windll.user32.UnhookWindowsHookEx.argtypes=(ctypes.wintypes.HHOOK,)
ctypes.windll.user32.UnhookWindowsHookEx.restype=ctypes.wintypes.BOOL



VK_KEYS={"cancel":0x03,"backspace":0x08,"tab":0x09,"clear":0x0c,"enter":0x0d,"shift":0x10,"ctrl":0x11,"alt":0x12,"pause":0x13,"capslock":0x14,"esc":0x1b,"spacebar":0x20,"pageup":0x21,"pagedown":0x22,"end":0x23,"home":0x24,"left":0x25,"up":0x26,"right":0x27,"down":0x28,"select":0x29,"print":0x2a,"execute":0x2b,"printscreen":0x2c,"insert":0x2d,"delete":0x2e,"help":0x2f,"0":0x30,"1":0x31,"2":0x32,"3":0x33,"4":0x34,"5":0x35,"6":0x36,"7":0x37,"8":0x38,"9":0x39,"a":0x41,"b":0x42,"c":0x43,"d":0x44,"e":0x45,"f":0x46,"g":0x47,"h":0x48,"i":0x49,"j":0x4a,"k":0x4b,"l":0x4c,"m":0x4d,"n":0x4e,"o":0x4f,"p":0x50,"q":0x51,"r":0x52,"s":0x53,"t":0x54,"u":0x55,"v":0x56,"w":0x57,"x":0x58,"y":0x59,"z":0x5a,"leftwindows":0xffff,"rightwindows":0xffff,"apps":0x5d,"sleep":0x5f,"0":0x60,"1":0x61,"2":0x62,"3":0x63,"4":0x64,"5":0x65,"6":0x66,"7":0x67,"8":0x68,"9":0x69,"*":0x6a,"+":0x6b,"separator":0x6c,"-":0x6d,"decimal":0x6e,"/":0x6f,"f1":0x70,"f2":0x71,"f3":0x72,"f4":0x73,"f5":0x74,"f6":0x75,"f7":0x76,"f8":0x77,"f9":0x78,"f10":0x79,"f11":0x7a,"f12":0x7b,"f13":0x7c,"f14":0x7d,"f15":0x7e,"f16":0x7f,"f17":0x80,"f18":0x81,"f19":0x82,"f20":0x83,"f21":0x84,"f22":0x85,"f23":0x86,"f24":0x87,"numlock":0x90,"scrolllock":0x91,"leftshift":0x10,"rightshift":0x10,"leftctrl":0x11,"rightctrl":0x11,"leftmenu":0x12,"rightmenu":0x12,"volumemute":0xad,"volumedown":0xae,"volumeup":0xaf,";":0xba,"+":0xbb,",":0xbc,"-":0xbd,".":0xbe,"/":0xbf,"`":0xc0,"[":0xdb,"\\":0xdc,"]":0xdd,"'":0xde,"windows":0xffff}
VK_SAME_KEYS={0x5b:0xffff,0x5c:0xffff,0xa0:0x10,0xa1:0x10,0xa2:0x11,0xa2:0x11,0xa4:0x12,0xa5:0x12}
for k,v in VK_KEYS.items():
	if (v in VK_SAME_KEYS):
		VK_KEYS[k]=VK_SAME_KEYS[v]



def init():
	def _handle(c,wp,lp):
		try:
			dt=ctypes.cast(lp,ctypes.POINTER(ctypes.wintypes.KBDLLHOOKSTRUCT)).contents
			if (dt.vk_code!=VK_PACKET and dt.flags&(LLKHF_INJECTED|LLKHF_ALTDOWN)!=LLKHF_INJECTED|LLKHF_ALTDOWN):
				if (dt.vk_code==0xa5 and _handle._ig_alt):
					_handle._ig_alt=False
				else:
					if (dt.scan_code==0x21d and dt.vk_code==0xa2):
						_handle._ig_alt=True
					if (dt.vk_code in VK_SAME_KEYS):
						dt.vk_code=VK_SAME_KEYS[dt.vk_code]
					if (dt.vk_code in VK_KEYS.values()):
						init._kb[dt.vk_code]=(wp in (WM_KEYDOWN,WM_SYSKEYDOWN))
						if (init._kb[dt.vk_code]):
							for k,v in init._hk:
								if (dt.vk_code in k):
									for e in k:
										if (not init._kb[e]):
											v=None
											break
									if (v is not None):
										if (v()):
											return -1
		except Exception as e:
			traceback.print_exception(None,e,e.__traceback__)
		return ctypes.windll.user32.CallNextHookEx(None,c,wp,lp)
	if (not hasattr(init,"_hk")):
		init._hk=[]
		init._kb={e:False for e in VK_KEYS.values()}
	_handle._ig_alt=False
	kb_cb=ctypes.wintypes.LowLevelKeyboardProc(_handle)
	ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL,kb_cb,ctypes.windll.kernel32.GetModuleHandleW(None),ctypes.wintypes.DWORD(0))
	atexit.register(ctypes.windll.user32.UnhookWindowsHookEx,kb_cb)



def register(hk,cb):
	if (not hasattr(init,"_hk")):
		init._hk=[]
		init._kb={e:False for e in VK_KEYS.values()}
	o=[]
	for e in hk.lower().split("+"):
		if (e not in VK_KEYS):
			raise RuntimeError(f"Unknown Key '{e}'!")
		o+=[VK_KEYS[e]]
	init._hk+=[(tuple(o),cb)]



def loop():
	msg=ctypes.wintypes.LPMSG()
	while (True):
		if (ctypes.windll.user32.PeekMessageW(msg,None,0,0,PM_REMOVE)!=0):
			ctypes.windll.user32.TranslateMessage(msg)
			ctypes.windll.user32.DispatchMessageW(msg)
