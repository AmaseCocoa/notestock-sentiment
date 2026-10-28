import re

preprocessing_rules = {
    r"https?://[\w?%&./=\-#~]+": "[URL]",
    r"@[\w.\-]+@[\w.\-]+\.[\w\-]+": "[MENTION]",
    r"@[\w.\-]+": "[MENTION]",
    r"[#＃][^\s#＃\s!@\$%^&*()\-+={}\[\]|\\:;\"'<>,.?/~`]+": "[HASHTAG]",
}

def batch_replace(text) -> str:
    for pattern, replacement in preprocessing_rules.items():
        text = re.sub(pattern, replacement, text)
    return text

def clean_text_optimized(text, max_emoji_len=20, replace_emoji_to_placeholder: bool = False):
    text = batch_replace(text)

    code_pattern = r"(```[\s\S]*?```|`[^`\n]+`)"
    tokens = re.split(code_pattern, text)

    normal_text_rules = [
        (r"\*\*([\s\(\S\)]*?)\*\*", r"\1"),
        (r"__([\s\(\S\)]*?)__", r"\1"),
        (r"<[^>]+>", ""),
        (rf":[\w.\-]{{{max_emoji_len},}}:", ""),
        (r"(:[\w.\-]+:)(\s*\1)+", r"\1"),
    ]

    if replace_emoji_to_placeholder:
        normal_text_rules.append((r":([\w.\-]+):", r"[EMOJI]"))
    else:
        normal_text_rules.append((r":([\w.\-]+):", r" \1 "))

    def remove_nested_brackets(target_text):
        nested_pattern = r"\$\[[^\s\]]+\s+([^\$\[\]]+?)\]"

        while True:
            next_text = re.sub(nested_pattern, r"\1", target_text)

            if next_text == target_text:
                break
            target_text = next_text

        target_text = re.sub(r"\$\[[^\s\]]+\s*\]", "", target_text)
        return target_text

    def clean_normal_text(target_text):
        target_text = remove_nested_brackets(target_text)

        for pattern, replacement in normal_text_rules:
            target_text = re.sub(pattern, replacement, target_text)
        return target_text

    processed_tokens = []
    for token in tokens:
        if token.startswith("```"):
            processed_tokens.append(" [CODE] ")
        elif token.startswith("`"):
            processed_tokens.append(token)
        else:
            processed_tokens.append(clean_normal_text(token))

    result_text = "".join(processed_tokens)
    result_text = re.sub(r" {2,}", " ", result_text)

    return result_text.strip()
