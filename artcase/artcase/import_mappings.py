from .models import Artifact, Creator
from collections import OrderedDict

mappings = {
    'artifact_primary': {
        'model': Artifact,
        'fields': {
            # 'Column Name': model_attribute,
            'Code Number': 'code_number',
            'Title': 'title_english',
            'Print Run': 'edition_size',
            'Condition': 'condition',
            'Notes': 'description',
            'Todo': 'description',
            #'Media': '',
            #'Media size': '',
            #'Print date': '',
            #'Publish date': '',
            #'Value': '',
        },
        'aggregate_fields': [
            # Fields which do not obliterate their target, but are
            # concatenated at the end of a presumably existing field.
            # Order depends on csv.
            'Notes',
            'Todo'
        ]
    }
}