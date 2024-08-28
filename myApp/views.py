from django.shortcuts import render,redirect
from .models import Cooperative, Admin,Season,CoUser,Product,Farmer,Inventory
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from  datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Inventory, Season, Product,Selle
from django.http import JsonResponse
from .models import Farmer
from django.utils import timezone
from django.db.models import Sum, F, Count
from django.db.models import FloatField
from datetime import datetime, timedelta
from django.db.models.functions import Cast
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError


def index(request):
    return render(request ,'myApp/index.html') 

def report(request):
    return render(request ,'myApp/report.html') 

def logincoperative(request):
    return render(request ,'myApp/loginhome.html')

def cooperative(request):
    return render(request ,'myApp/register_cooperative.html') 

def season(request):
    return render(request ,'myApp/register_season.html') 

def cousers(request):
    All_cooperative = Cooperative.objects.all()
    return render(request ,'myApp/register_couser.html',{'cooperatives': All_cooperative}) 

def listofaccounts(request):
    All_couser = CoUser.objects.all()
    return render(request ,'myApp/list_of_accounts.html',{'accounts': All_couser}) 

def receipt(request):
    return render(request ,'myApp/receipt.html') 

def admin_dashs(request):
    all_cooperatives = Cooperative.objects.all()  # Retrieve all instances of Cooperative
    count_cooperatives = all_cooperatives.count()  
    season = Season.objects.filter(status="active").first()
    return render(request, 'myApp/Admin.html', {
        'allcoperative': all_cooperatives,
        'count_cooperatives': count_cooperatives,
        'seasion': season,
    })


 
def listofcooperative(request):
    All_cooperative = Cooperative.objects.all()
    return render(request ,'myApp/list_of_cooperative.html',{'cooperatives': All_cooperative}) 

def listofseason(request):
    All_season= Season.objects.all()
    return render(request ,'myApp/list_of_season.html',{'seasons': All_season}) 

def displayProduct(request):
    return render(request ,'myApp/Register_Product.html')


def ceo_dash(request):
    co_name = request.session.get('co_name')

    # Fetching revenue data
    revenue_data = Inventory.objects.filter(co_name=co_name).values('created_at__month').annotate(total_revenue=Sum('unit_price')).order_by('created_at__month')

    # Fetching member growth data
    member_data = Farmer.objects.filter(co_name=co_name).values('created_at__month').annotate(new_members=Count('id')).order_by('created_at__month')

    # Fetching total quantity and total price from Sales
    total_quantity = Selle.objects.filter(co_name=co_name).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    total_products = Selle.objects.filter(co_name=co_name).values('product_name').distinct().count()
    total_price = Selle.objects.filter(co_name=co_name).aggregate(total_price=Sum('unit_price'))['total_price']

    # Calculate total amount
    total_amount = total_quantity * total_price if total_quantity and total_price else 0

    # Preparing data for charts
    months = [datetime.strptime(str(month['created_at__month']), "%m").strftime("%b") for month in revenue_data]
    revenue_values = [float(month['total_revenue']) for month in revenue_data]
    member_values = [month['new_members'] for month in member_data]

    context = {
        'co_name': co_name,
        'months': json.dumps(months),
        'revenue_values': json.dumps(revenue_values, cls=DjangoJSONEncoder),
        'member_values': json.dumps(member_values),
        'total_quantity': total_quantity,
        'total_products': total_products,
        'total_amount': total_amount,
    }

    return render(request, 'myApp/ceo_dashboard.html', context)
        
def admin_dash(request):     
     return render(request, 'myApp/admin_dashboard.html')           
 
def displayFamer(request):     
     return render(request, 'myApp/Register_Farmers.html')   
 
def displayInventory(request):     
     return render(request, 'myApp/Register_Inventory.html') 
 
def display_edit_storekeeper(request, id):
    storekeeper = get_object_or_404(CoUser, id=id)
    return render(request, 'myApp/edit_storekeeper.html', {'storekeeper': storekeeper})
 
