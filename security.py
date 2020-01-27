from .models import UserModel

my_user = UserModel(1, "lorosa", "123123")
def authenticate(username, password):
    return my_user
    
def identity(payload):
    return my_user
