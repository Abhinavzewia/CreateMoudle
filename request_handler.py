from http.server import BaseHTTPRequestHandler, HTTPServer
from mako.template import Template
import cgi
import mk_module

MODULE_DETAILS = {}
MODEL_DETIALS = []
MODEL_CNT = 0


main_html = open("static/html/main.html", "r")
main_html_read = main_html.read()
main_html.close()
model_details = open("static/html/model_details.html", "r")
model_details_read = model_details.read()
model_details.close()
error_file = open("static/html/error.html", "r")
error_file_read = error_file.read()
error_file.close()
completed_file = open("static/html/completed_page.html", "r")
completed_file_read = completed_file.read()
completed_file.close()


class BaseHTTRequestHandlerInherit(BaseHTTPRequestHandler):

    def return_html(self, file):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(file.encode("utf-8"))

    def do_GET(self):
        global MODEL_CNT
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(main_html_read.encode("utf-8"))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get("Content-type"))
        print(pdict)
        pdict["boundary"] = bytes(pdict["boundary"], "utf-8")
        print(pdict)
        if ctype == "multipart/form-data":
            fields = (cgi.parse_multipart(self.rfile, pdict))
            global MODULE_DETAILS
            if not MODULE_DETAILS:
                MODULE_DETAILS = {det: fields[det][0].decode('utf-8').strip() if isinstance(fields[det][0], bytes) else 
                                  fields[det][0].decode('utf-8').strip() for det in fields}
            if fields.get('is_model_details'):
                MODEL_DETIALS.append({field: fields[field][0].decode('utf-8').strip() if isinstance(fields[field][0], bytes) else
                                  fields[field][0].strip() for field in fields if not field.startswith("is_")
                                      and fields[field][0]})
            self.get_model_details()

    def get_model_details(self):
        global MODEL_CNT
        print(MODEL_CNT)
        print(MODULE_DETAILS)
        print(MODEL_DETIALS)
        if MODULE_DETAILS and int(MODULE_DETAILS['no_model']):
            if MODEL_CNT != int(MODULE_DETAILS['no_model']):
                MODEL_CNT += 1
                self.return_html(model_details_read)
            else:
                if MODULE_DETAILS and MODEL_DETIALS:
                    result = mk_module.arrange_data(MODEL_DETIALS, MODULE_DETAILS)
                    if result:
                        self.return_html(completed_file_read)
                    else:
                        self.return_html(error_file_read)