def edit_storekeeper(request, id):
    storekeeper = get_object_or_404(CoUser, id=id)
    if request.method == 'POST':
        storekeeper.user_name = request.POST['username']
        storekeeper.email = request.POST['email']
        storekeeper.phone_number = request.POST['phone']
        storekeeper.password = request.POST['password']
        storekeeper.save()
        co_name = request.session.get('co_name')
        accountlist=CoUser.objects.filter(co_name= co_name,role="StoreKeeper")     
        return render(request, 'myApp/list_StoreKeeper.html',{'accountlist':accountlist})     
    return render(request, 'edit_storekeeper.html', {'storekeeper': storekeeper})

def storekeeperaccount(request):     
     return render(request, 'myApp/ceo_create__storeKeeper_account.html')     
   
def displayselles(request):
    co_name = request.session.get('co_name') 
    Allproduct= Product.objects.filter(co_name=co_name)      
    return render(request, 'myApp/Register_selles.html',{'allproduct':Allproduct})  
  
def listofstorekeeper(request):
    co_name = request.session.get('co_name')
    accountlist=CoUser.objects.filter(co_name=co_name,role="StoreKeeper")     
    return render(request, 'myApp/list_StoreKeeper.html',{'accountlist':accountlist})     

def listofproduct(request):    
    co_name = request.session.get('co_name')
    productlist=Product.objects.filter(co_name = co_name)     
    return render(request, 'myApp/list_product.html',{'productlist':productlist})     

def edit_of_product(request , id):    
    productall= get_object_or_404(Product, id=id)    
    return render(request, 'myApp/edit_product.html',{'productall':productall})     

def edit_of_coperative(request , id):    
    coperativeall= get_object_or_404(Cooperative, id=id)    
    return render(request, 'myApp/edit_coperative.html',{'coperativeall':coperativeall})     

def edit_coperative_insert(request, id):
    coperative = get_object_or_404(Cooperative, id=id)
    if request.method == 'POST':
        coperative.co_name = request.POST['co_name']
        coperative.work = request.POST['work']
        coperative.location = request.POST['location']
        coperative.save()
        All_cooperative = Cooperative.objects.all()
        return render(request ,'myApp/list_of_cooperative.html',{'cooperatives': All_cooperative}) 
    return render(request, 'myApp/edit_coperative.html', {'coperative': coperative})

def edit_of_season(request , id):    
    seasonall= get_object_or_404(Season, id=id)    
    return render(request, 'myApp/edit_season.html',{'seasonall':seasonall})     

def edit_season_insert(request, id):
    season_s = get_object_or_404(Season, id=id)
    if request.method == 'POST':
        season_s.name = request.POST['name']
        season_s.startdate = request.POST['startdate']
        season_s.enddate = request.POST['enddate']
        season_s.status = request.POST['status']
        season_s.save()
        All_season = Season.objects.all()
        return render(request ,'myApp/list_of_season.html',{'seasons': All_season}) 
    return render(request, 'myApp/edit_season.html', {'season': season_s})

def edit_of_account(request , id):    
    userall= get_object_or_404(CoUser, id=id)    
    return render(request, 'myApp/edit_account.html',{'userall':userall})     

def edit_account_insert(request, id):
    accounts = get_object_or_404(CoUser, id=id)
    if request.method == 'POST':
        accounts.user_name = request.POST['username']
        accounts.email = request.POST['email']
        accounts.phone_number = request.POST['phone']
        accounts.password = request.POST['password']
        accounts.save()
        All_account = CoUser.objects.filter(role='CEO')
        return render(request ,'myApp/list_of_accounts.html',{'accounts': All_account}) 
    return render(request, 'myApp/edit_account.html', {'accounts': accounts})




def edit_of_selles(request , id):    
    sellesall= get_object_or_404(Selle, id=id)
    co_name = request.session.get('co_name') 
    productlist=Product.objects.filter(co_name= co_name)    
    return render(request, 'myApp/edit_selles.html',{'sellesall':sellesall,'productlist':productlist})     


def insert_dit_product(request, id):
    products = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        products.p_name = request.POST['product_name']
        products.Description = request.POST['Description']
        products.save()
        co_name = request.session.get('co_name')
        productlist=Product.objects.filter(co_name= co_name)     
        return render(request, 'myApp/list_product.html',{'productlist':productlist})     
    return render(request, 'list_product.html')

