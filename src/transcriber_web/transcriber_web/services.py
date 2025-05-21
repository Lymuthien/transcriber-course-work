from transcriber_service.infrastructure import (
    MongoUserRepository,
    MongoStorageRepository,
    MongoAudioRepository,
    JsonSerializer,
    PasswordManager,
    EmailService,
    Transcriber,
    StopwordsRemover,
    TextExporter,
)
from transcriber_service.application import (
    UserService,
    StorageService,
    AudioRecordService,
    AuthService,
    AudioTagService,
    AudioTextService,
    SerializerAdapter,
    EntityMapperFactory,
)
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class ServiceContainer(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceContainer, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        logger.info("Initializing service container")
        # Serializers

        base_serializer = JsonSerializer()
        entity_mapper_factory = EntityMapperFactory()
        serializer = SerializerAdapter(base_serializer, entity_mapper_factory)

        logger.info("Create serializers")

        # Repositories

        self.user_repository = MongoUserRepository(
            serializer, settings.MONGO_URI, settings.MONGO_DATABASE
        )
        self.storage_repository = MongoStorageRepository(
            serializer, settings.MONGO_URI, settings.MONGO_DATABASE
        )
        self.audio_repository = MongoAudioRepository(
            self.storage_repository,
            serializer,
            settings.MONGO_URI,
            settings.MONGO_DATABASE,
        )

        logger.info("Create repositories")

        # Infrastructure services

        password_manager = PasswordManager()
        email_service = EmailService(
            settings.SMTP_SERVER,
            settings.SMTP_PORT,
            settings.SENDER_EMAIL,
            settings.SENDER_PASSWORD,
        )
        transcriber = Transcriber(settings.PYANNOTE_TOKEN)
        stopwords_remover = StopwordsRemover()
        text_exporter = TextExporter()

        logger.info("Create infrastructure services")

        # Application services

        self.storage_service = StorageService(self.storage_repository)
        self.user_service = UserService(self.user_repository, self.storage_service)
        self.auth_service = AuthService(
            self.user_service, email_service, password_manager
        )
        self.audio_record_service = AudioRecordService(
            self.audio_repository, transcriber
        )
        self.audio_tag_service = AudioTagService(self.audio_repository)
        self.audio_text_service = AudioTextService(
            self.audio_repository, text_exporter, stopwords_remover
        )

        logger.info("Create application services")

        logger.info("Initialized service container")
