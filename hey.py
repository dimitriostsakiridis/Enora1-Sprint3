import jwt

users = []
secret_key = "mysecretkey"

def main():
    while True:       
        print("Welcome to the JWT Token Validation System")
        print("1. Create User")
        print("2. Validate Token")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            name = input("Enter username: ")
            newUser(name)
        elif choice == '2':
            token = input("Enter token: ")
            key = input("Enter secret key: ")
            scopes = input("Enter scopes (comma separated): ").split(",")
            result = validateToken(scopes,token,key)
            print(result)
        elif choice == '3':
            break




def validateToken(scopes,token,key):
    if not scopes:
        return [False,"Scopes not provided"]
    if not token:
        return [False,"Token not provided"]
    if not key:
        return [False,"Key not provided"]
    if not isinstance(scopes,list):
        return [False,"Scopes must be a list"]
        
    if key != secret_key:
        return [False,"Invalid Key"]
        
    try:
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        if decoded['scopes'] == scopes:
            if not all(scope in decoded['scopes'] for scope in scopes):
                missing = [scope for scope in scopes if scope not in decoded['scopes']]
                return [False, f"Invalid Token, one or more scopes are missing: {missing}"]
            return [True,decoded]
        else:
            return [False,"Scopes do not match"]
        
    
    except jwt.InvalidTokenError as e:
        return [False, f"Invalid Token: {str(e)}"]
    except Exception as e:
        return [False, f"Validation Error: {str(e)}"]


def newUser(name):
    payload = {
        'username':name,
        'scopes':['user'],
    }

    token = jwt.encode(payload,algorithm='HS256',key=secret_key)
    users.append(token)
    print(f"added {name} to users \n token: {token}")

def getUser(name):
    for user in users:
        decoded = jwt.decode(user,secret_key,algorithms=['HS256'])
        if decoded['username'] == name:
            return decoded
    return None


main()