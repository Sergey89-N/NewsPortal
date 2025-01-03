from django import template

register = template.Library()

# Список нежелательных слов
UNWANTED_WORDS = ['редиска', 'плохой', 'нежелательный']

@register.filter(name='censor')
def censor(value):
    for word in UNWANTED_WORDS:
        value = value.replace(word, '*' * len(word))
    return value
