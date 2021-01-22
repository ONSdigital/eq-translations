from babel import Locale
from babel.messages import pofile


class SchemaTranslation:

    catalog = []

    def __init__(self, catalog=None):
        self.catalog = catalog or self.catalog

    def load_from_io(self, file_io):
        self.catalog = pofile.read_po(file_io)

        # Babel doesn't support Ulster Scots, so we need to manually set it
        if self.catalog.locale_identifier == "sco_ulster":
            self.catalog.locale = Locale("eo")

    def load(self, translation_file_path):
        with open(translation_file_path, encoding="utf8") as translation_file:
            self.catalog = pofile.read_po(translation_file)

            # Babel doesn't support Ulster Scots, so we need to manually set it
            if self.catalog.locale_identifier == "sco_ulster":
                self.catalog.locale = Locale("eo")

    def save(self, translation_file_path):
        with open(translation_file_path, "w+b") as translation_file:  # pragma: no cover
            pofile.write_po(translation_file, self.catalog)  # pragma: no cover

    @property
    def language(self):
        if self.catalog and self.catalog.locale:
            return self.catalog.locale.language

    def get_translation(
        self, message_id, context=None,
    ):
        message = self.catalog.get(id=message_id, context=context)

        return message.string if message else None
