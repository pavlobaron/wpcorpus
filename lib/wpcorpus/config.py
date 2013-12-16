
import os
BASE_PATH = os.path.abspath(
    os.path.join(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            ".."),
        "..")
    )


print (BASE_PATH)
