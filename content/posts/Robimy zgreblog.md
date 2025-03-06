---
title: Robiemy zgreblog
---

Chcemy zrobić blog z notatek w Obsidianie. 

Do tego potrzebne są już zainstalowane:
- Obsidian
- python3
- git
- Go
- Hugo

Ja będę robił wszystko w wirtualnym środowisku pythona. Dlaczego? Bo tak. 


Najpierw stworzę sobie venv:

		mkdir ~/python_envs/hugo_website
		python3 -m venv ~/python_envs/hugo_website
		source ~/python_envs/hugo_website/bin/activate

No i mam. 

Teraz ściągnę do tego środowiska hugo:

		pip install hugo
		# sprawdzę czy jest:
		hugo version
		# powinien zwrócić komunikat o tym że działa przez pythona czy coś. 

Teraz trzeba stworzyć folder, w którym będzie nasza stronka. Robimy to zanim ją zainicjujemy, bo chcemy ją potem udostępniać przez GitHub Pages, więc musimy w tym folderze zainicjować repozytorium gita. 

		mkdir zgre_blog_test
		cd zgre_blog_test
		git init
		git config --global user.name "ChudyWoody"
		git config --global user.email "zgredek94@gmail.com"

Trzeba oczywiście podmienić na swoje configi gita.

Teraz trzeba zainicjować stronkę przy pomocy hugo. Idę do swojego folderu z venv i to robię:

		cd ~/python_envs/hugo_website
		hugo new site ../zgre_blog_test --force
Stworzył się nowy folder o nazwie zgre_blog_test, w którym jest prawie wszystko potrzebne do dalszej pracy. Żeby stronka jakoś wyglądała trzeba ściągnąć  hugo-theme i potem dostosować go do swoich potrzeb. Mi się podoba taki:
https://themes.gohugo.io/themes/hugo-coder

Najlepiej zrobić to dodając submoduł gita (czymkolwiek to jest,ale tak doradzają w tutorialach hugo i networkchucka)

		git submodule add -f https://github.com/luizdepra/hugo-coder.git themes/hugo-coder

Teraz jak już mamy ściągnięty theme w odpowiednim miejscu trzeba skopiować sobie jego konfigurację do naszego .../zgre_blog_test/hugo.toml

		cp ~/python_envs/hugo_python_website/zgre_blog_test/themes/hugo-coder/exampleSite/hugo.toml ~/python_envs/hugo_python_website/zgre_blog_test/hugo.toml

Sprawdźmy czy działa:
		
		hugo server -t themename
		hugo serve # w folderze zgre_blog_test
		# No i działa!

Co nie będzie działać to podstronki, dlatego że w folderze zgre_blog_test/content nic nie mamy. Żeby działały "Blog" i "Projects" trzeba tam utworzyć posts i projects itd, ale treść do nich doda się później:

		mkdir ./content/posts ./content/projects ./content/about ./content/contact

Teraz zajmiemy się synchronizacją naszej stronki z obsidianem. Posłuży nam do tego komenda rsync:

		rsync -av --delete "sourcepath" "destinationpath"

