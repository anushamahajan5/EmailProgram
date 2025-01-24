from msal import ConfidentialClientApplication

def get_microsoft_service(client_id, client_secret, tenant_id, user_token_file):
    app = ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )
    # Use MSAL to get tokens and connect
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token
