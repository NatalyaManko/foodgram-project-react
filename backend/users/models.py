from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validation_username


class User(AbstractUser):
    """Модель Пользователя"""

    username = models.CharField(
        'Логин',
        validators=(AbstractUser.username_validator, validation_username,),
        max_length=150,
        unique=True,
        help_text=('Требуется не более 150 символов.'
                   'Только буквы, цифры и @/./+/-/_.'),
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    email = models.EmailField(
        'Адрес электронной почты',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель Подписки на Пользователя"""

    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Подписчик',
                                 related_name='follows_user')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name='Подписан',
                                  related_name='follows_following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['follower', 'following'],
                name='unique_subsribe'
            )
        ]
        ordering = ('-id',)
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.follower} на {self.following}'
