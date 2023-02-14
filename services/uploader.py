

class Uploader:

    @staticmethod
    def upload_logo_company(instance, filename):
        return f"companies/{instance.slug}/{filename}"

    @staticmethod
    def upload_logo_category(instance, filename):
        return f"categories/{instance.slug}/{filename}"

    @staticmethod
    def upload_image_product(instance, filename):
        return f"categories/{instance.product.slug}/{filename}"