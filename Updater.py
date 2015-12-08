import urllib.request

page = urllib.request.urlopen('https://github.com/Lightning3105/Legend-Of-Aiopa-RPG/commits/master')
page = str(page.read())
ind = page.find('class="sha btn btn-outline"')
snip = page[ind + 38:ind + 45]
print(snip)