from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField()
    items = models.ManyToManyField('Item', related_name='articles', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ['id']


class Item(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    photo = models.ImageField(upload_to='media/data')
    category = models.ForeignKey('Category', related_name='items', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['id']


class Review(models.Model):
    name = models.CharField(max_length=150)
    text = models.TextField()
    star = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"
        ordering = ['star']


class Category(models.Model):
    title = models.CharField(max_length=150)
    is_main = models.BooleanField()
    main_category = models.ForeignKey('Category', related_name='sub_categories', on_delete=models.CASCADE, blank=True,
                                      null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['id']


class Cart(models.Model):
    sid = models.CharField(max_length=150, blank=True, null=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    items = models.ManyToManyField(Item, through='ItemInCart', related_name='cart')


class ItemInCart(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    count = models.IntegerField()


class Order(models.Model):
    items = models.ManyToManyField(Item, through='ItemInOrder')
    owner = models.CharField(max_length=150, default='no owner')

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['id']


class ItemInOrder(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    count = models.IntegerField()
