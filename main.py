import sys
from src.vista.InterfazAutoPerfecto import App_AutoPerfecto
from src.logica.Logica import Logica
from src.modelo.declarative_base import engine, Base

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    logica = Logica()

    app = App_AutoPerfecto(sys.argv, logica)
    sys.exit(app.exec_())
