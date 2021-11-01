def save_to_file(data: list, filename: str):
    """Save to file."""
    with open(f"{filename}", "w") as f:
        for item_ in data:
            f.write("%s\n" % item_)
