"""Case Leave Request module"""
#pylint: disable=too-few-public-methods
import sys
import json
import falcon
import jsend
import sentry_sdk
from .hooks import validate_access
from .process_maker import ProcessMaker

@falcon.before(validate_access)
class CaseLeaveRequest():
    """CaseLeaveRequest class"""
    def on_post(self, req, resp):
        #pylint: disable=no-self-use,too-many-locals
        """on post request
        """
        workspace = ''
        resp_msg = {'message': 'Welcome'}
        sentry_msg = 'CaseLeaveRequest.post'
        ext_id = ''

        try:
            if req.params and 'workspace' in req.params:
                workspace = req.params['workspace']

            with sentry_sdk.configure_scope() as scope:
                scope.set_extra('params', req.params)

            pm_obj = ProcessMaker()
            pm_obj.init(workspace)

            if req.content_length:
                submission_raw = req.stream.read(sys.maxsize)

                case_json = self.get_case_json(submission_raw)

                pm_resp = pm_obj.post(
                    'api/1.0/'+workspace+'/plugin-Ppssfgov/cases/leaveRequest',
                    json=case_json)

                with sentry_sdk.configure_scope() as scope:
                    scope.set_extra('processmaker_response', pm_resp)

                # default state
                resp.status = falcon.HTTP_400
                resp_msg = jsend.error(json.dumps(pm_resp))

                if pm_resp and "CASE_NUMBER" in pm_resp and "APP_UID" in pm_resp:
                    sentry_msg = 'Workers and Families First Program '
                    sentry_msg += 'Case '+pm_resp['CASE_NUMBER']+' created.'
                    ext_id = pm_resp['APP_UID']

                    resp.status = falcon.HTTP_200
                    resp_msg = jsend.success(pm_resp)
                    resp_msg['id'] = ext_id

            resp.body = json.dumps(resp_msg)

            with sentry_sdk.configure_scope() as scope:
                scope.set_extra('response', resp_msg)

            sentry_sdk.capture_message(sentry_msg, 'info')

        except Exception as err: # pylint: disable=broad-except
            error_msg = "error: {0}".format(err)
            print(error_msg)
            with sentry_sdk.configure_scope() as scope:
                scope.set_extra('error_msg', error_msg)
            resp.status = falcon.HTTP_400
            resp.body = json.dumps(jsend.error("Bad Request"))
            sentry_sdk.capture_message(sentry_msg, 'error')

    @staticmethod
    def get_case_json(submission_raw):
        """ Get case json """
        with sentry_sdk.configure_scope() as scope:
            scope.set_extra('submission_raw', submission_raw.decode('utf-8'))

        submission_json = json.loads(submission_raw)
        case_data = {"submission": {"data":{}}}
        case_data['submission']['data'] = submission_json
        case_json = json.dumps(case_data)

        with sentry_sdk.configure_scope() as scope:
            scope.set_extra('case_json', case_json)

        return case_json
