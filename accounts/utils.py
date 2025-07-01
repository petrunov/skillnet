def get_request_language(request, default="en"):
    """
    Extracts the language code from the Referer header.
    Assumes the first path segment after the domain is the language code (e.g., https://example.com/en/...).
    Falls back to default if invalid or missing.
    """
    supported_languages = {"en", "bg", "de"}  # extend as needed

    referer = request.headers.get("Referer")
    if referer:
        try:
            from urllib.parse import urlparse

            path = urlparse(referer).path
            lang_code = path.strip("/").split("/")[0]
            if lang_code in supported_languages:
                return lang_code
        except Exception:
            pass

    return default
