from babel.messages import pofile

from eq_translations.utils import are_dumb_strings_equal


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
        self,
        message_id_to_translate,
        pluralizable,
        answer_id=None,
        message_context=None,
    ):
        for message in self.catalog:
            if (
                message.id
                and not (message.pluralizable ^ pluralizable)
                and are_dumb_strings_equal(
                    message.id, message_id_to_translate, pluralizable=pluralizable
                )
            ):

                found = True
                comment_answer_ids = []

                if message.auto_comments:
                    comment_answer_ids = SchemaTranslation.get_comment_answer_ids(
                        message.auto_comments
                    )

                if answer_id or comment_answer_ids:
                    found = answer_id in comment_answer_ids

                    if message_context:
                        found &= message.context == message_context

                if found:
                    return message.string
