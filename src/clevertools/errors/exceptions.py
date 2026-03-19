from __future__ import annotations

class AppError(Exception):
    """Base class for all domain-specific errors in clevertools."""


class RecoverableError(AppError):
    """Error indicating the current operation can be skipped safely."""


class FatalError(AppError):
    """Error indicating execution should stop immediately."""


class ValidationError(RecoverableError):
    """Raised when input values fail semantic or structural validation."""


class TypeValidationError(ValidationError):
    """Raised when a value has an unexpected type."""


class ValueValidationError(ValidationError):
    """Raised when a value is syntactically valid but semantically unacceptable."""


class SchemaValidationError(ValidationError):
    """Raised when structured input violates the expected schema."""


class ParseError(ValidationError):
    """Raised when a value or payload cannot be parsed into the expected format."""


class FileFormatError(ParseError):
    """Raised when a file exists but its content format is invalid."""


class PathTraversalError(ValidationError):
    """Raised when a path attempts to escape an allowed root."""


class RangeValidationError(ValidationError):
    """Raised when a numeric value is outside the accepted range."""


class LengthValidationError(ValidationError):
    """Raised when a value exceeds or falls below expected length constraints."""


class DependencyError(FatalError):
    """Raised when a required dependency, binary, or runtime component is unavailable."""


class MissingResourceError(DependencyError):
    """Raised when a mandatory file, folder, or other resource cannot be found."""


class ResourceLockedError(RecoverableError):
    """Raised when a resource is temporarily locked by another process."""


class OptionalDependencyError(RecoverableError):
    """Raised when an optional dependency is unavailable and a fallback may be used."""


class SetupError(FatalError):
    """Raised when required setup steps could not be completed."""


class ConfigurationError(FatalError):
    """Raised when configuration values are missing, inconsistent, or invalid."""


class ConfigurationMissingError(ConfigurationError):
    """Raised when a required configuration key or section is missing."""


class ConfigurationConflictError(ConfigurationError):
    """Raised when configuration values are mutually inconsistent."""


class StartError(FatalError):
    """Raised when application start-up fails before normal execution begins."""


class InitializationError(StartError):
    """Raised when a component cannot be initialized during startup."""


class ExecutionError(FatalError):
    """Raised when a core runtime step fails during execution."""


class OperationError(ExecutionError):
    """Raised when a single operation fails during runtime processing."""


class StateError(ExecutionError):
    """Raised when runtime state is invalid for the requested operation."""


class ConcurrencyError(ExecutionError):
    """Raised for synchronization or concurrent access problems."""


class RetryLimitExceededError(ExecutionError):
    """Raised when a retry loop exceeds the configured maximum attempts."""


class CircuitOpenError(ExecutionError):
    """Raised when an operation is blocked by an open circuit-breaker policy."""


class APIError(FatalError):
    """Raised for failures while interacting with external APIs or services."""


class AuthenticationError(APIError):
    """Raised when API credentials are missing, invalid, or expired."""


class AuthorizationError(APIError):
    """Raised when credentials are valid but permissions are insufficient."""


class RequestError(APIError):
    """Raised when an outgoing request cannot be built or sent successfully."""


class ConnectivityError(RequestError):
    """Raised when a remote endpoint cannot be reached."""


class DNSResolutionError(ConnectivityError):
    """Raised when hostname resolution fails."""


class SSLHandshakeError(ConnectivityError):
    """Raised when TLS/SSL negotiation fails."""


class TimeoutRequestError(RequestError):
    """Raised when an external request exceeds the configured timeout."""


class RateLimitError(RequestError):
    """Raised when an API request is rejected due to throttling or quotas."""


class ResponseError(APIError):
    """Raised when an API response is malformed or semantically invalid."""


class ResponseParseError(ResponseError):
    """Raised when an API response body cannot be parsed."""


class ResponseStatusError(ResponseError):
    """Raised when an API response status code indicates failure."""


class ProtocolError(APIError):
    """Raised when a transport or protocol contract is violated."""


class StorageError(FatalError):
    """Raised for persistent storage related failures."""


class FileSystemError(StorageError):
    """Raised when filesystem operations fail unexpectedly."""


class FileReadError(FileSystemError):
    """Raised when file content cannot be read."""


class FileWriteError(FileSystemError):
    """Raised when file content cannot be written."""


class FileDeleteError(FileSystemError):
    """Raised when a file cannot be removed."""


class DirectoryCreateError(FileSystemError):
    """Raised when a directory cannot be created."""


