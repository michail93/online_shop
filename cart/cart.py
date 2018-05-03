from decimal import Decimal
from django.conf import settings
from shop.models import Product



class Cart(object):
    
    def __init__(self, request):
        #initialize of cart
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def add(self, product, quantity=1, update_quantity=False):
        # This method either adds product to cart or updates quantity of products in to cart
        product_id=str(product.id)

        if product_id not in self.cart:
            self.cart[product_id]={'quantity':0, 'price':str(product.price)}
        
        if update_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity']+=quantity
        self.save()

    def save(self):
        #update the session cart
        self.session[settings.CART_SESSION_ID]=self.cart
        #mark the session as "modified" to make sure it is saved
        self.session.modified=True

    def remove(self, product):
        #this method removes a product from the cart
        product_id=str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        #This method iterates through items of cart and retrieves products from the database
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        
        for product in products:
            self.cart[str(product.id)]['product']=product

        for item in self.cart.values():
            item['price']=Decimal(item['price'])
            item['total_price']=item['price']*item['quantity']
            yield item

    def __len__(self):
        #This method counts items in the cart
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price'])*item['quantity'] for item in self.cart.values())

    def clear(self):
        #This method removes cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified=True            









