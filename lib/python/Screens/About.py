from Screen import Screen
from Components.config import config
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button
from Components.config import config

from Components.Pixmap import MultiPixmap
from Components.Network import iNetwork

from Components.Label import Label
from Components.ProgressBar import ProgressBar
from os import popen
from Tools.StbHardware import getFPVersion

from boxbranding import getBoxType
boxtype = getBoxType()

from enigma import eTimer, eLabel, eConsoleAppContainer

from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
import skin


class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		hddsplit = skin.parameters.get("AboutHddSplit", 0)

		#AboutHddSplit = 0
		#try:
		#	hddsplit = skin.parameters.get("AboutHddSplit",(0))[0]
		#except:
		#	hddsplit = AboutHddSplit

		if boxtype == 'gb800solo':
			BoxName = "GigaBlue HD 800SOLO"
		elif boxtype == 'gb800se':
			BoxName = "GigaBlue HD 800SE"
		elif boxtype == 'gb800ue':
			BoxName = "GigaBlue HD 800UE"
		elif boxtype == 'gbquad':
			BoxName = "GigaBlue HD Quad"
		elif boxtype == 'gbuhdquad':
			BoxName = "GigaBlue UHD Quad"
		elif boxtype == 'gbquadplus':
			BoxName = "GigaBlue HD Quadplus"
		elif boxtype == 'gb800seplus':
			BoxName = "GigaBlue HD 800SEplus"
		elif boxtype == 'gb800ueplus':
			BoxName = "GigaBlue HD 800UEplus"
		elif boxtype == 'gbipbox':
			BoxName = "GigaBlue IP Box"
		elif boxtype == 'gbultra':
			BoxName = "GigaBlue HD Ultra"
		elif boxtype == 'gbultraue':
			BoxName = "GigaBlue HD Ultra UE"
		elif boxtype == 'gbultrase':
			BoxName = "GigaBlue HD Ultra SE"
		elif boxtype == 'gbx1':
			BoxName = "GigaBlue X1"
		elif boxtype == 'gbx2':
			BoxName = "GigaBlue X2"
		elif boxtype == 'gbx3':
			BoxName = "GigaBlue X3"
		elif boxtype == 'spycat':
			BoxName = "XCORE Spycat"
		elif boxtype == 'quadbox2400':
			BoxName = "AX Quadbox HD2400"
		else:
			BoxName = about.getHardwareTypeString()

		self.setTitle(_("About") + " " + BoxName)

		ImageType = about.getImageTypeString()
		self["ImageType"] = StaticText(ImageType)

		Boxserial = popen('cat /proc/stb/info/sn').read().strip()
		serial = ""
		if Boxserial != "":
			serial = ":Serial : " + Boxserial

		AboutHeader = _("About") + " " + BoxName 
		self["AboutHeader"] = StaticText(AboutHeader)

		AboutText = BoxName + " - " + ImageType + serial + "\n"

		#AboutText += _("Hardware: ") + about.getHardwareTypeString() + "\n"
		#AboutText += _("CPU: ") + about.getCPUInfoString() + "\n"
		#AboutText += _("Installed: ") + about.getFlashDateString() + "\n"
		#AboutText += _("Image: ") + about.getImageTypeString() + "\n"

		CPUinfo = _("CPU: ") + about.getCPUInfoString()
		self["CPUinfo"] = StaticText(CPUinfo)
		AboutText += CPUinfo + "\n"

		CPUspeed = _("Speed: ") + about.getCPUSpeedString()
		self["CPUspeed"] = StaticText(CPUspeed)
		#AboutText += "(" + about.getCPUSpeedString() + ")\n"

		ChipsetInfo = _("Chipset: ") + about.getChipSetString()
		self["ChipsetInfo"] = StaticText(ChipsetInfo)
		AboutText += ChipsetInfo + "\n"

		fp_version = getFPVersion()
		if fp_version is None:
			fp_version = ""
		else:
			fp_version = _("Frontprocessor version: %d") % fp_version
			#AboutText += fp_version +"\n"
		self["FPVersion"] = StaticText(fp_version) 

		AboutText += "\n"

		KernelVersion = _("Kernel version: ") + about.getKernelVersionString()
		self["KernelVersion"] = StaticText(KernelVersion)
		AboutText += KernelVersion + "\n"

		AboutText += _("DVB drivers: ") + self.realDriverDate() + "\n"
		#AboutText += _("DVB drivers: ") + about.getDriverInstalledDate() + "\n"

		EnigmaVersion = _("GUI Build: ") + about.getEnigmaVersionString() + "\n"
		self["EnigmaVersion"] = StaticText(EnigmaVersion)
		#AboutText += EnigmaVersion

		#AboutText += _("Enigma (re)starts: %d\n") % config.misc.startCounter.value

		FlashDate = _("Flashed: ") + about.getFlashDateString()
		self["FlashDate"] = StaticText(FlashDate)
		AboutText += FlashDate + "\n"

		ImageVersion = _("Last upgrade: ") + about.getImageVersionString()
		self["ImageVersion"] = StaticText(ImageVersion)
		AboutText += ImageVersion + "\n"

		EnigmaSkin = _("Skin: ") + config.skin.primary_skin.value[0:-9]
		self["EnigmaSkin"] = StaticText(EnigmaSkin)
		AboutText += EnigmaSkin + "\n"

		AboutText += _("Python version: ") + about.getPythonVersionString() + "\n"

		GStreamerVersion = _("GStreamer: ") + about.getGStreamerVersionString().replace("GStreamer","")
		self["GStreamerVersion"] = StaticText(GStreamerVersion)
		AboutText += GStreamerVersion + "\n"

		AboutText += "\n"
		self["TunerHeader"] = StaticText(_("Detected NIMs:"))
		#AboutText += _("Detected NIMs:") + "\n"

		nims = nimmanager.nimList(showFBCTuners=False)
		for count in range(len(nims)):
			if count < 4:
				self["Tuner" + str(count)] = StaticText(nims[count])
			else:
				self["Tuner" + str(count)] = StaticText("")
			AboutText += nims[count] + "\n"

		self["HDDHeader"] = StaticText(_("Detected HDD:"))

		AboutText += "\n"
		#AboutText +=  _("Detected HDD:") + "\n"
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			formatstring = hddsplit and "%s:%s, %.1f %sB %s" or "%s:(%s, %.1f %sB %s)"
			for count in range(len(hddlist)):
				if hddinfo:
					hddinfo += "\n"
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					hddinfo += formatstring % (hdd.model(), hdd.capacity(), hdd.free()/1024.0, "G", _("free"))
				else:
					hddinfo += formatstring % (hdd.model(), hdd.capacity(), hdd.free(), "M", _("free"))
		else:
			hddinfo = _("none")
		self["hddA"] = StaticText(hddinfo)
		AboutText += hddinfo 
		
		#AboutText += "\n\n" + _("Network Info") 
		#for x in about.GetIPsFromNetworkInterfaces():
		#	AboutText += "\n" + iNetwork.getFriendlyAdapterDescription(x[0]) + " :" + "/dev/" + x[0] + " " + x[1]

		self["AboutScrollLabel"] = ScrollLabel(AboutText)
		self["key_green"] = Button(_("Translations"))
		self["key_red"] = Button(_("Latest Commits"))
		self["key_blue"] = Button(_("Memory Info"))
		self["key_yellow"] = Button(_("Contact Info"))
		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"red": self.showCommits,
				"green": self.showTranslationInfo,
				"blue": self.showMemoryInfo,
				"yellow": self.showContactInfo,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

	def showTranslationInfo(self):
		self.session.open(TranslationInfo)

	def showContactInfo(self):
		self.session.open(ContactInfo)

	def showCommits(self):
		self.session.open(CommitInfo)

	def showMemoryInfo(self):
		self.session.open(MemoryInfo)

	def realDriverDate(self):
		realdate = about.getDriverInstalledDate()
		try:
			y = popen('lsmod').read().strip()
			if 'dvb' in y:
				drivername='dvb'
				x = popen('modinfo '+ drivername +' |grep -i version')
				x = x.read().strip().split()
				date = x[1];date = date[:14];b=date
				YY=b[0:4];MM=b[4:6];DD=b[6:8];HO=b[8:10];MI=b[10:12];SE=b[12:14]
				realdate=str(DD + '.' + MM + '.' + YY + ' - ' + HO  + ':' + MI + ':' + SE)
		except:
			realdate = about.getDriverInstalledDate()
		return realdate

class TranslationInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Translation"))
		# don't remove the string out of the _(), or it can't be "translated" anymore.
		# TRANSLATORS: Add here whatever should be shown in the "translator" about screen, up to 6 lines (use \n for newline)
		info = _("TRANSLATOR_INFO")
		if info == "TRANSLATOR_INFO":
			info = "(N/A)"

		infolines = _("").split("\n")
		infomap = {}
		for x in infolines:
			l = x.split(': ')
			if len(l) != 2:
				continue
			(type, value) = l
			infomap[type] = value
		#print infomap
		self["actions"] = ActionMap(["SetupActions"],{"cancel": self.close,"ok": self.close})

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")
		self["TranslatorName"] = StaticText(translator_name)

		linfo= ""
		linfo += _("Translations Info")		+ ":" + "\n\n"
		linfo += _("Project")				+ ":" + infomap.get("Project-Id-Version", "") + "\n"
		linfo += _("Language")				+ ":" + infomap.get("Language", "") + "\n"
		print infomap.get("Language-Team", "")
		if infomap.get("Language-Team", "") == "" or infomap.get("Language-Team", "") == "none":
			linfo += _("Language Team") 	+ ":" + "n/a"  + "\n"
		else:
			linfo += _("Language Team") 	+ ":" + infomap.get("Language-Team", "")  + "\n"
		linfo += _("Last Translator") 		+ ":" + translator_name + "\n"
		linfo += "\n"
		linfo += _("Source Charset")		+ ":" + infomap.get("X-Poedit-SourceCharset", "") + "\n"
		linfo += _("Content Type")			+ ":" + infomap.get("Content-Type", "") + "\n"
		linfo += _("Content Encoding")		+ ":" + infomap.get("Content-Transfer-Encoding", "") + "\n"
		linfo += _("MIME Version")			+ ":" + infomap.get("MIME-Version", "") + "\n"
		linfo += "\n"
		linfo += _("POT-Creation Date")		+ ":" + infomap.get("POT-Creation-Date", "") + "\n"
		linfo += _("Revision Date")			+ ":" + infomap.get("PO-Revision-Date", "") + "\n"
		linfo += "\n"
		linfo += _("Generator")				+ ":" + infomap.get("X-Generator", "") + "\n"

		if infomap.get("Report-Msgid-Bugs-To", "") != "":
			linfo += _("Report Msgid Bugs To")	+ ":" + infomap.get("Report-Msgid-Bugs-To", "") + "\n"
		else:
			linfo += _("Report Msgid Bugs To")	+ ":" + "arn354@email.de" + "\n"
		self["AboutScrollLabel"] = ScrollLabel(linfo)


