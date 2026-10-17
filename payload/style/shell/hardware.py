#!/usr/bin/env python3
"""Read-only hardware snapshot. Missing sensors stay unavailable; never wake a sleeping GPU."""
import json
import shutil
import subprocess
import time
from pathlib import Path

def read(path):
    try:return Path(path).read_text().strip()
    except (OSError,ValueError):return ''

def number(path,scale=1):
    try:return round(float(read(path))/scale,1)
    except ValueError:return None

def cpu_ticks():
    fields=read('/proc/stat').splitlines()[0].split()[1:9]
    values=list(map(int,fields))
    return sum(values),values[3]+values[4]

def snapshot():
    before=cpu_ticks();time.sleep(.15);after=cpu_ticks()
    elapsed=after[0]-before[0]
    usage=round(100*(1-(after[1]-before[1])/elapsed),1) if elapsed>0 else None
    mem={line.split(':')[0]:int(line.split()[1])*1024 for line in read('/proc/meminfo').splitlines() if len(line.split())>=2}
    total=mem.get('MemTotal',0);used=total-mem.get('MemAvailable',total)
    info=read('/proc/cpuinfo');cpu=next((line.split(':',1)[1].strip() for line in info.splitlines() if line.startswith('model name')),'Processor')
    temperatures=[];fans=[];gpus=[]
    for hw in sorted(Path('/sys/class/hwmon').glob('hwmon*')):
        name=read(hw/'name') or hw.name
        # NVIDIA sysfs reads may resume the GPU; skip sensors while suspended.
        if read(hw/'device/power/runtime_status') in {'suspended','suspending'}:continue
        for f in sorted(hw.glob('temp*_input')):
            value=number(f,1000)
            if value is not None and -20<=value<=150:
                label=read(f.with_name(f.name.replace('_input','_label'))) or f.stem.replace('_input','')
                temperatures.append({'name':name+' · '+label,'value':value,'unit':'°C'})
        for f in sorted(hw.glob('fan*_input')):
            value=number(f)
            if value is not None:fans.append({'name':name+' · '+(read(f.with_name(f.name.replace('_input','_label'))) or f.stem.replace('_input','')),'value':value,'unit':'RPM'})
    for card in sorted(Path('/sys/class/drm').glob('card[0-9]*')):
        if not (card/'device').exists() or '-' in card.name:continue
        vendor=read(card/'device/vendor');label={'0x10de':'NVIDIA','0x1002':'AMD','0x8086':'Intel'}.get(vendor,'GPU')+' · '+card.name
        sleeping=read(card/'device/power/runtime_status') in {'suspended','suspending'}
        busy=None if sleeping else number(card/'device/gpu_busy_percent')
        gpus.append({'name':label,'state':'Sleeping' if sleeping else (str(busy)+'% load' if busy is not None else 'Active · load sensor unavailable')})
    # Query active NVIDIA cards only when all NVIDIA devices are awake.
    nvidia=[d for d in Path('/sys/bus/pci/devices').glob('*') if read(d/'vendor')=='0x10de' and read(d/'class').startswith('0x03')]
    if nvidia and all(read(d/'power/runtime_status')=='active' for d in nvidia) and shutil.which('nvidia-smi'):
        try:
            result=subprocess.run(['nvidia-smi','--query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total','--format=csv,noheader,nounits'],capture_output=True,text=True,timeout=1.5)
            if result.returncode==0:
                rows=[]
                for line in result.stdout.splitlines():
                    values=[v.strip() for v in line.split(',')]
                    if len(values)==5:rows.append({'name':values[0],'state':values[1]+'°C · '+values[2]+'% load · '+values[3]+'/'+values[4]+' MiB'})
                if rows:gpus=[g for g in gpus if not g['name'].startswith('NVIDIA')]+rows
        except (OSError,subprocess.TimeoutExpired):pass
    disk=shutil.disk_usage(str(Path.home()))
    cpu_temps=[t['value'] for t in temperatures if any(w in t['name'].lower() for w in ['coretemp','k10temp','cpu','package','tctl','x86_pkg'])]
    return {'cpuName':cpu,'cpuUsage':usage,'cpuTemp':max(cpu_temps) if cpu_temps else None,
            'memoryUsed':round(used/1024**3,1),'memoryTotal':round(total/1024**3,1),'memoryPercent':round(used/total*100) if total else 0,
            'diskUsed':round(disk.used/1024**3),'diskTotal':round(disk.total/1024**3),'diskPercent':round(disk.used/disk.total*100),
            'uptime':round(float(read('/proc/uptime').split()[0])/3600,1),'temperatures':temperatures,'fans':fans,'gpus':gpus,'error':''}

if __name__=='__main__':
    try:print(json.dumps(snapshot()))
    except Exception as exc:print(json.dumps({'error':str(exc)}))
