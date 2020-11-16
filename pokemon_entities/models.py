from django.db import models

class Pokemon(models.Model):
    title = models.CharField('Русское название', max_length=200)
    title_jp = models.CharField('Японское название', max_length=200, blank=True)
    title_en = models.CharField('Английское название', max_length=200, blank=True)
    photo = models.ImageField('Изображение покемона', upload_to='pokemons', null=True)
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey(
        'Pokemon',
        verbose_name = "Из кого эвалюционирует",
        related_name='forward_evolutions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField('Широта')
    lon = models.FloatField('Долгота')
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name = "Вид покемона",
        on_delete=models.CASCADE
    )
    appeared_at = models.DateTimeField('Момент появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Момент исчезновения', null=True, blank=True)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return '{} {}'.format(self.pokemon.title, self.id)

