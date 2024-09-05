# Mani: Controla tus gastos

![Mani Logo](/static/rsz_icon.png)

## Resumen

Instala Mani en tu propio servidor y disfruta de controlar tus gastos. Esta aplicación está pensada
para un uso personal/familiar y se recomienda **ser instalada como app**

## Instalación: Modo fácil

Si tienes acceso SSH al servidor donde quieres desplegar, edita el comando deploy.sh con tus credenciales
y usa:

```bash
make deploy
```

## Instalación: Docker

### Clona el repositorio

Clona el repositorio donde consideres

### Construye la imagen

Usa:

```bash
make build
```

O el siguiente comando:

```bash
docker build -t mani --build-arg uid=`id -u` --build-arg gid=`id -g` --build-arg user=`whoami` -f docker/Dockerfile .
```

### Lanza el contenedor

Usa:

```bash
make run
```

O el siguiente comando:

```bash
docker compose -f docker/docker-compose.yml up -d
```

## Post instalación

Una vez arrancado el contenedor, este estará escuchando en el puerto 9637.
Usa cualquier servicio de proxy inverso para conectarlo a la url que consideres

### Crea un superusuario

Necesitarás acceder por ssh al servidor:

```bash
ssh <user>@<server>
```

Después accede a la bash del contenedor:

```bash
make bash
```

Y una vez dentro del contenedor, usa el siguiente comando y sigue las instrucciones:

```bash
python manage.py createsuperuser
```

### App Móvil

Una vez instalado el servidor, accede a este a través del navegador y en las opciones de este te permitirá
**instalar la web como app** dándole a "compartir" y seguidamente "añadir a inicio". Busca información de tu
navegador/SO
para encontrar cómo hacerlo.

### Usuarios y cuentas

Para crear usuarios y cuentas, añádelos a través del portal de administración como superusuario.

Accede al portal de administración con tu navegador en la url:

`https://<nombre-de-dominio>/admin`
