import tkinter
import webbrowser
from http.server import HTTPServer
import request_handler
import threading


def get_module_details():
    def run_fn():
        webbrowser.open("http://%s:%s" % (hostName, serverPort))
        run()

    def destroy_fn():
        webServer.server_close()
        print("Server stopped.")

    def thread():
        # Call work function
        t1 = threading.Thread(target=run_fn)
        t1.start()

    window = tkinter.Tk()
    window.title("MANAGE ODOO START")
    window.attributes('-fullscreen', True)
    text = tkinter.Label(window, text="ODOO START!", font=('Helvetica bold', 40))
    text.grid(row=0, column=3, padx=25, pady=65)
    run_btn = tkinter.Button(window, text="RUN", command=thread, bd=40, bg="grey", fg="Green", activeforeground="White",
                             activebackground="Green", font="Andalus", height=2, highlightcolor="purple",
                             justify="right",
                             padx=100, pady=100, relief="groove", )
    run_btn.grid(row=10, column=1, padx=60, pady=50)
    destroy = tkinter.Button(window, text="Quit", command=destroy_fn, bd=40, bg="grey", fg="red",
                             activeforeground="White",
                             activebackground="red", font="Andalus", height=2, highlightcolor="purple", justify="left",
                             padx=100, pady=100, relief="groove", )
    destroy.grid(row=10, column=4, padx=50, pady=50)
    lbl = tkinter.Label(window, text="")
    lbl.grid(pady=20)
    window.mainloop()
    webServer.server_close()
    print("Server stopped.")


def run():
    global webServer
    webServer = HTTPServer((hostName, serverPort), request_handler.BaseHTTRequestHandlerInherit)
    print("Server started http://%s:%s" % (hostName, serverPort))
    # webbrowser.open("http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")  # mk_module.making_structure()


if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 8080
    get_module_details()
