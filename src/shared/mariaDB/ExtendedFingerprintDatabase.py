import pandas as pd
from shared.mariaDB.FingerprintDatabase import FingerprintDatabase


class ExtendedFingerprintDatabase(FingerprintDatabase):
    """
    ExtendedFingerprintDatabase class.

    This class extends the FingerprintDatabase class
    with additional functionality.
    """

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
    ):
        super().__init__(host, user, password, database)

    @FingerprintDatabase.requires_connection
    @FingerprintDatabase.log_execution
    def export_database_to_dataframe(
        self,
        company: str,
        group: str,
    ) -> pd.DataFrame:
        """
        Export the entire database associated with the given company and
        group to a DataFrame.

        :param company: Company name.
        :type company: str

        :param group: Group name.
        :type group: str

        :return: DataFrame containing the exported data.
        :rtype: pd.DataFrame
        """

        fingerprints, table_ids = self.read_fingerprints(company, group)
        data = {"Fingerprint": fingerprints, "Table_ID": table_ids}
        df = pd.DataFrame(data)

        return df

    @FingerprintDatabase.requires_connection
    @FingerprintDatabase.log_execution
    def export_whole_database_to_dataframe(self) -> pd.DataFrame:
        """
        Export the entire database to a DataFrame.

        :return: DataFrame containing the exported data.
        :rtype: pd.DataFrame
        """

        fingerprints, table_ids = self.read_fingerprints_for_all()
        data = {"Fingerprint": fingerprints, "Table_ID": table_ids}
        df = pd.DataFrame(data)

        return df

    @FingerprintDatabase.requires_connection
    @FingerprintDatabase.log_execution
    def import_dataframe_to_database(
        self, company: str, group: str, dataframe: pd.DataFrame
    ) -> None:
        """
        Import data from a DataFrame to the database associated
        with the given company and group.

        :param company: Company name.
        :type company: str

        :param group: Group name.
        :type group: str

        :param dataframe: DataFrame containing the data to be imported.
        :type dataframe: pd.DataFrame
        """
        if "Fingerprint" not in dataframe.columns:
            raise ValueError("DataFrame must contain a 'Fingerprint' column.")

        fingerprints = dataframe["Fingerprint"].tolist()

        if not all(isinstance(fp, str) for fp in fingerprints):
            raise ValueError("All fingerprints must be strings.")

        existing_fingerprints, _ = self.read_fingerprints(
            company, group
        )  # Read existing fingerprints from the database

        with self.session_scope():
            for fingerprint in fingerprints:
                if (
                    fingerprint not in existing_fingerprints
                ):  # Check if the fingerprint already exists
                    self.save_fingerprints(fingerprint, company, group)

    @FingerprintDatabase.requires_connection
    @FingerprintDatabase.log_execution
    def import_dataframe_to_whole_database(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Import data from a DataFrame to the entire database.

        :param dataframe: DataFrame containing the data to be imported.
        :type dataframe: pd.DataFrame
        """

        required_columns = ["Fingerprint", "Company", "Group"]

        if not all(col in dataframe.columns for col in required_columns):
            raise ValueError(
                f"DataFrame not contain: {', '.join(required_columns)}.",
            )

        fingerprints = dataframe["Fingerprint"].tolist()
        companies = dataframe["Company"].tolist()
        groups = dataframe["Group"].tolist()

        if not all(isinstance(fp, str) for fp in fingerprints):
            raise ValueError("All fingerprints must be strings.")
        if not all(isinstance(cmp, str) for cmp in companies):
            raise ValueError("All company names must be strings.")
        if not all(isinstance(grp, str) for grp in groups):
            raise ValueError("All group names must be strings.")

        (
            existing_fingerprints,
            _,
        ) = (
            self.read_fingerprints_for_all()
        )  # Read existing fingerprints from the database

        with self.session_scope():
            for fingerprint, company, group in zip(
                fingerprints,
                companies,
                groups,
            ):
                if (
                    fingerprint not in existing_fingerprints
                ):  # Check if the fingerprint already exists
                    self.save_fingerprints(fingerprint, company, group)