class DirectoryReadError(FileSystemError):
    """Raised when a directory cannot be inspected."""


class DirectoryDeleteError(FileSystemError):
    """Raised when a directory cannot be removed."""


class DiskSpaceError(StorageError):
    """Raised when an operation fails due to insufficient disk space."""


class QuotaExceededError(StorageError):
    """Raised when a storage or service quota has been exceeded."""


class IntegrityError(StorageError):
    """Raised when stored data fails integrity checks."""


class SerializationError(ExecutionError):
    """Raised when structured data cannot be serialized."""


class DeserializationError(ParseError):
    """Raised when structured data cannot be deserialized."""


class DataError(RecoverableError):
    """Raised for logical data-level issues that may be recoverable."""


class DataNotFoundError(DataError):
    """Raised when requested data cannot be found."""


class DuplicateDataError(DataError):
    """Raised when duplicate data violates uniqueness expectations."""


class ConflictError(DataError):
    """Raised when an operation conflicts with the current data state."""


class StaleDataError(DataError):
    """Raised when data is outdated and no longer valid for the operation."""


class SecurityError(FatalError):
    """Raised for security-sensitive failures."""


class PermissionDeniedError(SecurityError):
    """Raised when an action is denied due to insufficient privileges."""


class TokenError(SecurityError):
    """Raised when tokens are missing, invalid, or expired."""


class EncryptionError(SecurityError):
    """Raised when encryption or decryption fails."""


class SignatureVerificationError(SecurityError):
    """Raised when a digital signature cannot be verified."""


class LoggingError(RecoverableError):
    """Raised when logging infrastructure fails but core execution may continue."""


class LoggerConfigurationError(LoggingError):
    """Raised when logger setup or structure definitions are invalid."""


class MessageFormatError(LoggingError):
    """Raised when a log message cannot be rendered in the expected format."""


class CLIError(RecoverableError):
    """Raised for command-line invocation and argument processing problems."""


class MissingArgumentError(CLIError):
    """Raised when a required command-line argument is missing."""


class InvalidArgumentError(CLIError):
    """Raised when a command-line argument value is invalid."""


class CacheError(RecoverableError):
    """Raised for cache-specific failures where fallback paths may exist."""


class CacheMissError(CacheError):
    """Raised when a requested key is not present in cache."""


class CacheSerializationError(CacheError):
    """Raised when cached payload serialization or deserialization fails."""


class LimitExceededError(RecoverableError):
    """Raised when an operation exceeds a configured logical limit."""


class ExecutionHaltedError(FatalError):
    """Raised when execution is intentionally stopped by failure policy."""


class PathError(ValidationError):
    """Raised when a path is invalid or not existent."""


class MaskError(OperationError):
    """Raised when masking a value failes"""


class SetupStepError(SetupError):
    """Raised when a single setup step fails."""


class SetupPathError(SetupError):
    """Raised when setup requires a missing or invalid path."""


class SetupPermissionError(SetupError):
    """Raised when setup cannot proceed due to missing permissions."""


class SetupTimeoutError(SetupError):
    """Raised when setup exceeds the allowed time window."""


class StartupDependencyError(StartError):
    """Raised when startup fails because required dependencies are unavailable."""


class StartupValidationError(StartError):
    """Raised when startup preconditions are not satisfied."""


class MainError(StartError):
    """Raised for errors related to main program startup logic."""


class MainImportError(MainError):
    """Raised when importing a main module fails."""


class MainExecutionError(MainError):
    """Raised when executing the main entry point fails."""


class RuntimeStepError(ExecutionError):
    """Raised when a runtime processing step fails."""


class RuntimeStateTransitionError(StateError):
    """Raised when transitioning runtime state is not possible."""


class RuntimeIOError(ExecutionError):
    """Raised when runtime I/O operations fail."""


class RuntimeNetworkError(ExecutionError):
    """Raised when runtime network communication fails."""


class RuntimeUnhandledError(ExecutionError):
    """Raised when an unexpected runtime exception is caught."""


class CleanupError(ExecutionError):
    """Raised when post-run cleanup fails."""


class ShutdownError(ExecutionError):
    """Raised when shutdown cannot complete cleanly."""


class SetupEnvironmentError(SetupError):
    """Raised when setup cannot prepare the required environment."""


class SetupDependencyInstallError(SetupError):
    """Raised when setup cannot install or activate dependencies."""


class SetupBootstrapError(SetupError):
    """Raised when bootstrap logic fails during setup."""


