# Herramienta de Sorteo - Club Atlético Osasuna

## Uso

1. **Instalar Docker**: En un sistema Windows, descargar la aplicación Docker Desktop e instalarla para poder ejecutar la aplicación del sorteo.
2. **Descargar imagen**: Una vez instalado Docker, iniciarlo y a través de PowerShell ejecutar: ```docker pull your-dockerhub-username/herramienta_sorteo:latest```
3. **Ejecutar aplicación**: Una vez descargada la imagen de la herramienta, ejecutarla desde PowerShell con: ```docker run -p 8000:8000 your-dockerhub-username/herramienta_sorteo:latest```
4. **Acceso a la aplicación**: En un navegador web, acceder a localhost:8000 donde estará disponible la herramienta.

## Descripción

Esta herramienta realiza un sorteo dividido en 3 fases, siguiendo los estatutos del Club Atlético Osasuna. Los participantes se dividen en millares y se seleccionan de acuerdo a las siguientes fases:

1. **Fase 1**: Se aplica a cada millar secuencialmente. Si el número de participantes del millar es igual o menor a 33, no se hace nada en esta fase. Si tiene más de 33 participantes, se realiza un sorteo aleatorio seleccionando 33 participantes y marcando al resto como participantes de reserva.
2. **Fase 2**: Se aplica a cada millar secuencialmente. No hace nada excepto en los millares que tienen exactamente 33 participantes. En este caso, selecciona a los 33 participantes y no realiza más acciones.
3. **Fase 3**: Se aplica a cada millar secuencialmente. Solo aplica cambios en millares con menos de 33 participantes. En estos casos, selecciona a los participantes de dicho millar y completa hasta 33 seleccionando participantes de reserva obtenidos en la primera fase.

## Subida de Datos

Los datos de los participantes deben subirse en formato CSV (comma separated values) con 4 columnas:

- Millar
- Orden
- Nº Socio
- Nombre

### Ejemplo de archivo CSV:

```plaintext
Millar,Orden,Nº Socio,Nombre
1,1,421,Javier García García
5,1,953,Sandra García García
7,5,1827,Daniel García García
9,7,2469,Isabel García García
```

## Información sobre desarrollador

- **Desarrollador**: Pablo Elso Yoldi
- **Contacto**: pelso49@gmail.com