class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.setTitle(_("Latest Commits"))
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))
		self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
				"left": self.left,
				"right": self.right,
				"deleteBackward": self.left,
				"deleteForward": self.right
			})

		self["key_red"] = Button(_("Cancel"))

		self.project = 0
		self.projects = [
			#("organisation",  "repository",           "readable name",                "branch"),
			("openmips",      "stbgui",               "openMips Enigma2",             "master"),
			("openmips",      "skin-pax",             "openMips Skin GigaBlue Pax",   "master"),
			("oe-alliance",   "oe-alliance-core",     "OE Alliance Core",             "3.4"),
			("oe-alliance",   "oe-alliance-plugins",  "OE Alliance Plugins",          "2.3"),
			("oe-alliance",   "enigma2-plugins",      "OE Alliance Enigma2 Plugins",  "2.3")
		]
		self.cachedProjects = {}
		self.Timer = eTimer()
		self.Timer.callback.append(self.readGithubCommitLogs)
		self.Timer.start(50, True)

	def readGithubCommitLogs(self):
		url = 'https://api.github.com/repos/%s/%s/commits?sha=%s' % (self.projects[self.project][0], self.projects[self.project][1], self.projects[self.project][3])
		# print "[About] url: ", url
		commitlog = ""
		from datetime import datetime
		from json import loads
		from urllib2 import urlopen
		try:
			commitlog += 80 * '-' + '\n'
			commitlog += self.projects[self.project][2] + ' - ' + self.projects[self.project][1] + ' - branch:' + self.projects[self.project][3] + '\n'
			commitlog += 'URL: https://github.com/' + self.projects[self.project][0] + '/' + self.projects[self.project][1] + '/tree/' + self.projects[self.project][3] + '\n'
			commitlog += 80 * '-' + '\n'
			for c in loads(urlopen(url, timeout=5).read()):
				creator = c['commit']['author']['name']
				title = c['commit']['message']
				date = datetime.strptime(c['commit']['committer']['date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%x %X')
				if title.startswith ("Merge "):
					pass
				else:
					commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
			commitlog = commitlog.encode('utf-8')
			self.cachedProjects[self.projects[self.project][2]] = commitlog
		except:
			commitlog += _("Currently the commit log cannot be retrieved - please try later again")
		self["AboutScrollLabel"].setText(commitlog)

	def updateCommitLogs(self):
		if self.cachedProjects.has_key(self.projects[self.project][2]):
			self["AboutScrollLabel"].setText(self.cachedProjects[self.projects[self.project][2]])
		else:
			self["AboutScrollLabel"].setText(_("Please wait"))
			self.Timer.start(50, True)

	def left(self):
		self.project = self.project == 0 and len(self.projects) - 1 or self.project - 1
		self.updateCommitLogs()

	def right(self):
		self.project = self.project != len(self.projects) - 1 and self.project + 1 or 0
		self.updateCommitLogs()

class ContactInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self["actions"] = ActionMap(["SetupActions"],{"cancel": self.close,"ok": self.close})
		self.setTitle(_("Manufacturer info"))
		self["manufacturerinfo"] = StaticText(self.getManufacturerinfo())

	def getManufacturerinfo(self):
		minfo = "Impex-Sat GmbH & Co. KG\n"
		minfo += "Beim Gie\xc3\x9fhaus 7\n"
		minfo += "(D) 25348 Gl\xc3\xbcckstadt\n\n"
		minfo += _("Phone") + "\t+49 4124 937262\n"
		minfo += "Fax\t+49 4124 937266\n\n"
		minfo += _("Store") + "\thttp://store.impex-sat.de\n"
		minfo += "eMail\tinfo@impex-sat.de\n"
		minfo += "eMail\tbestellung@impex-sat.de\n\n"
		minfo += _("Monday")   + "\t10:00 - 18:00\n"
		minfo += _("Tuesday")  + "\t10:00 - 18:00\n"
		minfo += _("Wednesday")+ "\t10:00 - 18:00\n"
		minfo += _("Thursday") + "\t10:00 - 18:00\n"
		minfo += _("Friday")   + "\t10:00 - 18:00\n"
		return minfo

class MemoryInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self["actions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"cancel": self.close,
				"ok": self.getMemoryInfo,
				"green": self.getMemoryInfo,
				"blue": self.clearMemory,
			})
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("Refresh"))
		self["key_blue"] = Label(_("Clear"))
		self['lmemtext'] = Label()
		self['lmemvalue'] = Label()
		self['rmemtext'] = Label()
		self['rmemvalue'] = Label()
		self['pfree'] = Label()
		self['pused'] = Label()
		self["slide"] = ProgressBar()
		self["slide"].setValue(100)
		self["params"] = MemoryInfoSkinParams()
		self.setTitle(_("MemoryInfo - only for Developers"))
		self['info'] = Label(_("This info is for developers only.\nIt is not important for a normal user.\nPlease - do not panic on any displayed suspicious information!"))
		self.onLayoutFinish.append(self.getMemoryInfo)

	def getMemoryInfo(self):
		try:
			ltext = rtext = ""
			lvalue = rvalue = ""
			mem = 1
			free = 0
			rows_in_column = self["params"].rows_in_column
			for i, line in enumerate(open('/proc/meminfo','r')):
				s = line.strip().split(None, 2)
				if len(s) == 3:
					name, size, units = s
				elif len(s) == 2:
					name, size = s
					units = ""
				else:
					continue
				if name.startswith("MemTotal"):
					mem = int(size)
				if name.startswith("MemFree") or name.startswith("Buffers") or name.startswith("Cached"):
					free += int(size)
				if i < rows_in_column:
					ltext += "".join((name,"\n"))
					lvalue += "".join((size," ",units,"\n"))
				else:
					rtext += "".join((name,"\n"))
					rvalue += "".join((size," ",units,"\n"))
			self['lmemtext'].setText(ltext)
			self['lmemvalue'].setText(lvalue)
			self['rmemtext'].setText(rtext)
			self['rmemvalue'].setText(rvalue)
			self["slide"].setValue(int(100.0*(mem-free)/mem+0.25))
			self['pfree'].setText("%.1f %s" % (100.*free/mem,'%'))
			self['pused'].setText("%.1f %s" % (100.*(mem-free)/mem,'%'))
		except Exception, e:
			print "[About] getMemoryInfo FAIL:", e

	def clearMemory(self):
		eConsoleAppContainer().execute("sync")
		open("/proc/sys/vm/drop_caches", "w").write("3")
		self.getMemoryInfo()

