# ============================================================
#  AH SPAM API - Single File (Accounts + API + Spam)
# ============================================================
import os
import sys
import json
import time
import uuid
import socket
import random
import threading
import urllib3
import http.client
import ssl
import gzip
from io import BytesIO
from datetime import datetime, timezone

import requests
import jwt as pyjwt
from flask import Flask, jsonify, request
from flask_cors import CORS
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from protobuf_decoder.protobuf_decoder import Parser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================================
#  CONSTANTS
# ============================================================
version = "2.132.6"
OB = "OB55"

Key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
Iv  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

GREEN  = '\033[92m'
YELLOW = '\033[93m'
RED    = '\033[91m'
RESET  = '\033[0m'


# ============================================================
#  ACCOUNTS (ضع حساباتك هنا)
# ============================================================

ACCOUNTS = [ ("8416732769", "721d84e50cfaf715a39f"), ("8416732768", "acb1f013fd65911cc2db"), ("8416732861", "743098ea6d26564f2bfa"), ("8416732864", "9fa909719f8d5a0c8a7c"), ("8416732968", "8009432c8642b2570187"), ("8418601769", "ef19e1dff76a00d7749e"), ("8418602822", "dcbfeb036bb2ad47a9d8"), ("8418602826", "4fca6106fbea06d705b4"), ("8418603043", "972afe8e19df9cacb2f9"), ("8418603243", "d2dfa5cad4910b83fa21"), ("8418603435", "fd42362ce1c8112d36e3"), ("8418603630", "6ca6f19e254a431aee4f"), ("8418603874", "e9e0bc37f5f6d4831916"), ("8418605172", "e4fdefb4063dcaff157e"), ("8418605478", "c6585d8cb43432a5e629"), ("8418605760", "25213a7bfced47c9d19e"), ("8418605904", "bec407c639c66243283f"), ("8418606036", "e757a567d873c5a6c30a"), ("8418606247", "324563a00ff2153170e0"), ("8418606297", "7a64f1f34a4002641a8b"), ("8418606419", "e1bb23a736445338dfb4"), ("8418607991", "263b283434f409be2b07"), ("8418608146", "a11604883927f2cfcb39"), ("8418608357", "70f3145b4d59766ad4d2"), ("8418608372", "e85550e5b0b0c3f5d46e"), ("8418608587", "ac9326a51d7a80cc5998"), ("8418608595", "02024340ca6f43c5ddbc"), ("8418608764", "3217e2e23b70f8f484a9"), ("8418608792", "0c3e6bc241a402dbdd62"), ("8418608928", "584e0e8dd867af0b2357"), ("8418609675", "c6a24ddb02efcff9124d"), ("8418609852", "6c8dc15b9dfd2533f802"), ("8418610009", "4b3e215feef8f22bb00c"), ("8418610110", "369181d997b1595e1a80"), ("8418610299", "00ae7a3daaec0a47b101"), ("8418610359", "2a0309910393a89d698f"), ("8418610536", "0e0a079a24f228ea970b"), ("8418610631", "3fde44e46a744c4d38b9"), ("8418612197", "f615c0bf87f1ea1c1e60"), ("8418612266", "e9588a16c88488838067"), ("8418612436", "4a1ee907e0f9588f2bbb"), ("8418612546", "854577ad31e5a2f692d0"), ("8418612637", "9df7e3cc294738a00ec9"), ("8418612715", "771dcfc191995fed3bec"), ("8418612839", "3dc91165c4eaff3e4982"), ("8418612924", "d04666568f7494ff4f9e"), ("8418613000", "c5d751392a36e1f844ac"), ("8418614042", "b999ccdffcd60c93fc82"), ("8418614059", "889b606038572c390f56"), ("8418614283", "4a6fce240a0b467b20dc"), ("8418614300", "be1b33660241f3bbba2c"), ("8418614475", "66d908df8b1a6fdc65dd"), ("8418614646", "2162c3e1c6481b6c7fbf"), ("8418614650", "da762589012cc156214a"), ("8418614812", "589fadf8c5d065ffb599"), ("8418615948", "881c22bad1279604f61a"), ("8404025307", "9a3828b6bbe2a4b5754e"), ("8404025304", "bba316849ab0e305be13"), ("8404025591", "d0df2e86b4a5d9b3cdb9"), ("8404025597", "37f31bf6b925e3430324"), ("8404025839", "38dc2a3bda6fcfe6bc3a"), ("8404025857", "9a99cf86bc48ac57ae75"), ("8404026209", "29eee78d945ce537d669"), ("8404026190", "41061631c8d10acec457"), ("8404026610", "599a4a445397d66f0bc5"), ("8404026611", "243ac5f0d218f018dfec"), ("8404026946", "7bca49df94b2562b0f5e"), ("8404027011", "f869e45dc592c62c85ad"), ("8404027239", "d9894b21976a5e21ed83"), ("8404027319", "a87a2dcf78743f47128c"), ("8404027566", "7cce67faa8dbb0a8964a"), ("8404027649", "a7243d93fdc7036bb8ce"), ("8404029304", "c3030cd0580c70cc8cd6"), ("8404029438", "5190a40c3907d863e9ba"), ("8404029518", "99e4ca44d9c0fef62cfb"), ("8404029614", "e77628267dc7ea6959e7"), ("8404029746", "2c6fb5606dda476cff1d"), ("8404029899", "b39c519057282c90766a"), ("8404029999", "3b4ec34bee5f7031972e"), ("8404030077", "bfbc9aaabb7030cf780f"), ("8404030166", "56a8e17fed7fcce6f349"), ("8404030248", "cae54c48d249e280300e"), ("8404031178", "3ab3f34f92266c5f0778"), ("8404031216", "11b7d952b7561c37b960"), ("8404031460", "71387da22f18bb3fc429"), ("8404031646", "32f33ebafe2687c3868a"), ("8404031729", "d906a8ac684122c01d30"), ("8404031941", "fee4cd27093c5b5eb1a7"), ("8404032031", "e6d22094e65162490b39"), ("8404032172", "a2778c9d97f5d5cd532a"), ("8404032297", "13ad5d53fb6325d677ec"), ("8404033991", "2dd88d1c5af908713f49"), ("8404034142", "130dc8a0336493dcebc4"), ("8404034251", "d34d282aa130503dd15b"), ("8404034498", "2c3ccfe239d633045454"), ("8404034575", "911e12e2e18a386f49d9"), ("8404034764", "ec80c826df7151fd3254"), ("8404034832", "d357d8be2f7efeb5e4fd"), ("8404034963", "1d1d9597c7a1edebc5ab"), ("8404035076", "8e0f4d49fe8d99b03985") ]
# ============================================================
#  HELPERS (من ch9ayfax1.py)
# ============================================================
def EnC_AEs(HeX):
    return AES.new(Key, AES.MODE_CBC, Iv).encrypt(pad(bytes.fromhex(HeX), AES.block_size)).hex()


