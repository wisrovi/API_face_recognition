from django.db import models

from api.base_model import BaseModel


# Create your models here.


class Organization(BaseModel):
    """Organization model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return first_name."""
        return self.name


class TypeDocument(BaseModel):
    """TypeDocument model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return first_name."""
        return self.name


class People(BaseModel):
    """People model."""

    organization = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name="persons"
    )

    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    second_surname = models.CharField(max_length=255)
    age = models.IntegerField()
    document = models.CharField(max_length=255)
    type_document = models.ForeignKey(
        "TypeDocument", on_delete=models.CASCADE, related_name="persons"
    )
    gender = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=255)

    fingerprint = models.CharField(max_length=1000, default="")
