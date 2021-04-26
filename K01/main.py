import sms

mensaje = input('Escribe tu mensaje: ')

salida = sms.traduce(mensaje)

print('{} es -{}-'.format(mensaje, salida))