class SetupValidationError(SetupError):
    """Raised when setup-generated values fail validation."""


class SetupResourceCreationError(SetupError):
    """Raised when setup cannot create required resources."""


class SetupTemplateRenderError(SetupError):
    """Raised when setup template rendering fails."""


class SetupMigrationError(SetupError):
    """Raised when setup migrations fail."""


class StartSequenceError(StartError):
    """Raised when the startup sequence is broken or incomplete."""


class StartHookError(StartError):
    """Raised when a startup hook fails."""


class StartConfigurationLoadError(StartError):
    """Raised when startup cannot load configuration."""


class StartHealthCheckError(StartError):
    """Raised when startup health checks fail."""


class StartServiceBindError(StartError):
    """Raised when startup cannot bind required services."""


class StartServiceStartError(StartError):
    """Raised when a required service cannot be started."""


class MainLoopError(MainError):
    """Raised when the main loop fails."""


class MainLoopInterruptedError(MainLoopError):
    """Raised when the main loop is interrupted unexpectedly."""


class MainLoopTimeoutError(MainLoopError):
    """Raised when the main loop exceeds its allowed timeout."""


class MainDispatchError(MainError):
    """Raised when dispatching work from main fails."""


class MainHandlerError(MainError):
    """Raised when a main-level handler fails."""


class RuntimeConfigurationReloadError(ExecutionError):
    """Raised when runtime configuration reload fails."""


class RuntimeDataLoadError(ExecutionError):
    """Raised when runtime data loading fails."""


class RuntimeDataSaveError(ExecutionError):
    """Raised when runtime data persistence fails."""


class RuntimeComputationError(ExecutionError):
    """Raised when runtime computation cannot complete."""


class RuntimeInvariantError(StateError):
    """Raised when a runtime invariant is violated."""


class RuntimeConcurrencyConflictError(ConcurrencyError):
    """Raised when runtime operations conflict under concurrency."""


class RuntimeRetryExhaustedError(RetryLimitExceededError):
    """Raised when runtime retries are exhausted."""


class RuntimeCancellationError(ExecutionError):
    """Raised when runtime execution is cancelled."""


class RuntimePluginError(ExecutionError):
    """Raised when a runtime plugin fails."""


class RuntimeExtensionError(ExecutionError):
    """Raised when a runtime extension fails."""


class RuntimeResourceLeakError(ExecutionError):
    """Raised when runtime detects resource leaks."""


class RuntimeSignalError(ExecutionError):
    """Raised when handling runtime signals fails."""


class ProgramInterruptionError(ExecutionHaltedError):
    """Raised when program flow is interrupted by external control."""


class SetupPrecheckError(SetupError):
    """Raised when setup prechecks fail."""


class SetupVersionCheckError(SetupError):
    """Raised when setup version compatibility checks fail."""


class SetupRegistryError(SetupError):
    """Raised when setup cannot access required registries."""


class SetupDownloadError(SetupError):
    """Raised when setup cannot download required assets."""


class SetupExtractionError(SetupError):
    """Raised when setup cannot extract downloaded artifacts."""


class SetupChecksumError(SetupError):
    """Raised when setup checksum verification fails."""


class SetupSeedDataError(SetupError):
    """Raised when setup cannot load initial seed data."""


class SetupSecretProvisionError(SetupError):
    """Raised when setup cannot provision required secrets."""


class SetupEnvWriteError(SetupError):
    """Raised when setup cannot write environment files."""


class SetupFinalizeError(SetupError):
    """Raised when final setup steps fail."""


class StartArgumentError(StartError):
    """Raised when startup arguments are invalid."""


class StartModeError(StartError):
    """Raised when startup mode selection is invalid."""


class StartOrderError(StartError):
    """Raised when startup ordering constraints are violated."""


class StartDependencyGraphError(StartError):
    """Raised when startup dependency graph resolution fails."""


class StartTimeoutError(StartError):
    """Raised when startup exceeds allowed time."""


class StartPortConflictError(StartError):
    """Raised when startup detects a port conflict."""


class StartProtocolNegotiationError(StartError):
    """Raised when startup protocol negotiation fails."""


class StartReadinessError(StartError):
    """Raised when startup readiness checks fail."""


class StartWarmupError(StartError):
    """Raised when startup warmup procedures fail."""


class MainBootstrapError(MainError):
    """Raised when main bootstrap procedures fail."""


class MainContextBuildError(MainError):
    """Raised when main cannot build execution context."""


