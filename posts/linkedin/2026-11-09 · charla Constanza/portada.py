"""Portada de YouTube para la charla «No es falta de esfuerzo, es falta de sistema» (9-nov-2026).
Usa la tarjeta tachada de los anuncios de X (creencia tachada en rojo, respuesta en amarillo). Sin caras."""
import os, sys, subprocess, tempfile
sys.path.insert(0, os.path.expanduser('~/Code/RLR_persona/posts/tanda2'))
from anuncios_trafico import tarjeta, CHROME
AQUI = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(tempfile.mkdtemp(), 'p.html')
open(f, 'w').write(tarjeta('ADMISIONES EN COLEGIOS PRIVADOS', 'No es falta de', 'esfuerzo.', 'Es falta de sistema.',
                           'Charla de 6 minutos · Constanza, la IA de admisiones de SuperLeads'))
out = os.path.join(AQUI, '00-portada-no-es-falta-de-esfuerzo-es-falta-de-sistema.png')
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                '--window-size=1600,900', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
print(out)