def DEc_AEs(HeX):
    return unpad(AES.new(Key, AES.MODE_CBC, Iv).decrypt(bytes.fromhex(HeX)), AES.block_size).hex()


def EnC_PacKeT(HeX, K, V):
    return AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(HeX), 16)).hex()


def DEc_PacKeT(HeX, K, V):
    return unpad(AES.new(K, AES.MODE_CBC, V).decrypt(bytes.fromhex(HeX)), 16).hex()


def EnC_Uid(H, Tp):
    e, H = [], int(H)
    while H:
        e.append((H & 0x7F) | (0x80 if H > 0x7F else 0))
        H >>= 7
    return bytes(e).hex() if Tp == 'Uid' else None


def EnC_Vr(N):
    if N < 0:
        return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N:
            BesTo |= 0x80
        H.append(BesTo)
        if not N:
            break
    return bytes(H)


def DEc_Uid(H):
    n = s = 0
    for b in bytes.fromhex(H):
        n |= (b & 0x7F) << s
        if not b & 0x80:
            break
        s += 7
    return n


def CrEaTe_VarianT(field_number, value):
    return EnC_Vr((field_number << 3) | 0) + EnC_Vr(value)


def CrEaTe_LenGTh(field_number, value):
    encoded_value = value.encode() if isinstance(value, str) else value
    return EnC_Vr((field_number << 3) | 2) + EnC_Vr(len(encoded_value)) + encoded_value


