import io
import re
from typing import Tuple

import requests
from flask import Request, jsonify

from eq_translations import SchemaTranslation


def log(line_no, o, t, d=None):
    return {"line_no": line_no, "original": o, "translated": t, "details": d}


def check(original, trans, lineno):
    log_msg = True

    errors = []

    if "  " in original:
        if log_msg:
            errors.append(log(lineno, original, trans, f"Extra unnecessary whitespace in original"))

    if "  " in trans:
        if log_msg:
            errors.append(log(lineno, original, trans, f"Extra unnecessary whitespace in translation"))

    placeholder_o = re.findall("\{.*?\}", original)
    if placeholder_o:
        placeholder_t = re.findall("\{.*?\}", trans)
        if any(p not in placeholder_t for p in placeholder_o):
            if log_msg:
                errors.append(
                    log(
                        lineno,
                        original,
                        trans,
                        {
                            "issue": "Missing placeholders",
                            "original": placeholder_o,
                            "translated": placeholder_t,
                        },
                    )
                )

    placeholder_o = re.findall("\%\(.*?\)", original)
    if placeholder_o:
        placeholder_t = re.findall("\%\(.*?\)", trans)
        if any(p not in placeholder_t for p in placeholder_o):
            if log_msg:
                errors.append(
                    log(
                        lineno,
                        original,
                        trans,
                        {
                            "issue": "Missing visually hidden placeholder",
                            "original": placeholder_o,
                            "translated": placeholder_t,
                        },
                    )
                )

    placeholder_o = re.findall("\<.*?\>", original)
    if placeholder_o:
        placeholder_t = re.findall("\<.*?\>", trans)
        if any(p not in placeholder_t for p in placeholder_o):
            if log_msg:
                errors.append(
                    log(
                        lineno,
                        original,
                        trans,
                        {
                            "issue": "Missing tags",
                            "original": placeholder_o,
                            "translated": placeholder_t,
                        },
                    )
                )

    placeholder_o = re.findall("\<.*?\/\>", original)
    if placeholder_o:
        placeholder_t = re.findall("\<.*?\/\>", trans)
        if any(p not in placeholder_t for p in placeholder_o):
            if log_msg:
                errors.append(
                    log(
                        lineno,
                        original,
                        trans,
                        {
                            "issue": "Missing tags",
                            "original": placeholder_o,
                            "translated": placeholder_t,
                        },
                    )
                )
    if (
        "> " in original
        and "> " not in trans
        and not trans.endswith(">?")
        and not trans.endswith(">")
        and ">." not in trans
        and ">," not in trans
    ):
        if log_msg:
            errors.append(log(lineno, original, trans, f"Mismatch Closing Braces"))

    if "href='" in original and "href='" not in trans:
        if log_msg:
            errors.append(log(lineno, original, trans, f"Mismatch href tag"))

    if (
        "> " not in original
        and "> " in trans
        and not original.endswith(">?")
        and not original.endswith(">")
        and ">." not in original
        and ">," not in original
    ):
        if log_msg:
            errors.append(
                log(lineno, original, trans, f"Mismatch Closing Braces Extra Found")
            )

    if "/" in original and "/" not in trans:
        if log_msg:
            errors.append(log(lineno, original, trans, f"Mismatch Closing Tags"))

    if " <" in original and " <" not in trans:
        if log_msg:
            errors.append(log(lineno, original, trans, f"Mismatch Opening Braces"))

    if " <" not in original and " <" in trans and not original.startswith("<"):
        if log_msg:
            errors.append(
                log(lineno, original, trans, f"Mismatch Opening Braces Extra Found")
            )

    if original.endswith(".") and not trans.endswith("."):
        if log_msg:
            errors.append(
                log(lineno, original, trans, f"Missing full stop in translation")
            )

    if not original.endswith(".") and trans.endswith("."):
        if log_msg:
            errors.append(
                log(lineno, original, trans, f"Missing full stop in original")
            )

    return errors


# pylint: disable=too-many-return-statements
def check_translations(request: Request) -> Tuple[str, int]:

    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url must be provided"}), 400

    if not url.endswith(".po"):
        return jsonify({"error": "please provide a url to a .po file"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

    try:
        translation = SchemaTranslation()
        translation.load_from_io(io.BytesIO(response.text.encode()))
        errors = []
        for msg in translation.catalog:
            original = msg.id
            transl = msg.string

            if not msg.lineno:
                continue

            if msg.pluralizable:
                original = msg.id[0]
                transl = msg.string[0]
                errors.extend(check(original, transl, msg.lineno))

                original = msg.id[1]
                for idx, tran in enumerate(msg.string[1:], start=1):
                    if not tran:
                        errors.append(
                            log(
                                msg.lineno,
                                original,
                                tran,
                                f"Missing plural translation for index {idx}",
                            )
                        )
                        continue

                    errors.extend(check(original, tran, msg.lineno))
                continue

            errors.extend(check(original, transl, msg.lineno))
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400

    return jsonify({"file_url": url, "issues": len(errors), "summary": errors}), 200
