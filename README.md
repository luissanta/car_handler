# Cars

Bienvenido a **Cars**, una aplicación diseñada para ayudar a los dueños de vehículos a gestionarlos de manera eficiente y efectiva. Con esta herramienta, podrás manejar todos los aspectos de la administración de tus autos, desde su creación y edición hasta su venta y desactivación. Además, ofrece un seguimiento detallado de los mantenimientos y la generación de reportes de gastos para cada vehículo.

## Características

- **Gestión de Vehículos**: Crea, edita, vende, consulta y desactiva autos de manera sencilla.
- **Seguimiento de Mantenimientos**: Lleva un registro minucioso de todos los mantenimientos realizados a tus vehículos.
- **Reportes de Gastos**: Genera informes detallados sobre los gastos asociados a cada auto.
- **Interfaz de Usuario**: Interfaz intuitiva y amigable desarrollada con PyQt5.
- **Datos Simulados**: Utiliza datos falsos para pruebas con la ayuda de Faker y faker-vehicle.

## Tecnologías Utilizadas

Esta aplicación está desarrollada con Python 3.9 y hace uso de las siguientes librerías:

- **SQLAlchemy**: ORM para la gestión de bases de datos.
- **PyQt5**: Biblioteca para crear interfaces gráficas de usuario.
- **coverage**: Herramienta para medir la cobertura de pruebas.
- **Faker**: Librería para generar datos falsos.
- **faker-vehicle**: Extensión de Faker para generar datos específicos de vehículos.

## Instalación

Para poner en marcha esta aplicación, sigue los siguientes pasos:

1. **Clona este repositorio:**

    ```bash
    git clone https://github.com/luissanta/car_handler.git
    cd car_handler
    ```

2. **Crea un entorno virtual e instálalo:**

    ```bash
    python3.9 -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3. **Ejecuta la aplicación:**

    ```bash
    python main.py
    ```

## Uso

1. **Interfaz de Usuario**: Una vez que la aplicación esté en funcionamiento, podrás gestionar tus vehículos a través de la interfaz gráfica.
2. **Gestión de Vehículos**: Agrega, edita, vende y desactiva vehículos utilizando las opciones del menú.
3. **Mantenimientos**: Registra y consulta los mantenimientos de cada vehículo.
4. **Reportes de Gastos**: Genera y revisa reportes detallados sobre los gastos de cada vehículo.

## Contribuir

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit de los mismos (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un nuevo Pull Request.