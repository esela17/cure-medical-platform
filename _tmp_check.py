text = open('index.html', encoding='utf-8').read()
idx = text.find('class="nav-links"')
print(text[idx:idx+700])