def edit_selle_insert(request, id):
    sale = get_object_or_404(Selle, id=id)
    if request.method == 'POST':
        sale.customer_National_id = request.POST['customer_National_id']
        sale.Customer_name = request.POST['Customer_name']
        sale.product_name = request.POST['product_name']
        sale.quantity = request.POST['quantity']
        sale.unit_price = request.POST['unit_price']
        sale.save()
        co_name = request.session.get('co_name')
        userid = request.session.get('user_id') 
        selleslist=Selle.objects.filter(co_name= co_name, userid=userid)     
        return render(request, 'myApp/listofselles.html',{'sellelist':selleslist})   
    return render(request, 'edit_selles.html', {'sale': sale})


def listofselles(request):    
    co_name = request.session.get('co_name')
    userid = request.session.get('user_id')
    selleslist=Selle.objects.filter(co_name= co_name, userid=userid)      
    return render(request, 'myApp/listofselles.html',{'sellelist':selleslist})     

def insertproduct(request):
    if request.method == 'POST':
        p_name = request.POST['product_name']
        description = request.POST['description']
        co_name = request.session.get('co_name')
        coop = Product.objects.create(p_name=p_name, Description=description,co_name=co_name)
        success_message = "Successfully added!"
        co_name = request.session.get('co_name')
        productlist=Product.objects.filter(co_name= co_name)     
        return render(request, 'myApp/list_product.html',{'productlist':productlist})     
    else:
        return render(request, 'myApp/Register_Product.html')
    
def insertsalles(request):
    if request.method == 'POST':
        nationaid = request.POST['nationaid']
        fullname = request.POST['fullname']
        co_name = request.session.get('co_name')
        product_name=request.POST['product_name']
        quantity=request.POST['quantity']
        unitprice=request.POST['unitprice']
        date_today = datetime.today().date()
        userid = request.session.get('user_id') 
        coop = Selle.objects.create(product_name=product_name,customer_National_id=nationaid,co_name=co_name,unit_price=unitprice,quantity=quantity,Customer_name=fullname,create_date=date_today,userid=userid)
        success_message = "Successfully added!"
        co_name = request.session.get('co_name')
        sellelist=Selle.objects.filter(co_name= co_name)     
        return render(request, 'myApp/listofselles.html',{'sellelist':sellelist})     
    else:
        return render(request, 'myApp/Register_Product.html')

def insertcooperative(request):
    if request.method == 'POST':
        co_name = request.POST['co_name']
        work = request.POST['work']
        location = request.POST['location'] 
        try:
            coop = Cooperative.objects.create(co_name=co_name, work=work, location=location)
            success_message = f"Successfully added {co_name}!"
        except IntegrityError:
            error_message = f"Cooperative : '{co_name}' already exists!"
            return render(request, 'myApp/register_cooperative.html', {'error_message': error_message})

        All_cooperative = Cooperative.objects.all()
        return render(request, 'myApp/list_of_cooperative.html', {'success_message': success_message,'cooperatives': All_cooperative})
    else:
        return render(request, 'myApp/register_cooperative.html')
    

def insertseason(request):
    if request.method == 'POST':
        season_name = request.POST['season_name']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        current_year = datetime.now().strftime('%Y')
        season_name_with_year = f"{season_name} {current_year}" 
        status = "pending"
        new_season = Season(name=season_name_with_year, startdate=startdate, enddate=enddate, status=status)
        new_season.save()        
        success_message = f"Successfully added {season_name_with_year}!"
        All_season = Season.objects.all()        
        return render(request, 'myApp/list_of_season.html', {'success_message': success_message,'seasons': All_season})
    
    return render(request, 'myApp/register_season.html')

def insertcouser(request):
    if request.method == 'POST':
        co_name = request.POST['co_name']
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password'] 

        try:
            new_CoUser = CoUser(co_name=co_name, user_name=username, email=email, password=password, phone_number=phone, role=role)
            new_CoUser.save()
            success_message = f"Successfully added {co_name}!"
            return render(request, 'myApp/register_couser.html', {'success_message': success_message})
        except IntegrityError:
            error_message = f"Cooperative '{co_name}' already exists!"
            return render(request, 'myApp/register_couser.html', {'error_message': error_message})

    return render(request, 'myApp/register_couser.html')

