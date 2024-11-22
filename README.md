# Node Monitoring Script

Script ini digunakan untuk memantau dan mengelola node di jaringan tertentu. Ini termasuk memperoleh token otentikasi, memverifikasi token, mendapatkan informasi node, memulai sesi, dan memantau status kesehatan sistem.

## Persyaratan

- Python 3.x
- Modul Python: `requests`, `logging`, `json`, `os`, `time`

Anda dapat menginstal modul yang diperlukan dengan menjalankan:

```bash
pip install requests
```

## Konfigurasi

Sebelum menjalankan script, pastikan Anda telah membuat file `config.json` di direktori yang sama dengan script ini. Contoh format `config.json`:

```json
{
    "walletType": "solana",
    "publicAddress": "4n8h1XcF7v8K1Jz5Bq3k9cLm9a1s2eD7cJ8p5w6q9r0m",
    "signature": "0xa3b240f1c9e57f2220618b4e3321ab244a5be6789d338b7e1m2b8eea23cf5a0ec6987e9553ea683cdcef82c8d432b1ee1f2a26349b9d181f50b95a1132921408",
    "publicKey": "0x3e91f45cd9c2bf8b8478f3df4bf19645bab4726d7cd4801ef01df2379d2cd447",
    "nodeId": "12D3KooWEDFTPCGoXXDbmNYpjyZTbz6eEZDyLfPW3Pqw83Ed3xUk"
}

```

## Cara Penggunaan

1. **Clone repositori ini** ke mesin lokal Anda:

   ```bash
   git clone https://github.com/learners00/bless.git
   cd bless
   ```

2. **Setup lingkungan Anda** dengan memastikan semua dependensi Python diinstal.

3. **Jalankan script** dengan perintah berikut:

   ```bash
   python bless.py
   ```

## Fitur

- **Otentikasi**: Mendapatkan dan memverifikasi token otentikasi untuk akses ke node.
- **Informasi Node**: Mendapatkan informasi detail dari node seperti ID, alamat IP, total hadiah, dan status koneksi.
- **Kesehatan Sistem**: Memeriksa status kesehatan sistem secara berkala.
- **Manajemen Sesi**: Memulai sesi baru jika diperlukan.
