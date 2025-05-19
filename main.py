from auth import register_user, login_user

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select option: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            register_user(username, password)
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            login_user(username, password)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