class MainConfigurationError(MainError):
    """Raised when main runtime configuration is invalid."""


class MainPipelineError(MainError):
    """Raised when main processing pipeline cannot be constructed."""


class MainRoutingError(MainError):
    """Raised when main routing or dispatch rules are invalid."""


class MainTaskScheduleError(MainError):
    """Raised when main cannot schedule tasks."""


class MainTaskExecutionError(MainError):
    """Raised when a main-managed task fails."""


class MainResultAggregationError(MainError):
    """Raised when main cannot aggregate task results."""


class MainExitError(MainError):
    """Raised when main cannot terminate cleanly."""


class RuntimeContractError(ExecutionError):
    """Raised when runtime contract assumptions are violated."""


class RuntimeDependencyUnavailableError(ExecutionError):
    """Raised when a runtime dependency becomes unavailable."""


class RuntimeBackpressureError(ExecutionError):
    """Raised when runtime cannot handle incoming workload pressure."""


class RuntimeQueueError(ExecutionError):
    """Raised when runtime queue management fails."""


class RuntimeQueueOverflowError(RuntimeQueueError):
    """Raised when runtime queue capacity is exceeded."""


class RuntimeQueueUnderflowError(RuntimeQueueError):
    """Raised when runtime consumes from an empty queue unexpectedly."""


class RuntimeBatchError(ExecutionError):
    """Raised when runtime batch processing fails."""


class RuntimeCheckpointError(ExecutionError):
    """Raised when runtime checkpointing fails."""


class RuntimeRecoveryError(ExecutionError):
    """Raised when runtime cannot recover from a failure state."""


class RuntimeRollbackError(ExecutionError):
    """Raised when runtime rollback fails."""


class RuntimeCommitError(ExecutionError):
    """Raised when runtime commit/finalization fails."""


class RuntimeConsistencyError(StateError):
    """Raised when runtime detects inconsistent state."""


class RuntimeDeadlockError(ConcurrencyError):
    """Raised when runtime detects a deadlock."""


class RuntimeLivelockError(ConcurrencyError):
    """Raised when runtime detects a livelock."""


class RuntimeThreadPoolError(ConcurrencyError):
    """Raised when runtime thread-pool operations fail."""


class RuntimeProcessPoolError(ConcurrencyError):
    """Raised when runtime process-pool operations fail."""


class RuntimeResourceExhaustedError(ExecutionError):
    """Raised when runtime resources are exhausted."""


class RuntimeMemoryPressureError(RuntimeResourceExhaustedError):
    """Raised when runtime is under critical memory pressure."""


class RuntimeCpuSaturationError(RuntimeResourceExhaustedError):
    """Raised when runtime CPU utilization reaches saturation."""


class RuntimeFileDescriptorError(RuntimeResourceExhaustedError):
    """Raised when runtime runs out of file descriptors."""


class RuntimeTemporaryFailureError(ExecutionError):
    """Raised for transient runtime failures that may be retried."""


class RuntimePermanentFailureError(ExecutionError):
    """Raised for non-recoverable runtime failures."""


class RuntimePolicyViolationError(ExecutionError):
    """Raised when runtime policy constraints are violated."""


class RuntimeFeatureFlagError(ExecutionError):
    """Raised when runtime feature-flag state is invalid."""


class DatabaseError(StorageError):
    """Raised for database related failures."""


class DatabaseConnectionError(DatabaseError):
    """Raised when a database connection cannot be established."""


class DatabaseAuthenticationError(DatabaseError):
    """Raised when database authentication fails."""


class DatabaseAuthorizationError(DatabaseError):
    """Raised when database permissions are insufficient."""


class DatabaseTimeoutError(DatabaseError):
    """Raised when a database operation times out."""


class DatabaseQueryError(DatabaseError):
    """Raised when a database query fails."""


class DatabaseQuerySyntaxError(DatabaseQueryError):
    """Raised when a database query has invalid syntax."""


class DatabaseConstraintError(DatabaseError):
    """Raised when a database constraint is violated."""


class DatabaseUniqueConstraintError(DatabaseConstraintError):
    """Raised when a uniqueness constraint is violated."""


class DatabaseForeignKeyConstraintError(DatabaseConstraintError):
    """Raised when a foreign-key constraint is violated."""


class DatabaseTransactionError(DatabaseError):
    """Raised when a database transaction fails."""


class DatabaseTransactionBeginError(DatabaseTransactionError):
    """Raised when opening a database transaction fails."""


