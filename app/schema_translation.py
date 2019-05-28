from babel.messages import pofile

from app.utils import dumb_to_smart_quotes


class SchemaTranslation:

    catalog = []

    def __init__(self, catalog=None):
        self.catalog = catalog or self.catalog

    def load(self, translation_file_path):
        with open(translation_file_path, encoding='utf8') as translation_file:
            self.catalog = pofile.read_po(translation_file)

    def save(self, translation_file_path):
        with open(translation_file_path, 'w+b') as translation_file:
            pofile.write_po(translation_file, self.catalog)

    def translate_message(self, message_to_translate, answer_id=None, message_context=None):
        for message in self.catalog:
            if message.id and dumb_to_smart_quotes(message.id) == dumb_to_smart_quotes(message_to_translate):
                found = True
                comment_answer_id = None

                if message.auto_comments:
                    for comment in message.auto_comments:
                        if 'answer-id' in comment:
                            comment_answer_id = comment.split(":")[1].strip()

                if answer_id or comment_answer_id:
                    if message_context:
                        found = comment_answer_id == answer_id and message.context == message_context
                    else:
                        found = comment_answer_id == answer_id

                if found:
                    return dumb_to_smart_quotes(message.string)
