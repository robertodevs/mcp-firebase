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

   ```bash
   python firebase.py
   ```

   The server will start in SSE (Server-Sent Events) mode.

2. **Using with Cursor IDE**

   - Open your project in Cursor IDE
   - The AI assistant will automatically detect and use the available MCP tools

3. **Using with Claude Desktop**
   - Ensure the MCP server is running
   - Connect Claude Desktop to the local MCP server

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
