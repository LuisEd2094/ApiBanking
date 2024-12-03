docker compose -f docker-compose.yml up --build

flask run 

nuwe
4a8a17fd-3c2f-4837-80ad-b1927435a7ed
PIN:
1810

nuwe1
c838e474-5163-42b9-b684-b721b0c7963f
"""/api/account/deposit
/api/account/withdraw
/api/account/fund-transfer
/api/account/transactions
"""

curl -X GET http://localhost:3000/market/prices
curl -X GET http://localhost:3000/api/account/net-worth "Authorization: Bearer $JWT_TOKEN"


curl -X POST http://localhost:3000/api/account/deposit -H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "amount":"20000"
}'

curl -X POST http://localhost:3000/api/account/withdraw -H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "amount":"100"
}'

curl -X POST http://localhost:3000/api/user-actions/enable-auto-invest \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810"
}'



curl -v -X POST http://localhost:3000/api/account/buy-asset \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin": "1810",
    "amount": 1000.0,
    "assetSymbol": "GOLD"
}'

curl -v -X POST http://localhost:3000/api/account/sell-asset \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin": "1810",
    "assetSymbol": "GOLD",
    "quantity": 0.3
}'

curl -X POST http://localhost:3000/api/account/fund-transfer -H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "amount":"100",
    "targetAccountNumber": "c838e474-5163-42b9-b684-b721b0c7963f"
}'

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..yVVzTo8eXOOrYr4lm8mQ9G8BI9oB-gdJE4aYm1btetU

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..Y-zhLjQiMVkuDnjKD4vv7K0ByHFs3f2FH9-QLwf9hLIcurl -X 
GET http://localhost:3000/api/account/transactions -H "Authorization: Bearer $JWT_TOKEN" 
curl -X GET http://localhost:3000/api/account/assets -H "Authorization: Bearer $JWT_TOKEN" 

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"TestTest1$",
    "email":"nuwenuwe@gmail.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'


curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"TestTest1$",
    "email":"nuwenuwe",
    "address":"Main St",
    "phoneNumber":"666888115"
}'




curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"nuwetest1$",
    "email":"nuwe@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'

Response: Password must contain at least one uppercase letter

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"Nuwetest",
    "email":"nuwe@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'

Response: Password must contain at least one digit and one special character

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"Nuwetest1",
    "email":"nuweeee@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'
Response: Password must contain at least one special character

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"Nuwetest$",
    "email":"nuweeee@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'


Response: Password must contain at least one digit

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"Nuwetest1 ",
    "email":"nuweeee@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'

Response: Password cannot contain whitespace

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"1.AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "email":"nuweeee@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'

Response: Password must be less than 128 characters long

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"Test1$",
    "email":"nuweeee@nuwe.com",
    "address":"Main St",
    "phoneNumber":"666888115"
}'



Response: Password must be at least 8 characters long

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name":"Nuwe Test",
    "password":"TestTest1$",
    "email":"nuwenuwe",
    "address":"Main St",
    "phoneNumber":"666888115"
}'
37432d1a-598c-4f4a-9475-4d436bfc6ca2


// TESTING AUTO

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name": "Nuwe Test",
    "password": "NuweTest1$",
    "email": "nuwe1@nuwe.com",
    "address": "Main St",
    "phoneNumber": "16166888116"
}'

curl -X POST http://localhost:3000/api/users/register \
-H "Content-Type: application/json" \
-d '{
    "name": "Nuwe Test",
    "password": "NuweTest1$",
    "email": "nuwe@nuwe.com",
    "address": "Main St",
    "phoneNumber": "116166888116"
}'

curl -v -X POST http://localhost:3000/api/account/buy-asset \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin": "1810",
    "amount": 1000.0,
    "assetSymbol": "GOLD"
}'

curl -X POST http://localhost:3000/api/account/deposit -H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "amount":"20000"
}'
curl -X POST "http://localhost:3000/api/user-actions/subscribe" \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin": "1810",
    "intervalSeconds": 5,
    "amount": "100"
}'


