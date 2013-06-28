from django.db import models
from xmodule.modulestore.django import modulestore
from xmodule.modulestore import Location


class CustomResponseTest(models.Model):
    '''model for a test of a custom response problem'''

    # the problem to test (location)
    # future-proof against long locations?
    problem_location = models.CharField(max_length=100, editable=False)

    # whether the problem should evaluate as correct or not
    correct = models.BooleanField()

    # the current state of the test
    verdict = models.NullBooleanField(editable=False)

    def make_capa(self):
        # create a preview capa problem
        try:
            problem_descriptor = modulestore().get(Location(self.problem_location))
        except:
            raise LookupError
        problem_module = get_preview_module(0, problem_descriptor)
        problem_capa = problem_module.lcp

        return problem_capa

    def run(self):
        '''run the test, and see if it passes'''
        if self.evaluate() == correct:
            self.verdict = True
        else:
            self.verdict = False

        #write the change to the database and return the result
        self.update(verdict=self.verdict)
        return self.verdict

    def evaluate(self):
        '''evaluate the problem with the input and return the correct/incorrect result'''

    def create_response_dictionary(self):
        '''create dictionary to be submitted to the grading function'''

    def create_children(self):
        '''create child responses and input entries when created'''

        # create a preview capa problem
        problem_capa = self.make_capa()

        # go through responder objects
        for responder_xml, responder in problem_capa.responders.iteritems():

            #put the response object in the database
            response_model = Response.objects.create(
                custom_response_test=self,
                xml=responder_xml,
                string_id=responder.id)

            #tell it to put its children in the database
            response_model.create_children()


class Response(models.Model):
    '''Object that corresponds to the <_____response> fields'''

    # the tests in which this response resides
    custom_response_test = models.ForeignKey(CustomResponseTest)

    # the string identifier
    string_id = models.CharField(max_length=100, editable=False, unique=True)

    # the inner xml of this response (used to extract the object quickly)
    xml = models.TextField(editable=False)

    def create_children(self, resp_obj=None):
        '''generate the database entries for the inputs to this response'''

        # see if we need to construct the object from database
        if resp_obj is None:
            resp_obj = self.make_capa()

        # go through inputs in this response object
        for entry in resp_obj.inputfields:
            # create the input models
            Input.objects.create(
                response=self,
                string_id=entry.attrib['id'])

    def make_capa(self):
        '''get the capa-response object to which this response model corresponds'''
        parent_capa = self.custom_response_test.make_capa()
        return parent_capa.reponders[self.xml]


class Input(models.Model):
    '''the input to a Response'''

    # The response in which this input lives
    response = models.ForeignKey(Response)

    # sequence (first response field, second, etc)
    string_id = models.CharField(max_length=100, editable=False, unique=True)

    # the input, supposed a string
    answer = models.CharField(max_length=50, blank=True)
