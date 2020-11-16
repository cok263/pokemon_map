import folium
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from .models import *


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url))

    pokemons_ = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons_:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def evalution_info(request, pokemon):
    if pokemon is None:
        return {}
    return {
        "title_ru": pokemon.title,
        "pokemon_id": pokemon.id,
        "img_url": request.build_absolute_uri(pokemon.photo.url)
    }


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    requested_pokemons = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    previous_evolution = requested_pokemon.previous_evolution

    try:
        next_evolution = requested_pokemon.forward_evolutions.get()
    except Pokemon.DoesNotExist:
        next_evolution = None

    pokemon = {
        'pokemon_id': pokemon_id,
        'title_ru': requested_pokemon.title,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': request.build_absolute_uri(requested_pokemon.photo.url),
        'entities': [],
        'next_evolution': evalution_info(
            request,
            next_evolution
        ),
        'previous_evolution': evalution_info(
            request,
            previous_evolution
        ),
    }

    for pokemon_entity in requested_pokemons:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            requested_pokemon.title,
            request.build_absolute_uri(requested_pokemon.photo.url)
        )
        pokemon['entities'].append(
            {
                'level': pokemon_entity.level,
                'lat': pokemon_entity.lat,
                'lon': pokemon_entity.lon,
            }
        )

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
