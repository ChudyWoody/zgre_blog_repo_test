#!/bin/bash
git add -A
git commit -m "poprawiony base url w hugo.toml na chudywoody.github.io/zgre_blog_repo_test. Kiedy robię lokalnie hugo serve--baseURL=\"http://localhost:1313/\" to zdjęcia działają, a przy zmienionym na repo samo hugo serve zdjęcia nie działają"
git push 
