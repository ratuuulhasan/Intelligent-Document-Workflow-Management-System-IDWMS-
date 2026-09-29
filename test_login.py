from services.auth_service import login

user = login("admin", "admin123")

print(user)