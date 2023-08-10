
from shared.mariaDB.ExtendedFingerprintDatabase import ExtendedFingerprintDatabase
from shared.mariaDB.FingerprintDatabase import FingerprintDatabase


if __name__ == "__main__":

    
    external = ExtendedFingerprintDatabase(
        host="mariaDB",
        user="fingerprint_FC_db",
        password="secret_fingerprint_password",
        database="fingerprintdb"
    )
    df = external.export_database_to_dataframe("My Company", "Group A")
    print(df.head())

    
    exit()
    

    fingerprint_db = FingerprintDatabase(host="mariaDB", user="fingerprint_FC_db", password="secret_fingerprint_password", database="fingerprintdb")

    fingerprints_to_save = ["fingerprint1", "fingerprint2", "fingerprint3"]
    single_fingerprint = "new_fingerprint"
    company = "My Company"
    group = "Group A"
    
    inserted_id = fingerprint_db.save_fingerprints(single_fingerprint, company, group)
    print("Inserted ID:", inserted_id)
    
    multiple_inserted_ids = fingerprint_db.save_fingerprints(fingerprints_to_save, company, group)
    print("Multiple Inserted IDs:", multiple_inserted_ids)
    
    fingerprints, table_ids = fingerprint_db.read_fingerprints(company, group)
    print("Fingerprints:", fingerprints)
    print("Table IDs:", table_ids)

