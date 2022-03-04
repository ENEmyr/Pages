from typing import List
import schemas.responses

STATUS_CODE_RESPONSE_MAP = {
     # need to change response model when it's properly coding
    200: {'desc': schemas.responses.STATUS200_DESC, 'model': schemas.responses.HTTPExceptionRes},
    400: {'desc': schemas.responses.STATUS400_DESC, 'model': schemas.responses.HTTPExceptionRes},
    401: {'desc': schemas.responses.STATUS401_DESC, 'model': schemas.responses.HTTPExceptionRes},
    403: {'desc': schemas.responses.STATUS403_DESC, 'model': schemas.responses.HTTPExceptionRes},
    404: {'desc': schemas.responses.STATUS404_DESC, 'model': schemas.responses.HTTPExceptionRes},
    413: {'desc': schemas.responses.STATUS413_DESC, 'model': schemas.responses.HTTPExceptionRes},
    415: {'desc': schemas.responses.STATUS415_DESC, 'model': schemas.responses.HTTPExceptionRes},
    500: {'desc': schemas.responses.STATUS500_DESC, 'model': schemas.responses.HTTPExceptionRes},
}

def gen_res_dict(
    status_codes: List[int] = None,
    # custom_responses: dict = None
    ) -> dict:
    generated = {}
    if status_codes != None:
        for code in status_codes:
            desc_model = {
                'description': STATUS_CODE_RESPONSE_MAP[code]['desc'],
                'model': STATUS_CODE_RESPONSE_MAP[code]['model']
            }
            generated[code] = desc_model
    # elif custom_responses != None:
    #     for code in custom_responses.keys():
    #         generated[code] = custom_responses[code]
    return generated
