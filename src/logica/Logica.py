import statistics

from datetime import datetime
from src.modelo.mantenimiento import Mantenimiento
from src.modelo.vehiculo import Vehiculo
from src.modelo.accion_mantenimiento import AccionMantenimiento
from src.modelo.declarative_base import engine, Base, Session


class Logica:

    def __init__(self):
        self.session = Session()
        Base.metadata.create_all(engine)

    def dar_autos(self):
        autos = [elem.__dict__ for elem in self.session.query(Vehiculo).all()]
        return sorted(autos, key=lambda x: x['marca'])

    def dar_auto(self, auto_id) -> dict:
        auto = self.session.query(Vehiculo).get(auto_id)
        if auto:
            return auto.__dict__
        return {}

    def crear_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) -> bool:
        es_valido = self.validar_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)
        if es_valido:
            es_repetido = self.validar_auto_repetido(marca, placa, modelo)
            if not es_repetido:
                vehiculo = Vehiculo(cilindraje=cilindraje, color=color, estado=False,
                                    kilometrajeCompra=kilometraje, marca=marca, modelo=modelo,
                                    placa=placa, tipoCombustible=tipo_combustible)
                self.session.add(vehiculo)
                self.session.commit()
                return True
            return False
        else:
            return False

    def validar_auto(self, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) -> bool:
        es_valido = False
        try:
            if str(marca) and str(placa) and int(modelo) \
                    and int(kilometraje) and str(color) and float(cilindraje) \
                    and str(tipo_combustible):
                if int(kilometraje) > 0 and float(cilindraje) > 0:
                    es_valido = True
        except ValueError:
            return es_valido
        return es_valido

    def validar_auto_repetido(self, marca, placa, modelo) -> bool:
        es_repetido = False
        auto_marca_modelo = self.session.query(Vehiculo) \
            .filter(Vehiculo.marca == marca, Vehiculo.modelo == modelo) \
            .first()
        auto_marca = self.session.query(Vehiculo).filter(Vehiculo.marca == marca).first()
        auto_placa = self.session.query(Vehiculo).filter(Vehiculo.placa == placa).first()
        if auto_marca or auto_marca_modelo or auto_placa:
            es_repetido = True
        return es_repetido

    def aniadir_mantenimiento(self, nombre, descripcion) -> bool:
        resultado = False
        if self.__validar_mantenimiento(nombre, descripcion):
            consulta = self.session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
            if not consulta:
                mantenimiento = Mantenimiento(nombre=nombre, descripcion=descripcion)
                self.session.add(mantenimiento)
                self.session.commit()
                resultado = True
        return resultado

    def editar_mantenimiento(self, id, nombre, descripcion):
        resultado = False
        try:
            if int(id) > 0 and self.__validar_mantenimiento(nombre, descripcion):
                consulta = self.session.query(Mantenimiento).filter(Mantenimiento.nombre == nombre).first()
                if consulta is None or consulta.id == id:
                    mantenimiento = self.session.query(Mantenimiento).get(id)
                    mantenimiento.nombre = nombre
                    mantenimiento.descripcion = descripcion
                    self.session.commit()
                    resultado = True
            return resultado
        except:
            return resultado

    def __validar_mantenimiento(self, nombre, descripcion) -> bool:
        if isinstance(nombre, str) and isinstance(descripcion, str) and len(nombre) > 0 and len(descripcion) > 0:
            return True
        else:
            return False

    def validar_crear_editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible):
        try:
            validacion = self.validar_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)
        except ValueError:
            return False
        return validacion

    def validar_crear_editar_mantenimiento(self, nombre, descripcion):
        return self.__validar_mantenimiento(nombre, descripcion)

    def crear_accion(self, nombre_mantenimiento, id_auto, valor, kilometraje, fecha) -> bool:
        es_valido = False
        try:
            mantenimiento = self.session.query(Mantenimiento) \
                .filter(Mantenimiento.nombre == nombre_mantenimiento) \
                .first()
            if mantenimiento is not None:
                if self.__validar_crear_accion(nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
                    accion_mantenimiento = AccionMantenimiento(mantenimientoId=mantenimiento.id,
                                                               vehiculoId=id_auto, costo=valor, kilometraje=kilometraje,
                                                               fecha=fecha)
                    self.session.add(accion_mantenimiento)
                    self.session.commit()
                    es_valido = True
        except ValueError:
            return False
        return es_valido

    def __validar_crear_accion(self, nombre_mantenimiento, id_auto, valor, kilometraje, fecha) -> bool:
        es_valido = False
        try:
            if int(id_auto) > 0 and float(valor) > 0 \
                    and int(kilometraje) > 0 and str(fecha):
                buscar_vehiculo = self.session.query(Vehiculo).filter(Vehiculo.id == id_auto).first()
                if buscar_vehiculo is not None and int(kilometraje) > buscar_vehiculo.kilometrajeCompra:
                    es_valido = True
        except ValueError:
            return False
        return es_valido

    def dar_acciones_auto(self, id_auto):
        acciones = [elem.__dict__ for elem in
                    self.session.query(AccionMantenimiento).filter(AccionMantenimiento.vehiculoId == id_auto)]
        for accion in acciones:
            accion['mantenimiento'] = self.session.query(Mantenimiento).get(accion['mantenimientoId'])
        return acciones

    def dar_accion(self, id_auto, id_accion) -> dict:
        accion_mantenimiento = self.session.query(AccionMantenimiento) \
            .filter(AccionMantenimiento.vehiculoId == id_auto, AccionMantenimiento.id == id_accion) \
            .first()
        if accion_mantenimiento:
            resultado = accion_mantenimiento.__dict__
            resultado['mantenimiento'] = self.session.query(Mantenimiento).get(resultado['mantenimientoId'])
            return resultado
        return {}

    def validar_crear_editar_accion(self, id_accion, nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
        validacion = False
        try:
            mantenimiento = self.session.query(Mantenimiento) \
                .filter(Mantenimiento.nombre == nombre_mantenimiento) \
                .first()
            if mantenimiento is not None:
                validacion = self.__validar_crear_accion(nombre_mantenimiento, id_auto, valor, kilometraje, fecha)
        except ValueError:
            validacion
        return validacion

    def eliminar_accion(self, id_auto, id_accion):
        es_valido = False
        try:
            if (int(id_auto) > 0 and int(id_accion) > 0):
                vehiculo = self.session.query(Vehiculo).get(id_auto)
                accion = self.session.query(AccionMantenimiento).get(id_accion)
                if vehiculo and accion:
                    mantenimiento = self.session.query(AccionMantenimiento).get(id_accion)
                    self.session.delete(mantenimiento)
                    self.session.commit()
                    es_valido = True
            return es_valido
        except:
            return es_valido

    def dar_mantenimientos(self):
        mantenimientos = [elem.__dict__ for elem in
                          self.session.query(Mantenimiento).all()]
        return sorted(mantenimientos, key=lambda x: x['nombre'])

    def vender_auto(self, id, kilometraje_venta, valor_venta) -> bool:
        es_valido = self.validar_vender_auto(id, kilometraje_venta, valor_venta)
        if es_valido:
            auto = self.session.query(Vehiculo).get(id)
            auto.kilometrajeVenta = kilometraje_venta
            auto.precioVenta = valor_venta
            auto.estado = True
            self.session.commit()
        return es_valido

    def validar_vender_auto(self, id, kilometraje_venta, valor_venta) -> bool:
        es_valido = False
        try:
            existe = self.session.query(Vehiculo).get(id)
            if existe is not None and int(kilometraje_venta) and float(valor_venta):
                if int(kilometraje_venta) > 0 and float(valor_venta) > 0:
                    es_valido = True
        except:
            return es_valido
        return es_valido

    def listar_acciones_por_anio(self, auto_id):
        acciones_auto = self.dar_acciones_auto(auto_id)
        resultado = {}
        for accion_auto in acciones_auto:
            datos_accion = accion_auto['fecha'].split("-")
            if datos_accion[0] in resultado:
                resultado[datos_accion[0]] = resultado[datos_accion[0]] + accion_auto['costo']
            else:
                resultado[datos_accion[0]] = accion_auto['costo']
        return dict(sorted(resultado.items()))

    def calcular_total_gastos(self, auto_id):
        acciones_auto = self.dar_acciones_auto(auto_id)
        resultado = 0
        for accion_auto in acciones_auto:
            resultado += accion_auto['costo']
        return resultado

    def __dar_acciones_auto_anio_actual(self, id_auto):
        anio_actual = str(datetime.today().year)
        acciones = [elem.__dict__ for elem in
                    self.session.query(AccionMantenimiento)
                        .filter(AccionMantenimiento.vehiculoId == id_auto)
                        .filter(AccionMantenimiento.fecha.ilike('%' + anio_actual + '%'))
                        .all()
                    ]
        for accion in acciones:
            accion['mantenimiento'] = self.session.query(Mantenimiento).get(accion['mantenimientoId'])
        return acciones

    def __validar_acciones_auto_anios_pasados(self, id_auto, nombre_mantenimiento) -> int:
        kilometraje_ultima_accion_pasada = 0
        mantenimiento = self.session.query(Mantenimiento)\
            .filter(Mantenimiento.nombre == nombre_mantenimiento)\
            .first()
        mantenimiento_id = mantenimiento.id
        anio_actual = str(datetime.today().year)
        acciones_anios_pasado = self.session.query(AccionMantenimiento)\
            .filter(AccionMantenimiento.vehiculoId == id_auto)\
            .filter(AccionMantenimiento.mantenimientoId == mantenimiento_id)\
            .filter(AccionMantenimiento.fecha.notlike('%' + anio_actual + '%'))\
            .order_by(AccionMantenimiento.kilometraje.desc())\
            .all()
        if acciones_anios_pasado:
            kilometraje_ultima_accion_pasada = acciones_anios_pasado[0].kilometraje
        return kilometraje_ultima_accion_pasada

    def calcular_gastos_por_kilometraje(self, auto_id) -> float:
        acciones_auto_anio_actual = self.__dar_acciones_auto_anio_actual(auto_id)
        acciones_unicas = set()
        valor_por_kilomentro = 0
        for accion_auto in acciones_auto_anio_actual:
            acciones_unicas.add(accion_auto['mantenimiento'].nombre)

        acciones_ordenadas = sorted(acciones_auto_anio_actual, key=lambda x: x['kilometraje'])
        promedios_acciones_mantenimiento = {}
        resultado_promedio_acciones_mantenimiento = 0
        for mantenimiento in acciones_unicas:
            sumatoria = 0
            auto = self.dar_auto(auto_id)
            kilometraje_ultima_accion_pasada = self.__validar_acciones_auto_anios_pasados(auto_id, mantenimiento)
            if kilometraje_ultima_accion_pasada > 0:
                kilometraje_inicial = kilometraje_ultima_accion_pasada
            else:
                kilometraje_inicial = auto['kilometrajeCompra']

            numero_acciones = 0
            for accion in acciones_ordenadas:
                if mantenimiento == accion['mantenimiento'].nombre:
                    sumatoria += accion['costo'] / (accion['kilometraje'] - kilometraje_inicial)
                    kilometraje_inicial = accion['kilometraje']
                    numero_acciones = numero_acciones + 1
            promedios_acciones_mantenimiento[mantenimiento] = sumatoria / numero_acciones
            resultado_promedio_acciones_mantenimiento += sumatoria / numero_acciones
        if resultado_promedio_acciones_mantenimiento > 0:
            valor_por_kilomentro = resultado_promedio_acciones_mantenimiento / len(acciones_unicas)
        return round(valor_por_kilomentro, 2)

    def dar_reporte_ganancias(self, auto_id):
        return self.listar_acciones_por_anio(auto_id), \
               self.calcular_gastos_por_kilometraje(auto_id), \
               self.calcular_total_gastos(auto_id)

    def editar_accion(self, id_accion, nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
        es_valido = False
        try:
            if self.__validar_editar_accion(id_accion, nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
                accion_recuperada = self.session.query(AccionMantenimiento).get(id_accion)
                mantenimiento = self.session.query(Mantenimiento) \
                    .filter(Mantenimiento.nombre == nombre_mantenimiento) \
                    .first()
                if mantenimiento is not None and accion_recuperada is not None:
                    accion_recuperada.costo = valor
                    accion_recuperada.fecha = fecha
                    accion_recuperada.kilometraje = kilometraje
                    accion_recuperada.mantenimientoId = mantenimiento.id
                    self.session.commit()
                    es_valido = True
            return es_valido
        except:
            return False

    def __validar_editar_accion(self, id_accion, nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
        es_valido = False
        try:
            if (int(id_accion) > 0 and str(nombre_mantenimiento) and int(id_auto) > 0 and float(valor) > 0 and int(
                    kilometraje) > 0 and str(fecha) and datetime.strptime(fecha, '%Y-%m-%d')):
                vehiculo_recuperado = self.session.query(Vehiculo).get(id_auto)
                if vehiculo_recuperado is not None and vehiculo_recuperado.estado == True:
                    return es_valido
                else:
                    if self.__validar_crear_accion(nombre_mantenimiento, id_auto, valor, kilometraje, fecha):
                        es_valido = True
            return es_valido
        except:
            return False

    def editar_auto(self, id, marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible) -> dict:
        vehiculo = self.session.query(Vehiculo).get(id)
        es_valido = self.validar_auto(marca, placa, modelo, kilometraje, color, cilindraje, tipo_combustible)
        if es_valido:
            vehiculo.marca = marca
            vehiculo.placa = placa
            vehiculo.modelo = modelo
            vehiculo.kilometrajeCompra = kilometraje
            vehiculo.color = color
            vehiculo.cilindraje = cilindraje
            vehiculo.tipoCombustible = tipo_combustible
            self.session.commit()
        return vehiculo

    def eliminar_mantenimiento(self, mantenimiento_id) -> bool:
        se_puede_eliminar = self.validar_eliminacion_mantenimiento(mantenimiento_id)
        if se_puede_eliminar:
            mantenimiento = self.session.query(Mantenimiento).get(mantenimiento_id)
            self.session.delete(mantenimiento)
            self.session.commit()
        return se_puede_eliminar

    def validar_eliminacion_mantenimiento(self, mantenimiento_id) -> bool:
        se_puede_eliminar = False
        acciones = self.session.query(AccionMantenimiento) \
            .filter(AccionMantenimiento.mantenimientoId == mantenimiento_id) \
            .all()
        if not acciones:
            se_puede_eliminar = True
        return se_puede_eliminar

    def eliminar_auto(self, auto_id) -> bool:
        se_puede_eliminar, vehiculo = self.__validar_eliminacion_auto(auto_id)
        if se_puede_eliminar:
            self.session.delete(vehiculo)
            self.session.commit()
        return se_puede_eliminar

    def __validar_eliminacion_auto(self, auto_id) -> tuple:
        se_puede_eliminar = False
        vehiculo = None
        if isinstance(auto_id, int) and auto_id > 0:
            vehiculo = self.session.query(Vehiculo).get(auto_id)
            acciones = self.session.query(AccionMantenimiento) \
                .filter(AccionMantenimiento.vehiculoId == auto_id) \
                .all()
            if vehiculo and not acciones:
                se_puede_eliminar = True
        return se_puede_eliminar, vehiculo
