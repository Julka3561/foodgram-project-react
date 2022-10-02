from django.contrib import admin
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'author',
                    'qty_of_favorites',
                    )
    list_editable = ('name', 'author')
    search_fields = ('name',)
    list_filter = ('author', 'tags')
    empty_value_display = '-пусто-'

    def qty_of_favorites(self, obj):
        return obj.favorite.count()

    qty_of_favorites.short_description = 'Количество в избранном'


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'slug',
                    )
    list_editable = ('name', 'slug',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'name',
                    'measurement_unit',
                    )
    list_editable = ('name', 'measurement_unit',)
    search_fields = ('name',)


class FavoriteAndCartAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'user',
                    'recipe',
                    )
    list_editable = ('user', 'recipe',)
    list_filter = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient,  IngredientAdmin)
admin.site.register(Favorite,  FavoriteAndCartAdmin)
admin.site.register(ShoppingCart, FavoriteAndCartAdmin)
