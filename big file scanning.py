import os

try:
    from tqdm import tqdm
    HAVE_TQDM = True
except ImportError:
    HAVE_TQDM = False


def get_line_iterator(fh, path, show_progress=True, chunk_size=1024*64):
    """
    Returns an iterator over lines in file handle `fh`.
    Handles large files, cross-platform line endings (\n, \r\n), and smooth tqdm updates.
    """
    if show_progress and HAVE_TQDM:
        filesize = os.path.getsize(path)
        pbar = tqdm(total=filesize, unit='B', unit_scale=True,
                    desc=os.path.basename(path))
        buf = ""
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                if buf:
                    yield buf
                break
            buf += chunk
            # Normalize Windows line endings to \n
            buf = buf.replace('\r\n', '\n').replace('\r', '\n')
            lines = buf.split("\n")
            for line in lines[:-1]:
                yield line + "\n"
            buf = lines[-1]  # keep the last partial line
            pbar.update(len(chunk.encode(fh.encoding or 'utf-8')))
        pbar.close()
    else:
        for line in fh:
            yield line


def get_script_dir():
    """
    Returns the directory where this script is located.
    Falls back to current working directory if __file__ is not defined.
    """
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # __file__ is not defined (e.g., interactive environment)
        return os.getcwd()


def main():
    script_dir = get_script_dir()
    path = os.path.join(script_dir, "example.txt")
    print(f"Looking for file at: {path}")  # debug

    # Auto-create example.txt if it doesn't exist
    if not os.path.exists(path):
        print(f"{path} not found, creating a dummy example.txt for testing.")
        with open(path, "w", encoding="utf-8") as f:
            for i in range(1, 101):
                f.write(f"Line {i}\n")

    # Open the file and read lines with progress bar
    with open(path, "r", encoding="utf-8") as fh:
        for line in get_line_iterator(fh, path, show_progress=True):
            print(line.strip())


if __name__ == "__main__":
    main()
