import unittest

from src.modelo.declarative_base import Session
from src.logica.Logica import Logica
from src.modelo.accion_mantenimiento import AccionMantenimiento
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.vehiculo import Vehiculo
from faker import Faker
from faker_vehicle import VehicleProvider


class AccionMantenimientoTestCase(unittest.TestCase):

    def setUp(self):
        self.coleccion = Logica()
        self.session = Session()
        self.fake = Faker()
        self.fake.add_provider(VehicleProvider)
        Faker.seed(0)

    def test_crear_accion_vehiculo(self):
        mantenimiento = self.crear_mock_mantenimiento()
        vehiculo = self.crear_mock_vehiculo()
        self.session.add(mantenimiento)
        self.session.add(vehiculo)
        self.session.commit()
        accion_a_crear = {
            'costo': self.fake.random_int(100000, 1000000),
            'fecha': self.fake.date(),
            'kilometraje': self.fake.random_int(10001, 100000),
            'vehiculoId': vehiculo.id,
            'mantenimiento': mantenimiento.nombre
        }
        resultado = self.coleccion.crear_accion(
            accion_a_crear['mantenimiento'],
            accion_a_crear['vehiculoId'],
            accion_a_crear['costo'],
            accion_a_crear['kilometraje'],
            accion_a_crear['fecha']
        )
        self.assertTrue(resultado)

    def test_crear_accion_invalida(self):
        mantenimiento = Mantenimiento(
            descripcion=self.fake.text(),
            nombre=self.fake.random_int(900, 5000),
        )
        vehiculo = self.crear_mock_vehiculo()
        accion_a_crear = {
            'costo': self.fake.random_int(100000, 2000000),
            'fecha': self.fake.date(),
            'kilometraje': self.fake.random_int(10001, 100000),
            'vehiculoId': vehiculo.id,
            'mantenimiento': mantenimiento.nombre
        }
        resultado = self.coleccion.crear_accion(
            accion_a_crear['mantenimiento'],
            accion_a_crear['vehiculoId'],
            accion_a_crear['costo'],
            accion_a_crear['kilometraje'],
            accion_a_crear['fecha']
        )
        self.assertFalse(resultado)

    def test_crear_accion_tipos_de_datos_invalidos(self):
        vehiculo = self.crear_mock_vehiculo()
        mantenimiento = self.crear_mock_mantenimiento()
        accion_a_crear = {
            'costo': self.fake.date(),
            'fecha': self.fake.date(),
            'kilometraje': self.fake.text(),
            'vehiculoId': vehiculo.id,
            'mantenimiento': mantenimiento.nombre
        }
        resultado = self.coleccion.crear_accion(
            accion_a_crear['mantenimiento'],
            accion_a_crear['vehiculoId'],
            accion_a_crear['costo'],
            accion_a_crear['kilometraje'],
            accion_a_crear['fecha']
        )
        self.assertFalse(resultado)

    def test_crear_accion_valores_menores_a_cero(self):
        vehiculo = self.crear_mock_vehiculo()
        mantenimiento = self.crear_mock_mantenimiento()
        accion_a_crear = {
            'costo': self.fake.random_int(-100000, -1),
            'fecha': self.fake.date(),
            'kilometraje': self.fake.random_int(-100000, -1),
            'vehiculoId': vehiculo.id,
            'mantenimiento': mantenimiento.nombre
        }
        resultado = self.coleccion.crear_accion(
            accion_a_crear['mantenimiento'],
            accion_a_crear['vehiculoId'],
            accion_a_crear['costo'],
            accion_a_crear['kilometraje'],
            accion_a_crear['fecha']
        )
        self.assertFalse(resultado)

    def test_crear_accion_validar_kilometraje_mayor_kilometraje_inicial(self):
        mantenimiento = self.crear_mock_mantenimiento()
        vehiculo = self.crear_mock_vehiculo()
        accion_a_crear = {
            'costo': self.fake.random_int(100000, 1000000),
            'fecha': self.fake.date(),
            'kilometraje': self.fake.random_int(0, 10),
            'vehiculoId': vehiculo.id,
            'mantenimiento': mantenimiento.nombre
        }
        resultado = self.coleccion.crear_accion(
            accion_a_crear['mantenimiento'],
            accion_a_crear['vehiculoId'],
            accion_a_crear['costo'],
            accion_a_crear['kilometraje'],
            accion_a_crear['fecha']
        )
        self.assertFalse(resultado)

    def test_listar_acciones_vacia(self):
        vehiculo = self.crear_mock_vehiculo()
        resultado = self.coleccion.dar_acciones_auto(vehiculo.id)
        self.assertListEqual(resultado, [])

    def test_listar_acciones(self):
        mantenimiento = self.crear_mock_mantenimiento()
        vehiculo = self.crear_mock_vehiculo()
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random_int(100000, 1000000),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        accion_a_crear_2 = AccionMantenimiento(
            costo=self.fake.random_int(100000, 2000000),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion_a_crear_1)
        self.session.add(accion_a_crear_2)
        self.session.commit()
        resultado = self.coleccion.dar_acciones_auto(vehiculo.id)
        self.assertEqual(len(resultado), 2)

    def test_listar_accion(self):
        mantenimiento = self.crear_mock_mantenimiento()
        vehiculo = self.crear_mock_vehiculo()
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random_int(100000, 1000000),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion_a_crear_1)
        self.session.commit()
        resultado = self.coleccion.dar_accion(vehiculo.id, accion_a_crear_1.id)

        self.assertEqual(resultado['costo'], accion_a_crear_1.costo)
        self.assertEqual(resultado['fecha'], accion_a_crear_1.fecha)
        self.assertEqual(resultado['kilometraje'], accion_a_crear_1.kilometraje)
        self.assertEqual(resultado['vehiculoId'], vehiculo.id)
        self.assertEqual(resultado['mantenimientoId'], mantenimiento.id)

    def test_editar_accion_mantenimiento_auto_vendido(self):    
        mantenimiento = self.crear_mock_mantenimiento()       
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=True,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        self.session.add(vehiculo)  
        self.session.commit()   
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random_int(100000, 1000000),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )        
        self.session.add(accion_a_crear_1)    
        self.session.commit()        
     
        resultado = self.coleccion.editar_accion(1, 1, 1, self.fake.random_int(50, 1000000), self.fake.random_int(10001, 1000000), self.fake.date())
        self.assertFalse(resultado)

    def test_editar_accion_mantenimiento_campos_vacios(self):
        resultado = self.coleccion.editar_accion("", "", "", "", "", "")
        self.assertEqual(resultado, False)

    def test_editar_accion_mantenimiento_valores_mayores_a_cero(self):
        mantenimiento = self.crear_mock_mantenimiento()
        resultado = self.coleccion.editar_accion(-1 ,mantenimiento.nombre , 1, 1, 1, "2022-09-20")        
        resultado2 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, -1, 1, 1, "2022-09-20")
        resultado3 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, -1, 1, "2022-09-20")
        resultado4 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, 1, -1, "2022-09-20")
        self.assertEqual(resultado, False)
        self.assertEqual(resultado2, False)
        self.assertEqual(resultado3, False)
        self.assertEqual(resultado4, False)

    def test_editar_accion_mantenimiento_validar_fecha(self):
        mantenimiento = self.crear_mock_mantenimiento()  
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=False,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        self.session.add(vehiculo)  
        self.session.commit()   
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random_int(100000, 1000000),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )        
        self.session.add(accion_a_crear_1)    
        self.session.commit()        
        resultado = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, 1, self.fake.random_int(10001, 1000000), "2022-09-20")
        resultado1 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, 1, self.fake.random_int(10001, 1000000), "2022-20-09")
        resultado2 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, 1, self.fake.random_int(10001, 1000000), "20-09-2022")
        resultado3 = self.coleccion.editar_accion(1 ,mantenimiento.nombre, 1, 1, self.fake.random_int(10001, 1000000), "sddsf")        
        self.assertEqual(resultado, True)
        self.assertEqual(resultado1, False)
        self.assertEqual(resultado2, False)
        self.assertEqual(resultado3, False)

    def test_editar_accion_mantenimiento(self):    
        mantenimiento = self.crear_mock_mantenimiento() 
        mantenimiento1 = self.crear_mock_mantenimiento()
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=False,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        self.session.add(vehiculo)  
        self.session.commit()   
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random.uniform(999.0, 99999.0),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )        
        self.session.add(accion_a_crear_1)    
        self.session.commit()        

        costo_fake = self.fake.random.uniform(99999.0, 1099999.0)
        fecha_fake = self.fake.date()
        kilometraje_fake = self.fake.random_int(10001, 1000000)
        resultado = self.coleccion.editar_accion(accion_a_crear_1.id,mantenimiento1.nombre, vehiculo.id,costo_fake ,kilometraje_fake ,fecha_fake )
        self.session.commit() 
        accion_recuperada = self.session.query(AccionMantenimiento).get(accion_a_crear_1.id)        
        self.assertEqual(resultado, True)
        self.assertEqual(accion_recuperada.costo, costo_fake)
        self.assertEqual(accion_recuperada.fecha, fecha_fake)
        self.assertEqual(accion_recuperada.kilometraje, kilometraje_fake)
        self.assertEqual(accion_recuperada.mantenimientoId, mantenimiento1.id)

    def test_borrar_accion_mantenimiento_datos_vacios(self):
        resultado = self.coleccion.eliminar_accion("", "")        
        self.assertFalse(resultado)

    def test_borrar_accion_mantenimiento_datos_invalidos(self):
        mantenimiento = self.crear_mock_mantenimiento() 
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=False,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        self.session.add(vehiculo)  
        self.session.commit()   
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random.uniform(999.0, 99999.0),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        accion_a_crear_2 = AccionMantenimiento(
            costo=self.fake.random.uniform(999.0, 99999.0),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion_a_crear_1) 
        self.session.add(accion_a_crear_2)
        self.session.commit()        
        resultado1 = self.coleccion.eliminar_accion(vehiculo.id, accion_a_crear_1.id)
        resultado2 = self.coleccion.eliminar_accion(-1, -1)
        resultado3 = self.coleccion.eliminar_accion(self.fake.name(), self.fake.name())
        self.assertEqual(resultado1, True)
        self.assertEqual(resultado2, False)
        self.assertEqual(resultado3, False)

    def test_borrar_accion_mantenimiento_id_inexistente(self):
        resultado = self.coleccion.eliminar_accion(self.fake.random_int(10001, 1000000), self.fake.random_int(10001, 1000000))        
        self.assertFalse(resultado)
    
    def test_borrar_accion_mantenimiento(self):
        mantenimiento = self.crear_mock_mantenimiento() 
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=False,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        self.session.add(vehiculo)  
        self.session.commit()   
        accion_a_crear_1 = AccionMantenimiento(
            costo=self.fake.random.uniform(999.0, 99999.0),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        accion_a_crear_2 = AccionMantenimiento(
            costo=self.fake.random.uniform(999.0, 99999.0),
            fecha=self.fake.date(),
            kilometraje=self.fake.random_int(10001, 1000000),
            vehiculoId=vehiculo.id,
            mantenimientoId=mantenimiento.id
        )
        self.session.add(accion_a_crear_1) 
        self.session.add(accion_a_crear_2)
        self.session.commit()        

        resultado = self.coleccion.eliminar_accion(vehiculo.id, accion_a_crear_1.id)
        self.session.commit()  
        validacion_eliminacion = self.session.query(AccionMantenimiento).all()
        self.assertTrue(resultado)
        self.assertEqual(len(validacion_eliminacion), 1)

    def crear_mock_vehiculo(self) -> Vehiculo:
        vehiculo = Vehiculo(
            cilindraje=self.fake.random_int(1000, 5000),
            color=self.fake.color_name(),
            estado=False,
            kilometrajeCompra=self.fake.random_int(1000, 10000),
            marca=self.fake.vehicle_make(),
            modelo=self.fake.vehicle_year(),
            placa=self.fake.license_plate(),
            tipoCombustible=self.fake.name()
        )
        
        self.session.add(vehiculo)
        self.session.commit()
        return vehiculo

    def crear_mock_mantenimiento(self) -> Mantenimiento:
        mantenimiento = Mantenimiento(
            descripcion=self.fake.text(),
            nombre=self.fake.name()
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
