from .models import Artifact, Creator
from collections import OrderedDict

mappings = {
    'artifact_primary': {
        'model': Artifact,
        'aggregate_fields': [
            # Fields which do not overwrite their target, but are
            # concatenated at the end of a presumably existing field.
            # Order depends on csv.
            'Notes',
            'Todo'
        ],
        'fields': {
            # 'CSV Column Name': target model attribute,
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
        }
    }
}