from typing import Any, Dict, List, Optional, Callable
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import BatchHttpRequest
from mcp.server.fastmcp import FastMCP
import os.path
import pickle

# Initialize FastMCP server
mcp = FastMCP("google-docs")

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive'
]

def get_credentials() -> Credentials:
    """Get valid user credentials from storage.
    
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    """
    creds = None
    # Use the user's home directory for token storage
    token_path = os.path.join(os.path.expanduser('~'), '.google-docs-token.pickle')
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def get_docs_service():
    """Get the Google Docs service instance."""
    creds = get_credentials()
    return build('docs', 'v1', credentials=creds)

def get_drive_service():
    """Get the Google Drive service instance."""
    creds = get_credentials()
    return build('drive', 'v3', credentials=creds)

# Document Management Tools
@mcp.tool()
async def get_document(document_id: str) -> Dict[str, Any]:
    """Get a Google Doc by its ID.
    
    Args:
        document_id: The ID of the document to retrieve
    """
    try:
        service = get_docs_service()
        
        doc = service.documents().get(documentId=document_id).execute()
        
        return {
            "success": True,
            "document_id": doc.get('documentId'),
            "title": doc.get('title'),
            "body": doc.get('body'),
            "revision_id": doc.get('revisionId')
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_document(title: str, content: str = "") -> Dict[str, Any]:
    """Create a new Google Doc with the specified title and content.
    
    Args:
        title: The title of the new document
        content: Optional initial content for the document
    """
    try:
        # First create the document in Drive
        drive_service = get_drive_service()
        file_metadata = {
            'name': title,
            'mimeType': 'application/vnd.google-apps.document'
        }
        file = drive_service.files().create(body=file_metadata).execute()
        
        # If content is provided, update the document
        if content:
            docs_service = get_docs_service()
            requests = [
                {
                    'insertText': {
                        'location': {
                            'index': 1
                        },
                        'text': content
                    }
                }
            ]
            docs_service.documents().batchUpdate(
                documentId=file['id'],
                body={'requests': requests}
            ).execute()
        
        return {
            "success": True,
            "document_id": file['id'],
            "title": title,
            "message": "Document created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        # Run the MCP server
        print("🚀 Starting Google Docs MCP server...")
        mcp.run(transport='sse')
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)
