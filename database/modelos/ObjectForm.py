

class BasicDto:
    """
    ErrorForm
    TypeDocumentUserForm
    ConsultLicenseForm
    RenewLicenseForm
    """
    token = str()

class LoginDto:
    """
    LoginUserForm
    """
    user = str()
    pwd = str()

class RecognitionDto:
    """
    ValidImageForm
    """
    token = str()
    image = str()

class PersonDto:
    """
    RegisterPersonForm
    """
    token = str()
    image = str()
    first_name = str()
    second_name = str()
    first_surname = str()
    second_surname = str()
    type_document = int()
    document_number = int()

class RelationPersonVector:
    """
    NewRelationPersonWithVectorForm
    """
    token = str()
    image = str()
    type_document = int()
    document_number = int()

class User_API:
    """
    RegisterNewUserForm
    """
    token = str()
    email = str()
    user = str()
    pwd = str()
    rol = str()
    name = str()
    surname = str()

