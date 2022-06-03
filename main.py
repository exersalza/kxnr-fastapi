import psutil

from fastapi import FastAPI

# client creation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:*',
    '127.0.0.1:*'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])


@app.get("/")
async def root():
    return {"message": "Hallo welt, kannst du mich hören?"}


@app.get('/sys/totalusage')
async def usage() -> dict:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    freq = {}
    disks = {'usage': {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': disk.percent
    }}

    for v, i in enumerate(psutil.cpu_freq(percpu=True)):
        freq[v] = {'current': i.current, 'min': i.min, 'max': i.max}

    for v, i in enumerate(psutil.disk_partitions()):
        disks[f'mount{v}'] = {'device': i.device,
                    'mountpoint': i.mountpoint,
                    'fstype': i.fstype,
                    'opts': i.opts,
                    'maxfile': i.maxfile,
                    'maxpath': i.maxpath}

    ret = {
        'memory': {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used,
            'free': memory.free,
            'buffered': memory.buffers,
            'active': memory.active,
            'inactive': memory.inactive,
            'shared': memory.shared,
            'slab': memory.slab
        },
        'cpu': {
            'percent': psutil.cpu_percent(),
            'count': psutil.cpu_count(),
            'freq': freq,
        },
        'disk': disks
    }
    return ret