def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            packet.extend(CrEaTe_LenGTh(field, CrEaTe_ProTo(value)))
        elif isinstance(value, int):
            packet.extend(CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(CrEaTe_LenGTh(field, value))
    return bytes(packet)


def DecodE_HeX(H):
    F = str(hex(H))[2:]
    return "0" + F if len(F) == 1 else F


def Fix_PackEt(parsed_results):
    result_dict = {}
    for result in parsed_results:
        field_data = {'wire_type': result.wire_type}
        if result.wire_type in ("varint", "string", "bytes"):
            field_data['data'] = result.data
        elif result.wire_type == 'length_delimited':
            field_data["data"] = Fix_PackEt(result.data.results)
        result_dict[result.field] = field_data
    return result_dict


def DeCode_PackEt(input_text):
    try:
        return json.dumps(Fix_PackEt(Parser().parse(input_text)))
    except Exception as e:
        print(f"error {e}")
        return None


def xBunnEr():
    avatar_list = [902033017, 902033016, 902029018, 902045007, 902049015, 902049016,
                   902049017, 902049018, 902000088, 902000306, 902026015, 902047006,
                   902048020, 902047016]
    return random.choice(avatar_list)


def GeneRaTePk(Pk1, N, K, V):
    PkEnc = EnC_PacKeT(Pk1, K, V)
    L = DecodE_HeX(len(PkEnc) // 2)
    pad_ = {2: "000000", 3: "00000", 4: "0000", 5: "000"}.get(len(L))
    if pad_ is None:
        raise ValueError(f"Unexpected length: {len(L)}")
    return bytes.fromhex(N + pad_ + L + PkEnc)


def SPamSq(Uid, K, V):
    same_value = random.choice([4096, 16384, 8192])
    fields = {
        1: 33,
        2: {
            1: int(Uid), 2: "ME", 3: 1, 4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] @CH9AYFAX1",
            7: 330, 8: 1000, 10: "ME",
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56, 97, 52,
                       52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1, 13: int(Uid),
            14: {1: 2203434355, 2: 8,
                 3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"},
            16: 1, 17: 1, 18: 312, 19: 46,
            23: bytes([16, 1, 24, 1]),
            24: xBunnEr(), 26: "", 28: "",
            31: {1: 1, 2: same_value}, 32: same_value,
            34: {1: int(Uid), 2: 8,
                 3: bytes([15, 6, 21, 8, 10, 11, 19, 12, 17, 4, 14, 20, 7, 2, 1, 5, 16, 3, 13, 18])}
        },
        10: "en", 13: {2: 1, 3: 1}
    }
    return GeneRaTePk(CrEaTe_ProTo(fields).hex(), '0515', K, V)


def _read_varint(blob, i):
    res = 0
    sh = 0
    while i < len(blob):
        b = blob[i]
        if isinstance(b, str):
            b = ord(b)
        i += 1
        res |= (b & 0x7F) << sh
        if not (b & 0x80):
            break
        sh += 7
    return res, i


def _decode_pb(blob):
    if isinstance(blob, str):
        blob = blob.encode('latin-1')
    fields = {}
    i = 0
    n = len(blob)
    while i < n:
        try:
            kk, i = _read_varint(blob, i)
        except Exception:
            break
        fn, wt = kk >> 3, kk & 0x07
        try:
            if wt == 0:
                val, i = _read_varint(blob, i)
            elif wt == 2:
                ln, i = _read_varint(blob, i)
                val = blob[i:i + ln]
                i += ln
            elif wt == 5:
                val = blob[i:i + 4]
                i += 4
            elif wt == 1:
                val = blob[i:i + 8]
                i += 8
            else:
                break
        except Exception:
            break
        fields[str(fn)] = val
    return fields


def _to_bytes(x):
    if x is None:
        return None
    if isinstance(x, bytes):
        return x
    if isinstance(x, str):
        return x.encode('latin-1')
    if isinstance(x, int):
        return str(x).encode('latin-1')
    return bytes(x)


def _to_int(x):
    if x is None:
        return 0
    if isinstance(x, int):
        return x
    if isinstance(x, bytes):
        try:
            return int(x.decode('ascii').strip('\x00'))
        except Exception:
            return 0
    if isinstance(x, str):
        try:
            return int(x)
        except Exception:
            return 0
    return 0


def _get_api_config():
    url = 'https://version.ffmax.purplevioleto.com/live/ver.php?lang=ar&device=android'
    try:
        j = requests.get(url, timeout=15, verify=False).json()
    except Exception:
        j = {}
    return {
        'client_ip': j.get('client_ip', ''),
        'vercfg_sign': j.get('vercfg_sign', ''),
    }


def CrEaTe_MaJoR_PaYlOaD(aCcEsS_ToKeN, aCcEsS_OpEnId, pLaTfOrM=4, cLiEnT_iP=None,
                        vErCfG_sIgN=None, tImE_sTr=None):
    if tImE_sTr is None:
        tImE_sTr = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    api = _get_api_config()
    if cLiEnT_iP is None:
        cLiEnT_iP = api['client_ip']
    if vErCfG_sIgN is None:
        vErCfG_sIgN = api['vercfg_sign']

    device_id = f"Google|{uuid.uuid4()}"
    lang_code = "en"

    fields = {
        3: tImE_sTr,
        4: "free fire",
        5: 1,
        7: f"{version}",
        8: "Android OS 14 / API-34 (UP1A.231005.007/E135FXXSEEZE2)",
        9: "Handheld",
        11: "CarrierDataNetwork",
        12: 1672,
        13: 750,
        14: "338",
        15: "ARMv7 VFPv3 NEON | 2002 | 8",
        16: 3702,
        17: "Mali-G52",
        18: "OpenGL ES 3.2 v1.r38p1-01bet0-mbs2v41_0.6d20ec041e51b2f2d25dfc265586ebe8",
        19: device_id,
        20: "104.28.197.151",
        21: lang_code,
        22: str(aCcEsS_OpEnId),
        23: str(pLaTfOrM),
        24: "Handheld",
        25: "samsung SM-E135F",
        26: "ME",
        29: str(aCcEsS_ToKeN),
        30: 1,
        42: "Cellular",
        57: "7428b253defc164018c604a1ebbfebdf",
        60: 52037,
        61: 5355,
        62: 3723,
        63: 3,
        64: 5483,
        65: 52037,
        66: 5483,
        67: 52037,
        73: 2,
        74: "/data/app/~~yACsV8QOk9OexgajWQP30A==/com.dts.freefireth-Bi_wPVrrhYM2nYncc29q7Q==/lib/arm",
        76: 1,
        77: "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~yACsV8QOk9OexgajWQP30A==/com.dts.freefireth-Bi_wPVrrhYM2nYncc29q7Q==/base.apk",
        78: 3,
        79: 1,
        81: "32",
        83: "2019121229",
        86: "OpenGLES2",
        87: 8191,
        88: int(pLaTfOrM),
        92: 16091,
        93: "android",
        94: "KqsHT3Yeqo3RLRl8efNiL3aL/1SHwlSrtK0DwNAqdkNBQz70TeVy+icaIwuR3UK4b65Uf3IG5xBFEv0uu+jQZI+rOYCmNCsXjJT4QcZaYgoaaUGG",
        95: 111107,
        96: "{\"cur_rate\":null,\"support_etc2\":false}",
        97: 1,
        98: 1,
        99: str(pLaTfOrM),
        100: str(pLaTfOrM),
        102: "4503454457550c0766",
        104: 53792,
        105: 1,
        106: "https://dl-bs.ggpolarbear.com/live/ABHotUpdates/|https://core-bs.ggpolarbear.com/live/ABHotUpdates/|6b2078db9d22dd98f8e9386a39af8462",
        107: "c8e41b7a93f02d56e1a94c7b8203f5d1",
    }
    return bytes(CrEaTe_ProTo(fields))



# ============================================================
#  AUTH FUNCTIONS
# ============================================================
class AuthFunctions:
    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.Token = None
        self.AutH_ToKeN_0115 = None
        self.host = None
        self.port = None
        self.host2 = None
        self.port2 = None
        self.key = None
        self.iv = None
        self.bot = None
        self.aCcEsS_ToKeN = None
        self.aCcEsS_UiD = None
        self.aCcEsS_pLaTfOrM = 4

    def finle_tokn(self, bot_uid, jwt_token, timedata, key, iv):
        try:
            e = AES.new(key, AES.MODE_CBC, iv).encrypt(
                pad(jwt_token.encode("utf-8"), AES.block_size)
            )
            head = (
                bytes.fromhex("7319")
                + int(bot_uid).to_bytes(8, "big")
                + int(timedata).to_bytes(4, "big")
                + b"\x00\x00\x00\x00"
                + len(e).to_bytes(4, "big")
            )
            return (head + e).hex()
        except Exception as e:
            print(f"finle_tokn Error: {e}")
            return None

    def sTeVe_GuEsT_EnTeR(self, uSeR_iD, uSeR_PaSs):
        url = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
        headers = {
            "Accept": "application/json",
            "Connection": "close",
            "Content-Type": "application/json; charset=utf-8",
            "Host": "100067.connect.garena.com",
            "User-Agent": "GarenaMSDK/4.0.42(A5010 ;Android 9;en;US;app 2.126.1 2019118045;)",
        }
        payload = {
            "client_id": 100067,
            "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
            "client_type": 2,
            "device_id": f"02-{uuid.uuid4()}",
            "password": f"{uSeR_PaSs}",
            "response_type": "token",
            "uid": int(uSeR_iD),
        }

        for attempt in range(5):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=15, verify=False)
                res = r.json()
                if res.get('code') == 1006 or 'error_too_many_requests' in str(res):
                    time.sleep(30 * (attempt + 1))
                    continue
                data = res.get('data', res)
                self.aCcEsS_ToKeN = data.get('access_token')
                self.aCcEsS_UiD = data.get('open_id') or data.get('uid')
                self.aCcEsS_pLaTfOrM = data.get('platform', 4)
                if not self.aCcEsS_ToKeN:
                    time.sleep(10)
                    continue
                time.sleep(0.2)
                return self.sTeVe_MaJoR_EnTeR(self.aCcEsS_ToKeN, self.aCcEsS_UiD)
            except Exception:
                time.sleep(10)
                continue

        print(f" - access_token missing after retries for {uSeR_iD}")
        return None

    def sTeVe_DatA_EnTeR(self, sTeVe_JwT, pAyLoAd_DatA):
        url = 'https://clientbp.ppmainecoonghj.com/GetLoginData'
        headers = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {sTeVe_JwT}',
            'X-Unity-Version': '2022.3.47f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': OB,
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Host': 'loginbp.ppmainecoonghj.com',
            'X-Ga-Sv': '1789534056',
            'Connection': 'close',
            'Accept-Encoding': 'gzip'
        }
        r = requests.post(url, headers=headers, data=pAyLoAd_DatA, verify=False, timeout=20)
        self.dEcOdEd_Pb = json.loads(DeCode_PackEt(r.content.hex()))
        aDdReSs  = self.dEcOdEd_Pb['32']['data']
        aDdReSs2 = self.dEcOdEd_Pb['14']['data']
        iP   = aDdReSs[:len(aDdReSs) - 6]
        iP2  = aDdReSs2[:len(aDdReSs2) - 6]
        pOrT = aDdReSs[len(aDdReSs) - 5:]
        pOrT2 = aDdReSs2[len(aDdReSs2) - 5:]
        return iP, pOrT, iP2, pOrT2

    def sTeVe_MaJoR_EnTeR(self, aCcEsS_ToKeN, aCcEsS_UiD):
        url = "https://loginbp.ppmainecoonghj.com/MajorLogin"
        headers = {
            'X-Unity-Version': '2022.3.47f1',
            'ReleaseVersion': OB,
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Host': 'loginbp.ppmainecoonghj.com',
            'X-Ga-Sv': '1789534056',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }

        pAyLoAd_DatA = CrEaTe_MaJoR_PaYlOaD(
            aCcEsS_ToKeN, aCcEsS_UiD, pLaTfOrM=self.aCcEsS_pLaTfOrM,
        )

        enc_hex = EnC_AEs(pAyLoAd_DatA.hex())
        eNcRyPtEd_PaYlOaD = bytes.fromhex(enc_hex) if isinstance(enc_hex, str) else enc_hex

        r = None
        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, data=eNcRyPtEd_PaYlOaD,
                                  verify=False, timeout=20)
                if r.status_code == 200:
                    break
                if r.status_code == 503:
                    time.sleep(10 * (attempt + 1))
                    continue
                return None
            except Exception:
                time.sleep(10)
                continue
        else:
            print(f" - MajorLogin failed HTTP 503 for {aCcEsS_UiD}")
            return None

        raw = r.content
        pb = None
        for offset in (0, 64, 10, 2, 8, 16, 32):
            try:
                candidate = _decode_pb(raw[offset:])
                if '1' in candidate and '8' in candidate and '22' in candidate and '23' in candidate:
                    pb = candidate
                    break
            except Exception:
                continue

        if pb is None:
            return None

        self.bot = _to_int(pb['1'])
        j = pb['8']
        self.sTeVe_JwT = j.decode('utf-8', 'ignore') if isinstance(j, bytes) else str(j)
        self.timedata = _to_int(pb.get('21'))
        self.k = _to_bytes(pb['22'])
        self.v = _to_bytes(pb['23'])

        iP, pOrT, iP2, pOrT2 = self.sTeVe_DatA_EnTeR(self.sTeVe_JwT, eNcRyPtEd_PaYlOaD)
        if not iP:
            print(" - GetLoginData failed")
            return None

        self.iP, self.pOrT = iP, pOrT
        self.iP2, self.pOrT2 = iP2, pOrT2

        self.sTeVe_AuTh_ToKeN = self.finle_tokn(
            bot_uid=self.bot, jwt_token=self.sTeVe_JwT,
            timedata=self.timedata, key=self.k, iv=self.v
        )

        if not self.sTeVe_AuTh_ToKeN:
            print(" - Auth Token failed!")
            return None

        self.Token = self.sTeVe_JwT
        self.AutH_ToKeN_0115 = self.sTeVe_AuTh_ToKeN
        self.host = self.iP
        self.port = self.pOrT
        self.host2 = self.iP2
        self.port2 = self.pOrT2
        self.key = self.k
        self.iv = self.v

        return self.sTeVe_AuTh_ToKeN, self.k, self.v

    def Get_FiNal_ToKen_0115(self):
        return self.sTeVe_GuEsT_EnTeR(self.id, self.password)


