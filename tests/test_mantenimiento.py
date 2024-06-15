import unittest

from src.modelo.accion_mantenimiento import AccionMantenimiento
from src.modelo.declarative_base import Session
from src.logica.Logica import Logica
from src.modelo.mantenimiento import Mantenimiento
from faker import Faker
from faker_vehicle import VehicleProvider
from src.modelo.vehiculo import Vehiculo


class MantenimientoTestCase(unittest.TestCase):

    def setUp(self):
        self.coleccion = Logica()
        self.session = Session()
        self.faker = Faker()
        self.faker.add_provider(VehicleProvider)
        Faker.seed(0)
        self.tipos_mantenimiento = ["Seguro", "Impuesto", "Cambio de aceite", "Combustible"]

    def test_crear_mantenimiento(self):
        resultado = self.coleccion.aniadir_mantenimiento(self.faker.random.choice(self.tipos_mantenimiento),
                                                         self.faker.text())
        self.assertTrue(resultado)

    def test_crear_mantenimiento_invalido(self):
        resultado = self.coleccion.aniadir_mantenimiento(self.faker.random.uniform(-999.999, 99999.999),
                                                         self.faker.pyint(0, 9999999))
        self.assertFalse(resultado)

    def test_crear_mantenimiento_repetido(self):
        self.faker.seed_instance(4)
        resultado = self.coleccion.aniadir_mantenimiento(self.faker.random.choice(self.tipos_mantenimiento),
                                                         self.faker.text())
        resultado1 = self.coleccion.aniadir_mantenimiento(self.faker.random.choice(self.tipos_mantenimiento),
                                                          self.faker.text())
        self.assertTrue(resultado)
        self.assertFalse(resultado1)

    def test_crear_mantenimiento_con_campos_vacios(self):
        resultado = self.coleccion.aniadir_mantenimiento('', '')
        resultado1 = self.coleccion.aniadir_mantenimiento(None, '')
        self.assertFalse(resultado)
        self.assertFalse(resultado1)

    def test_dar_mantenimientos(self):
        mantenimiento_1 = self.crear_mock_mantenimiento()
        mantenimiento_2 = self.crear_mock_mantenimiento()
        resultado = self.coleccion.dar_mantenimientos()
        self.assertEqual(len(resultado), 2)

    def test_dar_mantenimientos_orden_alfabetico(self):
        mantenimiento_1 = self.crear_mock_mantenimiento()
        mantenimiento_2 = self.crear_mock_mantenimiento()
        mantenimiento_3 = self.crear_mock_mantenimiento()
        mantenimiento_4 = self.crear_mock_mantenimiento()
        mantenimientos = [
            mantenimiento_1.nombre,
            mantenimiento_2.nombre,
            mantenimiento_3.nombre,
            mantenimiento_4.nombre
        ]
        mantenimientos_ordenados = sorted(mantenimientos)
        resultado = self.coleccion.dar_mantenimientos()
        self.assertEqual(resultado[0]['nombre'], mantenimientos_ordenados[0])
        self.assertEqual(resultado[1]['nombre'], mantenimientos_ordenados[1])
        self.assertEqual(resultado[2]['nombre'], mantenimientos_ordenados[2])
        self.assertEqual(resultado[3]['nombre'], mantenimientos_ordenados[3])

    def test_borrar_mantenimiento(self):
        mantenimiento = self.crear_mock_mantenimiento()
        resultado = self.coleccion.eliminar_mantenimiento(mantenimiento.id)
        validacion_eliminacion = self.coleccion.dar_mantenimientos()
        self.assertTrue(resultado)
        self.assertEqual(len(validacion_eliminacion), 0)

    def test_borrar_mantenimiento_asociado_auto(self):
        vehiculo = self.crear_mock_vehiculo()
        mantenimiento = self.crear_mock_mantenimiento()
        accion = self.crear_mock_accion(vehiculo.id, mantenimiento.id)
        resultado = self.coleccion.eliminar_mantenimiento(mantenimiento.id)
        validacion_eliminacion = self.coleccion.dar_mantenimientos()
        self.assertFalse(resultado)
        self.assertEqual(len(validacion_eliminacion), 1)

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
    
    def test_editar_mantenimiento_con_campos_vacios(self):                
        mantenimiento_editado = self.coleccion.editar_mantenimiento("", "", "")
        self.assertFalse(mantenimiento_editado)

    def test_editar_mantenimiento_validar_tipo_datos(self):
        resultado = self.crear_mock_mantenimiento()              
        mantenimiento_editado = self.coleccion.editar_mantenimiento(resultado.id, self.faker.random.choice(self.tipos_mantenimiento), self.faker.text())
        mantenimiento_editado1 = self.coleccion.editar_mantenimiento(-1, self.faker.random_int(1000, 5000), self.faker.random_int(1000, 5000))
        self.assertTrue(mantenimiento_editado)
        self.assertFalse(mantenimiento_editado1)

    def test_editar_mantenimiento_con_nombre_existente(self):
        resultado = self.crear_mock_mantenimiento()  
        resultado1 = self.crear_mock_mantenimiento()  
        mantenimiento_editado = self.coleccion.editar_mantenimiento(resultado.id, resultado1.nombre, resultado1.descripcion)        
        self.assertFalse(mantenimiento_editado)

    def test_editar_mantenimiento(self):
        resultado = self.crear_mock_mantenimiento()
        nombre = self.faker.random.choice(self.tipos_mantenimiento)
        descripcion = self.faker.text()
        mantenimiento_editado = self.coleccion.editar_mantenimiento(resultado.id, nombre, descripcion)
        mantenimiento_recuperado = self.session.query(Mantenimiento).get(resultado.id)
        self.session.commit()
        self.assertTrue(mantenimiento_editado)
        self.assertEqual(mantenimiento_recuperado.nombre, nombre)
        self.assertEqual(mantenimiento_recuperado.descripcion, descripcion)                

    def crear_mock_mantenimiento(self) -> Mantenimiento:
        mantenimiento = Mantenimiento(
            descripcion=self.faker.text(),
            nombre=self.faker.name()
        )
        self.session.add(mantenimiento)
        self.session.commit()
        return mantenimiento

    def crear_mock_accion(self, vehiculo_id, mantenimiento_id) -> AccionMantenimiento:
        accion = AccionMantenimiento(
            costo=self.faker.random_int(100000, 1000000),
            fecha=self.faker.date(),
            kilometraje=self.faker.random_int(10001, 100000),
            vehiculoId=vehiculo_id,
            mantenimientoId=mantenimiento_id
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
