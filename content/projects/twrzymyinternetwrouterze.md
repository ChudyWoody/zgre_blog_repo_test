---
title: twrzymy
---
![[Pasted image 20250304204829.png]]


sudo ip addres add 192.168.1.1 dev enp0s31f6
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
#sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
#sudo iptables -A FORWARD -i enp0s31f6 -o wlan0 -j ACCEPT
#sudo iptables-save > /etc/iptables/iptables.rules
sudo nano /etc/dnsmasq.conf




Chat gpt podpowiada: 

zidentyfikuj dostepne interfejsy:
ip link
moje to 
wlan0 - polaczony z ChudyWoody
enp0s31f6 - ethernet z karty sieciowej plyty glownej

internet przychodzi z wlan0
router podlaczony jest przez enp0s31f6 kablem ethernet do komputera

instaluje 
sudo pacman -S iptables dnsmasq

Czad podpowiada:
wlacz NAT z pomoca iptables
1. wlacz przekazywanie pakietow 
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

2. upewnij sie ze ustawienie jest trwale dodajac je do /etc/sysctl.conf (nie 
mialem takiego pliku, musialem go utworzyc) w tym pliku wpisalem 
net.ipv4.ip_forward=1

3. skonfiguruj itables, aby przesylaly ruch z 
enp0s31f6 (eth) do wlan0 (wifi) 
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i enp0s31f6 -o wlan0 -j ACCEPT

4. zapisz reguly iptables, aby byly trwale:
sudo iptables-save > /etc/iptables/iptables.rules

-to mi nie dzialalo, istnial juz plik iptables.rules, ktory nie dawal sie nadpisac, wiec zmienilem mu nazwe na iptables.rules.old i utworzylem nowy plik z outputem iptables-save
-gdy spisuje zajrzalem tam jeszcze raz i sa dwa pliki iptables.rules, czyli chyba usluga sobie zrobila nowy -----DO ZWERYFIKOWANIA -nie ma nowego, przywidzialo mi sie
Jesli iptables-service nie jest wlaczony czat powiedzial zeby sudo systemctl enable iptables i sudo systemctl start iptables


Potem czat powiedzial:
Skonfiguruj serwer DHCP za pomoca dnsmasq
1. otworz plik konfiguracyjny dnsmasq:
sudo nano /etc/dnsmasq.conf
-tu ta sama sytuacja co wyzej, nie dalo sie go edytowac, wiec zrobilem mv dnsmasq.conf dnsmasq.conf.old
-tu nowy plik sie nie powtarza
2. w pliku ktory utworzylem czat powiedzial zeby wpisac
interface=eth0
dhcp-range=192.168.1.100,162168.1.200,12h

3. uruchom i wlacz dnsmasq
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq
- tutaj mialem problem
sudo systemctl start dnsmasq
Job for dnsmasq.service failed because the control process exited with error code.
See "systemctl status dnsmasq.service" and "journalctl -xeu dnsmasq.service" for details.
[zgredek@zgredArch etc]$ systemctl status dnsmasq.service
× dnsmasq.service - dnsmasq - A lightweight DHCP and caching DNS server
     Loaded: loaded (/usr/lib/systemd/system/dnsmasq.service; disabled; preset: disabled)
     Active: failed (Result: exit-code) since Thu 2024-11-21 03:06:21 CET; 26s ago
 Invocation: d2d3e6cf66154b14b3da9fbff0737036
       Docs: man:dnsmasq(8)
    Process: 47820 ExecStartPre=/usr/bin/dnsmasq --test (code=exited, status=0/SUCCESS)
    Process: 47821 ExecStart=/usr/bin/dnsmasq -k --enable-dbus --user=dnsmasq --pid-file (code=exited, status=2)
   Main PID: 47821 (code=exited, status=2)

lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Scheduled restart job, restart counter is at 5.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Start request repeated too quickly.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Failed with result 'exit-code'.
lis 21 03:06:21 zgredArch systemd[1]: Failed to start dnsmasq - A lightweight DHCP and caching DNS server.
[zgredek@zgredArch etc]$ journalctl -xeu dnsmasq.service
lis 21 03:06:21 zgredArch dnsmasq[47821]: BŁĄD: nie udało się uruchomić dnsmasq-a
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
░░ Subject: Proces jednostki zakończył działanie
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ Proces ExecStart= należący do jednostki dnsmasq.service zakończył działanie.
░░ 
░░ Kod wyjścia procesu: „exited”, jego stan wyjścia: 2.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Failed with result 'exit-code'.
░░ Subject: Jednostka się nie powiodła
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ Jednostka dnsmasq.service przeszła do stanu „failed” (niepowodzenia)
░░ z wynikiem „exit-code”.
lis 21 03:06:21 zgredArch systemd[1]: Failed to start dnsmasq - A lightweight DHCP and caching DNS server.
░░ Subject: Zadanie uruchamiania dla jednostki dnsmasq.service się nie powiodło
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ Zadanie uruchamiania dla jednostki dnsmasq.service zostało ukończone z niepowodzeniem.
░░ 
░░ Identyfikator zadania: 14102, wynik zadania: failed.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Scheduled restart job, restart counter is at 5.
░░ Subject: Zaplanowano automatyczne ponowne uruchamianie jednostki
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ W wyniki skonfigurowania ustawienia Restart= zaplanowano automatyczne ponowne
░░ uruchamianie jednostki dnsmasq.service.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Start request repeated too quickly.
lis 21 03:06:21 zgredArch systemd[1]: dnsmasq.service: Failed with result 'exit-code'.
░░ Subject: Jednostka się nie powiodła
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ Jednostka dnsmasq.service przeszła do stanu „failed” (niepowodzenia)
░░ z wynikiem „exit-code”.
lis 21 03:06:21 zgredArch systemd[1]: Failed to start dnsmasq - A lightweight DHCP and caching DNS server.
░░ Subject: Zadanie uruchamiania dla jednostki dnsmasq.service się nie powiodło
░░ Defined-By: systemd
░░ Support: https://lists.freedesktop.org/mailman/listinfo/systemd-devel
░░ 
░░ Zadanie uruchamiania dla jednostki dnsmasq.service zostało ukończone z niepowodzeniem.
░░ 
░░ Identyfikator zadania: 14212, wynik zadania: failed.


---udalo sie go rozwiazac poprzez:
czat: Sprawdź, czy port 53 jest zajęty

dnsmasq używa domyślnie portu 53, który może być już zajęty przez inną usługę, np. systemd-resolved lub inny serwer DNS. Wykonaj:

sudo ss -tulpn | grep :53
output:
udp   UNCONN 0      0               127.0.0.54:53        0.0.0.0:*          
udp   UNCONN 0      0            127.0.0.53%lo:53        0.0.0.0:*          
udp   UNCONN 0      0                  0.0.0.0:5353      0.0.0.0:*          
udp   UNCONN 0      0                  0.0.0.0:5355      0.0.0.0:*          
udp   UNCONN 0      0                     [::]:5353         [::]:*          
udp   UNCONN 0      0                     [::]:5355         [::]:*          
tcp   LISTEN 0      4096            127.0.0.54:53        0.0.0.0:*          
tcp   LISTEN 0      4096               0.0.0.0:5355      0.0.0.0:*          
tcp   LISTEN 0      4096         127.0.0.53%lo:53        0.0.0.0:*          
tcp   LISTEN 0      4096                  [::]:5355         [::]:*    

i dodanie do /etc/dnsmasq.conf linii
port=5353

(systemd-resolved korzysta z tego portu najwyrazniej, czat proponowal wylaczenie tej uslugi, ale nie wiem co robi wiec zmienilem port)

wtedy 
sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq 

nie zwrocily bledu, ale 
sudo systemctl status dnsmasq
dal output
zgredek@zgredArch etc]$ sudo systemctl status dnsmasq
● dnsmasq.service - dnsmasq - A lightweight DHCP and caching DNS server
     Loaded: loaded (/usr/lib/systemd/system/dnsmasq.service; enabled; preset: disabled)
     Active: active (running) since Thu 2024-11-21 03:10:12 CET; 29s ago
 Invocation: 6018f11264b94535a1d171807186c649
       Docs: man:dnsmasq(8)
   Main PID: 47985 (dnsmasq)
      Tasks: 1 (limit: 9147)
     Memory: 988K (peak: 1.6M)
        CPU: 81ms
     CGroup: /system.slice/dnsmasq.service
             └─47985 /usr/bin/dnsmasq -k --enable-dbus --user=dnsmasq --pid-file

lis 21 03:10:13 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:15 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:18 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:21 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:24 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:27 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:31 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:33 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:36 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu
lis 21 03:10:39 zgredArch dnsmasq-dhcp[47985]: żądanie DHCP odebrano na interfejsie enp0s31f6, który nie ma adresu

wiec przypisalem ip mojemu portowi ethernet
sudo ip addr add 192.168.1.1/24 dev enp0s31f6
sudo ip link set enp0s31f6 up

wtedy restart i status pokazaly normalne outputy

5. Podlacz kabel ethernet miedzy komputerem a portem LAN routera
router powinien automatycznie uzyskac internet dzieki NAT i serwerowi DHCP skonfigurowanym na komputerze.