# ============================================================
#  FLASK APP + GLOBALS
# ============================================================
app = Flask(__name__)
CORS(app)

connected_clients = {}
connected_clients_lock = threading.Lock()

all_accounts = {}
all_accounts_lock = threading.Lock()

spam_speed = 2
spam_count = 1
spam_running = False
spam_targets = set()
state_lock = threading.Lock()

spam_event = threading.Event()


def set_acc_status(acc_id, status):
    with all_accounts_lock:
        if acc_id in all_accounts:
            all_accounts[acc_id]['status'] = status


# ============================================================
#  FF CLIENT (BOT)
# ============================================================
class FF_CLient(AuthFunctions):
    def __init__(self, id, password):
        super().__init__(id, password)
        self.running = True
        self.targets = set()
        self.send_lock = threading.Lock()
        self.account_uid = None
        self.cli = None
        self.cli2 = None
        self.spam_thread_started = False

        threading.Thread(target=self._auth_loop, daemon=True).start()
        threading.Thread(target=self._game_keepalive, daemon=True).start()
        threading.Thread(target=self._room_keepalive, daemon=True).start()
        self.start_continuous_spam()

    def _auth_loop(self):
        while self.running:
            set_acc_status(self.id, 'connecting')
            try:
                self.Get_FiNal_ToKen_0115()
                if self.AutH_ToKeN_0115:
                    try:
                        decoded = pyjwt.decode(self.Token, options={"verify_signature": False})
                        self.account_uid = decoded.get('account_id')
                    except Exception:
                        self.account_uid = None

                    with connected_clients_lock:
                        connected_clients[self.id] = self
                    set_acc_status(self.id, 'online')
                    print(f"{GREEN}Bot {self.id} Is Online ✅{RESET}")
                    return
            except Exception:
                pass
            time.sleep(3)

    def _game_keepalive(self):
        while self.running:
            if not self.AutH_ToKeN_0115:
                time.sleep(1)
                continue
            try:
                self.cli = socket.create_connection((self.host, int(self.port)), timeout=10)
                self.cli.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                self.cli.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.cli.send(bytes.fromhex(self.AutH_ToKeN_0115))

                while self.running:
                    try:
                        data = self.cli.recv(1024)
                        if not data:
                            break
                    except socket.timeout:
                        continue
                    except Exception:
                        break
            except Exception:
                pass
            finally:
                try:
                    self.cli.close()
                except Exception:
                    pass
            if self.running:
                time.sleep(3)

    def _room_keepalive(self):
        while self.running:
            if not self.AutH_ToKeN_0115:
                time.sleep(1)
                continue
            try:
                s = socket.create_connection((self.host2, int(self.port2)), timeout=10)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.send(bytes.fromhex(self.AutH_ToKeN_0115))

                with self.send_lock:
                    self.cli2 = s

                while self.running:
                    try:
                        data = s.recv(4096)
                        if not data:
                            break
                    except socket.timeout:
                        continue
                    except Exception:
                        break
            except Exception:
                pass
            finally:
                with self.send_lock:
                    self.cli2 = None
                set_acc_status(self.id, 'connecting')
            if self.running:
                time.sleep(3)

    def add_target(self, target_id):
        self.targets.add(str(target_id))

    def remove_target(self, target_id):
        self.targets.discard(str(target_id))

    def clear_targets(self):
        self.targets.clear()

    def start_continuous_spam(self):
        if self.spam_thread_started:
            return
        self.spam_thread_started = True
        threading.Thread(target=self._spam_loop, daemon=True).start()

    def _spam_loop(self):
        while self.running:
            with state_lock:
                running = spam_running
                targets_snapshot = list(self.targets)

            if not running or not targets_snapshot:
                spam_event.wait(timeout=1.0)
                spam_event.clear()
                continue

            try:
                with self.send_lock:
                    if self.cli2 and self.key and self.iv:
                        for target in targets_snapshot:
                            for _ in range(spam_count):
                                self.cli2.send(SPamSq(target, self.key, self.iv))
                        print(f"{YELLOW}from {self.id} => to {targets_snapshot} ({spam_count} requests){RESET}")
                    else:
                        time.sleep(0.5)
                        continue
            except Exception as e:
                print(f"{RED}from {self.id} => ERROR: {str(e)}{RESET}")
                time.sleep(0.5)
                continue

            time.sleep(spam_speed)


