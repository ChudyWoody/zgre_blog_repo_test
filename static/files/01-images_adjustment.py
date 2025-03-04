# python script to adjust images addreseess from obsidian to url 


import os
import re
import shutil

# Paths: 
    ## posts_dir ma być lokalizacją z postami do udostępnienia! w folderze stronki, nie w Obsidianie!
posts_dir = "/home/zgredek/Programowanie/python_envs/hugo_obsidian_website/zgre_blog_test/content/posts" 
	## folder z załącznikami Obsidiana
attachments_dir = "/home/zgredek/Dokumenty/Obsidian_Vault/zz Assets"
	## folder stronki ze zdjęciami
static_images_dir = "/home/zgredek/Programowanie/python_envs/hugo_obsidian_website/zgre_blog_test/static/images"

#Step 1: Process each markdown file in the posts directory
	## Pobiera nazwy plików w lokalizacji postów w folderze stronki i tworzy ich listę w zmiennej filename
for filename in os.listdir(posts_dir):
	## jeżeli plik się kończy na ".md" to...
	if filename.endswith(".md"):
    ## ...to tworzy pełną ścieżkę do pliku (dodaje nazwę pliku do ścieżki z postami)
		filepath = os.path.join(posts_dir, filename)
	## otwiera plik z postem w trybie read reprezentowany przez zmienną file
		with open(filepath, "r") as file:
    ## odczytuje całą zawartość tego pliku jako string w zmiennej content
			content = file.read()

# Step 2: Find all image links in the format ![Image Description](/images/Pasted%20image%20...%20.png)
	## w odczytanym pliku z postem w zmiennej content znajduje wewnętrzne linki obsidiana do zdjęć i wpisuje je do zmiennej images, mają postać: ![[Pasted image 20250304204829.png]]
		images = re.findall(r'\[\[([^]]*\.png)\]\]', content)
	## ta linia bierze każde znalezione zdjęcie i...
		for image in images:
    		# Prepare the Markdown-compatible link with %20 replacing spaces
	## i podmienia adres zdjęcia na taki, który zostanie rozpoznany przez Hugo przy kompilowaniu strony - zamienia spacje na %20 i podaje adres zdjęcia w folderze images (w static) 
			markdown_image = f"![{image.replace('.png', '').replace('_', ' ')}](/images/{image.replace(' ', '%20')})"
	## a następnie podmienia w zmiennej content (treść posta) frazę [[{nazwazdjęcia}]] na to co wygenerował powyżej
			content = content.replace(f"[[{image}]]", markdown_image)
# Step 4: Copy the image to the Hugo static directory if it exists
	## tworzy zmienną z adresem źródła, z którego Hugo będzie brał zdjęcia do kompilacji /source/images/nazwazdjęcia
			image_source = os.path.join(attachments_dir, image)
	## sprawdza czy ścieżka ze źródłem zdjęć (source/images) istnieje
			if os.path.exists(image_source):
    ## kopiuje z folderu Obsidiana zdjęcia do /source/image
				shutil.copy(image_source, static_images_dir)
	## otwiera plik z postem w trybie write jako zmienną file
		with open(filepath, "w") as file:
    ## zapisuje w zmiennej file (otwartym poście) podmienioną zawartość pliku z prawidłowymi adresami czytelnymi dla Hugo
			file.write(content)
print("Markdown files processed and images copied successfully")

