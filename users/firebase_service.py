import firebase_admin
from firebase_admin import credentials, auth

# Path to your service account key JSON file
cred = credentials.Certificate(
    r"C:\Users\ENVY\PycharmProjects\HealthEaseProject\health_ease\health_ease\settings\healthease-c8480-firebase-adminsdk-pi706-12c7dfd120.json")
firebase_admin.initialize_app(cred)


def create_firebase_user(user):
    try:
        # Create the user in Firebase
        user = auth.create_user(
            uid=str(user.id),
            email=user.email,
            display_name=f"{user.first_name} {user.last_name}",
        )
        print(f"Successfully created new user: {user.uid}")
        return user
    except Exception as e:
        print(f"Error creating new Firebase user: {e}")
        return None


def generate_custom_token(uid):
    try:
        # Generate a custom authentication token for the user
        custom_token = auth.create_custom_token(uid)
        return custom_token
    except Exception as e:
        print(f"Error generating custom token: {e}")
        return None

