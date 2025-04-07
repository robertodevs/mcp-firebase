from typing import Any, Dict, List, Optional
import firebase_admin
from firebase_admin import credentials, db, auth
from mcp.server.fastmcp import FastMCP

# Initialize Firebase with credentials from service account
cred = credentials.Certificate("service-account-key.json")
firebase_admin.initialize_app(cred)

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
async def get_user(uid: str) -> Dict[str, Any]:
    """Get user details by UID.
    
    Args:
        uid: User's unique identifier
    """
    try:
        user = auth.get_user(uid)
        return {
            "success": True,
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Realtime Database Tools
@mcp.tool()
async def set_data(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Set data at a specific path in the Realtime Database.
    
    Args:
        path: Database path (e.g., 'users/123')
        data: Data to set at the path
    """
    try:
        ref = db.reference(path)
        ref.set(data)
        return {
            "success": True,
            "path": path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def get_data(path: str) -> Dict[str, Any]:
    """Get data from a specific path in the Realtime Database.
    
    Args:
        path: Database path (e.g., 'users/123')
    """
    try:
        ref = db.reference(path)
        data = ref.get()
        return {
            "success": True,
            "data": data
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def update_data(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Update data at a specific path in the Realtime Database.
    
    Args:
        path: Database path (e.g., 'users/123')
        data: Data to update at the path
    """
    try:
        ref = db.reference(path)
        ref.update(data)
        return {
            "success": True,
            "path": path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@mcp.tool()
async def delete_data(path: str) -> Dict[str, Any]:
    """Delete data at a specific path in the Realtime Database.
    
    Args:
        path: Database path (e.g., 'users/123')
    """
    try:
        ref = db.reference(path)
        ref.delete()
        return {
            "success": True,
            "path": path
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Query Tools
@mcp.tool()
async def query_data(path: str, order_by: Optional[str] = None, limit: Optional[int] = None) -> Dict[str, Any]:
    """Query data from the Realtime Database with optional ordering and limiting.
    
    Args:
        path: Database path to query
        order_by: Field to order results by
        limit: Maximum number of results to return
    """
    try:
        ref = db.reference(path)
        query = ref
        
        if order_by:
            query = query.order_by_child(order_by)
        if limit:
            query = query.limit_to_first(limit)
            
        results = query.get()
        return {
            "success": True,
            "results": results
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
        mcp.run(transport='stdio')  # Using stdio for local development
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        exit(1)