class DatabaseTransactionCommitError(DatabaseTransactionError):
    """Raised when committing a database transaction fails."""


class DatabaseTransactionRollbackError(DatabaseTransactionError):
    """Raised when rolling back a database transaction fails."""


class DatabaseDeadlockError(DatabaseTransactionError):
    """Raised when the database reports a deadlock."""


class DatabaseSerializationConflictError(DatabaseTransactionError):
    """Raised when a database serialization conflict occurs."""


class DatabaseMigrationExecutionError(DatabaseError):
    """Raised when applying database migrations fails."""


class DatabaseMigrationVersionError(DatabaseError):
    """Raised when database migration versions are inconsistent."""


class DatabaseSeedExecutionError(DatabaseError):
    """Raised when seeding database data fails."""


class DatabasePoolError(DatabaseError):
    """Raised when database connection pool operations fail."""


class DatabasePoolExhaustedError(DatabasePoolError):
    """Raised when no database connections are available in pool."""


class DatabasePoolConfigurationError(DatabasePoolError):
    """Raised when database pool configuration is invalid."""


class DatabaseReplicaError(DatabaseError):
    """Raised when database replica access fails."""


class DatabasePrimaryUnavailableError(DatabaseError):
    """Raised when the primary database is unavailable."""


class DatabaseSchemaDriftError(DatabaseError):
    """Raised when database schema differs from expected definitions."""


class ExternalServiceError(APIError):
    """Raised for failures with external services."""


class ExternalServiceUnavailableError(ExternalServiceError):
    """Raised when an external service is unavailable."""


class ExternalServiceAuthenticationError(ExternalServiceError):
    """Raised when external service authentication fails."""


class ExternalServiceAuthorizationError(ExternalServiceError):
    """Raised when external service authorization fails."""


class ExternalServiceTimeoutError(ExternalServiceError):
    """Raised when an external service call times out."""


class ExternalServiceProtocolError(ExternalServiceError):
    """Raised when an external service violates protocol expectations."""


class ExternalServiceResponseError(ExternalServiceError):
    """Raised when external service responses are invalid."""


class ExternalServiceContractError(ExternalServiceError):
    """Raised when external service contracts are violated."""


class ExternalServiceRateLimitError(ExternalServiceError):
    """Raised when external services apply throttling limits."""


class ExternalServiceDependencyError(ExternalServiceError):
    """Raised when downstream external dependencies fail."""


class InternalServiceError(ExecutionError):
    """Raised for failures between internal services."""


class InternalServiceUnavailableError(InternalServiceError):
    """Raised when an internal service is unavailable."""


class InternalServiceDiscoveryError(InternalServiceError):
    """Raised when internal service discovery fails."""


class InternalServiceRegistrationError(InternalServiceError):
    """Raised when internal service registration fails."""


class InternalServiceProtocolError(InternalServiceError):
    """Raised when internal service protocol contracts are broken."""


class InternalServiceTimeoutError(InternalServiceError):
    """Raised when an internal service request times out."""


class InternalServiceContractError(InternalServiceError):
    """Raised when internal service contracts are violated."""


class InternalServiceVersionMismatchError(InternalServiceError):
    """Raised when internal service versions are incompatible."""


class WebhookError(APIError):
    """Raised for webhook processing failures."""


class WebhookSignatureError(SecurityError):
    """Raised when webhook signature verification fails."""


class WebhookPayloadError(ParseError):
    """Raised when webhook payload is malformed or invalid."""


class WebhookDeliveryError(RequestError):
    """Raised when webhook delivery to an endpoint fails."""


class WebhookReplayError(SecurityError):
    """Raised when a webhook replay attack is detected."""


class MessagingError(ExecutionError):
    """Raised for messaging system failures."""


class MessageBrokerConnectionError(MessagingError):
    """Raised when connecting to a message broker fails."""


class MessageBrokerAuthenticationError(MessagingError):
    """Raised when message broker authentication fails."""


class MessagePublishError(MessagingError):
    """Raised when publishing a message fails."""


class MessageConsumeError(MessagingError):
    """Raised when consuming a message fails."""


class MessageAcknowledgeError(MessagingError):
    """Raised when acknowledging a message fails."""


class MessageRejectError(MessagingError):
    """Raised when rejecting a message fails."""


class MessageRequeueError(MessagingError):
    """Raised when requeuing a message fails."""


class MessageOrderingError(MessagingError):
    """Raised when message ordering guarantees are violated."""


