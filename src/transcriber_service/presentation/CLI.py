from ..services import AuthService, StorageService, WhisperProcessor, AudioService


class AudioTranscriberCLI:
    """Command-line interface for audio transcription system."""

    def __init__(self):
        self.__auth_service = AuthService()
        self.__storage_service = StorageService()
        self.__audio_processor = WhisperProcessor()
        self.__audio_service = AudioService()
        self.__current_user = None
        self.__current_storage = None

    def run(self):
        """Main application loop."""
        while True:
            if not self.__current_user:
                self.show_guest_menu()
            else:
                self.show_main_menu()

    # Menu system
    def show_guest_menu(self):
        print("\n=== Guest Menu ===")
        print("1. Register\n"
              "2. Login\n"
              "3. Exit\n")
        choice = input("Choose option: ")

        if choice == "1":
            self.handle_registration()
        elif choice == "2":
            self.handle_login()
        elif choice == "3":
            exit()
        else:
            print("Invalid choice!")

    def show_main_menu(self):
        if self.__current_user.role == 'admin':
            self.show_admin_panel()
            return

        print("\n=== Main Menu ===\n"
              "1. Upload Audio\n"
              "2. List Records\n"
              "3. Manage Tags\n"
              "4. Logout\n"
              "5. Exit\n")

        choice = input("Choose option: ")
        # Обработка выбора...

    def handle_registration(self):
        print("\n=== Registration ===")
        email = input("Email: ")
        password = input("Password: ")

        try:
            self.__current_user = user = self.__auth_service.register(email, password)
            self.__current_storage = self.__storage_service.create_storage(user.id)
            print(f"User {email} created successfully!")
        except Exception as e:
            print(f"Registration failed: {str(e)}")

    def handle_login(self):
        print("\n=== Login ===")
        email = input("Email: ")
        password = input("Password: ")

        try:
            user = self.__auth_service.login(email, password)
            self.__current_user = user
            self.__current_storage = self.__storage_service.get_storage(user.id)
            print(f"Welcome {email}!")
        except Exception as e:
            print(f"Login failed: {str(e)}")

    def handle_audio_upload(self):
        print("\n=== Audio Upload ===")
        file_path = input("Enter file path: ")

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.__audio_service.create_audio(
                file_name=file_path.split("/")[-1],
                content=content,
                storage_id=self.__current_storage.id,
                transcribe_processor=self.__audio_processor,
                file_path=file_path
            )

            print(f"Uploaded successfully!")
        except FileNotFoundError:
            print("File not found!")
        except Exception as e:
            print(f"Upload failed: {str(e)}")

    def handle_tag_creation(self):
        # print("\n=== Create Tag ===")
        # tag_name = input("Enter tag name: ")
        #
        # try:
        #     tag = self.__storage_service.create_tag(tag_name)
        #     print(f"Tag '{tag_name}' created!")
        # except Exception as e:
        #     print(f"Tag creation failed: {str(e)}")
        pass

    def show_admin_panel(self):
        print("\n=== Admin Panel ===")
        print("1. List Users")
        print("2. Block User")
        print("3. Restore User")
        choice = input("Choose option: ")
        # Реализация админских функций...


if __name__ == "__main__":
    cli = AudioTranscriberCLI()
    cli.run()
