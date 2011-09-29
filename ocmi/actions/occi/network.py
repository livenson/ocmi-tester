import webunit2

from ocmi.config import c

class NetworkTest(webunit2.TestCase):

	def test_create(self, input_rendering = c('occi', 'input_rendering'), 
			      output_rendering = c('occi', 'output_rendering')):

        	net_category = c('occi', 'network_category')
	        net_attributes = c('occi', 'network_attribute')
        	endpoint = '%s/%s' %(c('occi', 'server'), c('occi', 'network_location'))

        	headers = {'Accept': output_rendering,
                	   'Category': net_category
                     	} 
        	resp = None
        	if input_rendering == 'text/occi':
			headers['Content-Type'] = input_rendering
			headers['X-OCCI-Attribute'] = net_attributes
			# XXX seems strange that creation is done via POST
			resp = self.post(path = endpoint, headers = headers)
		elif input_rendering == 'text/plain':
			post_parameters = {'Category': net_category,
                               		   'X-OCCI-Attribute': net_attributes
					  }
		resp = self.post(path = endpoint, headers = headers, post_params = post_parameters)
		resp.assertInBody("Location")
