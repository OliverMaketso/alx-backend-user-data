Session-based authentication is a mechanism where the server authenticates a user and then creates a session to track the user’s state. Here’s how it works:

    - User Login: The user provides credentials (e.g., username and password) to the server.
    - Session Creation: After successful authentication, the server creates a session ID, stores it in - memory or a database, and sends it to the client in a cookie.
    - Session Validation: On subsequent requests, the client sends the session ID to the server. The - - server validates the session ID to identify and authorize the user.
    - Stateful Server: The server must maintain session data, making it "stateful."