"""Image and asset management for chess pieces"""

import tkinter as tk
import os


class ImageManager:
    def __init__(self, base_path: str, square_size: int):
        self.base_path = base_path
        self.square_size = square_size
        self.images = {}
        self.load_images()

    def full_path(self, relative_path: str) -> str:
        """Get full path to an asset file"""
        absolute_path = os.path.dirname(self.base_path)
        return os.path.join(absolute_path, relative_path)

    def scale_img(
        self, image: tk.PhotoImage, x: int = 2, y: int = 2
    ) -> tk.PhotoImage:
        """Scale an image by subsampling"""
        image = image.subsample(x, y)
        return image

    def load_images(self) -> None:
        """Load all piece images and move indicators"""
        piece_types = ["R", "N", "B", "Q", "K", "P"]
        colors = ["b", "w"]

        for color in colors:
            folder = "black" if color == "b" else "white"
            for piece_type in piece_types:
                piece_name = f"{color}{piece_type}"
                image_path = self.full_path(
                    f"pieces/{folder}/{piece_name}.png"
                )
                self.images[piece_name] = self.scale_img(
                    tk.PhotoImage(file=image_path)
                )

        # Load move indicators
        self.images["O"] = self.scale_img(
            tk.PhotoImage(file=self.full_path("pieces/greycircle.png"))
        )
        self.images["-"] = self.scale_img(
            tk.PhotoImage(file=self.full_path("pieces/greydot.png"))
        )

    def get_image(self, piece_name: str) -> tk.PhotoImage:
        """Get image for a piece"""
        return self.images.get(piece_name)
