
from typing import Optional


class ItemInterface:

    def button(self, text: str, url: Optional[str]) -> dict:
        pass

    def image(self, img_url: str,
              accessibility_text: Optional[str] = None) -> dict:
        pass