class MessageDuplicateError(MessagingError):
    """Raised when duplicate message processing is detected."""


class MessageDeadLetterError(MessagingError):
    """Raised when dead-letter queue processing fails."""


class MessageSerializationFailureError(SerializationError):
    """Raised when message serialization fails."""


class MessageDeserializationFailureError(DeserializationError):
    """Raised when message deserialization fails."""


class EventBusError(ExecutionError):
    """Raised for event bus failures."""


class EventPublishError(EventBusError):
    """Raised when publishing an event fails."""


class EventSubscribeError(EventBusError):
    """Raised when subscribing to events fails."""


class EventDispatchError(EventBusError):
    """Raised when dispatching events to handlers fails."""


class EventHandlerError(EventBusError):
    """Raised when an event handler fails."""


class EventContractError(EventBusError):
    """Raised when event schema or contract validation fails."""


class EventReplayError(EventBusError):
    """Raised when event replay operations fail."""


class WorkerError(ExecutionError):
    """Raised for worker lifecycle and execution failures."""


class WorkerStartupFailureError(StartError):
    """Raised when a worker fails during startup."""


class WorkerShutdownFailureError(ShutdownError):
    """Raised when a worker fails during shutdown."""


class WorkerHeartbeatError(WorkerError):
    """Raised when worker heartbeat updates fail."""


class WorkerLeaseError(WorkerError):
    """Raised when worker lease acquisition or renewal fails."""


class WorkerCapacityError(WorkerError):
    """Raised when worker capacity limits are exceeded."""


class WorkerTaskClaimError(WorkerError):
    """Raised when a worker cannot claim a task."""


class WorkerTaskTimeoutError(WorkerError):
    """Raised when a worker task execution exceeds timeout."""


class SchedulerError(ExecutionError):
    """Raised for scheduler subsystem failures."""


class ScheduleParseError(ParseError):
    """Raised when schedule expressions cannot be parsed."""


class ScheduleValidationError(ValidationError):
    """Raised when schedule definitions are invalid."""


class ScheduleRegistrationError(SchedulerError):
    """Raised when registering a scheduled job fails."""


class ScheduledJobExecutionError(SchedulerError):
    """Raised when a scheduled job fails at execution time."""


class ScheduledJobMissedRunError(SchedulerError):
    """Raised when a scheduled job misses its execution window."""


class ScheduledJobConcurrencyError(SchedulerError):
    """Raised when scheduled job concurrency rules are violated."""


class IntegrationError(ExecutionError):
    """Raised for generic integration failures."""


class InternalIntegrationError(IntegrationError):
    """Raised when internal system integration points fail."""


class ExternalIntegrationError(IntegrationError):
    """Raised when external integration points fail."""


class MetricsError(RecoverableError):
    """Raised when metrics collection or emission fails."""


class MetricsBackendError(MetricsError):
    """Raised when metrics backend communication fails."""


class TracingError(RecoverableError):
    """Raised when distributed tracing fails."""


class TracingExportError(TracingError):
    """Raised when exporting traces fails."""


class AuditLogError(LoggingError):
    """Raised when audit-log recording fails."""


class SecretManagementError(SecurityError):
    """Raised when secret management operations fail."""


class SecretMissingError(SecretManagementError):
    """Raised when a required secret is missing."""


class SecretRotationError(SecretManagementError):
    """Raised when secret rotation fails."""


class SecretDecryptionError(SecretManagementError):
    """Raised when decrypting a secret fails."""


class CertificateError(SecurityError):
    """Raised for certificate related failures."""


class CertificateExpiredError(CertificateError):
    """Raised when a certificate is expired."""


class CertificateValidationError(CertificateError):
    """Raised when certificate validation fails."""


class CertificateChainError(CertificateError):
    """Raised when certificate chain validation fails."""


class InternalInvariantViolationError(StateError):
    """Raised when internal invariants are violated."""


class InternalProtocolError(ExecutionError):
    """Raised when internal protocols are violated."""


class ExternalProtocolMismatchError(ProtocolError):
    """Raised when external protocol versions or formats mismatch."""

class YamlIOError(Exception):
    """Base exception for YAML IO operations."""


class YamlReadError(YamlIOError):
    """Raised when reading YAML fails."""


class YamlWriteError(YamlIOError):
    """Raised when writing YAML fails."""

