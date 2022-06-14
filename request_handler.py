from http.server import BaseHTTPRequestHandler, HTTPServer
from mako.template import Template
import cgi
import mk_module

MODULE_DETAILS = {}
MODEL_DETIALS = []
MODEL_CNT = 0


def read_html(file):
    html = open("static/html/%s.html" % file, "r")
    html_read = html.read()
    html.close()
    return html_read


class BaseHTTRequestHandlerInherit(BaseHTTPRequestHandler):

    def return_html(self, file, path=None):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if path:
            mytem = Template(file)
            c = mytem.render(file_loc=path)
            self.wfile.write(bytes("%s" % c, "utf-8"))
        else:
            self.wfile.write(file.encode("utf-8"))

    def do_GET(self):
        global MODEL_CNT
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(read_html('main').encode("utf-8"))

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
                                  fields[det][0].strip() for det in fields}
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
                self.return_html(read_html('model_details'))
            else:
                if MODULE_DETAILS and MODEL_DETIALS:
                    result = mk_module.arrange_data(MODEL_DETIALS, MODULE_DETAILS)
                    if result:
                        self.return_html(read_html('completed_page'), result)
                    else:
                        self.return_html(read_html('error'))