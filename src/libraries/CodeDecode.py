class CodeDecode:
    import base64

    def base64_encode(self, string):
        """
        Removes any `=` used as padding from the encoded string.
        """
        encoded = self.base64.urlsafe_b64encode(string)
        return encoded.rstrip("=")

    def base64_decode(self, string):
        """
        Adds back in the required padding before decoding.
        """
        padding = 4 - (len(string) % 4)
        string = string + ("=" * padding)
        return self.base64.urlsafe_b64decode(string)
