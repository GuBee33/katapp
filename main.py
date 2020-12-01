from linkedary import app
import sys, getopt

def get_opt(argv):
    port=8080
    host="0.0.0.0"
    debug=False
    try:
        opts, args = getopt.getopt(argv,"hi:p:d:",["ip=","port=","debug="])
    except getopt.GetoptError:
        print('main.py -i <ip> -p <port> -d <True/False>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <ip> -p <port> -d <True/False>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            host = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-d", "--debug"):
            debug = arg
    return(host,debug,port)

if __name__ == "__main__":
    host,debug,port = get_opt(sys.argv[1:])
    app.run(host=host, debug=debug, port=port)