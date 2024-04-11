# glo-2005-tp

## Initialisation de la BD
Il faut avoir mysql et make d'installer sur sa machine.

Installer make:
``` bash
sudo apt install make -y
```

Afin d'initialiser la BD:
``` bash
make init-bd
```

## Executé le code
```
make run
```

## Rouler le serveur smtp
```
sudo python3 -m smtpd -c DebuggingServer -n localhost:1025
```