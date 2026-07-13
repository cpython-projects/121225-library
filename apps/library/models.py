import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


def age_validator(value):
    today = timezone.now().date()
    if value > today:
        raise ValidationError(f'You are not born')

    age = (today.year - value.year -
            ((today.month, today.year) < (value.month, value.day)))
    if not 6 <= age <= 120:
        raise ValidationError('Your age must be between 6 and 120!')


class Author(UUIDModel, TimeStampedModel):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    profile = models.URLField(blank=True, verbose_name=_('Profile URL'))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name=_('Rating')
    )

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Deleted at'))

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    def __str__(self):
        return f'{self.first_name[0]}. {self.last_name}; {self.date_of_birth}'


class AuthorDetail(TimeStampedModel):
    author = models.OneToOneField(
        Author,
        on_delete=models.CASCADE,
        related_name='details',
        verbose_name=_('Author')
    )

    biography = models.TextField(blank=True, verbose_name=_('Biography'))
    birth_city = models.CharField(blank=True, max_length=50, verbose_name=_('Birth City'))
    gender = models.CharField(choices=Gender.choices, max_length=1, verbose_name=_('Gender'))

    def __str__(self):
        return f'Details of {self.author}'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return self.name


class Library(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    location = models.CharField(max_length=50, verbose_name=_('Location'), unique=True)
    site = models.URLField(blank=True, verbose_name=_('Site'))
    slug = models.SlugField(max_length=70, unique=True, blank=True, verbose_name=_('Slug'))

    def __str__(self):
        return self.name


class Member(UUIDModel, TimeStampedModel):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin'),
        STAFF = 'employee', _('Employee'),
        VISITOR = 'visitor', _('Visitor')

    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    email = models.EmailField(blank=True, unique=True, verbose_name=_('Email'))
    gender = models.CharField(choices=Gender.choices, max_length=1, verbose_name=_('Gender'))
    date_of_birth = models.DateField(
        validators=[age_validator],
        verbose_name=_('Date of Birth')
    )
    role = models.CharField(
        choices=Role.choices, max_length=10, default=Role.VISITOR, verbose_name=_('Role')
    )
    active = models.BooleanField(default=True, verbose_name=_('Active'))
    libraries = models.ManyToManyField(Library, verbose_name=_('Libraries'), blank=True, related_name='members')

    @property
    def age(self):
        today = timezone.now().date()
        return (today.year - self.date_of_birth.year -
                ((today.month, today.year) < (self.date_of_birth.month, self.date_of_birth.day)))

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(UUIDModel, TimeStampedModel):
    class Genre(models.TextChoices):
        FICTION = 'Fiction', _('Fiction'),
        NON_FICTION = 'Non-Fiction', _('Non-Fiction')
        HORROR = 'Horror', _('Horror'),
        HISTORY = 'History', _('History')

    title = models.CharField(max_length=50, verbose_name=_('Title'))
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL,
        verbose_name=_('Author')
    )

    published_at = models.DateField()
    genre = models.CharField(choices=Genre.choices, max_length=20, verbose_name=_('Genre'))
    page_count = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name=_('Page Count')
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL,
        verbose_name=_('Category')
    )
    publisher = models.ForeignKey(
        Member,
        null=True,
        blank=True,
        related_name='books',
        on_delete=models.SET_NULL,
        verbose_name=_('Publisher')
    )
    libraries = models.ManyToManyField(Library, verbose_name=_('Libraries'), blank=True, related_name='books')
    description = models.TextField(blank=True, verbose_name=_('Summary'))

    @property
    def rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()
        if total_reviews == 0:
            return 0
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / total_reviews, 2)

    def __str__(self):
        return f'{self.title}'


class Posts(TimeStampedModel):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    body = models.TextField(verbose_name=_('Body'))
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Author'),
        related_name='posts'
    )

    moderated = models.BooleanField(default=False, verbose_name=_('Moderated'))
    library = models.ForeignKey(
        Library,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Library')
    )

    def __str__(self):
        return f'{self.title} - {self.author} - {self.body[:20]}'


class Borrow(TimeStampedModel):
    member = models.ForeignKey(
        Member,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='borrows',
        verbose_name=_('Member')
    )
    book = models.ForeignKey(
        Book,
        null=True,
        blank=True,
        related_name='borrows',
        on_delete=models.SET_NULL,
        verbose_name=_('Book')
    )
    library = models.ForeignKey(
        Library,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='borrows',
        verbose_name=_('Library')
    )
    borrow_date = models.DateField()
    return_date = models.DateField()
    returned = models.BooleanField(default=False, verbose_name=_('Returned'))

    @property
    def is_overdue(self):
        if self.returned:
            return True
        return self.return_date <= timezone.now().date()

    def __str__(self):
        return f'{self.member} - {self.book} - {self.return_date}'


class Review(TimeStampedModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Member, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews')
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()

    def __str__(self):
        return f"Review of {self.book} by {self.reviewer}"


class Event(UUIDModel, TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='events')
    books = models.ManyToManyField(Book, related_name='events', blank=True)

    def __str__(self):
        return self.title


class EventParticipant(TimeStampedModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='event_participations')
    registration_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.member} on {self.event}"








