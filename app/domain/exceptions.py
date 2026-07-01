class DomainError(Exception):
    """Base exception for domain-layer errors."""


class InvalidCourseError(DomainError):
    """
    Raised when a course violates its invariants
    (e.g. empty title or invalid structure).
    """
    pass


class InvalidModuleError(DomainError):
    """
    Raised when a module violates its invariants
    (e.g. empty title or invalid structure).
    """
    pass


class InvalidSectionError(DomainError):
    """
    Raised when a section violates its invariants
    (e.g. empty title or invalid structure).
    """
    pass


class InvalidLectureError(DomainError):
    """
    Raised when a lecture violates its invariants
    (e.g. empty title or invalid structure).
    """
    pass


class InvalidUserError(DomainError):
    """
    Raised when a user violates its invariants
    (e.g. empty title or invalid structure).
    """
    pass


class SectionQuestionAlreadyAttachedError(DomainError):
    pass


class SectionQuestionNotAttachedError(DomainError):
    pass


class InvalidQuestionError(DomainError):
    pass


class QuestionAttemptLimitExceededError(DomainError):
    pass


class InvalidAnswerOptionError(DomainError):
    pass


class InvalidQuestionAttemptError(DomainError):
    pass


class InvalidQuestionResultError(DomainError):
    pass


class QuestionAlreadySolvedError(DomainError):
    pass


class InvalidProgressError(DomainError):
    pass


class InvalidTaskError(DomainError):
    pass


class SectionTaskAlreadyAttachedError(DomainError):
    pass


class SectionTaskNotAttachedError(DomainError):
    pass


class InvalidTaskAttemptError(DomainError):
    """Некорректно собранная попытка."""
    pass


class TaskAttemptLimitExceededError(DomainError):
    """Нарушение лимита отправок."""
    pass


class TaskAlreadySolvedError(DomainError):
    """После успешного решения простую задачу не нужно решать заново."""
    pass


class InvalidCodeTaskError(DomainError):
    pass


class SectionCodeTaskAlreadyAttachedError(DomainError):
    pass


class SectionCodeTaskNotAttachedError(DomainError):
    pass


class InvalidCodeSubmissionError(DomainError):
    pass


class CodeSubmissionLimitExceededError(DomainError):
    pass


class CodeTaskAlreadySolvedError(DomainError):
    pass


class InvalidTestCaseError(DomainError):
    pass


class InvalidExecutionResultError(DomainError):
    pass
