from babel.messages import pofile

from eq_translations.utils import get_plural_forms_for_language


class SchemaTranslation:

    catalog = []

    def __init__(self, catalog=None):
        self.catalog = catalog or self.catalog

    def load(self, translation_file_path):
        with open(
            translation_file_path, encoding="utf8"
        ) as translation_file:  # pragma: no cover
            self.catalog = pofile.read_po(translation_file)  # pragma: no cover

    def save(self, translation_file_path):
        with open(translation_file_path, "w+b") as translation_file:  # pragma: no cover
            pofile.write_po(translation_file, self.catalog)  # pragma: no cover

    @property
    def language(self):
        if self.catalog and self.catalog.locale:
            return self.catalog.locale.language

    @property
    def plural_forms(self):
        if self.language:
            return get_plural_forms_for_language(self.language)

    def get_translation(
        self, message_id, context=None,
    ):
        message = self.catalog.get(id=message_id, context=context)

        return message.string if message else None