__all__ = (
    "YamlIOError",
    "YamlReadError",
    "YamlWriteError",
    "AppError",
    "RecoverableError",
    "FatalError",
    "ValidationError",
    "TypeValidationError",
    "ValueValidationError",
    "SchemaValidationError",
    "ParseError",
    "FileFormatError",
    "PathTraversalError",
    "RangeValidationError",
    "LengthValidationError",
    "DependencyError",
    "MissingResourceError",
    "ResourceLockedError",
    "OptionalDependencyError",
    "SetupError",
    "ConfigurationError",
    "ConfigurationMissingError",
    "ConfigurationConflictError",
    "StartError",
    "InitializationError",
    "ExecutionError",
    "OperationError",
    "StateError",
    "ConcurrencyError",
    "RetryLimitExceededError",
    "CircuitOpenError",
    "APIError",
    "AuthenticationError",
    "AuthorizationError",
    "RequestError",
    "ConnectivityError",
    "DNSResolutionError",
    "SSLHandshakeError",
    "TimeoutRequestError",
    "RateLimitError",
    "ResponseError",
    "ResponseParseError",
    "ResponseStatusError",
    "ProtocolError",
    "StorageError",
    "FileSystemError",
    "FileReadError",
    "FileWriteError",
    "FileDeleteError",
    "DirectoryCreateError",
    "DirectoryReadError",
    "DirectoryDeleteError",
    "DiskSpaceError",
    "QuotaExceededError",
    "IntegrityError",
    "SerializationError",
    "DeserializationError",
    "DataError",
    "DataNotFoundError",
    "DuplicateDataError",
    "ConflictError",
    "StaleDataError",
    "SecurityError",
    "PermissionDeniedError",
    "TokenError",
    "EncryptionError",
    "SignatureVerificationError",
    "LoggingError",
    "LoggerConfigurationError",
    "MessageFormatError",
    "CLIError",
    "MissingArgumentError",
    "InvalidArgumentError",
    "CacheError",
    "CacheMissError",
    "CacheSerializationError",
    "LimitExceededError",
    "ExecutionHaltedError",
    "PathError",
    "MaskError",
    "SetupStepError",
    "SetupPathError",
    "SetupPermissionError",
    "SetupTimeoutError",
    "StartupDependencyError",
    "StartupValidationError",
    "MainError",
    "MainImportError",
    "MainExecutionError",
    "RuntimeStepError",
    "RuntimeStateTransitionError",
    "RuntimeIOError",
    "RuntimeNetworkError",
    "RuntimeUnhandledError",
    "CleanupError",
    "ShutdownError",
    "SetupEnvironmentError",
    "SetupDependencyInstallError",
    "SetupBootstrapError",
    "SetupValidationError",
    "SetupResourceCreationError",
    "SetupTemplateRenderError",
    "SetupMigrationError",
    "StartSequenceError",
    "StartHookError",
    "StartConfigurationLoadError",
    "StartHealthCheckError",
    "StartServiceBindError",
    "StartServiceStartError",
    "MainLoopError",
    "MainLoopInterruptedError",
    "MainLoopTimeoutError",
    "MainDispatchError",
    "MainHandlerError",
    "RuntimeConfigurationReloadError",
    "RuntimeDataLoadError",
    "RuntimeDataSaveError",
    "RuntimeComputationError",
    "RuntimeInvariantError",
    "RuntimeConcurrencyConflictError",
    "RuntimeRetryExhaustedError",
    "RuntimeCancellationError",
    "RuntimePluginError",
    "RuntimeExtensionError",
    "RuntimeResourceLeakError",
    "RuntimeSignalError",
    "ProgramInterruptionError",
    "SetupPrecheckError",
    "SetupVersionCheckError",
    "SetupRegistryError",
    "SetupDownloadError",
    "SetupExtractionError",
    "SetupChecksumError",
    "SetupSeedDataError",
    "SetupSecretProvisionError",
    "SetupEnvWriteError",
    "SetupFinalizeError",
    "StartArgumentError",
    "StartModeError",
    "StartOrderError",
    "StartDependencyGraphError",
    "StartTimeoutError",
    "StartPortConflictError",
    "StartProtocolNegotiationError",
    "StartReadinessError",
    "StartWarmupError",
    "MainBootstrapError",
    "MainContextBuildError",
    "MainConfigurationError",
    "MainPipelineError",
    "MainRoutingError",
    "MainTaskScheduleError",
    "MainTaskExecutionError",
    "MainResultAggregationError",
    "MainExitError",
    "RuntimeContractError",
    "RuntimeDependencyUnavailableError",
    "RuntimeBackpressureError",
    "RuntimeQueueError",
    "RuntimeQueueOverflowError",
    "RuntimeQueueUnderflowError",
    "RuntimeBatchError",
    "RuntimeCheckpointError",
    "RuntimeRecoveryError",
    "RuntimeRollbackError",
    "RuntimeCommitError",
    "RuntimeConsistencyError",
    "RuntimeDeadlockError",
    "RuntimeLivelockError",
    "RuntimeThreadPoolError",
    "RuntimeProcessPoolError",
    "RuntimeResourceExhaustedError",
    "RuntimeMemoryPressureError",
    "RuntimeCpuSaturationError",
    "RuntimeFileDescriptorError",
    "RuntimeTemporaryFailureError",
    "RuntimePermanentFailureError",
    "RuntimePolicyViolationError",
    "RuntimeFeatureFlagError",
    "DatabaseError",
    "DatabaseConnectionError",
    "DatabaseAuthenticationError",
    "DatabaseAuthorizationError",
    "DatabaseTimeoutError",
    "DatabaseQueryError",
    "DatabaseQuerySyntaxError",
    "DatabaseConstraintError",
    "DatabaseUniqueConstraintError",
    "DatabaseForeignKeyConstraintError",
    "DatabaseTransactionError",
    "DatabaseTransactionBeginError",
    "DatabaseTransactionCommitError",
    "DatabaseTransactionRollbackError",
    "DatabaseDeadlockError",
    "DatabaseSerializationConflictError",
    "DatabaseMigrationExecutionError",
    "DatabaseMigrationVersionError",
    "DatabaseSeedExecutionError",
    "DatabasePoolError",
    "DatabasePoolExhaustedError",
    "DatabasePoolConfigurationError",
    "DatabaseReplicaError",
    "DatabasePrimaryUnavailableError",
    "DatabaseSchemaDriftError",
    "ExternalServiceError",
    "ExternalServiceUnavailableError",
    "ExternalServiceAuthenticationError",
    "ExternalServiceAuthorizationError",
    "ExternalServiceTimeoutError",
    "ExternalServiceProtocolError",
    "ExternalServiceResponseError",
    "ExternalServiceContractError",
    "ExternalServiceRateLimitError",
    "ExternalServiceDependencyError",
    "InternalServiceError",
    "InternalServiceUnavailableError",
    "InternalServiceDiscoveryError",
    "InternalServiceRegistrationError",
    "InternalServiceProtocolError",
    "InternalServiceTimeoutError",
    "InternalServiceContractError",
    "InternalServiceVersionMismatchError",
    "WebhookError",
    "WebhookSignatureError",
    "WebhookPayloadError",
    "WebhookDeliveryError",
    "WebhookReplayError",
    "MessagingError",
    "MessageBrokerConnectionError",
    "MessageBrokerAuthenticationError",
    "MessagePublishError",
    "MessageConsumeError",
    "MessageAcknowledgeError",
    "MessageRejectError",
    "MessageRequeueError",
    "MessageOrderingError",
    "MessageDuplicateError",
    "MessageDeadLetterError",
    "MessageSerializationFailureError",
    "MessageDeserializationFailureError",
    "EventBusError",
    "EventPublishError",
    "EventSubscribeError",
    "EventDispatchError",
    "EventHandlerError",
    "EventContractError",
    "EventReplayError",
    "WorkerError",
    "WorkerStartupFailureError",
    "WorkerShutdownFailureError",
    "WorkerHeartbeatError",
    "WorkerLeaseError",
    "WorkerCapacityError",
    "WorkerTaskClaimError",
    "WorkerTaskTimeoutError",
    "SchedulerError",
    "ScheduleParseError",
    "ScheduleValidationError",
    "ScheduleRegistrationError",
    "ScheduledJobExecutionError",
    "ScheduledJobMissedRunError",
    "ScheduledJobConcurrencyError",
    "IntegrationError",
    "InternalIntegrationError",
    "ExternalIntegrationError",
    "MetricsError",
    "MetricsBackendError",
    "TracingError",
    "TracingExportError",
    "AuditLogError",
    "SecretManagementError",
    "SecretMissingError",
    "SecretRotationError",
    "SecretDecryptionError",
    "CertificateError",
    "CertificateExpiredError",
    "CertificateValidationError",
    "CertificateChainError",
    "InternalInvariantViolationError",
    "InternalProtocolError",
    "ExternalProtocolMismatchError",
)