# ============================================================
#  START ACCOUNTS (from hardcoded list)
# ============================================================
def start_accounts():
    if not ACCOUNTS:
        print(f"{RED}No accounts found in ACCOUNTS list{RESET}")
        return

    with all_accounts_lock:
        for uid, pw in ACCOUNTS:
            all_accounts[uid] = {'id': uid, 'password': pw, 'status': 'offline'}

    for uid, pw in ACCOUNTS:
        try:
            FF_CLient(uid, pw)
        except Exception as e:
            set_acc_status(uid, 'offline')
            print(f"{RED}Failed to start {uid}: {e}{RESET}")
        time.sleep(0.05)

    print(f"{GREEN}Started {len(ACCOUNTS)} accounts{RESET}")


# ============================================================
#  TARGET MANAGEMENT
# ============================================================
def add_target_for_all(target_id):
    global spam_running
    with state_lock:
        spam_running = True
        spam_targets.add(target_id)
    with connected_clients_lock:
        for _, client in connected_clients.items():
            client.add_target(target_id)
    spam_event.set()


def remove_target_for_all(target_id):
    with state_lock:
        spam_targets.discard(target_id)
    with connected_clients_lock:
        for _, client in connected_clients.items():
            client.remove_target(target_id)
    spam_event.set()


def clear_all_targets():
    global spam_running
    with state_lock:
        spam_running = False
        spam_targets.clear()
    with connected_clients_lock:
        for _, client in connected_clients.items():
            client.clear_targets()
    spam_event.set()


