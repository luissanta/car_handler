from enum import Enum
import enum
import unittest

from src.modelo.declarative_base import Session
from src.logica.Logica import Logica
from src.modelo.accion_mantenimiento import AccionMantenimiento
from src.modelo.vehiculo import Vehiculo
from src.modelo.mantenimiento import Mantenimiento
from faker import Faker
from faker_vehicle import VehicleProvider
from datetime import datetime, date


class MantenimientoTestCase(unittest.TestCase):

    def setUp(self):
        self.coleccion = Logica()
        self.session = Session()
        self.faker = Faker()
        self.faker.add_provider(VehicleProvider)
        Faker.seed(0)

    def test_listar_acciones_por_anio_vacias(self):
        vehiculo = self.crear_mock_vehiculo()
        lista_acciones = self.coleccion.listar_acciones_por_anio(vehiculo.id)
        self.assertTrue(len(lista_acciones) == 0)

    def test_listar_acciones_por_anio(self):
        vehiculo = self.crear_mock_vehiculo()
        accion_1 = self.crear_mock_accion(vehiculo.id)
        accion_2 = self.crear_mock_accion(vehiculo.id)
        anio_accion_1 = accion_1.fecha.split("-")
        anio_accion_2 = accion_2.fecha.split("-")
        lista_acciones = self.coleccion.listar_acciones_por_anio(vehiculo.id)
        respuesta = {
            anio_accion_1[0]: accion_1.costo,
            anio_accion_2[0]: accion_2.costo
        }
        self.assertDictEqual(respuesta, lista_acciones)

    def test_listar_acciones_por_anio_ordenadas_desendente(self):
        vehiculo = self.crear_mock_vehiculo()
        accion_1 = self.crear_mock_accion(vehiculo.id)
        accion_2 = self.crear_mock_accion(vehiculo.id)
        lista_acciones = self.coleccion.listar_acciones_por_anio(vehiculo.id)
        anio_accion_1 = accion_1.fecha.split("-")
        anio_accion_2 = accion_2.fecha.split("-")
        respuesta = {
            anio_accion_1[0]: accion_1.costo,
            anio_accion_2[0]: accion_2.costo
        }
        lista_respuesta = list(respuesta)
        self.assertEqual(list(lista_acciones)[0], lista_respuesta[0])
        self.assertEqual(list(lista_acciones)[1], lista_respuesta[1])

    def test_calcular_gastos_por_kilometraje(self):
        vehiculo = Vehiculo(
            cilindraje=self.faker.random_int(1000, 5000),
            color=self.faker.color_name(),
            estado=True,
            kilometrajeCompra=91500,
            marca=self.faker.vehicle_make(),
            modelo=self.faker.vehicle_year(),
            placa=self.faker.license_plate(),
            tipoCombustible=self.faker.name()
        )
        mantenimiento_1 = self.crear_mock_mantenimiento()
        mantenimiento_2 = self.crear_mock_mantenimiento()
        mantenimiento_3 = self.crear_mock_mantenimiento()
        mantenimiento_4 = self.crear_mock_mantenimiento()
        mantenimiento_5 = self.crear_mock_mantenimiento()
        lista_acciones = [
            AccionMantenimiento(costo=350000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=92000, vehiculoId=1, mantenimientoId=mantenimiento_1.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=92000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=141220, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=92614, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=121210, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=93141, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=141220, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=93755, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=118220, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=94260, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=128570, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=94828, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=124660, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=95380, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=133860, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=95952, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=180000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=96100, vehiculoId=1, mantenimientoId=mantenimiento_3.id),
            AccionMantenimiento(costo=140000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=96300, vehiculoId=1, mantenimientoId=mantenimiento_4.id),
            AccionMantenimiento(costo=138230, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=96901, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=139380, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=97507, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=121440, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=98035, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=136850, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=98635, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=125810, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=99177, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=130410, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=99744, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=135700, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=100334, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=120290, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=100857, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=131330, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ABRIL),
                                kilometraje=101428, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=130180, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MAYO),
                                kilometraje=101994, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=115460, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MAYO),
                                kilometraje=102496, vehiculoId=1, mantenimientoId=mantenimiento_5.id),
            AccionMantenimiento(costo=360000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MAYO),
                                kilometraje=102596, vehiculoId=1, mantenimientoId=mantenimiento_1.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.JUNIO),
                                kilometraje=102606, vehiculoId=1, mantenimientoId=mantenimiento_2.id)
        ]
        self.session.add(vehiculo)

        for accion in lista_acciones:
            self.session.add(accion)
        self.session.add(vehiculo)
        self.session.commit()
        valor_km_costo_mantenimiento = self.coleccion.calcular_gastos_por_kilometraje(vehiculo.id)

        self.assertEqual(valor_km_costo_mantenimiento, 214.75)

    def test_calcular_gastos_ultimo_anio_por_kilometraje(self):
        vehiculo = Vehiculo(
            cilindraje=self.faker.random_int(1000, 5000),
            color=self.faker.color_name(),
            estado=True,
            kilometrajeCompra=91500,
            marca=self.faker.vehicle_make(),
            modelo=self.faker.vehicle_year(),
            placa=self.faker.license_plate(),
            tipoCombustible=self.faker.name()
        )
        mantenimiento_1 = self.crear_mock_mantenimiento()
        mantenimiento_2 = self.crear_mock_mantenimiento()

        lista_acciones = [
            AccionMantenimiento(costo=350000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=92500, vehiculoId=1, mantenimientoId=mantenimiento_1.id),
            AccionMantenimiento(costo=350000, fecha=self.obtener_fecha_por_anios_pasados(Meses.ENERO),
                                kilometraje=92000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=93000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=94000, vehiculoId=1, mantenimientoId=mantenimiento_2.id)
        ]
        self.session.add(vehiculo)

        for accion in lista_acciones:
            self.session.add(accion)
        self.session.add(vehiculo)
        self.session.commit()
        valor_km_costo_mantenimiento = self.coleccion.calcular_gastos_por_kilometraje(vehiculo.id)

        mantenimiento_tipo_1_accion_1 = lista_acciones[0].costo / (
                    lista_acciones[0].kilometraje - vehiculo.kilometrajeCompra)
        promedio_mantenimiento_tipo_1 = mantenimiento_tipo_1_accion_1
        mantenimiento_tipo_2_accion_1 = lista_acciones[2].costo / (
                    lista_acciones[2].kilometraje - lista_acciones[1].kilometraje)
        mantenimiento_tipo_2_accion_2 = lista_acciones[3].costo / (
                    lista_acciones[3].kilometraje - lista_acciones[2].kilometraje)
        promedio_mantenimiento_tipo_2 = (mantenimiento_tipo_2_accion_1 + mantenimiento_tipo_2_accion_2) / 2
        promedio_promedios = (promedio_mantenimiento_tipo_1 + promedio_mantenimiento_tipo_2) / 2

        self.assertEqual(valor_km_costo_mantenimiento, round(promedio_promedios, 2))

    def test_calcular_gastos_ultimo_anio_por_kilometraje_multiples_acciones_pasadas(self):
        vehiculo = Vehiculo(
            cilindraje=self.faker.random_int(1000, 5000),
            color=self.faker.color_name(),
            estado=True,
            kilometrajeCompra=91500,
            marca=self.faker.vehicle_make(),
            modelo=self.faker.vehicle_year(),
            placa=self.faker.license_plate(),
            tipoCombustible=self.faker.name()
        )
        mantenimiento_1 = self.crear_mock_mantenimiento()
        mantenimiento_2 = self.crear_mock_mantenimiento()

        lista_acciones = [
            AccionMantenimiento(costo=350000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.ENERO),
                                kilometraje=92500, vehiculoId=1, mantenimientoId=mantenimiento_1.id),
            AccionMantenimiento(costo=350000, fecha=self.obtener_fecha_por_anios_pasados(Meses.ENERO),
                                kilometraje=50000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=380000, fecha=self.obtener_fecha_por_anios_pasados(Meses.ENERO),
                                kilometraje=10000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=380000, fecha=self.obtener_fecha_por_anios_pasados(Meses.ENERO),
                                kilometraje=92000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.FEBRERO),
                                kilometraje=93000, vehiculoId=1, mantenimientoId=mantenimiento_2.id),
            AccionMantenimiento(costo=400000, fecha=self.obtener_fecha_anio_actual_por_mes(Meses.MARZO),
                                kilometraje=94000, vehiculoId=1, mantenimientoId=mantenimiento_2.id)
        ]
        self.session.add(vehiculo)

        for accion in lista_acciones:
            self.session.add(accion)
        self.session.add(vehiculo)
        self.session.commit()
        valor_km_costo_mantenimiento = self.coleccion.calcular_gastos_por_kilometraje(vehiculo.id)

        mantenimiento_tipo_1_accion_1 = lista_acciones[0].costo / (
                    lista_acciones[0].kilometraje - vehiculo.kilometrajeCompra)
        promedio_mantenimiento_tipo_1 = mantenimiento_tipo_1_accion_1
        mantenimiento_tipo_2_accion_1 = lista_acciones[4].costo / (
                    lista_acciones[4].kilometraje - lista_acciones[3].kilometraje)
        mantenimiento_tipo_2_accion_2 = lista_acciones[5].costo / (
                    lista_acciones[5].kilometraje - lista_acciones[4].kilometraje)
        promedio_mantenimiento_tipo_2 = (mantenimiento_tipo_2_accion_1 + mantenimiento_tipo_2_accion_2) / 2
        promedio_promedios = (promedio_mantenimiento_tipo_1 + promedio_mantenimiento_tipo_2) / 2

        self.assertEqual(valor_km_costo_mantenimiento, round(promedio_promedios, 2))

    def obtener_fecha_anio_actual_por_mes(self, mes):
        fecha = date(datetime.today().year, mes.value, self.faker.random_int(1, 28))
        return fecha.strftime('%Y-%m-%d')

    def obtener_fecha_por_anios_pasados(self, mes):
        fecha = date(datetime.today().year - self.faker.random_int(1, 5), mes.value, self.faker.random_int(1, 28))
        return fecha.strftime('%Y-%m-%d')

    def test_calcular_total_gastos(self):
        vehiculo = self.crear_mock_vehiculo()
        accion1 = self.crear_mock_accion(vehiculo.id)
        accion2 = self.crear_mock_accion(vehiculo.id)
        total_gastos = self.coleccion.calcular_total_gastos(vehiculo.id)
        self.assertEqual(total_gastos, accion1.costo + accion2.costo)

    def test_calcular_total_gastos_sin_acciones(self):
        vehiculo = self.crear_mock_vehiculo()
        total_gastos = self.coleccion.calcular_total_gastos(1)
        self.assertEqual(total_gastos, 0)

    def test_calcular_gastos_por_kilometraje_sin_acciones(self):
        vehiculo = self.crear_mock_vehiculo()
        valor_km_costo_mantenimiento = self.coleccion.calcular_gastos_por_kilometraje(1)
        self.assertEqual(valor_km_costo_mantenimiento, 0)

    def crear_mock_vehiculo(self) -> Vehiculo:
        vehiculo = Vehiculo(
            cilindraje=self.faker.random_int(1000, 5000),
            color=self.faker.color_name(),
            estado=False,
            kilometrajeCompra=self.faker.random_int(1000, 10000),
            marca=self.faker.vehicle_make(),
            modelo=self.faker.vehicle_year(),
            placa=self.faker.license_plate(),
            tipoCombustible=self.faker.name()
        )
        self.session.add(vehiculo)
        self.session.commit()
        return vehiculo

    def crear_mock_mantenimiento(self) -> Mantenimiento:
        mantenimiento = Mantenimiento(
            descripcion=self.faker.text(),
            nombre=self.faker.name()
        )
        self.session.add(mantenimiento)
        self.session.commit()
        return mantenimiento

    def crear_mock_accion(self, vehiculo_id) -> AccionMantenimiento:
        mantenimiento = self.crear_mock_mantenimiento()
        accion = AccionMantenimiento(
            costo=self.faker.random_int(100000, 1000000),
            fecha=self.faker.date(),
            kilometraje=self.faker.random_int(10001, 100000),
            vehiculoId=vehiculo_id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion)
        self.session.commit()
        return accion

    def tearDown(self):
        self.session = Session()
        acciones = self.session.query(AccionMantenimiento).all()
        vehiculos = self.session.query(Vehiculo).all()
        mantenimientos = self.session.query(Mantenimiento).all()

        for accion_mantenimiento in acciones:
            self.session.delete(accion_mantenimiento)

        for vehiculo in vehiculos:
            self.session.delete(vehiculo)

        for mantenimiento in mantenimientos:
            self.session.delete(mantenimiento)

        self.session.commit()
        self.session.close()


class Meses(enum.Enum):
    ENERO = 1
    FEBRERO = 2
    MARZO = 3
    ABRIL = 4
    MAYO = 5
    JUNIO = 6
    JULIO = 7
    AGOSTO = 8
    SEPTIEMBRE = 9
    OCTUBRE = 10
    NOVIEMBRE = 11
    DICIEMBRE = 12
