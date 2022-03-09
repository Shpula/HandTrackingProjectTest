import json
from ibm_watson import VisualRecognitionV4
from ibm_watson.visual_recognition_v4 import FileWithMetadata, AnalyzeEnums
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
apikey = 'YOUR API KEY HERE'
url = 'YOUR URL HERE'
collection = 'YOUR COLLECTION HERE'
authenticator = IAMAuthenticator(apikey)
service = VisualRecognitionV4('2018-03-19', authenticator=authenticator)
service.set_service_url(url)
path = 'PATH TO YOUR IMAGE'
with open(path, 'rb') as mask_img:
    analyze_images = service.analyze(collection_ids=[collection],
                                     features=[AnalyzeEnums.Features.OBJECTS.value],
                                    images_file=[FileWithMetadata(mask_img)]).get_result()
analyze_images