# ============================================================
#  API ROUTES
# ============================================================
@app.route('/spm', methods=['GET'])
def api_spam():
    uid = request.args.get('uid', '').strip()
    if not uid or not uid.isdigit():
        return jsonify({"success": False, "message": "خطأ ! الرجاء كتابة الأيدي الصحيح للاعب", "code": 400}), 400

    with connected_clients_lock:
        if not connected_clients:
            return jsonify({"success": False, "message": "no connected accounts", "code": 400}), 400

    with state_lock:
        if uid in spam_targets:
            return jsonify({"success": True, "message": f"هذا الحساب مضاف ب قائمة المستهدفين بالفعل !",
                            "active_targets": list(spam_targets), "code": 200})

    add_target_for_all(uid)
    with state_lock:
        active_targets = list(spam_targets)

    return jsonify({
        "success": True, "message": f"تم إضافة الحساب الى قائمة المستهدفين", "target": uid,
        "active_targets": active_targets, "bots_count": len(connected_clients),
        "spam_speed": spam_speed, "spam_count": spam_count, "code": 200
    })


@app.route('/remove', methods=['GET'])
def api_remove():
    uid = request.args.get('uid', '').strip()
    if not uid or not uid.isdigit():
        return jsonify({"success": False, "message": "خطأ ! الرجاء كتابة الأيدي الصحيح للاعب", "code": 400}), 400

    with state_lock:
        if uid not in spam_targets:
            return jsonify({"success": True, "message": f"هذا الحساب ليس من قائمة المستهدفين",
                            "active_targets": list(spam_targets), "code": 200})

    remove_target_for_all(uid)
    with state_lock:
        active_targets = list(spam_targets)

    return jsonify({"success": True, "message": f"تم إزالة الحساب من قائمة المستهدفين",
                    "active_targets": active_targets, "code": 200})