curl -X POST http://localhost:3000/api/user-actions/enable-auto-invest \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810"
}'
curl -X POST http://localhost:3000/api/account/pin/create \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "password":"NuweTest1$"
}'

curl -X POST http://localhost:3000/api/users/login \
-H "Content-Type: application/json" \
-d '{
    "identifier":"nuwe@nuwe.com",
    "password":"NuweTest1$"
}'
/api/user-actions/enable-auto-invest
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMDAzMjI2NywianRpIjoiOGFmYTAxYjYtODRlZi00MDUyLThmN2ItYzUwMDI0Y2ZkYzAwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNzMwMDMyMjY3LCJjc3JmIjoiNWMzZTg1ODYtZWQ4NS00ZmQ3LWI4YTEtZmNkNWE1MDMxYjUzIiwiZXhwIjoxNzMwMDMzMTY3fQ.XrqxcEU6Rj6LUgMUn5YvPR40NqC6IOpaK8OuBiE15CY
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMDAzMjI3NSwianRpIjoiYTlkYTUyMDAtZDMzZi00MjJkLWIwMGItMTE1N2U2ZGYyY2MxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNzMwMDMyMjc1LCJjc3JmIjoiYzNhYjA2MDYtZDY0OS00NThmLTg0MDQtYjFhY2M3M2ZjZTc5IiwiZXhwIjoxNzMwMDMzMTc1fQ.EjCbMLZtr0xln16-gpPlVl081yG1jE5viy1sSxeuwKk
export JWT_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcyOTk0NTQ0NywianRpIjoiNzcyODAyMjYtZjI3Yi00NDljLTgwYjItNjViNTA1NzcxYzVmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzI5OTQ1NDQ3LCJjc3JmIjoiMWE0OWZjZjUtNTg5Mi00ZTIyLTg4ZmMtMjk3M2RkOWVkYTk4IiwiZXhwIjoxNzI5OTQ2MzQ3fQ.vSXGobBRJU-2jaYAIjduN1rp7JQKq-t2nRLryDFOQhU"


curl -X GET http://localhost:3000/api/dashboard/user -H "Authorization: Bearer $JWT_TOKEN"
curl -X GET http://localhost:3000/api/users/logout -H "Authorization: Bearer $JWT_TOKEN"


/api/account/pin/create
/api/account/pin/update

curl -X POST http://localhost:3000/api/account/pin/create \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin":"1810",
    "password":"NuweTest1$"
}'

curl -X POST "http://localhost:3000/api/user-actions/subscribe" \
-H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "pin": "1810",
    "intervalSeconds": 5,
    "amount": "100"
}'

curl -X POST http://localhost:3000/api/account/pin/update -H "Authorization: Bearer $JWT_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "oldPin":"1810",
    "password":"NuweTest1$",
    "newPin": "1811"
}'

curl -X POST http://localhost:3000/api/auth/password-reset/send-otp \
-H "Content-Type: application/json" \
-d '{
    "identifier":"nuw2@nuwe.com"}'


curl -X POST http://localhost:3000/api/auth/password-reset/verify-otp \
-H "Content-Type: application/json" \
-d '{
    "identifier":"nuwe@nuwe.com",
    "otp":"434237"}'

curl -X POST http://localhost:3000/api/auth/password-reset \
-H "Content-Type: application/json" \
-d '{
    "identifier":"nuwe@nuwe.com",
    "resetToken": "9c26ac7e-c232-4e32-88f7-4564c4083f78",
    "newPassword": "PassTest"}'

    78820081-09a7-4259-96b4-e605cd1c04b9


{
    "pin":"1810",
    "password":"PassTest1$"
}

071148
/auth/password-reset/verify-otp
JWT_SECRET_KEY: your_super_secret_key
SECRET_KEY: your_default_secret_key    
MAIL_USE_TLS: false
MAIL_DEFAULT_SENDER: noreply@example.com
