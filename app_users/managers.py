from django.contrib.auth.models import UserManager
  

class UserModelManager(UserManager):
    def create_user(self, email, 
                    first_name=None, 
                    last_name=None, 
                    password=None, 
                    **extra_fields):
        
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        if first_name is None:
            first_name = "FirstName"

        if last_name is None:
            last_name = "LastName"

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, 
                         first_name=None, 
                         last_name=None, 
                         password=None,
                           **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)



class CustomerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_customer=True)
    

class AdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


