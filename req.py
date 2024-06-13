import requests
import json
import pandas as pd
import time



def get_list(payload: dict) -> str:
    url = "https://faskes.bpjs-kesehatan.go.id/aplicares/Pencarian/getList"

    r = requests.post(url, json=payload)
    return r.text

def parse_get_list(data: str) -> list:
    data = json.loads(data)
    result = []

    for item in data['row']:
        jnsppk = item['jnsppk']
        kdppk = item['kdppk']
        item_data = {"kdppk": kdppk, "jnsppk": jnsppk}
        result.append(item_data)
    return result

def get_data(payload: dict) -> dict:
    url = "https://faskes.bpjs-kesehatan.go.id/aplicares/Pencarian/getData"

    r = requests.post(url, json=payload)
    data = json.loads(r.text)
    return data

def parse_get_data(data: dict) -> dict:
    nama = data['profil']['nmppk']
    telepon = data['profil']['telpppk']
    alamat = data['profil']['nmjlnppk']

    result = {"nama": nama, "telepon": telepon, "alamat": alamat}
    if 'dokter' not in data:
        return result
    else:
        for dokter in data['dokter']:
            no = dokter['no']
            nama_dokter = dokter['namadokter']
            jenis = dokter['namajenistenagamedis']

            data_dokter = {f"nama dokter {no}": nama_dokter, f"jenis tenaga medis {no}": jenis}

            result.update(data_dokter)
    return result


if __name__ == "__main__":
    payload = {"params":
           {"sort":{},
            "search":{},
            "pagination":{
                "start":0,"totalItemCount":"831","number":831,"numberOfPages":84}
            },"propppk":13,"dati2ppk":"","jarakterdekat":0
            }
    
    all_data = get_list(payload)
    data_list = parse_get_list(all_data)

    table_data = []
    
    for i, data in enumerate(data_list):
        print(f"Processing {i+1} of {len(data_list)}")
        if data['jnsppk'] != 'R':
            details = get_data(data)
            rows = parse_get_data(details)
            table_data.append(rows)
            time.sleep(1)

    df = pd.DataFrame(table_data)
    df.to_excel("data.xlsx", index=False)
        
