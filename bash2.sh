email="$1"

# Make the curl POST request
curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name": "Nuwe Test",
    "password": "TestTest1$",
    "email": "'"$email"'",
    "address": "A",
    "phoneNumber": "666888115"
}' -i