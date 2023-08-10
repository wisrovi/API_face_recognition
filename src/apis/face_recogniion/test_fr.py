from src.shared.mariaDB.FingerprintDatabase import FingerprintDatabase

class TestFingerprintDatabase:
    def setup_method(self):
        # Create an instance of FingerprintDatabase for testing
        self.fingerprint_db = FingerprintDatabase(host="localhost", user="your_user", password="your_password", database="test_database")

    def test_save_and_read_fingerprints(self):
        company = "Test Company"
        group = "Test Group"
        fingerprints = ["test_fingerprint1", "test_fingerprint2"]

        # Save fingerprints for testing
        inserted_ids = self.fingerprint_db.save_fingerprints(fingerprints, company, group)
        assert len(inserted_ids) == len(fingerprints)

        # Read fingerprints from the database
        read_fingerprints, table_ids = self.fingerprint_db.read_fingerprints(company, group)

        assert read_fingerprints == fingerprints
        assert set(table_ids) == set(inserted_ids)

    def teardown_method(self):
        # Clean up by deleting test data
        self.fingerprint_db.engine.dispose()

if __name__ == "__main__":
    import pytest
    pytest.main()
