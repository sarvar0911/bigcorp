from django.db import models
from django.utils.text import slugify
import random, string
from django.urls import reverse


def rand_slug():
    """
    Returns a random 3-character slug based on lowercase ASCII letters and digits.

    This is used to generate unique slugs for categories and products.
    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    name = models.CharField('category', max_length=255, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True,null=True, related_name='children')
    slug = models.SlugField('URL',max_length=255, unique=True, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickbetter' + self.name)
        super(Category, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('shop:category-list', kwargs={'slug': self.slug})
    
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField('URL',max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField(upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'slug': self.slug})
    

class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Return a queryset of all products that are available.
        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    
    objects = ProductManager()
    
    class Meta:
        proxy = True    
    