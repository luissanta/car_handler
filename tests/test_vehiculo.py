import unittest

from src.modelo.declarative_base import Session

from src.logica.Logica import Logica
from src.modelo.vehiculo import Vehiculo
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.accion_mantenimiento import AccionMantenimiento
from faker import Faker
from faker_vehicle import VehicleProvider


class VehiculoTestCase(unittest.TestCase):

    def setUp(self):
        self.coleccion = Logica()
        self.session = Session()

        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()
        self.data_factory.add_provider(VehicleProvider)
        self.tipos_combustible = ["Gasolina", "Gas", "Disel", "Electricos"]

    def test_lista_vehiculos_vacia(self):
        resultado = self.coleccion.dar_autos()
        self.assertListEqual(resultado, [])

    def test_listar_vehiculos(self):
        vehiculo1 = self.crear_mock_vehiculo()
        vehiculo2 = self.crear_mock_vehiculo()
        resultado = self.coleccion.dar_autos()
        self.assertEqual(len(resultado), 2)

    def test_listar_vehiculo(self):
        vehiculo3 = Vehiculo(cilindraje=self.data_factory.random.uniform(1600.0, 1801.0),
                             color=self.data_factory.color_name(), estado=False,
                             kilometrajeCompra=self.data_factory.pyint(1, 100), marca=self.data_factory.vehicle_make(),
                             modelo=self.data_factory.vehicle_year(),
                             placa=self.data_factory.license_plate(),
                             tipoCombustible=self.data_factory.random.choice(self.tipos_combustible))

        self.session.add(vehiculo3)
        self.session.commit()
        resultado = self.coleccion.dar_auto(1)

        self.assertEqual(resultado['color'], vehiculo3.color)
        self.assertEqual(resultado['marca'], vehiculo3.marca)
        self.assertEqual(resultado['modelo'], vehiculo3.modelo)
        self.assertEqual(resultado['estado'], vehiculo3.estado)
        self.assertEqual(resultado['cilindraje'], vehiculo3.cilindraje)
        self.assertEqual(resultado['tipoCombustible'], vehiculo3.tipoCombustible)
        self.assertEqual(resultado['placa'], vehiculo3.placa)
        self.assertEqual(resultado['kilometrajeCompra'], vehiculo3.kilometrajeCompra)

    def test_listar_vehiculo_no_existente(self):
        resultado = self.coleccion.dar_auto(4)
        self.assertFalse(resultado)

    def test_crear_vehiculo(self):
        resultado = self.coleccion.crear_auto(self.data_factory.vehicle_make(), self.data_factory.license_plate(),
                                              self.data_factory.vehicle_year(), self.data_factory.pyint(1, 100),
                                              self.data_factory.color_name(),
                                              self.data_factory.random.uniform(1600.0, 1800.0),
                                              self.data_factory.random.choice(self.tipos_combustible))
        self.assertTrue(resultado)

    def test_crear_vehiculo_invalido(self):
        resultado = self.coleccion.crear_auto(self.data_factory.vehicle_make(), self.data_factory.license_plate(),
                                              self.data_factory.random.uniform(2000.11, 2022.88),
                                              self.data_factory.text(), self.data_factory.color_name(),
                                              self.data_factory.random.uniform(1600.0, 1800.0),
                                              self.data_factory.random.choice(self.tipos_combustible))
        self.assertFalse(resultado)

    def test_crear_vehiculo_repetido(self):
        marca = self.data_factory.vehicle_make()
        placa = self.data_factory.license_plate()
        modelo = self.data_factory.vehicle_year()
        kilometraje = self.data_factory.pyint(1, 100)
        color = self.data_factory.color_name()
        cilindraje = self.data_factory.random.uniform(1600.0, 1800.0)
        tipo_combustible = self.data_factory.random.choice(self.tipos_combustible)
        resultado = self.coleccion.crear_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)
        resultado1 = self.coleccion.crear_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)
        self.assertTrue(resultado)
        self.assertFalse(resultado1)

    def test_crear_vehiculo_con_campos_vacios(self):
        resultado = self.coleccion.crear_auto(None, '', 0, None, None, None, None)
        resultado1 = self.coleccion.crear_auto('', '', 0, None, '', None, '')
        self.assertFalse(resultado)
        self.assertFalse(resultado1)

    def test_crear_vehiculo_con_campos_mayor_a_cero(self):
        resultado = self.coleccion.crear_auto(self.data_factory.vehicle_make(), self.data_factory.license_plate(),
                                              self.data_factory.random.uniform(-2000.11, -2022.88),
                                              self.data_factory.text(), self.data_factory.color_name(),
                                              self.data_factory.random.uniform(-1600.0, -1800.0),
                                              self.data_factory.random.choice(self.tipos_combustible))
        self.assertFalse(resultado)

    def test_vender_vehiculo(self):
        vehiculo = self.crear_mock_vehiculo()
        kilometraje_venta = self.data_factory.pyint(101, 999999)
        precio_venta = self.data_factory.pyint(10, 1000000000)
        resultado = self.coleccion.vender_auto(vehiculo.id, kilometraje_venta, precio_venta)
        self.session.commit()
        vehiculo_vendido = self.session.query(Vehiculo).get(1)
        self.assertTrue(resultado)
        self.assertEqual(kilometraje_venta, vehiculo_vendido.kilometrajeVenta)
        self.assertEqual(precio_venta, vehiculo_vendido.precioVenta)
        self.assertEqual(vehiculo_vendido.estado, True)

    def test_vender_vehiculo_vacio(self):
        vehiculo = self.crear_mock_vehiculo()
        resultado = self.coleccion.vender_auto(None, None, None)
        resultado1 = self.coleccion.vender_auto(vehiculo.id, -1, -2)
        self.assertFalse(resultado)
        self.assertFalse(resultado1)

    def test_vender_vehiculo_invalido(self):
        vehiculo = self.crear_mock_vehiculo()
        resultado = self.coleccion.vender_auto(vehiculo.id, self.data_factory.pyint(0, 99),
                                               self.data_factory.pyint(-5000, -1))
        self.assertEqual(resultado, False)

    def test_vender_vehiculo_inexistente(self):
        resultado = self.coleccion.vender_auto(self.data_factory.pyint(0, 99), self.data_factory.pyint(0, 99),
                                               self.data_factory.pyint(0, 99))
        self.assertEqual(resultado, False)

    def test_listar_vehiculo_orden_ascendente_por_marca(self):
        vehiculo1 = self.crear_mock_vehiculo()
        vehiculo2 = self.crear_mock_vehiculo()
        vehiculo3 = self.crear_mock_vehiculo()
        vehiculo4 = self.crear_mock_vehiculo()
        vehiculo5 = self.crear_mock_vehiculo()
        vehiculo6 = self.crear_mock_vehiculo()
        vehiculo7 = Vehiculo(cilindraje=self.data_factory.pyint(1600, 1801), color=self.data_factory.color_name(),
                             estado=True,
                             kilometrajeCompra=self.data_factory.pyint(1, 100), marca="Audi",
                             modelo=self.data_factory.vehicle_year(),
                             placa=self.data_factory.license_plate(),
                             tipoCombustible=self.data_factory.random.choice(self.tipos_combustible))

        self.session.add(vehiculo7)
        self.session.commit()

        ordenamiento_por_marca = vehiculo1.marca, vehiculo2.marca, vehiculo3.marca, vehiculo4.marca, vehiculo5.marca, vehiculo6.marca, vehiculo7.marca
        ordenamiento_por_marca = sorted(ordenamiento_por_marca)
        resultado = self.coleccion.dar_autos()

        for i in range(7):
            self.assertEqual(resultado[i]['marca'], ordenamiento_por_marca[i])

    def test_editar_auto(self):
        vehiculo = self.crear_mock_vehiculo()
        vehiculo_editar = {
            'id': vehiculo.id,
            'marca': self.data_factory.vehicle_make(),
            'placa': self.data_factory.license_plate(),
            'modelo': self.data_factory.vehicle_year(),
            'kilometraje': self.data_factory.pyint(1, 10000),
            'color': self.data_factory.color_name(),
            'cilindraje': self.data_factory.pyint(1600, 4000),
            'tipo_combustible': self.data_factory.random.choice(self.tipos_combustible)
        }
        resultado = self.coleccion.editar_auto(
            vehiculo_editar['id'],
            vehiculo_editar['marca'],
            vehiculo_editar['placa'],
            vehiculo_editar['modelo'],
            vehiculo_editar['kilometraje'],
            vehiculo_editar['color'],
            vehiculo_editar['cilindraje'],
            vehiculo_editar['tipo_combustible'])
        self.assertEqual(resultado.id, vehiculo_editar['id'])
        self.assertEqual(resultado.marca, vehiculo_editar['marca'])
        self.assertEqual(resultado.placa, vehiculo_editar['placa'])
        self.assertEqual(resultado.modelo, int(vehiculo_editar['modelo']))
        self.assertEqual(resultado.kilometrajeCompra, int(vehiculo_editar['kilometraje']))
        self.assertEqual(resultado.color, vehiculo_editar['color'])
        self.assertEqual(resultado.cilindraje, float(vehiculo_editar['cilindraje']))
        self.assertEqual(resultado.tipoCombustible, vehiculo_editar['tipo_combustible'])

    def test_editar_auto_validacion_campos(self):
        vehiculo = self.crear_mock_vehiculo()
        vehiculo_editar = {
            'id': vehiculo.id,
            'marca': self.data_factory.vehicle_make(),
            'placa': self.data_factory.license_plate(),
            'modelo': self.data_factory.vehicle_make(),
            'kilometraje': self.data_factory.pyint(-10, -1),
            'color': self.data_factory.color_name(),
            'cilindraje': self.data_factory.pyint(-1600, -1000),
            'tipo_combustible': self.data_factory.random.choice(self.tipos_combustible)
        }
        resultado = self.coleccion.editar_auto(
            vehiculo_editar['id'],
            vehiculo_editar['marca'],
            vehiculo_editar['placa'],
            vehiculo_editar['modelo'],
            vehiculo_editar['kilometraje'],
            vehiculo_editar['color'],
            vehiculo_editar['cilindraje'],
            vehiculo_editar['tipo_combustible'])
        self.assertEqual(resultado.id, vehiculo.id)
        self.assertEqual(resultado.marca, vehiculo.marca)
        self.assertEqual(resultado.placa, vehiculo.placa)
        self.assertEqual(resultado.modelo, vehiculo.modelo)
        self.assertEqual(resultado.kilometrajeCompra, vehiculo.kilometrajeCompra)
        self.assertEqual(resultado.color, vehiculo.color)
        self.assertEqual(resultado.cilindraje, vehiculo.cilindraje)
        self.assertEqual(resultado.tipoCombustible, vehiculo.tipoCombustible)

    def test_borrar_auto_datos_vacios(self):
        resultado = self.coleccion.eliminar_auto("")
        self.assertFalse(resultado)

    def test_borrar_auto_datos_invalidos(self):
        vehiculo = self.crear_mock_vehiculo()
        resultado = self.coleccion.eliminar_auto(-1)
        resultado1 = self.coleccion.eliminar_auto("sdfs")
        resultado2 = self.coleccion.eliminar_auto(vehiculo.id)
        self.assertFalse(resultado)
        self.assertFalse(resultado1)
        self.assertTrue(resultado2)

    def test_borrar_auto_id_inexistente(self):
        resultado = self.coleccion.eliminar_auto(2)
        self.assertFalse(resultado)

    def test_borrar_auto_con_acciones_de_mantenimiento(self):
        vehiculo = self.crear_mock_vehiculo()
        mantenimiento = self.crear_mock_mantenimiento()
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.data_factory.random.uniform(999.0, 99999.0),
            fecha=self.data_factory.date(),
            kilometraje=self.data_factory.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        accion_a_crear_2 = AccionMantenimiento(
            costo=self.data_factory.random.uniform(999.0, 99999.0),
            fecha=self.data_factory.date(),
            kilometraje=self.data_factory.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion_a_crear_1) 
        self.session.add(accion_a_crear_2)
        self.session.commit()        

        resultado = self.coleccion.eliminar_auto(vehiculo.id)
        consultar_vehiculo = self.session.query(Vehiculo).get(vehiculo.id)
        self.assertFalse(resultado)        
        self.assertEqual(consultar_vehiculo, vehiculo)

    def test_borrar_auto(self):
        vehiculo = self.crear_mock_vehiculo()
        id_vehiculo = vehiculo.id
        resultado = self.coleccion.eliminar_auto(id_vehiculo)
        self.session.commit()
        consultar_vehiculo = self.session.query(Vehiculo).get(id_vehiculo)
        self.assertTrue(resultado)
        self.assertEqual(consultar_vehiculo, None)

    def crear_mock_vehiculo(self) -> Vehiculo:
        vehiculo = Vehiculo(cilindraje=self.data_factory.pyint(1600, 1801), color=self.data_factory.color_name(),
                            estado=False,
                            kilometrajeCompra=self.data_factory.pyint(1, 100), marca=self.data_factory.vehicle_make(),
                            modelo=self.data_factory.vehicle_year(),
                            placa=self.data_factory.license_plate(),
                            tipoCombustible=self.data_factory.random.choice(self.tipos_combustible))
        self.session.add(vehiculo)
        self.session.commit()
        return vehiculo

    def crear_mock_mantenimiento(self) -> Mantenimiento:
        mantenimiento = Mantenimiento(
            descripcion=self.data_factory.text(),
            nombre=self.data_factory.name()
        )
        self.session.add(mantenimiento)
        self.session.commit()
        return mantenimiento

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
