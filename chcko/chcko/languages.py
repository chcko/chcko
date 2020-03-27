# -*- coding: utf-8 -*-

'''
EACH DICT MUST CONTAIN AT LEAST ALL AVAILABLE LANGUAGES (see initdb.py and dodo.py)
'''

# >= texts are texts/fragments
# >= fragments are fragments
langnumkind = {
    'en':
    {   0:'problems',
        1:'texts',
        2:'courses',
        3:'examples',
        4:'summaries',
        5:'formal',
        6:'fragments',
        7:'remarks',
        8:'citations',
        9:'definitions',
        10:'theorems',
        11:'corollaries',
        12:'lemmas',
        13:'propositions',
        14:'axioms',
        15:'conjectures',
        16:'claims',
        17:'identities',
        18:'paradoxes',
        19:'meta'},
    'de':
    {   0:'Übungen',
        1:'Texte',
        2:'Kurse',
        3:'Beispiele',
        4:'Zusammenfassungen',
        5:'Formelles',
        6:'Fragmente',
        7:'Bemerkungen',
        8:'Zitate',
        9:'Definitionen',
        10:'Theoreme',
        11:'Korollare',
        12:'Lemmas',
        13:'Propositionen',
        14:'Axiome',
        15:'Vermutungen',
        16:'Behauptungen',
        17:'Identitäten',
        18:'Paradoxien',
        19:'Meta'},
}

langkindnum = {lng:{v: k for k, v in langnumkind[lng].items()} for lng in langnumkind}

def kindint(knd, numkind):
    """
    >>> kindint('Tex',langkindnum['de'])
    1
    >>> kindint('meta',langkindnum['en'])
    19
    >>> kindint(9,langkindnum['en'])
    9
    """
    try:
        return int(knd)
    except:
        try:
            return numkind[knd]
        except:
            for k in numkind:
                if knd in k:
                    return numkind[k]
            return -1


role_strings = {
    # these are listed on the page
    'en': ['School', 'Field', 'Teacher', 'Class', 'Role']
    ,'de': ['Schule', 'Bereich', 'Lehrer', 'Klasse', 'Rolle']
    # ... add more if some translations exist (defaults to en)
    #,'it': ['Scuola', 'Campo', 'Prof', 'Classe', 'Ruolo']
    #,'fr': ['École', 'Domaine', 'Prof', 'Classe', 'Rôle']
    #,'es': ['Escuola', 'Esfera', 'Prof', 'Clase', 'Rol']

}

languages = {'ab': 'Abkhazian',
             'aa': 'Afar',
             'af': 'Afrikaans',
             'sq': 'Albanian',
             'am': 'Amharic',
             'ar': 'Arabic',
             'an': 'Aragonese',
             'hy': 'Armenian',
             'as': 'Assamese',
             'ay': 'Aymara',
             'az': 'Azerbaijani',
             'ba': 'Bashkir',
             'eu': 'Basque',
             'bn': 'Bengali (Bangla)',
             'dz': 'Bhutani',
             'bh': 'Bihari',
             'bi': 'Bislama',
             'br': 'Breton',
             'bg': 'Bulgarian',
             'my': 'Burmese',
             'be': 'Byelorussian (Belarusian)',
             'km': 'Cambodian',
             'ca': 'Catalan',
             'zh': 'Chinese',
             'co': 'Corsican',
             'hr': 'Croatian',
             'cs': 'Czech',
             'da': 'Danish',
             'nl': 'Dutch',
             'en': 'English',
             'eo': 'Esperanto',
             'et': 'Estonian',
             'fo': 'Faeroese',
             'fa': 'Farsi',
             'fj': 'Fiji',
             'fi': 'Finnish',
             'fr': 'French',
             'fy': 'Frisian',
             'gl': 'Galician',
             'gd': 'Gaelic (Scottish)',
             'gv': 'Gaelic (Manx)',
             'ka': 'Georgian',
             'de': 'German',
             'el': 'Greek',
             'kl': 'Greenlandic',
             'gn': 'Guarani',
             'gu': 'Gujarati',
             'ht': 'Haitian Creole',
             'ha': 'Hausa',
             'he': 'Hebrew',
             'hi': 'Hindi',
             'hu': 'Hungarian',
             'is': 'Icelandic',
             'io': 'Ido',
             'id': 'Indonesian',
             'ia': 'Interlingua',
             'ie': 'Interlingue',
             'iu': 'Inuktitut',
             'ik': 'Inupiak',
             'ga': 'Irish',
             'it': 'Italian',
             'ja': 'Japanese',
             'jv': 'Javanese',
             'kn': 'Kannada',
             'ks': 'Kashmiri',
             'kk': 'Kazakh',
             'rw': 'Kinyarwanda (Ruanda)',
             'ky': 'Kirghiz',
             'rn': 'Kirundi (Rundi)',
             'ko': 'Korean',
             'ku': 'Kurdish',
             'lo': 'Laothian',
             'la': 'Latin',
             'lv': 'Latvian (Lettish)',
             'li': 'Limburgish ( Limburger)',
             'ln': 'Lingala',
             'lt': 'Lithuanian',
             'mk': 'Macedonian',
             'mg': 'Malagasy',
             'ms': 'Malay',
             'ml': 'Malayalam',
             'mt': 'Maltese',
             'mi': 'Maori',
             'mr': 'Marathi',
             'mo': 'Moldavian',
             'mn': 'Mongolian',
             'na': 'Nauru',
             'ne': 'Nepali',
             'no': 'Norwegian',
             'oc': 'Occitan',
             'or': 'Oriya',
             'om': 'Oromo (Afaan Oromo)',
             'ps': 'Pashto (Pushto)',
             'pl': 'Polish',
             'pt': 'Portuguese',
             'pa': 'Punjabi',
             'qu': 'Quechua',
             'rm': 'Rhaeto-Romance',
             'ro': 'Romanian',
             'ru': 'Russian',
             'sm': 'Samoan',
             'sg': 'Sangro',
             'sa': 'Sanskrit',
             'sr': 'Serbian',
             'sh': 'Serbo-Croatian',
             'st': 'Sesotho',
             'tn': 'Setswana',
             'sn': 'Shona',
             'ii': 'Sichuan Yi',
             'sd': 'Sindhi',
             'si': 'Sinhalese',
             'ss': 'Siswati',
             'sk': 'Slovak',
             'sl': 'Slovenian',
             'so': 'Somali',
             'es': 'Spanish',
             'su': 'Sundanese',
             'sw': 'Swahili (Kiswahili)',
             'sv': 'Swedish',
             'tl': 'Tagalog',
             'tg': 'Tajik',
             'ta': 'Tamil',
             'tt': 'Tatar',
             'te': 'Telugu',
             'th': 'Thai',
             'bo': 'Tibetan',
             'ti': 'Tigrinya',
             'to': 'Tonga',
             'ts': 'Tsonga',
             'tr': 'Turkish',
             'tk': 'Turkmen',
             'tw': 'Twi',
             'ug': 'Uighur',
             'uk': 'Ukrainian',
             'ur': 'Urdu',
             'uz': 'Uzbek',
             'vi': 'Vietnamese',
             'vo': 'Volapük',
             'wa': 'Wallon',
             'cy': 'Welsh',
             'wo': 'Wolof',
             'xh': 'Xhosa',
             'yi': 'Yiddish',
             'yo': 'Yoruba',
             'zu': 'Zulu'}
