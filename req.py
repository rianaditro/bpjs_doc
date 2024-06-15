import requests
import json
import pandas as pd
import time



def get_list(payload: dict) -> str:
    url = "https://faskes.bpjs-kesehatan.go.id/aplicares/Pencarian/getList"

    r = requests.post(url, json=payload)
    return r.text

def parse_get_list(data: str, dati2ppk:str) -> list:
    data = json.loads(data)
    result = []
    print(f"{data['totalItem']} of item found from {dati2ppk}")
    for item in data['row']:
        jnsppk = item['jnsppk']
        kdppk = item['kdppk']
        item_data = {"kdppk": kdppk, "jnsppk": jnsppk, "dati2ppk": dati2ppk, "totalItem": data["totalItem"]}
        result.append(item_data)
    return result

def get_list_by_dati2pplk(list_dati2ppk: list) -> list:
    result = []
    for item in list_dati2ppk:
        payload = {"params":{"sort":{},
                        "search":{},
                        "pagination":{"start":0,
                                #    "totalItemCount":"3",
                                    "number":999
                                #    ,"numberOfPages":1
                                    }},
            "propppk":"13",
            "dati2ppk":item['id'],
            # "jnsppk":item['jnsppk'],
            "jarakterdekat":0}
        # payload = {"propppk": 13, "dati2ppk": item['id']}
        data = get_list(payload)
        data = parse_get_list(data, item['name'])
        print(f"for {item} get {len(data)} items")
        for i in data:
            result.append(i)
    print(f"total items are {len(result)}")
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

def convert_jnsppk(code: str) -> str:
    if code == "R":
        return "Rumah Sakit"
    elif code == "P":
        return "Puskesmas"
    elif code == "U":
        return "Dokter Praktik Perorangan"
    elif code == "G":
        return "Dokter Gigi"
    elif code == "S":
        return "Klinik Utama"
    elif code == "B":
        return "Klinik Pratama"
    elif code == "A":
        return "Apotek"


if __name__ == "__main__":

    dati2ppk = [
    {
        "id": "0176",
        "name": "KAB. KULON PROGO"
    },
    {
        "id": "0177",
        "name": "KAB. BANTUL"
    },
    {
        "id": "0178",
        "name": "KAB. GUNUNG KIDUL"
    },
    {
        "id": "0179",
        "name": "KAB. SLEMAN"
    },
    {
        "id": "0180",
        "name": "KOTA YOGYAKARTA"
    }
]
    
    all_data = get_list_by_dati2pplk(dati2ppk)

    table_data = []
    
    for i, data in enumerate(all_data):
        print(f"Processing {i+1} of {len(all_data)}")
        details = get_data(data)
        rows = parse_get_data(details)
        rows['kabupaten/kota'] = data['dati2ppk']
        rows['jenis faskes'] = convert_jnsppk(data['jnsppk'])
        print(rows)
        table_data.append(rows)
        time.sleep(1)

    df = pd.DataFrame(table_data)
    df.to_excel("data.xlsx", index=False)
        
