"""Reviewed quote text and transparent PNG assets. Runtime uses only the standard library."""
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib

ROOT=Path(__file__).resolve().parent/'fastfetch-quotes'
# Exact display wording. Line breaks are visual layout, not added punctuation.
QUOTES={
    'plague-tale':('We will live.', 'And we will heal.'),
    'deltarune':('(Well, there is', 'a man here.)'),
    'deltarune-snowgrave':('Proceed',),
    'deltarune-adventure':('Nothing is', 'stronger than...', 'a... Flower\'s...', 'dream...!'),
    'deltarune-guardian':('AND TITANS', 'SHAPE FROM', 'DARKENED EYES.'),
    # Caesar +3 of THE WOODS REMEMBER WHAT THE TOWN FORGETS.
    'gravity-falls':('WKH ZRRGV UHPHPEHU', 'ZKDW WKH WRZQ', 'IRUJHWV.'),
    'spider-punk':('BREAK THE', 'CANON.'),
}

def quote_asset(theme):
    lines=QUOTES.get(theme)
    if lines is None:return None
    return ('\n'.join('$1'+line.center(26).rstrip() for line in lines)+'\n').encode()

def chunk(kind,data):
    return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)

def quote_png(theme,color):
    if theme not in QUOTES:return None
    if not re.fullmatch(r'#[0-9a-fA-F]{6}',color):raise ValueError('Invalid Fastfetch quote color.')
    manifest=json.loads((ROOT/'manifest.json').read_text());row=manifest['assets'][theme]
    path=ROOT/(theme+'.png')
    if path.is_symlink():raise ValueError('Linked Fastfetch quote asset was kept.')
    data=path.read_bytes()
    if hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('Fastfetch quote image checksum differs: '+theme)
    if data[:8]!=b'\x89PNG\r\n\x1a\n':raise ValueError('Invalid Fastfetch quote image.')
    if row.get('renderMode')=='full-color':
        # The approved illustration is delivered byte-for-byte, without tinting.
        if theme not in ('deltarune','deltarune-snowgrave') or len(data)<33 or data[12:16]!=b'IHDR' or struct.unpack('>II',data[16:24])!=(1254,1254) or data[24:26]!=b'\x08\x06':raise ValueError('Unexpected approved RGBA asset.')
        return data
    result=[data[:8]];offset=8;palette=False;alpha=False
    rgb=bytes.fromhex(color[1:])
    while offset<len(data):
        size=struct.unpack('>I',data[offset:offset+4])[0];kind=data[offset+4:offset+8];body=data[offset+8:offset+8+size];end=offset+12+size
        if len(body)!=size or end>len(data) or zlib.crc32(kind+body)&0xffffffff!=struct.unpack('>I',data[end-4:end])[0]:raise ValueError('Damaged Fastfetch quote PNG chunk.')
        if kind==b'IHDR' and (struct.unpack('>II',body[:8])!=(1536,1280) or body[8:10]!=b'\x08\x03'):raise ValueError('Unexpected Fastfetch quote dimensions/type.')
        if kind==b'PLTE':body=rgb*256;palette=True
        if kind==b'tRNS':
            if body!=bytes(range(256)):raise ValueError('Unexpected quote alpha palette.')
            alpha=True
        result.append(chunk(kind,body));offset=end
    if not palette or not alpha:raise ValueError('Fastfetch quote alpha palette is missing.')
    return b''.join(result)

def image_logo(path,compact=False,theme=None):
    # Kitty receives the actual PNG file. Explicit cells avoid terminal size probes.
    return {'type':'kitty-direct','source':str(path),'position':'left',
            'width':(40 if compact else 50) if theme in ('deltarune','deltarune-snowgrave') else (28 if compact else 36),
            'height':(20 if compact else 25) if theme in ('deltarune','deltarune-snowgrave') else (12 if compact else 15),
            'padding':{'left':1,'right':4}}
