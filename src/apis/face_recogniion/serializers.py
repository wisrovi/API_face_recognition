from pydantic import BaseModel
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class FaceCompareResult(BaseModel):
    image_filename: str
    match: bool


class FaceFingerprintCompareResult(BaseModel):
    fingerprint: Optional[List[str]]
    indices: Optional[List[int]]
    matched_indices: Optional[List[List[int]]]


class FingerprintCompareResult(BaseModel):
    matched_indices: Optional[List[List[int]]]


class FaceCompareFaceResult(BaseModel):
    image_filename: str
    results: List[FaceCompareResult]


class ImageCompareResult(BaseModel):
    image_filename: str
    match: bool
