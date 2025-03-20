import asyncio
import json
from demo.database import db

async def chat_handler(websocket):
    """
    WebSocket handler for chat functionality with proper database access.
    Uses thread-local connections and offloads DB operations to thread pool.
    """
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "system",
            "message": "Welcome to the chat server!"
        }))
        
        # Get active users on connection (using thread pool for DB access)
        active_users = await asyncio.to_thread(db.get_all_users)
        await websocket.send(json.dumps({
            "type": "system",
            "message": f"There are {len(active_users)} registered users"
        }))
        
        # Main message handling loop
        async for message_text in websocket:
            try:
                # Parse incoming message
                message_data = json.loads(message_text)
                
                # Handle different message types
                if message_data["type"] == "auth":
                    # Authenticate user
                    username = message_data["username"]
                    password = message_data["password"]
                    
                    # Run DB query in thread pool
                    user = await asyncio.to_thread(db.get_user, username)
                    
                    # Process authentication result
                    if user and user[2] == password:  # Assuming password is at index 2
                        await websocket.send(json.dumps({
                            "type": "auth_response",
                            "success": True,
                            "user_id": user[0]
                        }))
                    else:
                        await websocket.send(json.dumps({
                            "type": "auth_response",
                            "success": False
                        }))
                
                elif message_data["type"] == "chat_message":
                    # Store message in database (if needed)
                    user_id = message_data.get("user_id")
                    content = message_data.get("content")
                    
                    # Verify user exists before saving message
                    if user_id:
                        user = await asyncio.to_thread(db.get_user_by_id, user_id)
                        if user:
                            # Hypothetical method - you would implement this
                            await asyncio.to_thread(
                                db.save_message, 
                                user_id, 
                                content
                            )
                    
                    # Echo message back (or broadcast to other clients)
                    await websocket.send(json.dumps({
                        "type": "chat_message",
                        "user": user[1] if user else "Anonymous",  # username
                        "content": content
                    }))
                
                # Add more message type handlers as needed
                
            except json.JSONDecodeError:
                # Handle plain text messages
                await websocket.send(json.dumps({
                    "type": "chat_message",
                    "user": "System",
                    "content": f"Echo: {message_text}"
                }))
            except Exception as e:
                # Handle any other errors
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": str(e)
                }))
                
    except Exception as e:
        # Log connection errors
        print(f"WebSocket error: {e}")
    finally:
        # Always close the database connection for this thread
        db.close()