![API](https://github.com/flippe3/fireplace/blob/main/references/api_sketch.jpg?raw=true)

# API Methods
## token_required
Params: token

This is less a method to actually do something, but a wrapper method that can be added to every method with the referring annotation and therefore checks whether the user has a valid token.

## connect_db
This is also not a real API call but an assisting method to manage the connection to the database.

## signup
Params: name, password, token

This method takes the credentials of the user as input and creates a new user in the database.

## signin
Params: name password

Same as signup, it takes the credentials and logs in the user to the system.

## upload_file (token required)
Params: filename, fireplace_id

This method manages the uploading of pictures. It provides the functionality to add a picture to a certain fireplace.

## create (token required)
Params: name, latitude, longitude, wood

With this method, users can create new fireplaces after inserting the position and additional information.

## delete_api (token required)
Params: id

This method can be used to delete a fireplace. This can only be done by admins and not by users. If a fireplace no longer exists or a user has created a fireplace where there is no fireplace.

## allfireplaces
This method returns all fireplaces if a user requests them.

Returns lists: id, name, lat, long, wood

## detail
Params: id

This method gives the details to a fireplace based on the id.

Returns: id, name, lat, long, wood, temp, wind, cond

## allusers (token required)
This is an admin-only function that returns all users.

Returns lists: id, role

## delete_user (token required)
Params: username, token

This method provides the admins with the functionality of deleting a user.