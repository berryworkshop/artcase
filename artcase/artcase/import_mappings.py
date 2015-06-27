from .models import Artifact, Creator, Medium, Size, Organization
from collections import OrderedDict

mappings = {
    'artifact_primary': {
        'model': Artifact,
        'fields': {
            # 'CSV Column Name': target model attribute
            # 'None' means this column needs custom processing

            #'Code Number': 'code_number', # parsed automatically
            'Title': 'title_english_short',
            'Print Run': 'edition_size',
            'Condition': 'condition',
            'Notes': None,
            'Todo': None,
            'Media': None,
            'Media size': None,
            'Print date': None,
            'Publish date': None,
            'Value': None,
        }
    },
    'creator_primary': {
        'model': Creator,
        'fields': {
            # operations on this creator
            'Artist Name Roman': None,
            'Artist Notes': None,
            'Artist Name Cyrillic': None,

            # operations on artifact
            'Artifact Number': None,
            'Transcribed Name': None,
            'Poster Notes': None,

            # operations on second artist
            'Second Artist Name Roman': None,
            'Second Artist Name Cyrillic': None,
        }
    },
    'publisher_primary': {
        'model': Organization,
        'fields': {
            'Name': 'name',
            'Location': 'location',
            'Description': None,
            'Artifact Code': None,
        }
    },
    'printer_primary': {
        'model': Organization,
        'fields': {
            'Name': 'name',
            'Location': 'location',
            'Description': None,
            'Artifact Code': None,
        }
    },
    'glavlit_primary': {
        'model': Artifact,
        'fields': {
            'Glavlit Directory Number': 'glavlit',
        }
    },
    'translations_primary': {
        'model': Artifact,
        'fields': {
            #'Code Number': 'code_number', # parsed automatically
            'Title': 'title_english_full',
            #'Artist': None, # Defer to artists.csv
            'Print Run': None,
            'Type': None,
            #'Print Date': None, # Defer to artifacts.csv
            'Condition': None,
            'Notes': None,
        }
    }
}
