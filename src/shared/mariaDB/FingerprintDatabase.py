import io
import logging
import os
import time
from contextlib import contextmanager
from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from shared.LogProject import logger_custom
from shared.mariaDB.models import Base, FingerprintEntry


logger = logger_custom("fingerprint")

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("log_fingerprint.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class FingerprintDatabase:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        database: str,
        used_sqlite: bool = False,
    ):
        """
        Initialize the database.
        """

        self.used_sqlite = used_sqlite

        if used_sqlite:
            self._db_url = f"sqlite:///{database[0]}.db"
        else:
            self._db_url = (
                f"mysql+mysqlconnector://{user}:{password}@{host}/{database}",
            )

        self.__setup__()

    def __setup__(self):
        """
        Setup the database.
        """

        try:
            self.engine = create_engine(self._db_url)
            Base.metadata.create_all(self.engine)

            self.Session = sessionmaker(bind=self.engine)
            self._is_connected = True

            if self.used_sqlite:
                logger.info("Using SQLite database.")

        except Exception as e:
            print(f"Error connecting to the database: {e}")
            self._is_connected = False

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    @contextmanager
    def session_scope(self):
        if not self.is_connected:
            raise RuntimeError("Database connection is not established.")

        session = self.Session()

        try:
            yield session
            session.commit()

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def requires_connection(method):
        def wrapper(self, *args, **kwargs):
            if self.used_sqlite and not os.path.exists(
                "/app/fingerprintdb.db",
            ):
                self.__setup__()

            if not self.is_connected:
                raise RuntimeError("Database connection is not established.")

            return method(self, *args, **kwargs)

        return wrapper

    def log_execution(method: callable) -> callable:
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            method_name = method.__name__
            method_args = args
            method_kwargs = kwargs

            try:
                result = method(self, *args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                logger.info(
                    f"{current_time} - Method: {method_name} "
                    + f"| Args: {method_args} | Kwargs: {method_kwargs} "
                    + f"| Execution Time: {execution_time:.4f} seconds"
                )

                return result

            except Exception as e:
                end_time = time.time()
                execution_time = end_time - start_time
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                error_message = str(e)

                logger.error(
                    f"{current_time} - Method: {method_name} "
                    + f"| Args: {method_args} | Kwargs: {method_kwargs} "
                    + f"| Execution Time: {execution_time:.4f} "
                    + f"seconds | Error: {error_message}"
                )
                raise e

        return wrapper

    @requires_connection
    @log_execution
    def save_fingerprints(
        self,
        fingerprints: Union[str, List[str]],
        company: Optional[str] = "default_company",
        group: Optional[str] = "default_group",
    ) -> Union[int, List[int]]:
        """
        Save fingerprints to the database for the specified company and group.

        :param fingerprints: Fingerprint(s) to save. Can be a single
                fingerprint string or a list of fingerprint strings.
        :type fingerprints: Union[str, List[str]]

        :param company: Company name (optional, defaults to "default_company").
        :type company: str or None

        :param group: Group name (optional, defaults to "default_group").
        :type group: str or None

        :return: ID(s) of the inserted fingerprint entries.
        :rtype: Union[int, List[int]]
        """
        with self.session_scope() as session:
            if isinstance(fingerprints, str):
                fingerprints = [fingerprints]

            inserted_ids = []
            for fingerprint in fingerprints:
                new_entry = FingerprintEntry(
                    fingerprint=fingerprint, company=company, group=group
                )
                session.add(new_entry)
                try:
                    session.flush()
                    inserted_ids.append(new_entry.id)
                except IntegrityError:
                    session.rollback()
                    # Handle the case where the entry already exists (e.g.,
                    # log an error, raise an exception, etc.)

            if len(inserted_ids) == 1:
                return inserted_ids[0]
            else:
                return inserted_ids

    @requires_connection
    @log_execution
    def read_fingerprints(
        self,
        company: Optional[str] = None,
        group: Optional[str] = None,
        ids_tabla: Union[int, List[int]] = None,
    ) -> Tuple[List[str], List[int]]:
        """
        Read fingerprints from the database for the specified company,
        group, and/or table IDs.

        :param company: Company name (optional).
        :type company: str or None

        :param group: Group name (optional).
        :type group: str or None

        :param ids_tabla: ID(s) of the fingerprint entries
                          to retrieve (optional).
                          Can be a single integer ID or a list of integer IDs.
        :type ids_tabla: Union[int, List[int]] or None

        :return: Tuple containing lists of fingerprints and their
                corresponding table IDs.
        :rtype: Tuple[List[str], List[int]]
        """
        with self.session_scope() as session:
            query = session.query(FingerprintEntry)

            if company is not None:
                query = query.filter_by(company=company)

            if group is not None:
                query = query.filter_by(group=group)

            if ids_tabla is not None:
                if isinstance(ids_tabla, int):
                    query = query.filter_by(id=ids_tabla)
                elif isinstance(ids_tabla, list):
                    query = query.filter(FingerprintEntry.id.in_(ids_tabla))
                else:
                    raise ValueError(
                        "ids_tabla should be an integer or a list of integers."
                    )

            filtered_entries = query.all()

            table_ids = [entry.id for entry in filtered_entries]
            fingerprints = [entry.fingerprint for entry in filtered_entries]

            return fingerprints, table_ids

    @requires_connection
    @log_execution
    def read_fingerprints_to_dataframe(
        self,
        company: Optional[str] = None,
        group: Optional[str] = None,
        ids_tabla: Union[int, List[int]] = None,
    ) -> pd.DataFrame:
        """
        Read fingerprints from the database for the specified company,
        group, and/or table IDs,
        and return the data as a DataFrame.

        :param company: Company name (optional).
        :type company: str or None

        :param group: Group name (optional).
        :type group: str or None

        :param ids_tabla: ID(s) of the fingerprint entries
                          to retrieve (optional).
                          Can be a single integer ID or a list of integer IDs.
        :type ids_tabla: Union[int, List[int]] or None

        :return: DataFrame containing the fingerprint data.
        :rtype: pd.DataFrame
        """

        fingerprints, table_ids = self.read_fingerprints(
            company,
            group,
            ids_tabla,
        )
        data = {"Fingerprint": fingerprints, "Table_ID": table_ids}
        df = pd.DataFrame(data)

        return df

    @requires_connection
    @log_execution
    def update_fingerprint(
        self,
        ids_tabla: Union[int, List[int]],
        fingerprints: Union[str, List[str]],
        company: Optional[str] = None,
        group: Optional[str] = None,
    ) -> Union[int, List[int]]:
        """
        Update fingerprints in the database with the given IDs
        and/or fingerprints.

        :param company: Company name (optional).
        :type company: str or None

        :param group: Group name (optional).
        :type group: str or None

        :param ids_tabla: ID(s) of the fingerprint entries to update.
                          Can be a single integer ID or a list of integer IDs.
        :type ids_tabla: Union[int, List[int]]

        :param fingerprints: New fingerprint(s) to update with.
                             Can be a single fingerprint string or
                             a list of fingerprint strings.
        :type fingerprints: Union[str, List[str]]

        :return: ID(s) of the updated fingerprint entries.
        :rtype: Union[int, List[int]]
        """

        if isinstance(ids_tabla, int):
            ids_tabla = [ids_tabla]
            fingerprints = [fingerprints]

        elif isinstance(ids_tabla, list) and isinstance(fingerprints, list):
            if len(ids_tabla) != len(fingerprints):
                raise ValueError(
                    "The lists IDs and fingerprints have different lengths.",
                )
        else:
            raise ValueError(
                "Invalid input. Both ids_tabla and fingerprints"
                + "should be either integers or lists."
            )

        updated_ids = []
        with self.session_scope() as session:
            query = session.query(FingerprintEntry)
            if company is not None:
                query = query.filter_by(company=company)
            if group is not None:
                query = query.filter_by(group=group)

            if isinstance(ids_tabla, list):
                query = query.filter(FingerprintEntry.id.in_(ids_tabla))
            else:
                query = query.filter_by(id=ids_tabla)

            for fingerprint_id, new_fingerprint in zip(
                ids_tabla,
                fingerprints,
            ):
                entry = query.filter_by(id=fingerprint_id).first()
                if entry:
                    entry.fingerprint = new_fingerprint
                    updated_ids.append(fingerprint_id)

        return updated_ids

    @requires_connection
    @log_execution
    def delete_fingerprints(
        self,
        company: Optional[str] = None,
        group: Optional[str] = None,
        ids_tabla: Union[int, List[int]] = None,
    ) -> None:
        """
        Delete fingerprints from the database for the specified company,
        group, and/or table IDs.

        :param company: Company name (optional).
        :type company: str or None

        :param group: Group name (optional).
        :type group: str or None

        :param ids_tabla: ID(s) of the fingerprint entries
                          to delete (optional).
                          Can be a single integer ID or a list of integer IDs.
        :type ids_tabla: Union[int, List[int]] or None
        """
        with self.session_scope() as session:
            query = session.query(FingerprintEntry)

            if company is not None:
                query = query.filter_by(company=company)

            if group is not None:
                query = query.filter_by(group=group)

            if ids_tabla is not None:
                if isinstance(ids_tabla, int):
                    query = query.filter_by(id=ids_tabla)
                elif isinstance(ids_tabla, list):
                    query = query.filter(FingerprintEntry.id.in_(ids_tabla))
                else:
                    raise ValueError(
                        "ids_tabla should be an integer or a list of integers."
                    )

            query.delete(synchronize_session=False)

    @requires_connection
    @log_execution
    def count_fingerprints(
        self, company: Optional[str] = None, group: Optional[str] = None
    ) -> int:
        """
        Count the number of fingerprints in the database for
        the specified company and/or group.

        :param company: Company name (optional).
        :type company: str or None

        :param group: Group name (optional).
        :type group: str or None

        :return: Number of fingerprints in the database.
        :rtype: int
        """
        with self.session_scope() as session:
            query = session.query(FingerprintEntry)

            if company is not None:
                query = query.filter_by(company=company)

            if group is not None:
                query = query.filter_by(group=group)

            return query.count()

    @requires_connection
    @log_execution
    def generate_histogram(self) -> Tuple[Image.Image, List[Tuple[str, int]]]:
        """
        Generate a histogram of various categories in the database
        and return the image buffer and data matrix.

        :return: Tuple containing the image buffer and data matrix.
        :rtype: Tuple[Image.Image, List[Tuple[str, int]]]
        """
        with self.session_scope() as session:
            query = session.query(
                FingerprintEntry.company,
                FingerprintEntry.group,
                func.count(FingerprintEntry.id),
            )
            query = query.group_by(
                FingerprintEntry.company,
                FingerprintEntry.group,
            )
            results = query.all()

            company_group_counts = {}
            no_company_group_count = 0
            no_group_company_count = 0
            no_company_no_group_count = 0

            for result in results:
                company, group, count = result
                if company and group:
                    company_group_counts[(company, group)] = count
                elif company:
                    no_group_company_count += count
                elif group:
                    no_company_group_count += count
                else:
                    no_company_no_group_count += count

            labels = [
                "Company",
                "Group",
                "Company-Group",
                "No Company-Group",
                "Company-No Group",
                "No Company-No Group",
            ]
            sizes = [
                sum(1 for _ in company_group_counts.keys()),
                no_group_company_count,
                len(company_group_counts),
                no_group_company_count,
                no_company_group_count,
                no_company_no_group_count,
            ]

            plt.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                shadow=True,
                startangle=140,
            )
            plt.axis("equal")
            plt.title("Histogram of Various Categories in the Database")

            # Save the plot to a buffer and convert to PIL image
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            plt.close()
            buffer.seek(0)
            image = Image.open(buffer)

            # Prepare data matrix
            data_matrix = list(zip(labels, sizes))

            return image, data_matrix

    @requires_connection
    @log_execution
    def delete_database_sqlite(self):
        """
        Delete the SQLite database file.

        This method will close the existing database connection,
        if any, and then delete the database file.

        Note: Use this method with caution as it will permanently
        delete the database file and its contents.
        """
        if self.used_sqlite:
            raise RuntimeError(
                "This method can only be used with SQLite databases.",
            )

        if self._is_connected:
            self.engine.dispose()  # Close the existing connection if it's open

        # Delete the database file if it exists
        if os.path.exists(
            self._db_url[10:]
        ):  # Removing 'sqlite:///' from the beginning
            os.remove(self._db_url[10:])
            print("SQLite database file deleted.")
        else:
            print("SQLite database file does not exist.")


# Example usage
if __name__ == "__main__":
    fingerprint_db = FingerprintDatabase(
        host="mariaDB",
        user="fingerprint_FC_db",
        password="secret_fingerprint_password",
        database="fingerprintdb",
    )

    fingerprints_to_save = ["fingerprint1", "fingerprint2", "fingerprint3"]
    single_fingerprint = "new_fingerprint"
    company = "My Company"
    group = "Group A"

    inserted_id = fingerprint_db.save_fingerprints(
        single_fingerprint,
        company,
        group,
    )
    print("Inserted ID:", inserted_id)

    multiple_inserted_ids = fingerprint_db.save_fingerprints(
        fingerprints_to_save, company, group
    )
    print("Multiple Inserted IDs:", multiple_inserted_ids)

    fingerprints, table_ids = fingerprint_db.read_fingerprints(company, group)
    print("Fingerprints:", fingerprints)
    print("Table IDs:", table_ids)
