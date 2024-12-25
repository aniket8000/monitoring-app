import psutil
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") #/ means home path
def index():
    cpu_percent = psutil.cpu_percent(interval=1)    #  1 variable for cpu usage 
    mem_percent = psutil.virtual_memory().percent   # 2nd variable for memory usage 
    Message = None
    if cpu_percent > 80 or mem_percent > 80:
        Message = "High CPU or Memory Utilization detected. Please scale up"

    return render_template("index.html", cpu_metric=cpu_percent, mem_metric=mem_percent, message=Message)

if __name__ =='__main__':
    app.run(debug=True, host='0.0.0.0')
