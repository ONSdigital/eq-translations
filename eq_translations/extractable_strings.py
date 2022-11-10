EXTRACTABLE_STRINGS = [
    {"json_path": "$.title", "description": "Questionnaire title"},
    {"json_path": "$.legal_basis", "description": "Questionnaire legal basis"},
    {"json_path": "$.messages.*", "description": "Global answer error message"},
    {"json_path": "$.submission.button", "description": "Submission button"},
    {
        "json_path": "$.submission.guidance",
        "description": "Submission guidance",
    },
    {"json_path": "$.submission.title", "description": "Submission title"},
    {"json_path": "$.submission.warning", "description": "Submission warning"},
    {
        "json_path": "$.post_submission.guidance.contents[*].title",
        "description": "Post submission guidance heading",
    },
    {
        "json_path": "$.post_submission.guidance.contents[*].description",
        "description": "Post submission guidance description",
    },
    {
        "json_path": "$.post_submission.guidance.contents[*].list[*]",
        "description": "Post submission guidance list item",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {"json_path": "$.sections[*].title", "description": "Section title"},
    {"json_path": "$..page_title", "description": "Page title"},
    {
        "json_path": "$.sections[*].repeat.title",
        "description": "Section title (repeating section)",
    },
    {
        "json_path": "$.sections[*].repeat.page_title",
        "description": "Section page title suffix (repeating section)",
    },
    {
        "json_path": "$.sections[*].summary.items[*].title",
        "description": "Section summary item title",
    },
    {
        "json_path": "$.sections[*].summary.items[*].add_link_text",
        "description": "Section summary list add link",
    },
    {
        "json_path": "$.sections[*].summary.items[*].empty_list_text",
        "description": "Section summary empty list text",
    },
    {"json_path": "$..groups[*].title", "description": "Group title"},
    {"json_path": "$..blocks[*].title", "description": "Block title"},
    {"json_path": "$..summary.title", "description": "List collector summary heading"},
    {
        "json_path": "$..summary.item_title",
        "description": "List collector summary item",
    },
    {
        "json_path": "$..summary.empty_list_text",
        "description": "List collector empty list text",
    },
    {
        "json_path": "$..summary.add_link_text",
        "description": "List collector add link text",
    },
    {
        "json_path": "$..add_block.cancel_text",
        "description": "List collector add block cancel link",
    },
    {"json_path": "$..content.title", "description": "Content page main heading"},
    {"json_path": "$..content.instruction[*]", "description": "Content instruction"},
    {
        "json_path": "$..content.contents[*].title",
        "description": "Content page heading",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].description",
        "description": "Content page description",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].list[*]",
        "description": "Content page list item",
        "context": "Content",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..content.contents[*].definition.title",
        "description": "Definition title",
        "context": "Content",
    },
    {
        "json_path": "$..content.contents[*].definition.contents[*].description",
        "description": "Definition description",
        "context": "Content",
    },
    {"json_path": "$..question.title", "description": "Question text"},
    {
        "json_path": "$..question.description[*]",
        "description": "Question description",
        "context": "Question",
    },
    {
        "json_path": "$..question.instruction[*]",
        "description": "Question instruction",
        "context": "Question",
    },
    {
        "json_path": "$..question.warning",
        "description": "Question warning",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].title",
        "description": "Question definition link",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].title",
        "description": "Question definition heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].description",
        "description": "Question definition description",
        "context": "Question",
    },
    {
        "json_path": "$..question.definitions[*].contents[*].list[*]",
        "description": "Question definition list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..question.guidance.contents[*].title",
        "description": "Question guidance heading",
        "context": "Question",
    },
    {
        "json_path": "$..question.guidance.contents[*].description",
        "description": "Question guidance description",
        "context": "Question",
    },
    {
        "json_path": "$..question.guidance.contents[*].list[*]",
        "description": "Question guidance list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..question.calculation.title",
        "description": "Question calculation title",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].validation.messages.*",
        "description": "Answer error message",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].label",
        "description": "Answer",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].instruction",
        "description": "Checkbox answer instruction",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].placeholder",
        "description": "Dropdown field placeholder text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].description",
        "description": "Answer description",
        "context": "Question",
        "additional_context": ["Answer"],
    },
    {
        "json_path": "$..answers[*].playback",
        "description": "Relationships playback template",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].label",
        "description": "Answer option",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].description",
        "description": "Answer option description",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].detail_answer.label",
        "description": "Detail answer label",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].detail_answer.description",
        "description": "Detail answer description",
        "context": "Question",
        "additional_context": ["AnswerOption"],
    },
    {
        "json_path": "$..answers[*].options[*].title",
        "description": "Relationships answer option question text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].options[*].playback",
        "description": "Relationships answer option playback text",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.show_guidance",
        "description": "Answer guidance show link",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.hide_guidance",
        "description": "Answer guidance hide link",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].title",
        "description": "Answer guidance heading",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].description",
        "description": "Answer guidance description",
        "context": "Question",
    },
    {
        "json_path": "$..answers[*].guidance.contents[*].list[*]",
        "description": "Answer guidance list item",
        "context": "Question",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..primary_content[*].title",
        "description": "Introduction primary content",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..primary_content[*].contents[*].list[*]",
        "description": "Introduction primary content list item",
        "context": "PrimaryContent",
        "additional_context": ["ListHeading", "ListDescription"],
    },
    {
        "json_path": "$..primary_content[*].contents[*].description",
        "description": "Introduction primary content description",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..primary_content[*].contents[*].guidance.contents[*].title",
        "description": "Introduction primary content guidance title",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..primary_content[*].contents[*].guidance.contents[*].description",
        "description": "Introduction primary content guidance description",
        "context": "PrimaryContent",
    },
    {
        "json_path": "$..preview_content.title",
        "description": "Introduction preview content title",
        "context": "PreviewContent",
    },
    {
        "json_path": "$..preview_content.contents[*].description",
        "description": "Introduction preview content description",
        "context": "PreviewContent",
    },
    {
        "json_path": "$..preview_content.questions[*].question",
        "description": "Introduction preview content question title",
        "context": "PreviewContent",
    },
    {
        "json_path": "$..preview_content.questions[*].contents[*].description",
        "description": "Introduction preview question content description",
        "context": "PreviewContent",
        "additional_context": ["PreviewQuestionListHeading"],
    },
    {
        "json_path": "$..preview_content.questions[*].contents[*].list[*]",
        "description": "Introduction preview question list item",
        "context": "PreviewContent",
        "additional_context": ["PreviewQuestionListHeading"],
    },
    {
        "json_path": "$..secondary_content[*].contents[*].title",
        "description": "Introduction secondary content contents title",
    },
    {
        "json_path": "$..secondary_content[*].contents[*].list[*]",
        "description": "Introduction secondary content contents list item",
    },
    {
        "json_path": "$..secondary_content[*].contents[*].description",
        "description": "Introduction secondary content contents description",
    },
]

CONTEXT_DEFINITIONS = {
    "Question": {
        "parent_schema_property": "question",
        "property": "title",
        "text": "{context}",
    },
    "Content": {
        "parent_schema_property": "content",
        "property": "title",
        "text": "{context}",
    },
    "Answer": {
        "parent_schema_property": "answers",
        "property": "label",
        "text": "For answer: {context}",
    },
    "AnswerOption": {
        "parent_schema_property": "options",
        "property": "label",
        "text": "For answer option: {context}",
    },
    "ListHeading": {
        "parent_schema_property": "contents",
        "property": "title",
        "text": "For heading: {context}",
    },
    "ListDescription": {
        "parent_schema_property": "contents",
        "property": "description",
        "text": "For description: {context}",
    },
    "PrimaryContent": {
        "parent_schema_property": "primary_content",
        "property": "title",
        "text": "{context}",
    },
    "PreviewContent": {
        "parent_schema_property": "preview_content",
        "property": "title",
        "text": "{context}",
    },
    "PreviewQuestionListHeading": {
        "parent_schema_property": "questions",
        "property": "question",
        "text": "For question: {context}",
    },
}
