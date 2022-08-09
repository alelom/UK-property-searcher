def only_text_containing(texts: list, filter_texts: list):
    result = set()
    for text in texts:
        for filter_text in filter_texts:
            if filter_text in text:
                result.add(text)
    return list(result)

def exclude_text_containing(texts: list, filter_texts: list):
    to_exclude = only_text_containing(texts, filter_texts)
    return [t for t in texts if not t in to_exclude]

def floorplan_image_urls(texts: list):
    endings_to_exclude = ["_bp_pd_h_r.jpg", "_bp_mpu_r"]

    return exclude_text_containing(texts, endings_to_exclude)