----- no wiec wlaczylem router i z laptopa polaczylem sie z routerem haslami z naklejki, 
kiedys gdy tego probowalem nie pozwalal (router) skonfigurowac, a dzis pozwolil, nawet pokazuje ze ma polaczenie z internetem, ale yt nie otwiera
przechodze wiec do sekcji porad GPT Testowanie i debugowanie

6. Testowanie i debugowanie
upewnij sie ze NAT dziala
sudo iptables -t nat -L

sprawdz logi dnsmasq, jesli DHCP nie dziala
sudo journalctl -u dnsmasq


kolejna sesja z czatem

Konfiguracja dnsmasq

Plik dnsmasq.conf musisz edytować, aby ustawić serwer DHCP dla interfejsu Ethernet (enp0s31f6). Oto kroki:

    Otwórz plik:

sudo nano /etc/dnsmasq.conf

Dodaj/zmodyfikuj następujące linie:

# Interfejs, na którym działa serwer DHCP
interface=enp0s31f6

# Zakres adresów IP przydzielanych urządzeniom
dhcp-range=192.168.2.10,192.168.2.100,12h

# Adres bramy domyślnej (twój komputer, bo to on przekazuje internet)
dhcp-option=3,192.168.2.1

# Serwery DNS (możesz użyć Google lub innych)
dhcp-option=6,8.8.8.8,8.8.4.4

# Nie działaj jako serwer DNS na innych interfejsach
bind-interfaces

Włącz i uruchom dnsmasq

    Włącz usługę dnsmasq:

sudo systemctl enable dnsmasq
sudo systemctl start dnsmasq

sudo systemctl status dnsmasq
● dnsmasq.service - dnsmasq - A lightweight DHCP and caching DNS server
● dnsmasq.service - dnsmasq - A lightweight DHCP and caching DNS server
     Loaded: loaded (/usr/lib/systemd/system/dnsmasq.service; enabled; preset: disabled)
     Active: active (running) since Thu 2024-11-21 03:15:45 CET; 2h 23min ago
 Invocation: cb363a0c0902486185d3ae855ec92235
       Docs: man:dnsmasq(8)
   Main PID: 48303 (dnsmasq)
      Tasks: 1 (limit: 9147)
     Memory: 1.1M (peak: 1.8M)
        CPU: 198ms
     CGroup: /system.slice/dnsmasq.service
             └─48303 /usr/bin/dnsmasq -k --enable-dbus --user=dnsmasq --pid-file

lis 21 04:56:43 zgredArch dnsmasq-dhcp[48303]: DHCPREQUEST(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1
lis 21 04:56:43 zgredArch dnsmasq-dhcp[48303]: DHCPACK(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1 dlinkrouter519E
lis 21 04:57:19 zgredArch dnsmasq-dhcp[48303]: DHCPDISCOVER(enp0s31f6) 78:98:e8:63:51:a1
lis 21 04:57:19 zgredArch dnsmasq-dhcp[48303]: DHCPOFFER(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1
lis 21 04:57:19 zgredArch dnsmasq-dhcp[48303]: DHCPREQUEST(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1
lis 21 04:57:19 zgredArch dnsmasq-dhcp[48303]: DHCPACK(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1 dlinkrouter519E
lis 21 05:01:55 zgredArch dnsmasq-dhcp[48303]: DHCPDISCOVER(enp0s31f6) 78:98:e8:63:51:a1
lis 21 05:01:55 zgredArch dnsmasq-dhcp[48303]: DHCPOFFER(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1
lis 21 05:01:55 zgredArch dnsmasq-dhcp[48303]: DHCPREQUEST(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1
lis 21 05:01:55 zgredArch dnsmasq-dhcp[48303]: DHCPACK(enp0s31f6) 192.168.1.197 78:98:e8:63:51:a1 dlinkrouter51

zainstalowalem narzedzie tcpdump
sudo pacman -S tcpdump

i uruchomilem
sudo tcpdump -i enp0s31f6

i widzialem ze przesyla toco mam otwarte na kompie (disneyplus i strona chata)
ale laptop polaczony z routerem wciaz nie mial internetu

no to od poczatku spis danych 

ip addres na kompie
3: enp0s31f6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 2c:56:dc:d3:d9:ab brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.1/24 scope global enp0s31f6
       valid_lft forever preferred_lft forever
    inet 192.168.2.1/32 scope global enp0s31f6
       valid_lft forever preferred_lft forever

sprawdzilem iptables i byly ok




widac w trakcie konfiguracji nadalem mu dwa adresy, a na routerze wczesniej zmienilem 
default gateway i primary dns sercver na 192.168.2.1

gdy zmienilem ustawienia na routerze na 
static ip
ip addres na 192.168.1.2
subnet mask 255.255.255.0
default gateway 192.168.1.1
primary dns server 8.8.8.8

to zaczelo dzialac!!!!! :D:D:D:D:D:D:D::D