gdzie "sourcepath" to lokalizacja postów w Obsidianie, które chcemy na stronce, a "destinationpath" to lokalizacja postów w plikach stronki. Opcja -a to archive - kopiuje z symlinkami i uprawnieniami i innymi metadanymi, opcja -v to verbose - żeby nam powiedział czy wszystko spoko i co jest niespoko, opcja --delete - usunie w destinationpath to czego nie ma w sourcepath. Dla mnie to będzie:

	rsync -av --delete /home/zgredek/Dokumenty/Obsidian_Vault/Inbox/*.md /home/zgredek/Programowanie/python_envs/hugo_obsidian_website/zgre_blog_test/content/posts
![[Pasted image 20250304230039.png]]
Warto w ogóle sobie wcześniej przygotować kilka testowych postów, najlepiej ze zdjęciami, żeby sprawdzić jak to się sprawuje. A sprawuje się średnio ze zdjęciami, bo Obsidian trzyma załączniki tam gdzie mu się powie, z reguły w folderze wyszczególnionym w ustawieniach przez użytkownika (tak polecam mieć skonfigurowane) i w samych notatkach ma wewnętrzne swoje linki do załączników. Trzeba to jakoś obejść, a pythonowe obejście napisał networkchuck. Ja je troszeńkę pozmieniam, bo w chuckowym skrypcie zostawały wykrzykniki przed zdjęciami. 
Pamiętaj że dla pythona ważne są tabulatory, trzeba je usunąć, bo w tej notce są po dwa przed każdą "zerową" kolumną. 

```# python script to adjust images addreseess from obsidian to url

  
  

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
```

Sprawdźmy czy działa:

	hugo serve -t hugo-coder
I w przeglądarce localhost:1313.
Powinno działać, jeśli nie działa to usuń zawartość folderu public, żeby hugo na nowo wygenerował stronkę. Jeśli się tego nie zrobi to samo generowanie na nowo nie pomaga. 

Jadymy dalyj. 

Teraz trzeba przygotować Githuba. 
Załóż konto i tak dalej. Stwórz nowe repozytorium, np o nazwie bloga.

Będziemy potrzebować sposobu żeby się weryfikować przy uploadowaniu, więc trzeba sobie stworzyć klucze ssh. Służy do tego komenda:

		ssh-keygen -t rsa -b 4096 -C "your_email@example.com" # i wiadomo, podmień na swoje

W Githubie wejdź w Settings (pod zdjęciem profilu), po lewej będzie zakładka SSH and GPG keys. W Nagłówku SSH keys wklej swój publiczny klucz ssh (calutki, z pierwszym i ostatnim słowem). Klucz znajdzie się w folderze ~/.ssh/
Otwórz go sobie:

		cat ~/.ssh/id_rsa.pub # z rozwinięciem .pub jest publiczny, id_rsa to domyślna nazwa, ten drugi bez rozwinięcia jest prywatny, ma tu zostać. 

Żeby przetestować czy udaje się zweryfikować można zrobić tak:

		ssh -T git@github.com
		# powinien pojawić się taki komentarz:
		Hi ChudyWoody! You've successfully authenticated, but GitHub does not provide shell access.

Do tej pory pracowaliśmy na lokalnym repozytorium gita na naszym kompie, ale git się o tym nie kapnie póki mu nie powiemy żeby się kapnął. Musimy mu powiedzieć, że to w naszym folderze jest źródłem dla zgre_blog_test_repo na githubie:

		git remote add origin git@github.com:ChudyWoody/zgre_blog_repo_test
		# po dwukropku dajemy swoją nazwę użytkownika w GitHubie, po slashu nazwę repozytorium (tą na githubie, może się różnić od lokalnego folderu jak u mnie). Origin to powszechny sposób etykietowania czy coś.

Następnie trzeba dodać wszystkie zmiany jakie poczyniliśmy w lokalnym folderze do lokalnego repo (upewnij się że jesteś w odpowiednim miejscu):

		pwd # powinieneś być w swoim folderze z plikami stronki
		git add . # doda zmiany do repozytorium zdalnego (na kompie)
		git commit -m "pierwszy commit" # doda pierwszy commit, -m służy do dodania komentarza
		git push -u origin master # wyśle rzeczy do githuba? Tak, pośle rzeczy do githuba.

***TO CHYBA NIEWAŻNE 
Teraz będziemy się rozjeżdżać z Chuckiem, bo on swoją stronkę hostuje na Hostinger, ale my chcemy używać tylko Github Pages. 

		# Tworzy nową gałąź (GHPages) zawierającą tylko pliki z katalogu `public`
		git subtree split --prefix public -b GHPages-deploy

		# Wypycha (`push`) nową gałąź `hostinger-deploy` do zdalnej gałęzi `GHPages` na GitHubie
		git push origin GHPages-deploy:GHPages --force # force zmusza do nadpisania, jeśli taka gałąź już istnieje
		
		# Usuwa lokalną gałąź GHPages-deploy (nie jest już potrzebna, służyła tylko do pushnięcia jej do GitHuba)
		git branch -D GHPages-deploy

***Dobra, mamy gałązkę z samą stronką do publikowania.***

Github Pages normalnie pozwala na publikowanie stron zrobionych w Jekyllu, ale hugo ma sposób żeby to obejść. 
https://gohugo.io/hosting-and-deployment/hosting-on-github/

Trzeba wejść w swoje repo ze stronką, wejść w ustawienia repo (nie użytkowanika jak wcześniej, ustawienia repo będą na poziomej wstążce ***,musimy też wybrać odpowiedniego brancha - GHPages w naszym przypadku).*** Po lewej będzie zakładka Pages. Pod nagłówkiem "Build and deploymment" wybieramy Source "GitHub Actions" (nie trzeba nijak potwierdzać). 

W naszym lokalnym folderze trzeba utworzyć nowy katalog z plikiem hugo.yaml

		mkdir -p .github/workflows
		touch .github/workflows/hugo.yaml

W utworzonym pliku trzeba przekleić ustawieniadla workflowa zmieniając odpowiednio branch i wersję hugo jeśli jest potrzeba.
Treść dla pliku hugo.yaml
https://gohugo.io/hosting-and-deployment/hosting-on-github/#step-6

Następnie według instrukcji z gohugo

		git add -A
		git commit -m "Create hugo.yaml"
		git push # nie trzeba robić "-u origin master", git pamięta że ma pushować do master

Następnie trzeba uruchomić workflow. By to zrobić wybieramy nasz repo ze stronką, przechodzimy do Actions na wstążce, po lewej będzie "All workflows" z "Deploy Hugo site to Pages".  Klikamy na niego, po prawej się on pojawi z przyciskiem Run workflow. Można tam wybrać branche
### problem - czy trzeba wybierać branch GHPages? czy niepotrzebnie ją zrobiłem wcześniej?

Po kliknięciu będzie się chwilę kulać. Jak znaczek się zmieni na zielony znaczy że skończył. 
Wtedy można kliknąć na ten nasz workflow, pokażą się boksy "build" i "deploy". Pod drugim będzie link do naszej stronki. 

### problem - stronka się wygenerowała, ale zdjęcia są złe, trzeba pokminić nad lokalizacjami, problem pewnie jest w hugo.yaml który źle mi interpretuje lokalizacje zdjęć