@app.route('/stop', methods=['GET'])
def api_stop():
    clear_all_targets()
    return jsonify({"success": True, "message": "spam stopped", "code": 200})


@app.route('/targets', methods=['GET'])
def api_targets():
    with state_lock:
        active_targets = list(spam_targets)
    return jsonify({"success": True, "active_targets": active_targets,
                    "count": len(active_targets), "code": 200})


@app.route('/status', methods=['GET'])
def api_status():
    with connected_clients_lock:
        online_ids = set(connected_clients.keys())
        online_list = [{
            'id': c.id,
            'player_uid': getattr(c, 'account_uid', None),
            'targets': list(c.targets),
            'status': 'online'
        } for c in connected_clients.values()]

    with all_accounts_lock:
        offline_list = [{'id': a['id'], 'status': a['status']}
                        for a in all_accounts.values() if a['id'] not in online_ids]
    total = len(all_accounts)

    with state_lock:
        running = spam_running
        active_targets = list(spam_targets)

    return jsonify({
        "success": True,
        "online": online_list,
        "online_count": len(online_list),
        "offline": offline_list,
        "offline_count": len(offline_list),
        "total": total,
        "spam_running": running,
        "active_targets": active_targets,
        "spam_speed": spam_speed,
        "spam_count": spam_count,
        "code": 200
    })


