import logging
import os
import pickle

from fastapi import HTTPException

from config.config_project import (
    CONFIDENCE,
    DATABASE,
    ERROR_533_BAD_FINGERPRINT,
    HOST,
    PASSWORD,
    PATH_FR,
    USE_SQLITE,
    USER,
)
from shared.mariaDB.FingerprintDatabase import FingerprintDatabase

fingerprint_db = FingerprintDatabase(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE,
    used_sqlite=bool(os.environ.get("DEBUG", USE_SQLITE)),
)

face_code = None
if os.path.exists(PATH_FR):
    with open(PATH_FR, "rb") as f:
        face_code = pickle.load(f)
    face_code.distance = CONFIDENCE
else:
    raise Exception("The path to the face recognition model is not correct.")


def read_database(company, group):
    """
    Read the database of fingerprints and faces.
    """

    fingerprints, table_ids = fingerprint_db.read_fingerprints(company, group)
    return fingerprints, table_ids


"""
The nexts functions are used for the API.
"""


def buffer_to_fingerprint(
    buffer_list: list,
    company: str = None,
    group: str = None,
    save: bool = False,
) -> list:
    """
    Convert a face to a fingerprint.

    :param buffer_list: list of images.
    :param company: company name.
    :param group: group name.
    :param save: save in database.
    :return: list of fingerprints.
    """

    fingerprints_db = []
    table_ids = []

    for i, image_buffer in enumerate(buffer_list):
        face_code.path = image_buffer
        fingerprints_db.append(face_code.fingerprint)

        if save:
            inserted_id = fingerprint_db.save_fingerprints(
                face_code.fingerprint, company, group
            )

            table_ids.append(inserted_id)

        else:
            table_ids.append(i)

    return fingerprints_db, table_ids


def fingerprint_vs_fingerprint(
    fingerprints_list: list,
    fingerprints_db: list,
) -> list:
    """
    Compare two fingerprints.

    :param fingerprints_list: list of fingerprints.
    :param fingerprints_db: list of fingerprints.
    :return: list of matches.
    """

    if not isinstance(fingerprints_list, list):
        fingerprints_list = [fingerprints_list]

    if not isinstance(fingerprints_db, list):
        fingerprints_db = [fingerprints_db]

    table_ids = [i for i in range(len(fingerprints_db))]

    result_matches = []

    for fingerprint in fingerprints_list:
        face_code.fingerprint = fingerprint

        result = face_code.compare_fingerprints(fingerprints_db, table_ids)
        result_matches.append(result if result else [-1])

    return result_matches


def face_vs_fingerprint(
    buffer_list: list,
    fingerprints_db: list,
) -> list:
    """
    Compare a face to a fingerprint.

    :param buffer_list: list of images in bytes.
    :param fingerprints_db: list of fingerprints.
    :return: list of matches.
    """

    if not isinstance(fingerprints_db, list):
        fingerprints_db = [fingerprints_db]

    table_ids = [i for i in range(len(fingerprints_db))]

    result_matches = []

    for image_buffer in buffer_list:
        face_code.path = image_buffer

        result = face_code.compare_fingerprints(fingerprints_db, table_ids)
        result_matches.append(result if result else [-1])

    return result_matches


def fingerprint_vs_database(
    fingerprints_list: list,
    company: str,
    group: str,
) -> list:
    """
    Compare a fingerprint to a database.

    :param fingerprints_list: list of fingerprints.
    :param company: company name.
    :param group: group name.
    :return: list of matches.
    """

    fingerprints_db, table_ids = read_database(company, group)
    result_matches = []

    for i, fingerprint in enumerate(fingerprints_list):

        try:
            face_code.fingerprint = fingerprint

        except Exception as e:
            logging.exception(e)

            raise HTTPException(
                status_code=ERROR_533_BAD_FINGERPRINT[0],
                detail=ERROR_533_BAD_FINGERPRINT[1] + f"[{i}].",
            )

        result = face_code.compare_fingerprints(fingerprints_db, table_ids)

        result_matches.append(result if result else [-1])

    return result_matches


def faces_vs_database(
    buffer_list: list,
    company: str,
    group: str,
) -> list:
    """
    Compare a face to a database.

    :param buffer_list: list of images in bytes.
    :param company: company name.
    :param group: group name.
    :return: list of matches.
    """

    fingerprints_db, table_ids = read_database(company, group)

    result_matches = []

    for image_buffer in buffer_list:
        face_code.path = image_buffer

        result = face_code.compare_fingerprints(fingerprints_db, table_ids)
        result_matches.append(result if result else [-1])

    return result_matches
