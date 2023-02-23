from rest_framework.test import APITestCase
from rest_framework import status
from .models import Cart, User
from product.models import Category, Product


class CartTests(APITestCase):
    def test_create_cart_item(self):
        self.test_user = User.objects.create(name="Test User")
        self.test_category = Category.objects.create(
            name="Test Category", parent_category_id=None
        )

        self.test_product = Product.objects.create(
            category=self.test_category, title="Test Product", price=10.00
        )
        data = {"user": self.test_user.id, "item": self.test_product.id, "quantity": 1}
        response = self.client.post("/cart/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().item.title, self.test_product.title)

        self.test_user = User.objects.create(name="Test User 3")
        self.test_category = Category.objects.create(
            title="Test Category 3", parent_category_id=1
        )

        self.test_product = Product.objects.create(
            category=self.test_category, title="Test Product3", price=30.00
        )

        self.test_cart_item = Cart.objects.create(
            user=self.test_user, item=self.test_product, quantity=4
        )

        response = self.client.get("/cart/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