@app.route('/bots', methods=['GET'])
def api_bots():
    with connected_clients_lock:
        bots = [{
            'id': c.id,
            'player_uid': getattr(c, 'account_uid', None),
            'targets': list(c.targets),
            'status': 'online'
        } for c in connected_clients.values()]
    return jsonify({"success": True, "bots": bots, "count": len(bots), "code": 200})


@app.route('/health', methods=['GET'])
def api_health():
    with connected_clients_lock:
        online = len(connected_clients)
    with all_accounts_lock:
        total = len(all_accounts)
    with state_lock:
        running = spam_running
        targets = len(spam_targets)

    return jsonify({
        "success": True, "status": "running", "bots_online": online,
        "bots_total": total, "spam_running": running,
        "active_targets": targets, "code": 200
    })


@app.route('/settings', methods=['GET'])
def api_settings():
    global spam_speed, spam_count
    speed = request.args.get('speed')
    count = request.args.get('count')

    if speed is not None:
        try:
            new_speed = float(speed)
            if new_speed < 0.05:
                return jsonify({"success": False, "message": "speed must be >= 0.05", "code": 400}), 400
            spam_speed = new_speed
        except ValueError:
            return jsonify({"success": False, "message": "invalid speed value", "code": 400}), 400

    if count is not None:
        try:
            new_count = int(count)
            if new_count < 1:
                return jsonify({"success": False, "message": "count must be >= 1", "code": 400}), 400
            spam_count = new_count
        except ValueError:
            return jsonify({"success": False, "message": "invalid count value", "code": 400}), 400

    spam_event.set()
    return jsonify({"success": True, "spam_speed": spam_speed,
                    "spam_count": spam_count, "code": 200})


# ============================================================
#  RUNNER
# ============================================================
def run_api():
    print(f"{GREEN}[START]{RESET} ch9ayfax1 Single-File API")
    print(f"{YELLOW}Accounts loaded: {len(ACCOUNTS)}{RESET}")
    print(f"{YELLOW}Default settings:{RESET}")
    print(f"  spam speed: {spam_speed} sec")
    print(f"  requests per target: {spam_count}")
    print(f"{YELLOW}Endpoints:{RESET}")
    print(f"  /spm?uid=UID")
    print(f"  /remove?uid=UID")
    print(f"  /stop")
    print(f"  /targets")
    print(f"  /status")
    print(f"  /bots")
    print(f"  /health")
    print(f"  /settings?speed=0.1&count=10")

    threading.Thread(target=start_accounts, daemon=True).start()
    app.run(host='0.0.0.0', port=8002, debug=False, threaded=True, use_reloader=False)


if __name__ == "__main__":
    run_api()