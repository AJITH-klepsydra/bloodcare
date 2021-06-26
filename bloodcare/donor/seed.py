
DONORS = [{
    'name' :"Ajith kumar P M",
    'mobile_no':"+918943234482",
    'email':"ajithpmuralidharan01@gmail.com",
    'age':19,
    'pin_code':670645 ,
    'distict':"wayanad",
    'subdistrict':"mananthavady",
    'address':"Red street kochi kerala",
    'blood_group':"O+",
    'latitude':11.628705,
    'longitude':76.081251,
},
{
    'name' :"Arun kumar P M",
    'mobile_no':"+918943235482",
    'email':"atids@gmail.com",
    'age':22,
    'pin_code':670648 ,
    'distict':"wayanad",
    'subdistrict':"vaithiri",
    'address':"Red street kochi kerala",
    'blood_group':"O-",
    'latitude':11.665612,
    'longitude':76.262665,
},
{
    'name' :"Niranjan B",
    'mobile_no':"+918943234482",
    'email':"niranjan@gmail.com",
    'age':18,
    'pin_code':670641 ,
    'distict':"trivandrum",
    'subdistrict':"valapattanam",
    'address':"Red street malabar kerala",
    'blood_group':"AB-",
    'latitude':8.487073,
    'longitude':76.952418,
},
{
    'name' :"Amal nath",
    'mobile_no':"+918993234482",
    'email':"amal@gmail.com",
    'age':65,
    'pin_code':670685 ,
    'distict':"wayanad",
    'subdistrict':"mananthavady",
    'address':"Red street kochi kerala",
    'blood_group':"A+",
    'latitude':11.551659,
    'longitude':76.040262,
},
{
    'name' :"Jijo",
    'mobile_no':"+919943234482",
    'email':"jijo@gmail.com",
    'age':19,
    'pin_code':670654 ,
    'distict':"wayanad",
    'subdistrict':"mananthavady",
    'address':"Red street kochi kerala",
    'blood_group':"A+",
    'latitude':11.728705,
    'longitude':76.581251,
},]
from django.http.response import JsonResponse
from .models import Donor
from .serializers import DonorSerializer
# def donor_add(request):
#     ser = DonorSerializer(data=DONORS,many = True)
#     if ser.is_valid():
#         ser.save()
#         return JsonResponse({"MSG":"DONE"})
    


def donor_add(request):
    for donor in DONORS:
        Donor.objects.all().create(
                name=donor['name'],
                mobile_no=donor["mobile_no"],
                email=donor["email"],
                age=donor['age'],
                pin_code=donor['pin_code'] ,
                distict=donor["distict"],
                subdistrict=donor["subdistrict"],
                address= donor["address"],
                blood_group="blood_group",
                latitude=donor['latitude'],
                longitude=donor['longitude'],
        )
        print("object created")
    return JsonResponse({"MSG":"What the udck"})