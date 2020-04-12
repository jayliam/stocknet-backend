from django.shortcuts import render
from .forms import nOrderCForm
from .models import nOrderS,nOrderC,nSupplierOrder,nClientOrder
from django.http import JsonResponse
from django.template.loader import render_to_string

def nOrderC_list(request):
    nOrderCs = nOrderC.objects.all()
    return render(request, 'dashboard/order/Nordercreate.html', {'nOrderCs': nOrderCs})

def nOrderC_create(request):
    data = dict()
    if request.method == 'POST':
        form = nOrderCForm(request.POST)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True                
        else:
            data['form_is_valid'] = False
    else:
        form = nOrderCForm()

    context = {'form': form}
    html_form = render_to_string('dashboard/order/partial_nOrderC_create.html',
        context,
        request=request,
    )
    return JsonResponse({'html_form': html_form})