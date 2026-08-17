import unittest
from extract import extract_title

class TestHTMLNode(unittest.TestCase):

    def test_heading(self):
        md = """
Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

# Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien
"""
        node = extract_title(md)
        self.assertEqual(
            node,
            "Here's the deal, **I like Tolkien**."
        )
    if __name__ == "__main__":
        unittest.main()