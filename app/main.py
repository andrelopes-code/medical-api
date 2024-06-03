from fastapi import FastAPI
import debugpy

app = FastAPI(title='Medical Appointments', version='0.1.0')


debugpy.listen(('0.0.0.0', 5678))

laa = ['aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa', 'aaaa']