def login_co_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            co_user = CoUser.objects.get(email=email, password=password)
            request.session['user_id'] = co_user.id
            request.session['user_role'] = co_user.role
            request.session['user_name'] = co_user.user_name
            request.session['email'] = co_user.email
            request.session['co_name'] = co_user.co_name
            
            if co_user.role == 'CEO':
                return redirect('ceo_dashboard')
            elif co_user.role == 'StoreKeeper':
                return redirect('storekeeper_dashboard')
            else:
                messages.error(request, 'Invalid role')
                return redirect('login_co_user') 
        
        except CoUser.DoesNotExist:
            pass
        try:
            farmer = Farmer.objects.get(email=email, password=password)
            request.session['user_id'] = farmer.id
            request.session['email'] = farmer.email
            request.session['co_name'] = farmer.co_name
            request.session['name'] =farmer.name

            famer_id=farmer.nation
            
            famerinfo=Inventory.objects.filter(farmer_id=famer_id)
            return render ( request, 'myApp/farmer_dashboard.html', {
            'farmer_count': famerinfo }
            )
        
        
        except Farmer.DoesNotExist:
            pass
        try:
            admin = Admin.objects.get(email=email, password=password)
            request.session['user_id'] = admin.id
            request.session['email'] = admin.email

            all_user=CoUser.objects.filter(role='CEO')
            count_acount =all_user.count()  
            season = Season.objects.filter(status='active').first()
            all_coperative=Cooperative.objects.all()
            count_cooperatives = all_coperative.count()
            return render(request, 'myApp/admin_dashboard.html', {
            'allcoperative': all_coperative,
            'count_cooperatives': count_cooperatives,
            'seasion': season,
            'count_account': count_acount
    })
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login_co_user')
    
    return render(request, 'myApp/loginhome.html')


