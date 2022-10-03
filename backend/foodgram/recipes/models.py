from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Model for recipes tags."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    color = models.CharField(
        max_length=7,
        verbose_name='Цвет в HEX'
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        null=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Model for recipes ingredients."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurment_unit'],
                name='unique_name_measurment_unit'
            )
        ]

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Model to link recipes and ingredients with addition of `amount` field"""
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='ingredients')
    amount = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Количество не может быть меньше 1.'),
        ],
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return f'{self.ingredient}: {self.amount}'


class Recipe(models.Model):
    """Recipe model"""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )

    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка'
    )

    text = models.TextField(
        verbose_name='Описание'
    )

    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1, 'Время приготовления не может '
                              'быть менее минуты.'),
        ],
        verbose_name='Время приготовления (в минутах)'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )

    ingredients = models.ManyToManyField(
        IngredientRecipe,
        verbose_name='Ингредиенты',
        related_name='recipes',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['-created']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Model for users favorites recipes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_user_fav_recipe'
        )


class ShoppingCart(models.Model):
    """Model for users favorites recipes."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'списки покупок'
        models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_user_cart_recipe'
        )
