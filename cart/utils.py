# import hashlib

# def _cart_id(request):
#     # Generate a unique identifier for the user's cart based on session or other data
#     if request.user.is_authenticated:
#         # If user is authenticated, use their username or user ID as part of the identifier
#         cart_id = hashlib.sha256(request.user.username.encode('utf-8')).hexdigest()
#     else:
#         # If user is anonymous, use session ID
#         cart_id = request.session.session_key
#         if cart_id is None:
#             # Create a new session if it doesn't exist
#             request.session.create()
#             cart_id = request.session.session_key
    
#     return cart_id