def storekeeper_dash(request):
    # Retrieve session data
    co_name = request.session.get('co_name', 'Unknown Company')
    user_id = request.session.get('user_id', None)

    # Get current month and year
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Count farmers
    farmer_count = Farmer.objects.filter(
        co_name=co_name,
        created_at__month=current_month,
        created_at__year=current_year
    ).count()

    # Aggregate total quantities in Inventory
    total_quantity = Inventory.objects.filter(
        co_name=co_name,
        created_at__month=current_month,
        created_at__year=current_year
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    # Calculate sum of quantities from Selle within the last 24 hours
    last_24_hours = timezone.now() - timezone.timedelta(hours=24)
    total_selle_quantity = Selle.objects.filter(
        co_name=co_name,
        create_date__gte=last_24_hours
    ).aggregate(Sum('quantity'))['quantity__sum'] or 0

    return render(request, 'myApp/storekeeper_dashboard.html', {
        'farmer_count': farmer_count,
        'total_quantity': total_quantity,
        'total_selle_quantity': total_selle_quantity,
        'co_name': co_name
    })


def logout_user(request):
    request.session.flush()
    return redirect('login_co_user')
        
def admin_dash(request):     
<<<<<<< HEAD
     return render(request, 'myApp/admin_dashboard.html')          
=======
     return render(request, 'myApp/admin_dashboard.html')       

# def ceo_dash(request):  
#      return render(request, 'myApp/ceo_dashboard.html')     
>>>>>>> 05e53e84251c8ceda9a17c22814b84aecd1ecc65

def ceo_create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        role = request.POST['role']
        password = request.POST['password']
        co_name = request.session.get('co_name')

        try:
            new_CoUser = CoUser( user_name=username, email=email,  password=password,  phone_number=phone, role=role,co_name=co_name)
            new_CoUser.save()
            success_message = f"Successfully added  Account status is Pending."
            co_name = request.session.get('co_name')
            accountlist=CoUser.objects.filter(co_name=co_name,role="StoreKeeper")     
            return render(request, 'myApp/list_StoreKeeper.html',{'accountlist':accountlist}) 
        except IntegrityError:
            error_message = f"Fail To create account Contact to Admin!"
            return render(request, 'myApp/ceo_create__storeKeeper_account.html', {'error_message': error_message})
        
    return render(request, 'myApp/ceo_create__storeKeeper_account.html')


def record_farmer(request):
    if request.method == 'POST':
        nation = request.POST.get('nation')
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        co_name = request.session.get('co_name')
        if len(nation) != 16 or not nation.isdigit():
            messages.error(request, "National ID must be exactly 16 digits.")
            return redirect('list_farmers')

        try:
            user = CoUser.objects.get(id=request.session['user_id'])
            if user.role == 'StoreKeeper':
                farmer = Farmer.objects.create(
                    nation=nation,
                    name=name,
                    email=email,
                    password=password,
                    phone=phone,
                    co_name=co_name 
                )

                messages.success(request, "Farmer registered successfully.")
                return redirect('list_farmers')
            else:
                messages.error(request, "You don't have permission to record farmers.")
        except CoUser.DoesNotExist:
            messages.error(request, "User does not exist or is not authorized.")

    return render(request, 'myApp/Register_Farmers.html')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Farmer, CoUser


def edit_farmer(request, farmer_id):
    farmer = get_object_or_404(Farmer, id=farmer_id)

    if request.method == 'POST':
        farmer.nation = request.POST.get('nation')
        farmer.name = request.POST.get('name')
        farmer.email = request.POST.get('email')
        farmer.password = request.POST.get('password')
        farmer.phone = request.POST.get('phone')

        # Validate National ID
        if len(farmer.nation) != 16 or not farmer.nation.isdigit():
            messages.error(request, "National ID must be exactly 16 digits.")
            return redirect('edit_farmer', farmer_id=farmer_id)

        try:
            # Check if the logged-in user is a StoreKeeper
            user = CoUser.objects.get(id=request.session['user_id'])
            if user.role == 'StoreKeeper':
                farmer.save()
                messages.success(request, "Farmer updated successfully.")
                return redirect('list_farmers')
            else:
                messages.error(request, "You don't have permission to edit farmers.")
        except CoUser.DoesNotExist:
            messages.error(request, "User does not exist or is not authorized.")

    return render(request, 'myApp/edit_farmer.html', {'farmer': farmer})

def list_farmers(request):
    # Fetch co_name and user_id from session
    co_name = request.session.get('co_name')
   
    # Filter farmers based on co_name and user_id
    farmers = Farmer.objects.filter(
        co_name=co_name,
   
    )

    return render(request, 'myApp/list_farmers.html', {'farmers': farmers})

# def listofinventory(request):

#     co_name = request.session.get('co_name')
#     product_list=Product.objects.filter(co_name=co_name)

#     return render(request, 'myApp/list_farmers.html', {'farmers': farmers})



def record_inventory(request):
    if request.method == 'POST':
        season_id = request.POST['season_id']
        farmer_id = request.POST['farmer_id']
        farmer_name = request.POST['farmer_name']
        product_name_id = request.POST['product_name']
        quantity = request.POST['quantity']
        unit_price = request.POST['unit_price']

        co_name = request.session.get('co_name')
        storekeeper_id = request.session.get('user_id')
        print("co_name from session:", co_name)
        print("storekeeper_id from session:", storekeeper_id)

        if not all([co_name, storekeeper_id]):
            messages.error(request, 'Session data is missing. Please log in again.')
            return redirect('login_co_user')

        # Calculate total amount
        total_amount = int(quantity) * float(unit_price)

        # Create inventory record
        inventory_item = Inventory.objects.create(
            storekeeper_id=storekeeper_id,
            season_id_id=season_id,
            co_name=co_name,
            farmer_id=farmer_id,
            farmer_name=farmer_name,
            product_name_id=product_name_id,
            quantity=quantity,
            unit_price=unit_price
        )

        all_haverst=Inventory.objects.filter(co_name=co_name)
        return render(request, 'myApp/List_Inventory.html', {
        'inventory_items': all_haverst
         })


        # Redirect to receipt view
        #return redirect('record_inventory', inventory_id=inventory_item.id, total_amount=str(total_amount))

    co_name = request.session.get('co_name')
    seasons = Season.objects.all()
    products = Product.objects.filter(co_name=co_name)

    return render(request, 'myApp/Register_Inventory.html', {'seasons': seasons, 'products': products})

def receipt(request, inventory_id):
    inventory_item = get_object_or_404(Inventory, id=inventory_id)
    total_amount = inventory_item.quantity * inventory_item.unit_price
    return render(request, 'myApp/Receipts.html', {
        'inventory_item': inventory_item,
        'total_amount': total_amount
    })

def list_inventory(request):
    
    co_name = request.session.get('co_name')
    user_id = request.session.get('user_id')  

    inventory_items = Inventory.objects.filter(
        co_name=co_name,
        storekeeper_id=user_id
    )

    return render(request, 'myApp/List_Inventory.html', {'inventory_items': inventory_items})


def edit_inventory(request, id):
    inventory_item = get_object_or_404(Inventory, id=id)
    
    if request.method == 'POST':
        inventory_item.season_id_id = request.POST['season_id']
        inventory_item.farmer_id = request.POST['farmer_id']
        inventory_item.farmer_name = request.POST['farmer_name']
        inventory_item.product_name_id = request.POST['product_name']
        inventory_item.quantity = request.POST['quantity']
        inventory_item.unit_price = request.POST['unit_price']
        
        inventory_item.save()
        messages.success(request, 'Inventory record updated successfully.')
        return redirect('list_inventory')
    
    seasons = Season.objects.all()
    products = Product.objects.all()
    return render(request, 'myApp/Edit_Inventory.html', {
        'inventory_item': inventory_item,
        'seasons': seasons,
        'products': products
    })


def farmer_dashboard(request):
    user_id = request.session.get('user_id')
    try:
        farmer = Farmer.objects.get(id=user_id)
    except Farmer.DoesNotExist:
        pass    
    context = {
        'farmer': farmer 
    }    
    return render(request, 'myApp/farmer_dashboard.html', context)



def get_farmer_name(request):
    farmer_id = request.GET.get('farmer_id')
    try:
        farmer = Farmer.objects.get(nation=farmer_id)
        return JsonResponse({'farmer_name': farmer.name})
    except Farmer.DoesNotExist:
        return JsonResponse({'error': 'Farmer not found'}, status=404)
    
def daily_report(request):
    if request.method == 'POST':
        report_type = request.POST['report_type']
        
        if report_type == 'Daily':
            date = request.POST['date']
            # Fetch farmers registered on the given date
            farmers = Farmer.objects.filter(created_at__date=date)

            # Fetch inventory records on the given date
            inventory_report = Inventory.objects.filter(created_at__date=date).values('product_name').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )

            # Fetch sales records on the given date
            sales_report = Selle.objects.filter(create_date=date).values('product_name').annotate(
                total_quantity_sold=Sum('quantity'),
                total_amount_gained=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )
        
        elif report_type == 'Interval':
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            # Fetch farmers registered between the given dates
            farmers = Farmer.objects.filter(created_at__date__range=[start_date, end_date])

            # Fetch inventory records between the given dates
            inventory_report = Inventory.objects.filter(created_at__date__range=[start_date, end_date]).values('product_name').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )

            # Fetch sales records between the given dates
            sales_report = Selle.objects.filter(create_date__range=[start_date, end_date]).values('product_name').annotate(
                total_quantity_sold=Sum('quantity'),
                total_amount_gained=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )

        context = {
            'farmers': farmers,
            'inventory_report': inventory_report,
            'sales_report': sales_report
        }
        
        return render(request, 'myApp/daily_report.html', context)

    return render(request, 'myApp/daily_report.html')

