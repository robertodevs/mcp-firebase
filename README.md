# Firebase MCP Server

A Firebase Admin SDK MCP (Model-Controller-Provider) server that provides a set of tools for managing Firebase Authentication and Firestore operations. This server can be used with Cursor IDE or Claude Desktop for seamless integration with AI assistants.

## Features

### Authentication Tools

- `create_user`: Create new Firebase users
- `get_users`: List all users in Firebase Auth
- `get_user`: Get specific user details
- `update_user`: Update user properties (email, display name, password)
- `delete_user`: Remove users from Firebase Auth
- `verify_email`: Generate email verification links
- `reset_password`: Generate password reset links

### Firestore Tools

- `get_collections`: List all Firestore collections
- `get_documents`: List all documents in a collection
- `get_document`: Get specific document data
- `create_document`: Create new documents
- `update_document`: Update existing documents
- `delete_document`: Remove documents from Firestore
- `batch_write`: Perform multiple write operations atomically

## Prerequisites

- Python 3.7 or higher
- Firebase project with Admin SDK enabled
- Firebase service account key
- Cursor IDE or Claude Desktop (for AI assistant integration)

## Setup

1. **Create a Firebase Project**

   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create a new project or select an existing one
   - Enable Authentication and Firestore services

2. **Get Firebase Admin SDK Credentials**

   - In Firebase Console, go to Project Settings > Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file as `service-account-key.json` in your project root

3. **Install Dependencies**

   ```bash
   pip install firebase-admin fastmcp
   ```

4. **Configure the Server**
   - Update the service account key path in `firebase.py`:
     ```python
     cred = credentials.Certificate("path/to/your/service-account-key.json")
     ```

## Running the Server

1. **Start the MCP Server**

   You can run the server in several ways:

   ```bash
   # Using the MCP CLI (recommended)
   mcp dev firebase.py

   # With environment variables
   mcp dev firebase.py -v FIREBASE_KEY=path/to/key.json

   # With custom name
   mcp dev firebase.py --name "Firebase Tools Server"

   # Load environment variables from file
   mcp dev firebase.py -f .env
   ```

2. **Install in Claude Desktop**

   ```bash
   # Basic installation
   mcp install firebase.py

   # Install with custom name
   mcp install firebase.py --name "Firebase Tools"

   # Install with environment variables
   mcp install firebase.py -v FIREBASE_KEY=path/to/key.json -v OTHER_VAR=value
   mcp install firebase.py -f .env
   ```

3. **Direct Execution**

   For advanced scenarios, you can run the server directly:

   ```python
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("Firebase Tools")

   if __name__ == "__main__":
       mcp.run()
   ```

   Then run with:

   ```bash
   python firebase.py
   # or
   mcp run firebase.py
   ```

## Debugging

1. **Server Logs**

   The MCP server provides detailed logging. You can enable debug logs by setting the environment variable:

   ```bash
   mcp dev firebase.py -v MCP_LOG_LEVEL=debug
   ```

2. **Lifespan Management**

   For debugging initialization and cleanup, implement the lifespan API:

   ```python
   from contextlib import asynccontextmanager
   from collections.abc import AsyncIterator
   from mcp.server import Server

   @asynccontextmanager
   async def server_lifespan(server: Server) -> AsyncIterator[dict]:
       # Initialize Firebase on startup
       firebase_app = initialize_firebase()
       try:
           yield {"firebase": firebase_app}
       finally:
           # Cleanup on shutdown
           await firebase_app.delete()

   # Pass lifespan to server
   server = Server("firebase-tools", lifespan=server_lifespan)
   ```

3. **Tool Testing**

   You can test individual tools using the MCP CLI:

   ```bash
   # Test a specific tool
   mcp test firebase.py --tool create_user

   # Test with specific arguments
   mcp test firebase.py --tool create_user --args '{"email": "test@example.com"}'
   ```

4. **Integration Testing**

   For testing the full server integration:

   ```bash
   # Start server in test mode
   mcp dev firebase.py --test

   # In another terminal, run integration tests
   mcp test-integration firebase.py
   ```

## Usage Examples

### Authentication Operations

```python
# Create a new user
await create_user(email="user@example.com", password="securepassword123")

# Update user properties
await update_user(
    user_id="user123",
    email="newemail@example.com",
    display_name="New Name"
)

# Send email verification
await verify_email(
    user_id="user123",
    action_url="https://yourapp.com/verified"
)

# Generate password reset link
await reset_password(
    email="user@example.com",
    action_url="https://yourapp.com/reset-complete"
)
```

### Firestore Operations

```python
# Create a document
await create_document(
    collection_id="users",
    document_id="user123",
    data={
        "name": "John Doe",
        "age": 30
    }
)

# Update a document
await update_document(
    collection_id="users",
    document_id="user123",
    data={
        "age": 31
    }
)

# Get document data
await get_document(
    collection_id="users",
    document_id="user123"
)

# Perform atomic batch operations
await batch_write(operations=[
    {
        "type": "create",
        "collection_id": "users",
        "document_id": "user1",
        "data": {
            "name": "John Doe",
            "email": "john@example.com"
        }
    },
    {
        "type": "update",
        "collection_id": "profiles",
        "document_id": "profile1",
        "data": {
            "age": 30,
            "occupation": "Developer"
        }
    },
    {
        "type": "delete",
        "collection_id": "temp",
        "document_id": "temp1"
    }
])
```

## Response Format

All tools return responses in a consistent format:

```python
# Success response
{
    "success": True,
    "data": {...}  # or relevant success data
    "message": "Operation completed successfully"
}

# Error response
{
    "success": False,
    "error": "Error message details"
}
```

## Security Considerations

1. **Service Account Key**

   - Never commit your `service-account-key.json` to version control
   - Add it to `.gitignore`
   - Use environment variables in production

2. **Authentication**
   - Always validate user input
   - Implement proper error handling
   - Follow Firebase security best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues and feature requests, please create an issue in the GitHub repository.
