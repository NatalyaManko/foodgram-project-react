from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validation_username


class User(AbstractUser):
    """Модель Пользователя"""
<<<<<<< HEAD
<<<<<<< HEAD

    username = models.CharField(
        'Логин',
=======
    username = models.CharField(
        'Username',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
    username = models.CharField(
        'Username',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        validators=(AbstractUser.username_validator, validation_username,),
        max_length=150,
        unique=True,
        help_text=('Требуется не более 150 символов.'
<<<<<<< HEAD
<<<<<<< HEAD
                   'Только буквы, цифры и @/./+/-/_.'),
=======
                    'Только буквы, цифры и @/./+/-/_.'),
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
                    'Только буквы, цифры и @/./+/-/_.'),
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        error_messages={
            'unique': 'Пользователь с таким именем уже существует.',
        },
    )
    email = models.EmailField(
<<<<<<< HEAD
<<<<<<< HEAD
        'Адрес электронной почты',
=======
        'email address',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
        'email address',
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
<<<<<<< HEAD
<<<<<<< HEAD
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

=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель Подписки на Пользователя"""
<<<<<<< HEAD
<<<<<<< HEAD

    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Подписчик',
                                 related_name='follows_user')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name='Подписан',
=======
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
    follower = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name = 'Подписчик',
                             related_name='follows_user')
    following = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name = 'Подписан',
<<<<<<< HEAD
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
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
<<<<<<< HEAD
<<<<<<< HEAD
        return f'{self.follower} на {self.following}'
=======
        return f'{self.follower} на {self.following}' 
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
=======
        return f'{self.follower} на {self.following}' 
>>>>>>> 152dd30ebbb1a1a6a72d4166ef0c99464dc51bc3
