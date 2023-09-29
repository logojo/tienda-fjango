from django.db import models

class ProductManager(models.Manager):

    def productsByUser(self, user):
        return self.filter(
            user_created = user
        )
    
    def productsWithStock(self):
        return self.filter(
            #el gt es para indicar que es mayor a
            stok__gt = 0
        ).order_by('-num_sales')
    
    def productsByGender(self, genero):  
            if genero == "m": 
               return self.filter( 
                    woman = True
               )
            elif genero == "h":                
               return self.filter( 
                    man = True
               )
            else: 
                return self.filter( 
                    man = True,
                    woman = True
                )
    ## **filters los 2 asterisco indican que esa variable es un diccionario(arreglo)       
    def productsByFilter(self, **filters):  
            return self.filter( 
                   woman=filters['woman'],
                   man=filters['man'],                 
                   name__icontains=filters['name']
            )
          