def daily_reports(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type', '')

        def parse_date(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError("Invalid date format. It must be in YYYY-MM-DD format.")

        if report_type == 'Daily':
            date_str = request.POST.get('date', '')
            date = parse_date(date_str)

            farmers = Farmer.objects.filter(created_at__date=date)
            inventory_report = Inventory.objects.filter(created_at__date=date).values('product_name').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )
            sales_report = Selle.objects.filter(create_date=date).values('product_name').annotate(
                total_quantity_sold=Sum('quantity'),
                total_amount_gained=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )
        
        elif report_type == 'Interval':
            start_date_str = request.POST.get('start_date', '')
            end_date_str = request.POST.get('end_date', '')
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)

            farmers = Farmer.objects.filter(created_at__date__range=[start_date, end_date])
            inventory_report = Inventory.objects.filter(created_at__date__range=[start_date, end_date]).values('product_name').annotate(
                total_quantity=Sum('quantity'),
                total_amount=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )
            sales_report = Selle.objects.filter(create_date__range=[start_date, end_date]).values('product_name').annotate(
                total_quantity_sold=Sum('quantity'),
                total_amount_gained=Sum(F('quantity') * F('unit_price'), output_field=FloatField())
            )

        context = {
            'farmers': farmers,
            'inventory_report': inventory_report,
            'sales_report': sales_report
        }
        
        return render(request, 'myApp/report.html', context)

    return render(request, 'myApp/report.html')