
from pprint import pprint

class ValveDict(dict):
	def __str__(self):
		out = ''
		for key, value in self.items():
			out += '\t"%s" "%s"\n' % (key, value)
		return out

	def __repr__(self):
		return self.__str__()

	def loads(maptext):
		valvedict = ValveDict()
		for line in maptext.splitlines():
			key, value = line.strip('"').split('" "')
			valvedict[key] = value

		return valvedict
class ValveMap(ValveDict):

	mapversion = 0

	def __init__(self, *args, **kw):
		super(ValveMap, self).__init__(*args, **kw)
		self.itemlist = super(ValveMap, self).keys()

		# Defualt New Map
		self['versioninfo'] = ValveDict({
			"editorversion": 400,
			"editorbuild": 6550,
			"mapversion": 0,
			"formatversion": 100,
			"prefab": 0,
		})
		self['viewsettings'] = ValveDict({
			"bSnapToGrid": 1,
			"bShowGrid": 1,
			"bShowLogicalGrid": 0,
			"nGridSpacing": 64,
			"bShow3DGrid": 0,
		})
		self['world'] = ValveDict({
			"id": 1,
			"mapversion": 0,
			"classname": "worldspawn",
			"skyname": None,
			"maxpropscreenwidth": -1,
			"detailvbsp": None,
			"detailmaterial": None,
		})
		self['cameras'] = ValveDict({
			"activecamera": -1,
		})
		self['cordon'] = ValveDict({
			"mins": (-1024, -1024, -1024),
			"maxs": ( 1024,  1024,  1024),
			"active": 0,
		})

	def __str__(self):
		out = ''
		for key, value in self.items():
			out += '%s\n{\n%s}\n' % (key, value)
		return out

	def save(self):
		self.mapversion += 1
		self['versioninfo']['mapversion'] = self.mapversion
		self['world']['mapversion'] = self.mapversion

	def loads(maptext, baseclass=None):
		if None == baseclass:
			baseclass = ValveMap
		valvemap = baseclass()
		if not isinstance(valvemap, ValveMap):
			raise TypeError('`baseclass` is not valid Valve Map/child.')

		blockname = None
		blocktext = None
		for line in maptext.splitlines():
			if line.startswith('}') or line.startswith('{'):
				continue
			if line.startswith('\t'):
				blocktext.append(line[1:])
				continue

			if None != blockname:
				valvemap[blockname] = ValveDict.loads('\n'.join(blocktext))

			blockname = line
			blocktext = []

		return valvemap
#
# TEST
#

#!python2
if __name__ == '__main__':
	import gamelib

	if True:
		with open('demofile.vmf', 'r') as demofile:
			mymap = gamelib.TF2.loads(demofile.read())
	else:
		mymap = gamelib.TF2()

	mymap.save()
	with open('demofile.vmf', 'w') as demofile:
		print(str(mymap))
		demofile.write(str(mymap))
