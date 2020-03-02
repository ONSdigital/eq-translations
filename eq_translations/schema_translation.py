from babel.messages import pofile


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

    @staticmethod
    def get_comment_answer_ids(comments):
        return [
            comment.split(":")[1].strip()
            for comment in comments
            if "answer-id" in comment
        ]

    def get_translation(
        self, message_id_to_translate, message_context=None,
    ):
        message = self.catalog.get(id=message_id_to_translate, context=message_context)

        if message:
            return message.string
