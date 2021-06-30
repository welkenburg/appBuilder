import cssutils

# not done yet

sheet = cssutils.parseFile('dark.css')

for item in sheet:
	if item.type == item.STYLE_RULE:
		print(item.selectorText)
		for property in item.style:
			print(property.name)
			print(property.value)
	