class MemoryInfoSkinParams(HTMLComponent, GUIComponent):
	def __init__(self):
		GUIComponent.__init__(self)
		self.rows_in_column = 25

	def applySkin(self, desktop, screen):
		if self.skinAttributes is not None:
			attribs = [ ]
			for (attrib, value) in self.skinAttributes:
				if attrib == "rowsincolumn":
					self.rows_in_column = int(value)
			self.skinAttributes = attribs
		return GUIComponent.applySkin(self, desktop, screen)

	GUI_WIDGET = eLabel

class SystemNetworkInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		Screen.setTitle(self, _("Network Information"))
		self.skinName = ["SystemNetworkInfo", "WlanStatus"]
		self["LabelBSSID"] = StaticText()
		self["LabelESSID"] = StaticText()
		self["LabelQuality"] = StaticText()
		self["LabelSignal"] = StaticText()
		self["LabelBitrate"] = StaticText()
		self["LabelEnc"] = StaticText()
		self["BSSID"] = StaticText()
		self["ESSID"] = StaticText()
		self["quality"] = StaticText()
		self["signal"] = StaticText()
		self["bitrate"] = StaticText()
		self["enc"] = StaticText()

		self["IFtext"] = StaticText()
		self["IF"] = StaticText()

		self.iface = None
		self.createscreen()
		self.iStatus = None

		if iNetwork.isWirelessInterface(self.iface):
			try:
				from Plugins.SystemPlugins.WirelessLan.Wlan import iStatus
				self.iStatus = iStatus
			except:
				pass
			self.resetList()
			self.onClose.append(self.cleanup)
		self.updateStatusbar()

		self["key_red"] = StaticText(_("Close"))

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

	def createscreen(self):
		self.AboutText = ""
		self.iface = "eth0"
		eth0 = about.getIfConfig('eth0')
		if eth0.has_key('addr'):
			self.iface = 'eth0'
		eth1 = about.getIfConfig('eth1')
		if eth1.has_key('addr'):
			self.iface = 'eth1'
		ra0 = about.getIfConfig('ra0')
		if ra0.has_key('addr'):
			self.iface = 'ra0'
		wlan0 = about.getIfConfig('wlan0')
		if wlan0.has_key('addr'):
			self.iface = 'wlan0'
		self.AboutText += iNetwork.getFriendlyAdapterName (self.iface) + ":" + iNetwork.getFriendlyAdapterDescription(self.iface) +"\n"

		def nameserver():
			nameserver=""
			i=0
			for line in open('/etc/resolv.conf','r'):
				line = line.strip()
				if "nameserver" in line:
					i=i+1
					nameserver += str(i) +".Nameserver" + ":"  +line.strip().replace("nameserver ","")+"\n"
					if nameserver.strip() == "0.0.0.0":
						nameserver =  _("Nameserver is off")
					else:
						nameserver =  nameserver.strip()
			return nameserver

		def domain():
			domain=""
			for line in open('/etc/resolv.conf','r'):
				line = line.strip()
				if "domain" in line:
					domain +=line.strip().replace("domain ","")
					return domain
				else:
					domain = _("no domain name found")
					return domain

		def gateway():
			gateway=""
			for line in popen('ip route show'):
				line = line.strip()
				if "default via " in line:
					line = line.split(' ')
					line =line[2]
					return line
				else:
					line = _("no gateway found")
					return line

		def netspeed():
			netspeed=""
			for line in popen('ethtool eth0 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)

		def netspeed_eth1():
			netspeed=""
			for line in popen('ethtool eth1 |grep Speed','r'):
				line = line.strip().split(":")
				line =line[1].replace(' ','')
				netspeed += line
				return str(netspeed)

		if eth0.has_key('addr'):
			if eth0.has_key('ifname'):
				self.AboutText += _('Interface: /dev/' + eth0['ifname'] + "\n")
			self.AboutText += _("Network Speed:") + netspeed() + "\n"
			if eth0.has_key('hwaddr'):
				self.AboutText += _("MAC:") + eth0['hwaddr'] + "\n"
			self.AboutText += "\n" + _("IP:") + eth0['addr'] + "\n"
			self.AboutText += _("Gateway:") + gateway() + "\n"
			self.AboutText += nameserver() + "\n"
			if eth0.has_key('netmask'):
				self.AboutText += _("Netmask:") + eth0['netmask'] + "\n"
			if eth0.has_key('brdaddr'):
				if eth0['brdaddr']=="0.0.0.0":
					self.AboutText += _('Broadcast:') + eth0['brdaddr']  + _("(DHCP is off)") + "\n"
				else:
					self.AboutText += _('Broadcast:' + eth0['brdaddr'] + "\n")
			self.AboutText += _("Domain:") + domain() + "\n"
			self.iface = 'eth0'

		eth1 = about.getIfConfig('eth1')
		if eth1.has_key('addr'):
			if eth1.has_key('ifname'):
				self.AboutText += _('Interface:/dev/' + eth1['ifname'] + "\n")
			self.AboutText += _("NetSpeed:") + netspeed_eth1() + "\n"
			if eth1.has_key('hwaddr'):
				self.AboutText += _("MAC:") + eth1['hwaddr'] + "\n"
			self.AboutText += "\n" + _("IP:") + eth1['addr'] + "\n"
			self.AboutText += _("Gateway:") + gateway() + "\n"
			self.AboutText += nameserver() + "\n"
			if eth1.has_key('netmask'):
				self.AboutText += _("Netmask:") + eth1['netmask'] + "\n"
			if eth1.has_key('brdaddr'):
				if eth1['brdaddr']=="0.0.0.0":
					self.AboutText += _('Broadcast:') + eth1['brdaddr']  + _("(DHCP is off)") + "\n"
				else:
					self.AboutText += _('Broadcast:' + eth1['brdaddr'] + "\n")
			self.AboutText += _("Domain:") + domain() + "\n"
			self.iface = 'eth1'

		ra0 = about.getIfConfig('ra0')
		if ra0.has_key('addr'):
			if ra0.has_key('ifname'):
				self.AboutText += _('Interface:/dev/') + ra0['ifname'] + "\n"
			self.AboutText += "\n" +  _("IP:") + ra0['addr'] + "\n"
			if ra0.has_key('netmask'):
				self.AboutText += _("Netmask:") + ra0['netmask'] + "\n"
			if ra0.has_key('brdaddr'):
				self.AboutText += _("Broadcast:") + ra0['brdaddr'] + "\n"
			if ra0.has_key('hwaddr'):
				self.AboutText += _("MAC:") + ra0['hwaddr'] + "\n"
			self.iface = 'ra0'

		wlan0 = about.getIfConfig('wlan0')
		if wlan0.has_key('addr'):
			if wlan0.has_key('ifname'):
				self.AboutText += _('Interface:/dev/') + wlan0['ifname'] + "\n"
			if wlan0.has_key('hwaddr'):
				self.AboutText += _("MAC:") + wlan0['hwaddr'] + "\n"
			self.AboutText += "\n" + _("IP:") + wlan0['addr'] + "\n"
			self.AboutText += _("Gateway:") + gateway() + "\n"
			self.AboutText += nameserver() + "\n"
			if wlan0.has_key('netmask'):
				self.AboutText += _("Netmask:") + wlan0['netmask'] + "\n"
			if wlan0.has_key('brdaddr'):
				if wlan0['brdaddr']=="0.0.0.0":
					self.AboutText += _('Broadcast:') + wlan0['brdaddr'] + _("(DHCP is off)") + "\n"
				else:
					self.AboutText += _('Broadcast:') + wlan0['brdaddr'] + "\n"
			self.AboutText += _("Domain:") +  domain() + "\n"
			self.iface = 'wlan0'

		#not use this , adapter make reset after  4GB (32bit restriction)
		#rx_bytes, tx_bytes = about.getIfTransferredData(self.iface)
		#self.AboutText += "\n" + _("Bytes received:") + "\t" + rx_bytes + '  (~'  + str(int(rx_bytes)/1024/1024)  + ' MB)'  + "\n"
		#self.AboutText += _("Bytes sent:") + "\t" + tx_bytes + '  (~'  + str(int(tx_bytes)/1024/1024)+ ' MB)'  + "\n"

		hostname = file('/proc/sys/kernel/hostname').read()
		self.AboutText += _("Hostname:") + hostname + "\n"
		self["AboutScrollLabel"] = ScrollLabel(self.AboutText)

	def cleanup(self):
		if self.iStatus:
			self.iStatus.stopWlanConsole()

	def resetList(self):
		if self.iStatus:
			self.iStatus.getDataForInterface(self.iface, self.getInfoCB)

	def getInfoCB(self, data, status):
		self.LinkState = None
		if data is not None:
			if data is True:
				if status is not None:
					if self.iface == 'wlan0' or self.iface == 'ra0':
						if status[self.iface]["essid"] == "off":
							essid = _("No Connection")
						else:
							essid = status[self.iface]["essid"]
						if status[self.iface]["accesspoint"] == "Not-Associated":
							accesspoint = _("Not-Associated")
							essid = _("No Connection")
						else:
							accesspoint = status[self.iface]["accesspoint"]
						if self.has_key("BSSID"):
							self.AboutText += _('Accesspoint:') + accesspoint + '\n'
						if self.has_key("ESSID"):
							self.AboutText += _('SSID:') + essid + '\n'

						quality = status[self.iface]["quality"]
						if self.has_key("quality"):
							self.AboutText += _('Link Quality:') + quality + '\n'

						if status[self.iface]["bitrate"] == '0':
							bitrate = _("Unsupported")
						else:
							bitrate = str(status[self.iface]["bitrate"]) + " Mb/s"
						if self.has_key("bitrate"):
							self.AboutText += _('Bitrate:') + bitrate + '\n'

						signal = status[self.iface]["signal"]
						if self.has_key("signal"):
							self.AboutText += _('Signal Strength:') + signal + '\n'

						if status[self.iface]["encryption"] == "off":
							if accesspoint == "Not-Associated":
								encryption = _("Disabled")
							else:
								encryption = _("Unsupported")
						else:
							encryption = _("Enabled")
						if self.has_key("enc"):
							self.AboutText += _('Encryption:') + encryption + '\n'

						if status[self.iface]["essid"] == "off" or status[self.iface]["accesspoint"] == "Not-Associated" or status[self.iface]["accesspoint"] is False:
							self.LinkState = False
						else:
							self.LinkState = True
						self["AboutScrollLabel"].setText(self.AboutText)

	def exit(self):
		self.close(True)

	def updateStatusbar(self):
		self["IFtext"].setText(_("Network:"))
		self["IF"].setText(iNetwork.getFriendlyAdapterDescription(self.iface)  + " - " +iNetwork.getFriendlyAdapterName(self.iface) )
		#self["IF"].setText(iNetwork.getFriendlyAdapterName(self.iface))
		if iNetwork.isWirelessInterface(self.iface):
			try:
				self.iStatus.getDataForInterface(self.iface, self.getInfoCB)
			except:
				pass
		else:
			iNetwork.getLinkState(self.iface, self.dataAvail)

	def dataAvail(self, data):
		self.LinkState = None
		for line in data.splitlines():
			line = line.strip()
			if 'Link detected:' in line:
				if "yes" in line:
					self.LinkState = True
				else:
					self.LinkState = False