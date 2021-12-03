from libraries.CodeGenerator import CodeGenerator

class GeneradorLicenseAndToken():
    from datetime import datetime, timedelta

    def __init__(self):
        self.code = CodeGenerator(30)

    def GetNow(self):
        return self.datetime.now()

    def CrearLicencia(self, dias_vencimiento = 30):
        now = self.datetime.now()
        expiration = self.FormatearFecha( now + self.timedelta( days=dias_vencimiento ) )
        str_licencia = self.code.License()
        return (expiration, str_licencia)

    def CrearToken(self):
        now = self.datetime.now()
        expiration = self.FormatearFecha(now + self.timedelta( hours=1 ))
        str_token = self.code.Token()
        return (expiration, str_token)

    def FormatearFecha(self, fecha):
        formato = '%m/%d/%y %H:%M:%S'
        fecha = fecha.strftime( '%x %X' )
        fecha = self.datetime.strptime( fecha, formato )
        return fecha