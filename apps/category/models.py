from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=1200)
    query_title = models.CharField(max_length=1200,blank=True,null=True)
    is_special = models.BooleanField(default = False)
    color = models.CharField(max_length = 50)
    slug = models.SlugField(unique=True, blank=True,null=True)

    def save(self, *args, **kwargs):
       
        if not self.slug:
            self.slug = slugify(self.title)
            self.query_title = self.title.lower()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    category = models.ForeignKey(Category,related_name="related_subcategory",on_delete=models.CASCADE)
    query_title = models.CharField(max_length=1200,blank=True,null=True)
    title = models.CharField(max_length=1200)
    full_title = models.CharField(max_length=1500,blank=True,null=True)
    slug = models.SlugField(unique=True, blank=True,null=True)

    def __str__(self):
        return f"{self.category.title} > {self.title}"
    
    
    def save(self, *args, **kwargs):
      
        if not self.slug:
            self.slug = slugify(self.category.title+ " " + self.title)
            self.query_title = self.title.lower()
            self.update_full_title()

        super().save(*args, **kwargs)
    
    def update_full_title(self):
        self.full_title = self.__str__()

    class Meta:
        verbose_name_plural = "SubCategory"


    

class SubSubCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory,related_name="related_subsubcategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=1200)
    query_title = models.CharField(max_length=1200,blank=True,null=True)
    full_title = models.CharField(max_length=1500,blank=True,null=True)
    slug = models.SlugField(unique=True, blank=True,null=True)

    
    def __str__(self):
        return f"{self.subcategory.category.title} > {self.subcategory.title} > {self.title}"

    def save(self, *args, **kwargs):
      
        if not self.slug:
            self.slug = slugify(self.subcategory.category.title+ " " + self.subcategory.title + " " + self.title)
            self.query_title = self.title.lower()
            self.update_full_title()  # Update the combined title field
            

        super().save(*args, **kwargs)


    def update_full_title(self):
        self.full_title = self.__str__()


    class Meta:
        verbose_name_plural = "SubSubCategory"