from django.http import HttpResponse
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location
from models import ContentTest
from capa.capa_problem import LoncapaProblem

from contentstore.views.preview import get_preview_module


def test_problem(request):
    '''page showing summary of tests for this problem'''

    #authentication check?!!!

    #check that the problem exists
    name = request.GET['problem']
    org = 'test'
    course = '123'
    category = 'problem'
    tag = 'i4x'
    location = Location({"name": name,'org': org, 'course': course, 'category': category, 'tag': tag})

    try:
        problem = modulestore().get_item(location)
        problem1 = modulestore().collection.find({"_id.name": name})
    except:
        return HttpResponse("Problem: "+name+"  Doesn't seems to exist :(")

    print(type(problem))

    #get tests for this problem
    try:
        tests = ContentTest.objects.filter(problem_location=unicode(location))
        # pass these to a template to render them

    except:
        #return blank page with option for creating a test
        HttpResponse(u'No tests for this problem yet!')

    answer_dict = {u'i4x-test-123-problem-b0be451a94504a6aad56ed239bf4e70d_2_1': u'5381', u'i4x-test-123-problem-b0be451a94504a6aad56ed239bf4e70d_3_1':6}
    module = get_preview_module(0, problem)
    return_dict = module.lcp.grade_answers(answer_dict)
    # return_dict ={}

    resp_ids = []
    for r in module.lcp.responders.values():
        resp_ids.append(r.id)
    return HttpResponse(str(return_dict))


def edit_test(request):
    '''edit/create more tests for a problem'''

def new_test(request):
    '''make a new test'''