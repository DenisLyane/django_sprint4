# НЕ ПРОХОДИТ pytest, если каждую модель
# вынести по отдельным файлам в папку models
# о проблеме писал Вам в "Пачке"
# папку моделей ПЕРЕИМЕНОВАЛ СПЕЦИАЛЬНО,
# что бы можно было отправить на ревью!
# (тесты валятся с папкой названной "models"),
# (Переименовал в models_blogicum)
# Кэш чистил, не помогло.

from .posts import Post
from .category import Category
from .comments import Comment
from .location import Location
from .users import User

__all__ = ["Post", "Comment", "Category", "Location", "User"]
