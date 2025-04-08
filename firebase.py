from typing import Any, Dict, List, Optional
import firebase_admin
from firebase_admin import credentials, db, auth, firestore
from mcp.server.fastmcp import FastMCP
import uuid
from datetime import datetime
import json
import ast

# Initialize Firebase with credentials from service account
cred = credentials.Certificate("/Users/robertojuarez/Documents/personal/weather/service-account-key.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Initialize FastMCP server
mcp = FastMCP("firebase")

# Authentication Tools
@mcp.tool()
async def create_user(email: str, password: str) -> Dict[str, Any]:
    """Create a new Firebase user.
    
    Args:
        email: User's email address
        password: User's password
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {
            "success": True,
            "uid": user.uid,
            "email": user.email
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_users() -> Dict[str, Any]:
    """Get all users in the database."""
    try:
        users = [user.uid for user in auth.list_users().users]
        return {
            "success": True,
            "users": users
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_user(user_id: str) -> Dict[str, Any]:
    """Get a user from the database."""
    try:
        user = auth.get_user(user_id)
        return {
            "success": True,
            "user": {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def delete_user(user_id: str) -> Dict[str, Any]:
    """Delete a user from the database."""
    try:
        auth.delete_user(user_id)
        return {
            "success": True,
            "message": f"User {user_id} deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_user(user_id: str, email: Optional[str] = None, display_name: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
    """Update a Firebase user's properties.
    
    Args:
        user_id: The user's UID
        email: Optional new email address
        display_name: Optional new display name
        password: Optional new password
    """
    try:
        update_params = {}
        if email is not None:
            update_params['email'] = email
        if display_name is not None:
            update_params['display_name'] = display_name
        if password is not None:
            update_params['password'] = password
            
        user = auth.update_user(user_id, **update_params)
        return {
            "success": True,
            "user": {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def verify_email(user_id: str, action_url: str = None) -> Dict[str, Any]:
    """Generate and send an email verification link to a user.
    
    Args:
        user_id: The user's UID
        action_url: Optional. The URL to redirect to after email verification.
                   If not provided, the default Firebase action URL will be used.
    """
    try:
        # Get the user to verify their email exists
        user = auth.get_user(user_id)
        
        # Generate the email verification link
        action_code_settings = None
        if action_url:
            action_code_settings = auth.ActionCodeSettings(
                url=action_url,
                handle_code_in_app=True
            )
            
        link = auth.generate_email_verification_link(
            user.email,
            action_code_settings=action_code_settings,
            app=None
        )
        
        return {
            "success": True,
            "email": user.email,
            "verification_link": link,
            "message": f"Verification email link generated for user {user_id}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def reset_password(email: str, action_url: str = None) -> Dict[str, Any]:
    """Generate a password reset link for a user.
    
    Args:
        email: The user's email address
        action_url: Optional. The URL to redirect to after password reset.
                   If not provided, the default Firebase action URL will be used.
    """
    try:
        # Configure the action code settings if a custom URL is provided
        action_code_settings = None
        if action_url:
            action_code_settings = auth.ActionCodeSettings(
                url=action_url,
                handle_code_in_app=True
            )
        
        # Generate the password reset link
        reset_link = auth.generate_password_reset_link(
            email,
            action_code_settings=action_code_settings,
            app=None
        )
        
        return {
            "success": True,
            "email": email,
            "reset_link": reset_link,
            "message": f"Password reset link generated for {email}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Firestore Tools
@mcp.tool()
async def get_collections() -> Dict[str, Any]:
    """Get all collections in the database."""
    try:
        collections = [collection.id for collection in db.collections()]
        return {
            "success": True,
            "collections": collections,
            "count": len(collections)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get collections: {str(e)}"
        }

@mcp.tool()
async def get_documents(collection_id: str) -> Dict[str, Any]:
    """Get all documents in a collection."""
    try:
        docs = [doc.id for doc in db.collection(collection_id).get()]
        return {
            "success": True,
            "documents": docs,
            "count": len(docs)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get documents from collection {collection_id}: {str(e)}"
        }

@mcp.tool()
async def get_document(collection_id: str, document_id: str) -> Dict[str, Any]:
    """Get a document from a collection."""
    try:
        doc = db.collection(collection_id).document(document_id).get()
        return {
            "success": True,
            "data": doc.to_dict() if doc.exists else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def create_document(collection_id: str, document_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a document in a collection."""
    try:
        db.collection(collection_id).document(document_id).set(data)
        return {
            "success": True,
            "message": f"Document {document_id} created successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_document(collection_id: str, document_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update a document in a collection."""
    try:
        db.collection(collection_id).document(document_id).update(data)
        return {
            "success": True,
            "message": f"Document {document_id} updated successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def delete_document(collection_id: str, document_id: str) -> Dict[str, Any]:
    """Delete a document from a collection."""
    try:
        db.collection(collection_id).document(document_id).delete()
        return {
            "success": True,
            "message": f"Document {document_id} deleted successfully"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        # Run the MCP server
        print("🚀 Starting MCP server...")
        mcp.run(transport='sse')  # Using stdio for local development
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)
